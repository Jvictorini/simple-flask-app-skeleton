import os
import sys
import random
import datetime
import requests
from surflesson import db, bcrypt
from surflesson.models import User, LessonType, Lesson, Message
from lorem_text import lorem

host = 'localhost'  # host where the system is running
port = 5000  # port where the process is running


def reload_database():
    exit_reload = False
    try:
        response = requests.get(f'http://{host}:{port}')
        print('The website seems to be running. Please stop it and run this file again.', file=sys.stderr)
        exit_reload = True
    except:
        pass
    if exit_reload:
        exit(11)
    try:
        os.remove('surflesson/site.db')
        print('previous DB file removed')
    except:
        print('no previous file found')

    db.create_all()

    # creating two users
    # hashed_password = bcrypt.generate_password_hash('testing').decode('utf-8')
    # default_user1 = User(username='Default',
    #                      email='default@test.com',
    #                      image_file='another_pic.jpeg',
    #                      password=hashed_password)
    # db.session.add(default_user1)
    #
    # hashed_password = bcrypt.generate_password_hash('testing2').decode('utf-8')
    # default_user2 = User(username='Default Second',
    #                      email='second@test.com',
    #                      image_file='7798432669b8b3ac.jpg',
    #                      password=hashed_password)
    # db.session.add(default_user2)
    #
    # hashed_password = bcrypt.generate_password_hash('testing3').decode('utf-8')
    # default_user3 = User(username='Default Third',
    #                      email='third@test.com',
    #                      password=hashed_password)
    # db.session.add(default_user3)

    # TODO: Here you should include the generation of rows for your database
    hashed_password = bcrypt.generate_password_hash('testing').decode('utf-8')

    instructor_1 = User(type_of_user=1, username='Jacobi', email='victorini@gmail.com', password=hashed_password)
    db.session.add(instructor_1)

    level_1_lesson = LessonType(title='Level 1', price=650, content='This is level 1')
    db.session.add(level_1_lesson)
    db.session.commit()

    level_2_lesson = LessonType(title='Level 2', price=700, content='This is level 2')
    db.session.add(level_2_lesson)
    db.session.commit()

    # lesson_1 = Lesson(date_for_lesson='4 Juni 2021 8.00', lesson_type_id=level_1_lesson.id)
    # db.session.add(lesson_1)

    lesson_1 = Lesson(date_for_lesson=datetime.date(2021,6,7),time_for_lesson='10:00', lesson_type_id=level_1_lesson.id, user_id=instructor_1.id)
    db.session.add(lesson_1)

    # lesson_2 = Lesson(date_for_lesson='5 Juni 2021 10.00', lesson_type_id=level_2_lesson.id)
    # db.session.add(lesson_2)

    lesson_2 = Lesson(date_for_lesson=datetime.date(2021,5,5), time_for_lesson='9:00', lesson_type_id=level_2_lesson.id, user_id=instructor_1.id)
    db.session.add(lesson_2)

    hashed_password = bcrypt.generate_password_hash('testing1').decode('utf-8')

    student_1 = User(type_of_user=2, username='Johanna', email='johanna@gmail.com', password=hashed_password)
    db.session.add(student_1)

    message_1 = Message(content='hur surfa man?', author=student_1, lesson=lesson_1)
    db.session.add(message_1)
    db.session.commit()

    lesson_1.users.append(student_1)
    lesson_1.users.append(instructor_1)


    try:
        db.session.commit()
        print('\nFinalized - database created successfully!')
    except Exception as e:
        print('The operations were not successful. Error:', file=sys.stderr)
        print(e, file=sys.stderr)
        db.session.rollback()


if __name__ == '__main__':
    reload_database()
