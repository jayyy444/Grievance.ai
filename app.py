import os
from flask import Flask
from flask_login import LoginManager
from models import db, User
from config import Config

def download_nltk_data():
    try:
        import nltk
        for item in ['punkt', 'brown', 'averaged_perceptron_tagger']:
            try:
                nltk.data.find(f'corpora/{item}')
            except LookupError:
                nltk.download(item, quiet=True)
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
    except Exception:
        pass

def create_admin(app):
    with app.app_context():
        admin_email = app.config['ADMIN_EMAIL']
        admin_password = app.config['ADMIN_PASSWORD']
        if not User.query.filter_by(email=admin_email).first():
            from werkzeug.security import generate_password_hash
            admin = User(
                name='Administrator',
                email=admin_email,
                password=generate_password_hash(admin_password),
                phone='0000000000',
                address='System Admin',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from routes.auth import auth_bp
    from routes.complaints import complaints_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(complaints_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    with app.app_context():
        db.create_all()
        create_admin(app)
        download_nltk_data()

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
