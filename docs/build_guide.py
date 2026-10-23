"""Rebuild the illustrated guide: pip install reportlab Pillow; python docs/build_guide.py."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from PIL import Image
ROOT=Path(__file__).resolve().parent
c=canvas.Canvas(str(ROOT/'ClassPulse_Installation_and_Demo.pdf'),pagesize=(595,842))
c.setTitle('ClassPulse - Installation and Demo Guide')
style=ParagraphStyle('body',fontName='Helvetica',fontSize=12,leading=18,textColor=HexColor('#33343d'))
def text(s,y,x=44,w=507):
 p=Paragraph(s,style);_,h=p.wrap(w,700);p.drawOn(c,x,y-h);return y-h-14
def page(n,title,sub):
 c.setFillColor(HexColor('#f5f5f8'));c.rect(0,0,595,842,fill=1,stroke=0)
 c.setFillColor(HexColor('#625de9'));c.setFont('Helvetica-Bold',10);c.drawString(44,801,'CLASSPULSE / START HERE')
 c.setFillColor(HexColor('#1d1d1f'));c.setFont('Helvetica-Bold',26);c.drawString(44,755,title)
 text(sub,731)
 c.setFont('Helvetica',9);c.setFillColor(HexColor('#777784'));c.drawString(44,25,'Actual Flask app | Fictional demonstration data');c.drawRightString(551,25,str(n))
def pic(name,x,y,w,maxh=500):
 p=ROOT/'images'/name;im=Image.open(p);h=w*im.height/im.width
 if h>maxh:w=w*maxh/h;h=maxh
 c.drawImage(str(p),x,y-h,width=w,height=h);return y-h
page(1,'Your first working classroom.','A small question. Every voice. A teacher who can see the evidence.')
y=pic('home.png',44,674,507,365)-24
for s in ['<b>What you are building:</b> a classroom feedback loop. A teacher asks a question; students answer without entering names; machine learning groups similar wording; the teacher checks the originals and asks again.','<b>What is already built:</b> the app, separate teacher/student views, local ML, evidence review, follow-up rounds, export and a labelled sample class.','<b>Start with this guide.</b> It replaces the Streamlit setup instructions in the earlier planning PDF. Keep README.md for detailed technical instructions.']:y=text(s,y)
c.showPage()
page(2,'Install. Then open.','Use a laptop with Python, a browser and internet for the first installation.')
y=674
for s in ['<b>1. Get Python.</b> Open python.org/downloads. Install Python 3.13 or 3.14. On Windows, enable Add Python to PATH if offered. Finish the installer.','<b>2. Extract the ZIP.</b> On Windows, right-click and choose Extract All. On Mac, double-click the ZIP. Open the ClassPulse folder. Do not move app.py away from static or templates.','<b>3. Start.</b> Windows: double-click START_WINDOWS.bat. Mac: open START_MAC.command. If needed, open Terminal in this folder and type <b>zsh START_MAC.command</b>, then Enter.','<b>4. Wait.</b> The first start downloads dependencies. Keep the terminal open. If an error appears, read the last line before retrying.','<b>5. Choose your teacher password.</b> Use at least 10 characters. Typing is hidden on purpose. Enter it, press Enter, and repeat it. Keep it private.','<b>6. Visit http://localhost:8765.</b> Click Teacher studio and sign in. This address works on this laptop; it is not a public submission link.','<b>If you forget the password:</b> stop the server with Ctrl+C. Mac: run .venv/bin/python setup.py. Windows: run .venv\\Scripts\\python setup.py. Restart the launcher.']:y=text(s,y)
c.showPage()
page(3,'Try both sides.','Use a normal browser window for the teacher and an incognito window for a student.')
pic('student.png',350,674,201,535)
y=674
for s in ['<b>1.</b> In Teacher studio, click Explore a sample class. Eight fictional answers appear, clearly labelled.','<b>2.</b> Copy the student link. Open a private/incognito window on the same laptop and paste it.','<b>3.</b> Type: The velocity stays constant, so acceleration is zero. Choose a confidence level and press Send my answer.','<b>4.</b> Return to the teacher window. Within a few seconds, the total changes from eight to nine. This extra answer came from your separate student session.','<b>For a real class:</b> create a new empty room instead of using the sample. Phones need a reachable hosted address; localhost on a phone means that phone.']:y=text(s,y,w=285)
c.showPage()
page(4,'Reveal. Inspect. Decide.','The original answers matter more than an impressive-looking chart.')
y=pic('patterns.png',44,674,507,300)-20
for s in ['<b>1.</b> Click Close this round, then Reveal patterns. Local ML works without an API key.','<b>2.</b> Expand the original answers under a group. Check every interpretation against the actual words. Similar wording can hide opposite meanings.','<b>3.</b> Write your interpretation or correction. Click Mark as reviewed, or reject the interpretation if it is wrong.','<b>Explain honestly:</b> local TF-IDF and K-means group similar words. Teaching prompts are templates. Optional Gemini mode needs a private server API key and has not been verified here with a live key.']:y=text(s,y)
c.showPage()
page(5,'Ask again. Close the loop.','Show how the teacher acts on the evidence, not just how a dashboard looks.')
y=pic('followup.png',44,674,507,320)-20
for s in ['<b>1.</b> Click Edit &amp; open the next round. Replace the suggested question with: A cyclist travels straight at steady speed. What is its acceleration? Explain.','<b>2.</b> Add the teacher reference: Zero, because velocity is constant. Open the round.','<b>3.</b> The student window receives the new question automatically. Send another answer. Check the live count and round comparison.','<b>4.</b> Export the room JSON if needed. The comparison shows submissions and self-reported uncertainty, not measured learning gains.']:y=text(s,y)
c.showPage()
page(6,'Present in four minutes.','Rehearse once. Keep the story small, concrete and honest.')
y=674
for s in ['<b>0:00-0:30 - Problem.</b> A raised hand does not reveal what the whole class understands. Quiet students need a low-pressure way to explain their thinking.','<b>0:30-1:20 - Live answer.</b> Show the labelled sample, then add one fresh answer in a separate student window. Point to the changing count.','<b>1:20-2:30 - AI with evidence.</b> Close, analyse and open the source answers. Explain the actual mode and one limitation. Show a teacher correction.','<b>2:30-3:30 - Teacher action.</b> Open a follow-up question and answer it. Explain why this is a feedback loop rather than an automatic grading tool.','<b>3:30-4:00 - Finish.</b> Name the stack: Python, Flask, SQLite and scikit-learn. State what is tested and what remains a prototype. Do not claim classroom results you have not measured.','<b>Before submission:</b> public app URL; public GitHub source and README; 3-5 minute video on Drive; all links work in incognito. GITHUB_SETUP.txt explains the browser-only upload steps.','<b>Timing:</b> the reported 11 am Pakistan start plus five hours gives 4 pm Pakistan on 23 October 2026. Follow official changes. No code pushes after the deadline.','<b>Package status:</b> a working local app and source files do not automatically create a public website, repository or uploaded video. Check docs/SUBMISSION_CHECKLIST.txt.']:y=text(s,y)
c.save()
print('Created six-page installation and demo guide.')
