from app import db
from models import Feedback, User

db.drop_all()
db.create_all()

user = User(username='Briskrem', password='1234', email='crissjoedoe@gmail.com', first_name='chris', last_name='joseph')

feedback = Feedback(title='curtains', content='these curtains were exactly like in the photo', username='Briskrem')

db.session.add(user)
db.session.add(feedback)
db.session.commit()

