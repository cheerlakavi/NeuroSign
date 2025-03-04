from flask import Flask, render_template
from dyslexia_app import dyslexia_bp
from sign_language_app import sign_language_bp

app = Flask(__name__)
app.register_blueprint(dyslexia_bp)
app.register_blueprint(sign_language_bp)

@app.route('/')
def home():
    return render_template('mainpage.html')

if __name__ == '__main__':
    app.run(debug=True)
