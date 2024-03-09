"""Seed file to make sample data for db."""

from models import User, Post, Tag, PostTag, db
from app import app

db.drop_all()
db.create_all()

u1 = User(first_name="Miffy", last_name="Balloon")
u2 = User(first_name="Monchiichi", last_name="Flowers")
u3 = User(first_name="Choochoo", last_name="Cat")
u4 = User(first_name="Pochacco", last_name="Soccer")
u5 = User(first_name="Matcha", last_name="Lover")

c1 = "We all know Miffy Bunny, the world-famous rabbit, but have you met the rest of her family? Miffy has a father and mother, a grandpa and grandma, and there’s also a story where Baby Bunny joins the family. Was it a boy or girl bunny? We’ll never know, because Dick Bruna kept that a secret. Did you know that Miffy also has a favourite aunt? Her name is Aunt Alice and she Miffy’s father’s sister. Uncle Pilot isn’t really Miffy’s uncle. He’s just a friend of the family, but Miffy calls him “uncle”, Dutch people commonly do."
c2 = "For people who speak Dutch, “nijntje” is a logical contraction of “konijntje” (meaning “little bunny”). But things are different outside the Netherlands, where “nijntje” is difficult to pronounce for most people. The word for “bunny” is also different in every language, so Dick Bruna went in search of an international name for his little bunny. Together with his English translator, he came up with the name “Miffy”. It’s the kind of sound a bunny might make, but it has no special meaning. It’s also a name that is easy to pronounce in any language."
c3 = "Monchhichi was created in 1974 on the idea that such a doll, as a gift, could inspire friendship, love and happiness to the younger ones but also people of all ages. This philosophy has been guiding Sekiguchi and the product development since then. Today, Sekiguchi is glad to offer a fine selection of home-designed models to fans outside of Japan. We hope you’ll enjoy them as much as we enjoyed creating them!"
c4 = "A cute stuffed cat from [choo choo cat] from Korea has appeared. The cat can be made to sit, making it perfect for interior decoration in your room."
c5 = "Pochacco is a curious little guy who loves going for walks and eating banana ice cream. This sports-minded pup is a great basketball player and a not too shabby soccer goalie too!"
c6 = "These white chocolate matcha-covered strawberries are the perfect romantic treat and they're SO easy to make with only 3 ingredients! They're a unique twist on classic chocolate-covered strawberries for matcha lovers."
c7 = "This matcha tiramisu (also known as matchamisu) is my twist on the classic Italian tiramisu. This green tea dessert features layers of spongey and delicious matcha-soaked homemade ladyfingers placed within a creamy matcha mascarpone filling. With its vibrant green color and unique, mouthwatering flavor, this is one of the matcha recipes you don’t want to miss out on."

p1 = Post(title="Miffy Bunny",content=c1,user_id=1)
p2 = Post(title="the name 'miffy'",content=c2,user_id=1)
p3 = Post(title="Monchiichi",content=c3,user_id=2)
p4 = Post(title="Choo Choo Cat For Sale",content=c4,user_id=3)
p5 = Post(title="About Me",content=c5,user_id=4)
p6 = Post(title="Matcha-covered Strawberries",content=c6,user_id=5)
p7 = Post(title="Matcha Tiramisu",content=c7,user_id=5)

t1 = Tag(name='miffy',tagged=[PostTag(post_id=1), PostTag(post_id=2)])
t2 = Tag(name='matcha',tagged=[PostTag(post_id=6), PostTag(post_id=7)])

db.session.add_all([u1,u2,u3,u4,u5])

db.session.commit()

db.session.add_all([p1,p2,p3,p4,p5,p6,p7])

db.session.commit()

db.session.add_all([t1,t2])

db.session.commit()