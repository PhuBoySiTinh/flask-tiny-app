from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, db
from .forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("index.html")

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    posts = Post.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', user=current_user, posts=posts)

@main.route('/dashboard/add_post', methods=['POST'])
@login_required
def add_post():
    title = request.form.get('title')
    content = request.form.get('content')
    if title and content:
        new_post = Post(title=title, content=content, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard/delete_posts', methods=['POST'])
@login_required
def delete_posts():
    post_ids = request.form.getlist('post_ids')
    if post_ids:
        Post.query.filter(Post.id.in_(post_ids), Post.user_id == current_user.id).delete(synchronize_session=False)
        db.session.commit()
    return redirect(url_for('main.dashboard'))


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        return "Access Denied", 403
    users = User.query.all()
    return render_template('admin.html', users=users)

@main.route('/admin/block/<int:user_id>')
@login_required
def block_user(user_id):
    if not current_user.is_admin:
        return "Access Denied", 403
    user = User.query.get(user_id)
    if user:
        user.is_active = False
        db.session.commit()
    return redirect(url_for('main.admin'))

@main.route('/admin/unblock/<int:user_id>')
@login_required
def unblock_user(user_id):
    if not current_user.is_admin:
        return "Access Denied", 403
    user = User.query.get(user_id)
    if user:
        user.is_active = True
        db.session.commit()
    return redirect(url_for('main.admin'))

@main.route('/admin/reset_password/<int:user_id>')
@login_required
def reset_password(user_id):
    if not current_user.is_admin:
        return "Access Denied", 403
    user = User.query.get(user_id)
    if user:
        user.password = generate_password_hash("newpassword123")
        db.session.commit()
    return redirect(url_for('main.admin'))


