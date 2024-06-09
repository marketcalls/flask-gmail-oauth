from flask import Flask, redirect, url_for, session, request, render_template, flash
from authlib.integrations.flask_client import OAuth
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
import requests
import base64

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

oauth = OAuth(app)
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    access_token_url=os.getenv('OAUTH_ACCESS_TOKEN_URL'),
    authorize_url=os.getenv('OAUTH_AUTHORIZE_URL'),
    authorize_params=None,
    access_token_params=None,
    client_kwargs={'scope': os.getenv('OAUTH_SCOPE')},
    userinfo_endpoint=os.getenv('OAUTH_USERINFO_ENDPOINT'),  # Explicitly set userinfo_endpoint
    jwks_uri=os.getenv('OAUTH_JWKS_URI'),  # Explicitly set jwks_uri
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    redirect_uri = url_for('authorized', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/logout')
def logout():
    session.pop('google_token')
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    token = oauth.google.authorize_access_token()
    session['google_token'] = token
    user_info = oauth.google.get(os.getenv('OAUTH_USERINFO_ENDPOINT')).json()
    session['user_info'] = user_info
    return redirect(url_for('index'))

@app.route('/preview', methods=['POST'])
def preview():
    recipient = request.form['recipient']
    subject = request.form['subject']
    mode = request.form['mode']
    body_text = request.form.get('body_text', '')
    body_html = request.form.get('body_html', '')
    return render_template('preview.html', recipient=recipient, subject=subject, mode=mode, body_text=body_text, body_html=body_html)

@app.route('/send', methods=['POST'])
def send():
    if 'google_token' not in session:
        return redirect(url_for('login'))

    recipient = request.form['recipient']
    subject = request.form['subject']
    body_text = request.form.get('body_text', '')
    body_html = request.form.get('body_html', '')
    mode = request.form['mode']

    token = session['google_token']
    headers = {'Authorization': f'Bearer {token["access_token"]}'}

    msg = Message(subject, recipients=[recipient], sender=app.config['MAIL_DEFAULT_SENDER'])
    
    if mode == 'plain':
        msg.body = body_text
    elif mode == 'html':
        msg.html = body_html

    # Send email using Gmail API
    url = os.getenv('GMAIL_API_SEND_URL')
    raw_message = base64.urlsafe_b64encode(msg.as_string().encode()).decode()
    raw_message = {'raw': raw_message}

    response = requests.post(url, headers=headers, json=raw_message)
    if response.status_code == 200:
        return redirect(url_for('sent'))
    else:
        return f"Failed to send email: {response.text}"

@app.route('/sent')
def sent():
    return render_template('sent.html')

if __name__ == "__main__":
    app.run(debug=True)
