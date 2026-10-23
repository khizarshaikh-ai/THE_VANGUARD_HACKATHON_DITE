import os,json,secrets,sqlite3,hmac,time
from pathlib import Path
from functools import wraps
from flask import Flask,request,session,jsonify,render_template
from werkzeug.security import generate_password_hash,check_password_hash
from analysis import analyse
ROOT=Path(__file__).parent
SAMPLES=['Zero because velocity is constant.','Same speed and direction means no acceleration.','Velocity is constant so acceleration is zero.','The car accelerates because it is moving.','A moving car always has acceleration.','It has acceleration because it moves forward.','I do not understand acceleration yet.','I am not sure what acceleration means.']
QUESTION='A car moves in a straight line at constant speed. What is its acceleration, and why?'
REFERENCE='Acceleration is zero because velocity is not changing in magnitude or direction.'
def create_app(config=None):
    app=Flask(__name__);instance=Path(os.environ.get('CLASSPULSE_DATA',str(ROOT/'instance')));instance.mkdir(parents=True,exist_ok=True)
    sf=instance/'settings.json';settings=json.loads(sf.read_text()) if sf.exists() else {}
    key=os.environ.get('SECRET_KEY') or settings.get('secret_key')
    if not key:
        key=secrets.token_hex(32);settings['secret_key']=key;sf.write_text(json.dumps(settings));sf.chmod(0o600)
    app.config.update(SECRET_KEY=key,DATABASE=str(instance/'classpulse.db'),PASSWORD_HASH=settings.get('password_hash',''),GEMINI_API_KEY=os.environ.get('GEMINI_API_KEY',''),GEMINI_MODEL=os.environ.get('GEMINI_MODEL','gemini-3.8-flash'),MAX_CONTENT_LENGTH=32768,SESSION_COOKIE_HTTPONLY=True,SESSION_COOKIE_SAMESITE='Lax',SESSION_COOKIE_SECURE=os.environ.get('COOKIE_SECURE','0')=='1')
    if os.environ.get('TEACHER_PASSWORD'):app.config['PASSWORD_HASH']=generate_password_hash(os.environ['TEACHER_PASSWORD'])
    if config:app.config.update(config)
    def db():
        c=sqlite3.connect(app.config['DATABASE'],timeout=10);c.row_factory=sqlite3.Row;c.execute('PRAGMA foreign_keys=ON');return c
    with db() as c:c.executescript('''CREATE TABLE IF NOT EXISTS rooms(code TEXT PRIMARY KEY,title TEXT NOT NULL,created REAL,sample INTEGER DEFAULT 0);CREATE TABLE IF NOT EXISTS rounds(id INTEGER PRIMARY KEY,room TEXT REFERENCES rooms(code) ON DELETE CASCADE,question TEXT,reference TEXT,state TEXT DEFAULT 'open',result TEXT,review TEXT DEFAULT 'pending',note TEXT DEFAULT '',created REAL);CREATE TABLE IF NOT EXISTS responses(id INTEGER PRIMARY KEY,round_id INTEGER REFERENCES rounds(id) ON DELETE CASCADE,token TEXT,body TEXT,confidence TEXT,created REAL,UNIQUE(round_id,token));''')
    attempts={}
    def err(msg,code=400):return jsonify(error=msg),code
    def teacher(fn):
        @wraps(fn)
        def wrap(*a,**k):
            if not session.get('teacher'):return err('Sign in as teacher first.',401)
            return fn(*a,**k)
        return wrap
    def field(d,k,n,required=True):
        v=d.get(k,'')
        if not isinstance(v,str):raise ValueError('Invalid '+k)
        v=v.strip()
        if (required and not v) or len(v)>n:raise ValueError(f'{k}: enter '+('1-' if required else 'at most ')+str(n)+' characters.')
        return v
    @app.before_request
    def guard():
        session.setdefault('csrf',secrets.token_hex(24));session.setdefault('student',secrets.token_hex(20))
        if request.method=='POST' and not hmac.compare_digest(str(request.headers.get('X-CSRF-Token','')),session['csrf']):return err('Page expired. Refresh and retry.',403)
    @app.after_request
    def headers(r):
        r.headers.update({'X-Content-Type-Options':'nosniff','Referrer-Policy':'same-origin','Cache-Control':'no-store','X-Frame-Options':'DENY','Content-Security-Policy':"default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'; img-src 'self' data:; connect-src 'self'; base-uri 'self'; frame-ancestors 'none'"});return r
    @app.errorhandler(ValueError)
    def bad(e):return err(str(e))
    @app.errorhandler(413)
    def large(e):return err('Request too large.',413)
    @app.get('/')
    def home():return render_template('index.html',csrf=session['csrf'],configured=bool(app.config['PASSWORD_HASH']))
    @app.get('/health')
    def health():return jsonify(status='ok')
    @app.get('/api/me')
    def me():return jsonify(teacher=bool(session.get('teacher')),gemini=bool(app.config['GEMINI_API_KEY']),model=app.config['GEMINI_MODEL'])
    @app.post('/api/login')
    def login():
        ip=request.remote_addr or 'unknown';now=time.time();recent=[t for t in attempts.get(ip,[]) if now-t<60];attempts[ip]=recent
        if len(recent)>=8:return err('Wait one minute before trying again.',429)
        attempts[ip].append(now);pw=(request.get_json(silent=True) or {}).get('password','')
        if not isinstance(pw,str) or not app.config['PASSWORD_HASH'] or not check_password_hash(app.config['PASSWORD_HASH'],pw):return err('Password not recognised. Use your setup password.',401)
        session['teacher']=True;attempts.pop(ip,None);return jsonify(ok=True)
    @app.post('/api/logout')
    def logout():session.pop('teacher',None);return jsonify(ok=True)
    @app.get('/api/rooms')
    @teacher
    def rooms():
        with db() as c:rows=c.execute('SELECT * FROM rooms ORDER BY created DESC LIMIT 30').fetchall()
        return jsonify(rooms=[dict(r) for r in rows])
    @app.post('/api/rooms')
    @teacher
    def create():
        d=request.get_json(silent=True) or {};title=field(d,'title',80);q=field(d,'question',600);ref=field(d,'reference',1200);code=secrets.token_hex(3).upper()
        with db() as c:
            c.execute('INSERT INTO rooms VALUES(?,?,?,0)',(code,title,time.time()));c.execute('INSERT INTO rounds(room,question,reference,created) VALUES(?,?,?,?)',(code,q,ref,time.time()))
        return jsonify(code=code)
    @app.post('/api/demo')
    @teacher
    def demo():
        code=secrets.token_hex(3).upper()
        with db() as c:
            c.execute('INSERT INTO rooms VALUES(?,?,?,1)',(code,'Motion & understanding',time.time()));rid=c.execute('INSERT INTO rounds(room,question,reference,created) VALUES(?,?,?,?)',(code,QUESTION,REFERENCE,time.time())).lastrowid
            for i,body in enumerate(SAMPLES):c.execute('INSERT INTO responses(round_id,token,body,confidence,created) VALUES(?,?,?,?,?)',(rid,'sample-'+str(i),body,['sure','unsure','stuck'][i%3],time.time()))
        return jsonify(code=code)
    @app.get('/api/room/<code>')
    def room(code):
        with db() as c:
            room=c.execute('SELECT * FROM rooms WHERE code=?',(code.upper(),)).fetchone()
            if not room:return err('Room not found. Check the six-character code.',404)
            out=[]
            for r in c.execute('SELECT * FROM rounds WHERE room=? ORDER BY id',(room['code'],)).fetchall():
                item={'id':r['id'],'question':r['question'],'state':r['state'],'submitted':bool(c.execute('SELECT 1 FROM responses WHERE round_id=? AND token=?',(r['id'],session['student'])).fetchone())}
                if session.get('teacher'):
                    rows=c.execute('SELECT id,body,confidence FROM responses WHERE round_id=? ORDER BY id',(r['id'],)).fetchall();item.update(reference=r['reference'],responses=[dict(x) for x in rows],result=json.loads(r['result']) if r['result'] else None,review=r['review'],note=r['note'])
                out.append(item)
        return jsonify(room=dict(room),rounds=out)
    @app.post('/api/round/<int:rid>/answer')
    def answer(rid):
        d=request.get_json(silent=True) or {};body=field(d,'body',400);conf=d.get('confidence','unsure')
        if conf not in ('sure','unsure','stuck'):return err('Choose a confidence level.')
        with db() as c:
            c.execute('BEGIN IMMEDIATE');r=c.execute('SELECT * FROM rounds WHERE id=?',(rid,)).fetchone()
            if not r:return err('Question not found.',404)
            if r['state']!='open':return err('This round is closed. Wait for the next question.',409)
            if c.execute('SELECT COUNT(*) FROM responses WHERE round_id=?',(rid,)).fetchone()[0]>=50:return err('This prototype round is full.',409)
            try:c.execute('INSERT INTO responses(round_id,token,body,confidence,created) VALUES(?,?,?,?,?)',(rid,session['student'],body,conf,time.time()))
            except sqlite3.IntegrityError:return err('Your answer has already been received.',409)
        return jsonify(ok=True)
    @app.post('/api/round/<int:rid>/close')
    @teacher
    def close(rid):
        with db() as c:
            if not c.execute("UPDATE rounds SET state='closed' WHERE id=? AND state='open'",(rid,)).rowcount:return err('Round already closed or unavailable.',409)
        return jsonify(ok=True)
    @app.post('/api/room/<code>/round')
    @teacher
    def next_round(code):
        d=request.get_json(silent=True) or {};q=field(d,'question',600);ref=field(d,'reference',1200)
        with db() as c:
            c.execute('BEGIN IMMEDIATE')
            if not c.execute('SELECT 1 FROM rooms WHERE code=?',(code,)).fetchone():return err('Room not found.',404)
            if c.execute("SELECT 1 FROM rounds WHERE room=? AND state IN ('open','analysing')",(code,)).fetchone():return err('Close the current round and finish analysis first.',409)
            if c.execute('SELECT COUNT(*) FROM rounds WHERE room=?',(code,)).fetchone()[0]>=5:return err('Maximum five rounds per room.')
            c.execute('INSERT INTO rounds(room,question,reference,created) VALUES(?,?,?,?)',(code,q,ref,time.time()))
        return jsonify(ok=True)
    @app.post('/api/round/<int:rid>/analyse')
    @teacher
    def run_analysis(rid):
        mode=(request.get_json(silent=True) or {}).get('mode','local')
        if mode not in ('local','gemini'):return err('Unknown analysis mode.')
        with db() as c:
            c.execute('BEGIN IMMEDIATE');r=c.execute('SELECT * FROM rounds WHERE id=?',(rid,)).fetchone()
            if not r:return err('Question not found.',404)
            if r['state']!='closed':return err('Close responses before analysis.',409)
            answers=[dict(a) for a in c.execute('SELECT id,body FROM responses WHERE round_id=? ORDER BY id',(rid,)).fetchall()]
            if not answers:return err('Collect an answer first.')
            c.execute("UPDATE rounds SET state='analysing' WHERE id=?",(rid,))
        try:
            result=analyse(r['question'],r['reference'],answers,mode,app.config['GEMINI_API_KEY'],app.config['GEMINI_MODEL'])
            with db() as c:c.execute("UPDATE rounds SET result=?,review='pending',note='' WHERE id=?",(json.dumps(result),rid))
        except Exception as e:
            app.logger.warning('Analysis failed: %s',type(e).__name__);return err('Analysis failed. Check API access/quota or choose Local ML. No results were invented.',502)
        finally:
            with db() as c:c.execute("UPDATE rounds SET state='closed' WHERE id=?",(rid,))
        return jsonify(ok=True)
    @app.post('/api/round/<int:rid>/review')
    @teacher
    def review(rid):
        d=request.get_json(silent=True) or {};state=d.get('review');note=field(d,'note',1200,False)
        if state not in ('reviewed','rejected'):return err('Choose a review status.')
        with db() as c:
            if not c.execute('UPDATE rounds SET review=?,note=? WHERE id=? AND result IS NOT NULL',(state,note,rid)).rowcount:return err('Analyse first.',409)
        return jsonify(ok=True)
    @app.get('/api/room/<code>/export')
    @teacher
    def export(code):
        r=room(code)
        if isinstance(r,tuple):return r
        r.headers['Content-Disposition']='attachment; filename=classpulse-'+code+'.json';return r
    @app.post('/api/room/<code>/delete')
    @teacher
    def delete(code):
        with db() as c:c.execute('DELETE FROM rooms WHERE code=?',(code,))
        return jsonify(ok=True)
    return app
if __name__=='__main__':
    from waitress import serve
    print('ClassPulse: http://localhost:'+os.environ.get('PORT','8765'))
    serve(create_app(),host=os.environ.get('HOST','127.0.0.1'),port=int(os.environ.get('PORT','8765')),threads=8)
