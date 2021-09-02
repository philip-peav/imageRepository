from flask import render_template, url_for, flash, redirect, abort
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, PostForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os

db.create_all()

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    posts.reverse()
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account has been created!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        
        else:
            flash('Login Failed! Please check Email and Password!', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    return render_template('account.html', title='Account')


def save_image(posted_image):
    random_hex = secrets.token_hex(8)
    file_name, file_extension = os.path.splitext(posted_image.filename)
    image_filename = random_hex + file_extension
    image_path = os.path.join(app.root_path, 'static/posted_imgs', image_filename)
    posted_image.save(image_path)

    return image_filename

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        image_file = save_image(form.image.data)
        post = Post(title=form.title.data, content=image_file, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Image has been posted!', 'success')
        print(image_file)
        return redirect(url_for('home'))
        
    return render_template('new_post.html', title ='New Post', form=form)


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)
    

@app.route("/post/delete/<post_id>", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    image_filepath = os.path.join(app.root_path, 'static/posted_imgs', post.content)
    os.remove(image_filepath)
    flash('Image has been deleted!', 'success')
    return redirect(url_for('home'))