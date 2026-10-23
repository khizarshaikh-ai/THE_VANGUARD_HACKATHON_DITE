# """First-run password setup followed by the local web server."""
import os,json,runpy
from pathlib import Path
root=Path(__file__).parent
settings=Path(os.environ.get('CLASSPULSE_DATA',str(root/'instance')))/'settings.json'
existing=json.loads(settings.read_text()) if settings.exists() else {}
if not os.environ.get('TEACHER_PASSWORD') and not existing.get('password_hash'):
    runpy.run_path(str(root/'setup.py'),run_name='__main__')
from app import create_app
from waitress import serve
print('Open http://localhost:'+os.environ.get('PORT','8765')+' in your browser. Keep this window open.')
serve(create_app(),host=os.environ.get('HOST','127.0.0.1'),port=int(os.environ.get('PORT','8765')),threads=8)
