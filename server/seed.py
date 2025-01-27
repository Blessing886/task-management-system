#!/usr/bin/env python3

from app import app
from models import db, User, Department, Task, TaskAssignment, Comment

with app.app_context():

    User.query.delete()
    Department.query.delete()
    Task.query.delete()
    TaskAssignment.query.delete()
    Comment.query.delete()

    users = []
    departments = []
    tasks = []
    task_assignment = []
    comments = []

    # user instances
    users.append(User(name = 'Nelson Oketch', email = 'nelson@gmail.com', role = 'Manager'))
    users.append(User(name = 'Tina Moraa', email = 'tina@gmail.com', role = 'Manager'))
    users.append(User(name = 'Richard Medo', email = 'medo@gmail.com', role = 'employee'))
    users.append(User(name = 'Betty Aziz', email = 'betty@gmail.com', role = 'employee'))
    users.append(User(name = 'Ness Wafula', email = 'ness@gmail.com', role = 'employee'))
    users.append(User(name = 'Mejju Kombo', email = 'mejju@gmail.com', role = 'employee'))

    db.session.add_all(users)
    db.session.commit()

    # department instances
    departments.append(Department(name = 'Electrical Engineering', description = 'Handles electrical and electronic issues.', manager_id = users[0].id))
    departments.append(Department(name = 'Mechanical Engineering', description = 'Handles mechanical related issues.', manager_id = users[1].id))

    db.seesion.add_all(departments)
    db.seesion.commit()

    # assigning users to departments
    users[0].department = departments[0]
    users[1].department = departments[1]
    users[2].department = departments[0]
    users[3].department = departments[1]
    users[4].department = departments[0]
    users[5].department = departments[1]
    
    db.session.commit()
