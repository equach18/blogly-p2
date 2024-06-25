"""Seed file to make sample data for db."""

from app import app
from models import User, Post, db

# Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()

    User.query.delete()
    Post.query.delete()


    # Add sample employees and departments
    tom = User(first_name='Tom',last_name='Doe')
    bob = User(first_name='Bob',last_name='Chin')

    db.session.add_all([tom, bob])
    db.session.commit()

    p1 = Post(title='First Post!', content='I have no idea what to say.', user_id='1')
    p2 = Post(title='Second Post!', content='I still have no idea what to say.', user_id='2')

    db.session.add_all([p1,p2])
    db.session.commit()

