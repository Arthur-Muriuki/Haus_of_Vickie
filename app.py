from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# --- Email configuration ---
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.getenv('EMAIL_USER'),
    MAIL_PASSWORD=os.getenv('EMAIL_PASS'),
)

mail = Mail(app)

# --- Home route ---
@app.route('/')
def home():
    return render_template('index.html')

# --- Contact form handler ---
@app.route('/send', methods=['POST'])
def send():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Build the email
    msg = Message(
        subject=f"New message from {name}",
        sender=os.getenv('EMAIL_USER'),    # your Gmail
        recipients=[os.getenv('EMAIL_USER')],
        body=f"""
        You have a new message!

        From: {name}
        Email: {email}

        Message:
        {message}
        """
    )

    try:
        mail.send(msg)
        return jsonify({"status": "success", "message": "Message sent successfully!"})
    except Exception as e:
        print("❌ Email Error:", e)
        return jsonify({"status": "error", "message": "Failed to send message"}), 500

# --- Run the app ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
