from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()

@app.route('/')
def homepage():
    """Redirects to list of users."""

    return redirect("/users")

@app.route('/users')
def list_users():
    """Show all users with links for more details. Contains link to add a user"""
    users = User.query.all()
    return render_template("index.html", users=users)

@app.route('/users/new')
def show_user_form():
    """Shows an add form for users"""
    return render_template("new-user.html")

@app.route('/users/new', methods=['POST'])
def add_user():
    """Processes the add form, adding a new user and goes back to /users"""

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    img_url = request.form['img-url'] or None

    user = User(first_name=first_name, last_name=last_name, image_url=img_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_info(user_id):
    """Shows information about the given user."""
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', user=user)


@app.route('/users/<int:user_id>/edit')
def show_edit_user(user_id):
    """Shows the edit page for the user. """
    user = User.query.get_or_404(user_id)
    return render_template('edit-user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """Finalize the edits of a user"""
    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first-name'] or user.first_name
    user.last_name = request.form['last-name'] or user.last_name
    user.img_url = request.form['img-url'] or None

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Finalize the edits of a user"""
    user = User.query.get_or_404(user_id)

    user.query.filter_by(id = user_id).delete()
    
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """Shows form to add a post for that user"""
    user = User.query.get_or_404(user_id)
    return render_template('post-form.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def handle_post_form(user_id):
    """Handles post add and redirects to the user detail page."""
    
    title = request.form['title']
    content = request.form['content']
    
    post = Post(title=title, content=content,user_id=user_id)
    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route('/posts/<post_id>')
def show_post(post_id):
    """shows the post and buttons to cancel, edit, and delete"""
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',post=post)

@app.route('/posts/<post_id>/edit')
def show_edit_post(post_id):
    """Shows form to edit a post and to cancel"""
    post = Post.query.get_or_404(post_id)
    return render_template('edit-post.html', post=post)
    
@app.route('/posts/<post_id>/edit', methods=['POST'])
def handle_post_edit(post_id):
    """Handles the editing of a post. Redirects back to the post view"""
    post = Post.query.get_or_404(post_id)
    
    post.title = request.form['title'] or post.title
    post.content = request.form['content'] or post.content

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post.id}")

@app.route('/posts/<post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Deletes the post."""
    post = Post.query.get_or_404(post_id)
    
    post.query.filter_by(id=post_id).delete()
    
    db.session.commit()
    
    return redirect(f"/")