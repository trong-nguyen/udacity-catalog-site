from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from datetime import datetime

DB_NAME = 'catalog'

# create a SQL engine to PostgreSQL
# https://stackoverflow.com/questions/23839656/sqlalchemy-no-password-supplied-error
engine = create_engine('postgresql:///{}'.format(DB_NAME))

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


class User(Mixin, Base):
    name = Column(String(256))
    email = Column(String, nullable=False)
    picture = Column(String)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }


class Sport(Mixin, Base):
    title = Column(String(256))
    gears = relationship('Gear', backref='sport')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'gears': [g.title for g in self.gears]
        }


class Gear(Mixin, Base):
    title = Column(String(256), nullable=False)
    description = Column(String)
    sport_id = Column(Integer, ForeignKey('sport.id'), nullable=False)
    added_on = Column(DateTime, default=datetime.utcnow)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.sport.title,
            'added_on': self.added_on.strftime('%H:%M:%S %m-%d-%y')
        }

# physically create the database
Base.metadata.create_all(engine)
