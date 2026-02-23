from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FileField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import pandas as pd
from flask_bootstrap import Bootstrap4

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
bootstrap = Bootstrap4(app)

# Load jobs data
jobs_df = pd.read_csv('jobs.csv')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    biodata = db.Column(db.Text)
    resume_filename = db.Column(db.String(100))
    preferences = db.Column(db.String(200))  # comma-separated skills/preferences

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Applied')

# Forms
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class ProfileForm(FlaskForm):
    biodata = TextAreaField('Biodata')
    resume = FileField('Resume (PDF only)')
    preferences = StringField('Job Preferences/Skills (comma-separated)')
    submit = SubmitField('Update Profile')

# Routes
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email already exists', 'danger')
        else:
            hashed_password = generate_password_hash(form.password.data)
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully', 'success')
            return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.biodata = form.biodata.data
        current_user.preferences = form.preferences.data
        if form.resume.data:
            filename = secure_filename(form.resume.data.filename)
            if filename and filename.lower().endswith('.pdf'):
                form.resume.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                current_user.resume_filename = filename
            else:
                flash('Only PDF files are allowed for resume', 'danger')
                return redirect(url_for('profile'))
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.biodata.data = current_user.biodata
        form.preferences.data = current_user.preferences
    return render_template('profile.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    # Simple recommendation: match preferences with job skills
    recommended_jobs = []
    if current_user.preferences:
        user_skills = [skill.strip().lower() for skill in current_user.preferences.split(',')]
        for _, job in jobs_df.iterrows():
            if job['skills_required'].lower() in user_skills:
                recommended_jobs.append(job.to_dict())
    return render_template('dashboard.html', jobs=recommended_jobs[:5])  # Show top 5

@app.route('/jobs')
@login_required
def jobs():
    jobs_list = jobs_df.to_dict('records')
    return render_template('jobs.html', jobs=jobs_list)

@app.route('/apply/<job_title>')
@login_required
def apply(job_title):
    job = jobs_df[jobs_df['job_title'] == job_title].iloc[0]
    application = Application(user_id=current_user.id, job_title=job['job_title'], company=job['company'])
    db.session.add(application)
    db.session.commit()
    flash('Application submitted successfully', 'success')
    return redirect(url_for('dashboard'))

@app.route('/applications')
@login_required
def applications():
    apps = Application.query.filter_by(user_id=current_user.id).all()
    return render_template('applications.html', applications=apps)

@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
