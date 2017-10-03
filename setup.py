import sys
import os
from models import session, DB_NAME
from models import Sport, Gear

def is_db_ok(name):
	if not os.path.exists(name):
		return True

	q = (
		'database {} exists, erase it?'
		' (y to proceed)'
		).format(name)
	inp = raw_input(q)

	if inp == 'y':
		# We have to remove the database
		# and rewire its internals
		os.remove(name)

		from models import Base, create_engine

		# recreate the SQL engine
		engine = create_engine('sqlite:///{}'.format(name))

		# rebinding Base's engine
		Base.metadata.bind = engine

		# recreate the database
		Base.metadata.create_all(engine)
		return True
	else:
		return False

def populate_data(session):
	# Populating data
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

if __name__ == '__main__':
	if is_db_ok(DB_NAME):
		populate_data(session)

