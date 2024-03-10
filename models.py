"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime, timezone

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def connect_db(app):
    with app.app_context():
        db.app = app
        db.init_app(app)

class User(db.Model):
    """User"""
    __tablename__ = 'users'

    icon = '/static/user.png'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(40),
                           nullable=False)
    last_name = db.Column(db.String(40))
    image_url = db.Column(db.String,
                          nullable=False,
                          default=icon)
    
    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} {self.image_url}>"

class Post(db.Model):
    """Post"""
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(60),
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='SET NULL'))

    tagged = db.relationship('PostTag', cascade='all,delete', backref='post')
        
    def __repr__(self):
        return f"<Post {self.title} {self.content[0:10]} {self.created_at} {self.user_id}>"
    
    @classmethod
    def get_post_tags(cls,tag_id):
        """Get all post's tags."""
        return db.session.query(PostTag,Tag,cls).join(Tag).join(cls).filter(cls.id == tag_id).all()
        
class Tag(db.Model):
    """Tag"""
    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(60),
                     nullable=False,
                     unique=True)
    
    tagged = db.relationship('PostTag', backref='tag')
    
    def __repr__(self):
        return f"<Tag {self.name}>"
    
    @classmethod
    def get_tagged_posts(cls,tag_id):
        """Get all tagged posts."""
        return db.session.query(PostTag,cls,Post).join(cls).join(Post).filter(cls.id == tag_id).all()
   
class PostTag(db.Model):
    """Posts and Tags"""
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id', ondelete='CASCADE'),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id', ondelete='SET NULL'),
                       primary_key=True,
                       nullable=True)

    def __repr__(self):
        return f"<PostTag {self.post_id} {self.tag_id}>"
    
    