import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from surflesson import app, db, bcrypt
from surflesson.forms import RegistrationForm, LoginForm, UpdateAccountForm, CreateLessonForm
from surflesson.models import User, Lesson, LessonType, Message
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

@app.route("/")
@app.route("/home")
def home():
    lessons = []
    lessons = Lesson.query.all()
    lesson_type = []
    lesson_type = LessonType.query.all()
    messages = []
    messages = Message.query.all()


    return render_template('home.html', lessons=lessons, lesson_type=lesson_type, messages=messages)


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
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',
                           title='Register',
                           form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html',
                           title='Login',
                           form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_compressed_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def save_raw_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    form_picture.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_compressed_picture(form.picture.data)
            #picture_file = save_raw_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',
                           title='Account',
                           image_file=image_file,
                           form=form)


# TODO: create here your routes
@app.route("/create_lesson", methods=['GET', 'POST'])
def create_lesson():
    form = CreateLessonForm()
    lesson_types = LessonType.query.all()
    for lesson_type in lesson_types:
        form.lesson_type.choices.append((lesson_type.id, lesson_type.title ))
    if form.validate_on_submit():
        lesson = Lesson(date_for_lesson=form.date_for_lesson.data, time_for_lesson=form.time_for_lesson.data, lesson_type_id=form.lesson_type.data)
        db.session.add(lesson)
        db.session.commit()
        flash('Your lesson has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_lesson.html',
                           title='Create Lesson',
                           form=form)


@app.route("/lesson/<int:lesson_id>")
def lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    return render_template('lesson.html', lesson=lesson)


@app.route("/lesson/<int:lesson_id>/delete", methods=['POST'])
@login_required
def delete_lesson(lesson_id):
    lesson_to_delete = Lesson.query.get_or_404(lesson_id)
    #messages_to_delete = Message.query.get_or_404(lesson_id)
 #   if post_to_delete.author != current_user:
  #      abort(403)  # only the author can delete their posts
    # first we need to delete all the comments
    # this can be also configured as "cascade delete all"
    # so that all comments are deleted automatically
    # I personally prefer explicitly deleting the child rows
    # see models.py file, class Comment

   #we have to delete messages also...
    # for message in messages_to_delete.lesson_id:
    #     db.session.delete(message)
    db.session.delete(lesson_to_delete)
    db.session.commit()
    flash('The lesson has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/lesson/<int:lesson_id>/update", methods=['GET', 'POST'])
@login_required
def update_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    lesson_types = LessonType.query.all()
    form = CreateLessonForm()

    for lesson_type in lesson_types:
        form.lesson_type.choices.append((lesson_type.id, lesson_type.title ))

    if form.validate_on_submit():
        lesson.date_for_lesson = form.date_for_lesson.data
        lesson.time_for_lesson = form.time_for_lesson.data
        lesson_types.title = form.lesson_type.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('lesson', lesson_id=lesson.id))
    elif request.method == 'GET':
        form.date_for_lesson.data = lesson.date_for_lesson
        form.time_for_lesson.data = lesson.time_for_lesson
        form.lesson_type.data = lesson.lesson_type_id
    return render_template('create_lesson.html', title='Update Lesson',
                           form=form, legend='Update Lesson')

