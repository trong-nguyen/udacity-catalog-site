import sys
import os
from models import session, DB_NAME
from models import Sport, Gear, User


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

    def find_object(name, objects):
        try:
            return next(o for o in objects if o.title == name)
        except:
            print 'Error finding id of object with name', name
            raise

    gears = [
        {
            'title': 'Basketball Net',
            'description': (
                "A QUALITY SLAM DUNK If you're not"
                "impressed with the quality of our basketball nets,"
                "we'll refund your money-no questions asked"
                ),
            'sport_name': 'Basketball',
        },
        {
            'title': 'Climbing Harness',
            'description': (
                "Traditional buckle, harness construction distributes"
                " pressure to keep you comfortable while climbing;waist"
                " belt and leg loop are lineed with breathable mesh to"
                " ensure comfort in warm temperatures."
                ),
            'sport_name': 'Rock Climbing',
        },
        {
            'title': 'Foosball Tabletop',
            'description': 'High Quality wood build withstands wear',
            'sport_name': 'Foosball',
        },
        {
            'title': 'Mondor Knee-High Skating Socks 2 Pairs',
            'description': '85% nylon microfiber, 15% lycra (r) spandex',
            'sport_name': 'Skating',
        },
        {
            'title': 'Nike Swoosh Headband',
            'description': (
                'Nike Swoosh Headband, '
                'Embroidered Swoosh logo, '
                'Machine washable, '
                'Easy care'
                ),
            'sport_name': 'Basketball',
        },
        {
            'title': 'Stick',
            'description': (
                'Includes official size 65mm low density street'
                ' hockey ball'
                ),
            'sport_name': 'Hockey',
        },
        {
            'title': 'Goggles',
            'description': (
                "Swimming Goggles, PHELRENA Professional Swim"
                " Goggles Anti Fog UV Protection No Leaking"
                " for Adult Men Women Kids Swim"
                ),
            'sport_name': 'Snowboarding',
        },
        {
            'title': 'Two shinguards',
            'description': (
                "2 Pair Youth Soccer Shin Guards, Kids Soccer"
                " Child Calf Protective Gear Soccer Equipment"
                " for 5-12 Years Old Boys Girls Children Teenagers"
                ),
            'sport_name': 'Soccer',
        },
        {
            'title': 'Shinguards',
            'description': 'Hard shell with foam backing for added protection',
            'sport_name': 'Soccer',
        },
        {
            'title': 'Frisbee',
            'description': (
                "Discraft 175 gram Ultra-Star Sportdisc-Nite-Glo,"
                " colors may vary'"
                ),
            'sport_name': 'Frisbee',
        },
        {
            'title': 'Bat',
            'description': (
                "PowerNet Sweet Spot Training Bat and 3.2\""
                " Progressive Weighted Ball (9 Pack) PRO Bundle"
                " for Baseball Softball"
                ),
            'sport_name': 'Baseball',
        },
        {
            'title': 'Jersey',
            'description': "adidas Men's Soccer Estro Jersey'",
            'sport_name': 'Soccer',
        },
        {
            'title': 'Soccer Cleats',
            'description': (
                "Dream Pairs 151028-151030 Men's Sport"
                " Flexible Athletic Free Running Light Weight"
                " Indoor/Outdoor Lace Up Soccer Shoes"
                ),
            'sport_name': 'Soccer',
        }
    ]

    # processing the relationship Sport-Gears
    for gear in gears:
        obj = find_object(gear['sport_name'], sports)
        del gear['sport_name']
        #re-assign
        gear['sport'] = obj
        gear['sport_id'] = obj.id


    gears = [Gear(**g) for g in gears]
    session.add_all(gears)
    session.commit()


    # users
    user_data = [
        {
            'name': 'Dale',
            'email': 'dale@a.com',
            'password': 'p'
        },
        {
            'name': 'Jenny',
            'email': 'jen@b.com',
            'password': 'p'
        },
        {
            'name': 'Trong Nguyen',
            'email': 'trongn@c.com',
            'password': 'p'
        }
    ]
    users = [User(name=d['name'], email=d['email']) for d in user_data]
    # for i, user in enumerate(users):
    #     user.hash_password(user_data[i]['password'])
    session.add_all(users)
    session.commit()


if __name__ == '__main__':
    if is_db_ok(DB_NAME):
        populate_data(session)
