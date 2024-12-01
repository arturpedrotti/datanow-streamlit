from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Define static folder as a child of datanow
app.static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))

# Secret key for session management
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key_here')

# Flask-Mail configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# Initialize Flask-Mail
mail = Mail(app)

# Serve the homepage
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Handle newsletter subscription
@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    if email:
        try:
            # Create the email message
            msg = Message(
                subject='Bem-vindo à Newsletter do DataNow',
                sender=app.config['MAIL_USERNAME'],
                recipients=[email]
            )

            # Load welcome message content
            with open(os.path.join('..', 'templates', 'welcome_message.html'), 'r', encoding='utf-8') as file:
                content = file.read()

            # Attach the logo to the email
            logo_path = os.path.join(app.static_folder, 'shared_assets/shared_images/pic01.jpg')
            with open(logo_path, 'rb') as logo:
                msg.attach(
                    'logo.png',
                    'image/png',
                    logo.read(),
                    'inline',
                    headers=[['Content-ID', '<Logo>']]
                )

            # Replace the placeholder in the HTML content with the attached logo's Content-ID
            content = content.replace('cid:logo_image', 'cid:Logo')
            msg.html = content

            # Send the email
            mail.send(msg)
            flash('Email enviado com sucesso!', 'success')
        except Exception as e:
            print(f"Erro: {e}")
            flash('Ocorreu um erro ao enviar o email. Tente novamente mais tarde.', 'danger')
    else:
        flash('Por favor, insira um email válido.', 'warning')

    return redirect(url_for('index'))

# Serve static files from the datanow/static folder
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# Debug endpoint to test static file accessibility
@app.route('/test_static')
def test_static():
    return f'''
    <h1>Test Static Assets</h1>
    <img src="{url_for('static', filename='shared_assets/shared_images/pic01.jpg')}" alt="Test Image">
    '''

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

