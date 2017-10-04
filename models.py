from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

DB_NAME = 'catalog.db'

# create the SQL engine
engine = create_engine('sqlite:///{}'.format(DB_NAME))

# initiate and bind it to the Alchemy layer
Base = declarative_base()
Base.metadata.bind = engine

session = sessionmaker(bind=engine)()

class Mixin(object):
	"""Implements the basic id and class-name based __tablename__"""
	@declared_attr
	def __tablename__(cls):
		return cls.__name__.lower()

	id = Column(Integer, primary_key=True)


class Sport(Mixin, Base):
	title = Column(String(128))

	@property
	def serialize(self):
		gears = session.query(Gear).filter_by(sport_id=self.id)

		return {
			'id': self.id,
			'title': self.title,
			'gears': [g.title for g in gears]
		}

class Gear(Mixin, Base):
	title = Column(String(128), nullable=False)
	description = Column(String)
	sport_id = Column(Integer, ForeignKey('sport.id'), nullable=False)
	added_on = Column(DateTime, default=datetime.utcnow)

	@property
	def serialize(self):
		cat = session.query(Sport).filter_by(id=self.sport_id).one().title

		return {
			'id': self.id,
			'title': self.title,
			'description': self.description,
			'category': cat,
			'added_on': self.added_on.strftime('%H:%M:%S %m-%d-%y')
		}

# physically create the database
Base.metadata.create_all(engine)