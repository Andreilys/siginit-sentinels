from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired
from urllib.parse import urlparse
from sqlalchemy.exc import SQLAlchemyError
from models import User
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
from app import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        
        if not username or not password:
            current_app.logger.warning("Login attempt with missing credentials")
            flash('Both username and password are required', 'danger')
            return render_template('auth/login.html', form=form)
        
        current_app.logger.info(f"Login attempt for user: {username}")
        
        try:
            # Check database connection first
            db.session.execute(db.text('SELECT 1'))
            
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                login_user(user, remember=remember)
                current_app.logger.info(f"Successful login for user: {username}")
                
                # Get next page from session
                next_page = request.args.get('next')
                if not next_page or urlparse(next_page).netloc != '':
                    next_page = url_for('main.dashboard')
                    
                return redirect(next_page)
            
            current_app.logger.warning(f"Failed login attempt for user: {username} - Invalid credentials")
            flash('Invalid username or password', 'danger')
            
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error during login: {str(e)}")
            flash('Database connection error. Please try again later.', 'danger')
        except Exception as e:
            current_app.logger.error(f"Unexpected error during login: {str(e)}")
            flash('An unexpected error occurred. Please try again.', 'danger')
            
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
