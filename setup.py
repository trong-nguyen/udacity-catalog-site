from models import Sport, Gear
from models import session

soccer = Sport(title='Soccer')
session.add(soccer)
session.commit()

glove = Gear(
	title='Glove',
	description='To catch balls',
	sport_id=soccer.id
	)

ball = Gear(
	title='Ball',
	description='To allow players score and maneuver',
	sport_id=soccer.id
	)

session.add(glove)
session.add(ball)
session.commit()
