from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for users."""

    def setUp(self):
        """Add sample user and sample post."""

        users = db.session.execute(db.select(User)).scalars()
        for user in users:
            db.session.delete(user)

        posts = db.session.execute(db.select(Post)).scalars()
        for post in posts:
            db.session.delete(post)

        user = User(first_name="Test", last_name="User", image_url="https://i.pinimg.com/736x/39/d3/e0/39d3e06ebb09a79f805356b9db516078.jpg")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user_first_name = user.first_name
        self.user_last_name = user.last_name
        self.user_image_url = user.image_url

        post = Post(title="Test Title", content="Test Content", user_id=user.id)
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id
        self.title = post.title
        self.content = post.content
        self.created_at = post.created_at
        self.post_user_id = post.user_id

    def tearDown(self):
        """Clean any fouled transaction."""

        db.session.rollback()

    def test_root(self):
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)   

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Users', html)     

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add User', html)

    def test_new_user_form(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<button>Add</button>', html)       

    def test_add_user(self):
        with app.test_client() as client:
            d = {"firstName": "Test", "lastName": "User", "imageURL": "https://i.pinimg.com/736x/39/d3/e0/39d3e06ebb09a79f805356b9db516078.jpg"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"{self.user_first_name} {self.user_last_name}", html)

    def test_user_page(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"{self.user_first_name} {self.user_last_name}'s Page", html)  

    def test_edit_user_page(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"Edit {self.user_first_name} {self.user_last_name}", html)  

    def test_update_user(self):
        with app.test_client() as client:
            new_name = "Update"
            d = {"firstName": new_name, "lastName": self.user_last_name, "imageURL": self.user_image_url}
            resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"{new_name} {self.user_last_name}", html)  

    def test_delete_user(self):
        with app.test_client() as client:
            d = {"id": self.user_id}
            resp = client.post(f"/users/{self.user_id}/delete", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(f"{self.user_first_name} {self.user_last_name}", html)  

    def test_add_post(self):
        with app.test_client() as client:
            d = {"title": self.title, "content": self.content}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"{self.title}", html)  

    def test_update_post(self):
        with app.test_client() as client:
            new_title = "Update"
            d = {"title": new_title, "content": self.content}
            resp = client.post(f"/posts/{self.post_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(new_title, html)  

    def test_delete_post(self):
        with app.test_client() as client:
            d = {"id": self.post_id}
            resp = client.post(f"/posts/{self.post_id}/delete", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(self.title, html)  
            




        