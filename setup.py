import json,secrets,getpass,os
from pathlib import Path
from werkzeug.security import generate_password_hash
p=Path(os.environ.get('CLASSPULSE_DATA',str(Path(__file__).parent/'instance')));p.mkdir(parents=True,exist_ok=True);f=p/'settings.json';s=json.loads(f.read_text()) if f.exists() else {}
print('Create a teacher password, at least 10 characters. Stored as a hash.')
a=getpass.getpass('Password: ');b=getpass.getpass('Repeat: ')
if len(a)<10 or a!=b:raise SystemExit('Passwords must match and contain 10 or more characters. Run setup again.')
s.update(secret_key=s.get('secret_key') or secrets.token_hex(32),password_hash=generate_password_hash(a));f.write_text(json.dumps(s));f.chmod(0o600)
print('Ready. Run: python app.py')
