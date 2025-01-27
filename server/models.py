from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

# Models go here!
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    role = db.Column(db.Enum('Manager', 'Employee', name='user_role'), nullable=False)

    #Relationships
    department = db.relationship('Department', back_populates='users')
    created_tasks = db.relationship('Task', back_populates='created_by')
    assigned_tasks = db.relationship('Task', secondary='task_assignment', back_populates='assigned_users')
    comments = db.relationship('Comment', back_populates='user')
    managed_department = db.relationship('Department', back_populates='manager', uselist=False)


    serialize_rules = ('-department.users', '-created_tasks.created_by', '-assigned_tasks.assigned_users', '-comments.user')

    #email validation
    # @validates('email')
    # def validate_email(self, key, email):
        # if '@' not in email:
            # raise ValueError("Invalid email address")
        # return email
    
class Department(db.Model, SerializerMixin):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

    # relationships
    manager = db.relationship('User', back_populates='managed_department')
    users = db.relationship('User', back_populates='department')

    serialize_rules = ('-manager.department', '-users.department')

class Task(db.Model, SerializerMixin):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum('Pending', 'In Progress', 'Completed', 'On Hold', name='task_status'))
    priority = db.Column(db.String)
    created_by_user_id = db.Column(db.Integer)
    due_date = db.Column(db.Date)
    comments_text = db.Column(db.Text)

    # relationships
    created_by = db.relationship('User', back_populates='created_tasks')
    assigned_users = db.relationship('User', secondary='task_assignment', back_populates='assigned_tasks')
    comments = db.relationship('Comment', back_populates='task')

    serialize_rules = ('created_by.created_tasks', '-assigned_users.assigned_tasks', '-comments.task')

class TaskAssignment(db.Model, SerializerMixin):
    __tablename__ = 'task_assignment'

    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    serialize_rules = ('-task.assigned_users', '-user.assigned_tasks')

class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)

    # relationships
    task = db.relationship('Task', back_populates='comments')
    user = db.relationship('User', back_populates='comments')

    serialize_rules = ('-task.comments', '-user.comments')

