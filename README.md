
# Flask Mailer Test

This is a simple Flask application that uses OAuth 2.0 for Google login and Gmail API to send emails. The application includes three main pages: the email form, the email preview, and a confirmation page upon successful email sending.

## Project Structure

```
FLASK MAILER TEST
│
├── templates
│   ├── index.html
│   ├── preview.html
│   └── sent.html
│
├── venv
│   └── ...
├── .env
├── .gitignore
├── app.py
└── requirements.txt
```

## Getting Started

### Prerequisites

- Python 3.x
- A Google Cloud project with OAuth 2.0 credentials

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-username/flask-mailer-test.git
cd flask-mailer-test
```

2. **Create and activate a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install the dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory with the following content:

```plaintext
SECRET_KEY=your_secret_key
MAIL_DEFAULT_SENDER=your_email@gmail.com
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
OAUTH_ACCESS_TOKEN_URL=https://oauth2.googleapis.com/token
OAUTH_AUTHORIZE_URL=https://accounts.google.com/o/oauth2/auth
OAUTH_SCOPE=openid email https://www.googleapis.com/auth/gmail.send https://www.googleapis.com/auth/userinfo.email
OAUTH_USERINFO_ENDPOINT=https://www.googleapis.com/oauth2/v3/userinfo
OAUTH_JWKS_URI=https://www.googleapis.com/oauth2/v3/certs
GMAIL_API_SEND_URL=https://www.googleapis.com/gmail/v1/users/me/messages/send
```

### Setting Up Google Cloud Project

1. **Create a new project in Google Cloud Console**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Click on the project dropdown at the top left and select "New Project"
   - Name your project and click "Create"

2. **Enable Gmail API**
   - Navigate to the [Gmail API](https://console.cloud.google.com/apis/library/gmail.googleapis.com)
   - Click "Enable"

3. **Create OAuth 2.0 credentials**
   - Go to the [Credentials page](https://console.cloud.google.com/apis/credentials)
   - Click on "Create Credentials" and select "OAuth 2.0 Client IDs"
   - Set the "Application type" to "Web application"
   - Add `http://localhost:5000` to "Authorized JavaScript origins"
   - Add `http://localhost:5000/login/authorized` to "Authorized redirect URIs"
   - Click "Create"
   - Copy the "Client ID" and "Client Secret" to your `.env` file

### Test Email IDs in Google Cloud Console

You can use the following test email IDs for testing the application:
in the oAuth Consent screen and goto the Test users section and add
the test users 

### Usage

1. **Run the Flask application**

```bash
python app.py
```

2. **Access the application**

Open your web browser and go to `http://127.0.0.1:5000/login` to login to application using gmail
and `http://127.0.0.1:5000/` to send email



## License

This project is licensed under the MIT License.
