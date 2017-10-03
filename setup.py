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
	sports = [
		'Soccer',
		'Basketball',
		'Baseball',
		'Frisbee',
		'Snowboarding',
		'Rock Climbing',
		'Foosball',
		'Skating',
		'Hockey'
	]
	sports = [Sport(title=t) for t in sports]

	session.add_all(sports)
	session.commit()

	def find_id(name, objects):
		try:
			return next(o for o in objects if o.title==name).id
		except:
			print 'Error finding id of object with name', name
			raise

	gears = [
		{
			'title': 'Stick',
			'description': '',
			'sport_id': find_id('Hockey', sports)
		},
		{
			'title': 'Goggles',
			'description': '',
			'sport_id': find_id('Snowboarding', sports)
		},
		{
			'title': 'Two shinguards',
			'description': '',
			'sport_id': find_id('Soccer', sports)
		},
		{
			'title': 'Shinguards',
			'description': '',
			'sport_id': find_id('Soccer', sports)
		},
		{
			'title': 'Frisbee',
			'description': '',
			'sport_id': find_id('Frisbee', sports)
		},
		{
			'title': 'Bat',
			'description': '',
			'sport_id': find_id('Baseball', sports)
		},
		{
			'title': 'Jersey',
			'description': '',
			'sport_id': find_id('Soccer', sports)
		},
		{
			'title': 'Soccer Cleats',
			'description': '',
			'sport_id': find_id('Soccer', sports)
		}
	]

	gears = [Gear(**g) for g in gears]
	session.add_all(gears)
	session.commit()

if __name__ == '__main__':
	if is_db_ok(DB_NAME):
		populate_data(session)

