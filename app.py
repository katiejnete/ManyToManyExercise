"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = '38432084'

connect_db(app)
app.app_context().push()

@app.route('/')
def home_page():
    """Redirects to list of all users in db"""
    return render_template('home.html')

@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    users = User.query.all()
    return render_template('list_users.html', users=users)

@app.route('/users/new')
def new_user_form():
    """Shows form to add a new user"""
    return render_template('new_user.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    """Inserts new user to db, and redirect to user detail page"""
    first_name = request.form["firstName"]
    last_name = request.form["lastName"]
    image_url = request.form["imageURL"]
    last_name = last_name if last_name else None
    image_url = image_url if image_url else None
    new_user = User(first_name=first_name,last_name=last_name,image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def user_page(user_id):
    """Shows user detail page"""
    u = User.query.get_or_404(user_id)
    return render_template("user.html", user=u)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Shows edit page for specific user"""
    u = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=u)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """Updates user on db"""
    u = User.query.get_or_404(user_id)
    u.first_name = request.form["firstName"] if request.form["firstName"] else u.first_name
    u.last_name = request.form["lastName"] if request.form["lastName"] else u.last_name
    u.image_url = request.form["imageURL"] if request.form["imageURL"] else u.image_url
    db.session.add(u)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Deletes user from db"""
    u = User.query.get_or_404(user_id)
    db.session.delete(u)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    """Shows form to user to add new post"""
    u = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('new_post.html', user=u, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """Handles new post submission"""
    post_data = request.form
    title = post_data.getlist('title')[0]
    content = post_data.getlist('content')[0]
    tagged = [PostTag(tag_id=tag_id) for tag_id in post_data.getlist('tag')]
    new_post = Post(title=title,content=content,user_id=user_id,tagged=tagged)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def post_page(post_id):
    """Shows post page"""
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    tags = [tag for (post_tag,tag,post) in Post.get_post_tags(post_id)]
    
    return render_template("post.html", post=post, user_id=user_id,tags=tags)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Shows edit form to edit post"""
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    tags = Tag.query.all()
    tagged = [tag for (post_tag,tag,post) in Post.get_post_tags(post_id)]
    checked = [tag for tag in tagged if tag in tags]
    unchecked = [tag for tag in tags if tag not in tagged]
    return render_template('edit_post.html',post=post, user_id=user_id, tagged=checked, untagged=unchecked)

@app.route('/posts/<int:post_id>/edit',methods=["POST"])
def update_post(post_id):
    """Updates post on db"""
    post = Post.query.get_or_404(post_id)
    post_data = request.form
    for pt in post.tagged:
        db.session.delete(pt)
        db.session.commit()
    post.title = post_data.getlist('title')[0] if request.form["title"] else post.title
    post.content = post_data.getlist('content')[0] if request.form["content"] else post.content    
    post.tagged = [PostTag(tag_id=tag_id, post_id=post_id) for tag_id in post_data.getlist('tag')]    
    db.session.add(post)
    db.session.commit()
    return redirect(f"/posts/{post_id}")

@app.route('/posts/<int:post_id>/delete',methods=["POST"])
def delete_post(post_id):
    """Deletes user from db"""
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route('/tags')
def list_tags():
    """Shows all tags with links to tag detail page."""
    tags = Tag.query.all()
    return render_template('list_tags.html',tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_page(tag_id):
    """Shows detail about tag."""
    t = Tag.query.get_or_404(tag_id)
    posts = [post for (post_tag,tag,post) in Tag.get_tagged_posts(tag_id)]
    return render_template('tag.html', tag=t, posts=posts)

@app.route('/tags/new')
def new_tag_form():
    """Shows form to add new tag."""
    return render_template('new_tag.html')

@app.route('/tags/new', methods=["POST"])
def add_tag():
    """Adds tag to db."""
    name = request.form["name"]
    new_tag = Tag(name=name)
    try:
        db.session.add(new_tag)
        db.session.commit()
    except:
        flash('Tag name already exists.')
    return redirect ('/tags')
    
@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """Shows form to edit tag."""
    return render_template('edit_tag.html',tag_id=tag_id)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def update_tag(tag_id):
    """Updates tag on db."""
    name = request.form["name"]
    tag = Tag.query.get_or_404(tag_id)
    tag.name = name
    try:
        db.session.add(tag)
        db.session.commit()
    except:
        flash('Tag name unchanged. Tag name already exists.')
    return redirect(f"/tags/{tag_id}")

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Delete tag on db."""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')


