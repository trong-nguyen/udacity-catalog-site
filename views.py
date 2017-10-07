import json
from flask import (Flask, jsonify,
	request, url_for, abort, g as app_g,
	make_response, render_template, flash,
    session as user_session,
	)
from models import Sport, Gear, User, session as db_session
from oauth2client.client import (
    flow_from_clientsecrets,
    FlowExchangeError
    )
import requests
import random
import string

app = Flask(__name__)

def make_session_secret_state():
    '''
    Make a random string representing
    a per-session identifier
    '''
    return ''.join([random.choice(string.ascii_uppercase + string.digits)
        for x in range(32)])


def get_gplus_token_info(token):
    url = (
        'https://www.googleapis.com/oauth2/v1'
        '/tokeninfo?access_token={}'
        ).format(token)
    res = requests.get(url)
    if res.ok:
        return res.json()
    else:
        return None


def requires_auth(f):
    def deco(*args, **kwargs):
        if 'email' not in user_session:
            return login()
        return f(*args, **kwargs)
    return deco


@app.route('/login')
def login():
    user_session['state'] = state = make_session_secret_state()
    access_token = user_session.get('access_token')
    if (access_token is not None
        and get_gplus_token_info(access_token) is not None
        ):
        return render_template(
            'login_already.html',
            name=user_session.get('name'),
            picture=user_session.get('picture')
            )
    else:
        return render_template('login.html', state=state)


@app.route('/logout')
def logout():
    return gdisconnect()


def gdisconnect():
    access_token = user_session.get('access_token')
    print access_token
    if not access_token:
        return make_response(
            json.dumps('User not logged in'),
            401
            )

    # revoke token
    url = (
        'https://accounts.google.com/o/oauth2/revoke'
        '?token={}'
        ).format(access_token)

    res = requests.get(url)
    if res.ok:
        for state in [
            'access_token',
            'gplus_id',
            'provider',
            'name',
            'picture',
            'email'
            ]:
            del user_session[state]
        return make_response(
            json.dumps('Successfully disconnected from gplus'),
            200
            )
    else:
        return make_response(
            json.dumps('Failed to revoke tokens'),
            400
            )

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # check state
    if request.args.get('state') != user_session['state']:
        return make_response(
            json.dumps('App client in disguise, mismatched state'),
            400
            )

    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        return make_response(
            json.dumps('OAuth flow failed'),
            401
            )

    access_token = credentials.access_token

    result = get_gplus_token_info(access_token)
    if result is None:
        return json.dumps('Invalid access token'), 500


    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        return json.dumps('Mismatched claimed id vs. token id'), 400

    client_secrets = json.loads(open('client_secrets.json', 'r').read())
    gclient_id = client_secrets['web']['client_id']
    if result['issued_to'] != gclient_id:
        return json.dumps('Mismatched requested id vs. issued client id'), 400

    stored_access_token = user_session.get('access_token')
    stored_gplus_id = user_session.get('gplus_id')

    already_logged_in = (stored_access_token is not None
        and gplus_id == stored_gplus_id)

    # just take the newest one no matter what
    user_session['access_token'] = credentials.access_token
    user_session['gplus_id'] = gplus_id

    if already_logged_in:
        return json.dumps('User already logged in'), 200

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    user_session['provider'] = 'google'
    user_session['name'] = data['name']
    user_session['picture'] = data['picture']
    user_session['email'] = data['email']

    # see if user exists, if not then create
    user = db_session.query(User).filter_by(email=data['email']).first()
    if not user:
        user = User(
            email=data['email'],
            name=data['name'],
            picture=data['picture']
            )
        db_session.add(user)
        db_session.commit()

    user_session['user_id'] = user.id
    flash('You are logged in as {}'.format(user_session['name']))
    return render_template(
        'login_success.html',
        name=user_session['name'],
        picture=user_session['picture']
        )


@app.route('/')
@app.route('/catalog')
def show_catalog():
	categories = db_session.query(Sport).all()

	num_latest = 10
	items = db_session.query(Gear).order_by(Gear.added_on.desc())
	latest_items = items.limit(num_latest).all()
	latest_items = [item.serialize for item in items]
	return render_template(
		'catalog_latest.html',
		categories=categories,
		items=latest_items,
        session=user_session,
		)

@app.route('/catalog/<string:sport_name>/items')
def show_gears(sport_name):
	sport = db_session.query(Sport).filter_by(title=sport_name).first()
	if sport is None:
		return make_response(
			json.dumps('Invalid sport name: {}'.format(sport_name)),
			404
			)

	categories = db_session.query(Sport).all()
	items = db_session.query(Gear).filter_by(sport_id=sport.id).all()
	return render_template(
		'catalog_items.html',
		categories=categories,
		items=items,
		category=sport.title,
        session=user_session,
		)

@app.route('/catalog/<string:sport_name>/<string:gear_name>')
def show_gear(sport_name, gear_name):
	sport = db_session.query(Sport).filter_by(title=sport_name).first()
	if sport is None:
		return make_response(
			json.dumps('Invalid sport name: {}'.format(sport_name)),
			404
			)

	q = db_session.query(Gear)
	try:
		item = q.filter_by(sport_id=sport.id, title=gear_name).one()
	except:
		return make_response(
			json.dumps('Invalid gear name: {}'.format(gear_name)),
			404
			)

	return render_template(
		'item_details.html',
		item=item,
		category=sport.title,
        session=user_session,
		)


"""
HERE
"""
@app.route('/catalog/edit')
def edit_gear():
    data = map(request.args.get, ['title', 'description', 'category'])

    if not all(data):
        return json.dumps('Invalid data {}'.format(data), 400)

    title, description, category = data

    cat = db_session.query(Sport).filter_by(title=category).first()
    if not cat:
        return json.dumps('Invalid category {}'.format(category), 400)

    gear = db_session.query(Gear).filter_by(title=title).first()

    if gear:
        gear.description = description
        gear.sport = cat
    else:
        gear = Gear(title=title, description=description, sport=cat)
        db_session.add(gear)
        db_session.commit()

    return jsonify(gear.serialize), 200

@app.route('/catalog/<string:sport>', methods=['POST'])
def add_gear(sport):
	item = request.json
	print 'adding item {}'.format(gear, item)
	response = make_response(json.dumps('Added {}'.format(item)), 200)
	return response

# @app.route('/catalog/<string:sport>/<string:gear>/edit', methods=['PUT'])
# def edit_gear(sport, gear):
# 	print 'editing item {} with values {}'.format(gear, request.json)
# 	response = make_response(json.dumps('Item {} edited'.format(gear)), 200)
# 	return response

@app.route('/catalog/<string:sport>/<string:gear>/edit', methods=['DELETE'])
def delete_gear(sport, gear):
	response = make_response(json.dumps('Deleted gear {}'.format(gear)), 204)
	return response


@app.route('/api/<string:version>')
@app.route('/api/<string:version>/catalog')
def api_show_catalog(version):
	response = jsonify([
		{
			'name': "Soccer",
			'items': ['a', 'b', 'c']
		},
		{
			'name': "Basketball",
			'items': ['a', 'e', 'f', 'g']
		}
	]), 200
	return response


@app.route('/api/<string:version>/catalog/<string:sport>')
def api_show_gears(version, sport):
	response = jsonify([
		'gloves',
		'balls',
		'socks'
	]), 200
	return response

@app.route('/api/<string:version>/catalog/<string:sport>/<string:gear>')
def api_show_gear(version, sport, gear):
	response = jsonify({
		'title': 'gloves',
		'description': 'wear it and catch balls',
		'category': 'Soccer'
	}), 200
	return response

@app.route('/register', methods=['POST'])
def register():
    body = request.json
    creds = map(body.get, ['email', 'name', 'password'])

    if not all(creds):
        return make_response(
            json.dumps('Please provide valid email, name, AND password'),
            400,
            )

    email, name, password = creds

    if db_session.query(User).filter_by(email=email).first() is not None:
        return make_response(
            json.dumps('Email {} has been used'.format(email)),
            400,
            )

    user = User(email=email, name=name)
    user.hash_password(password)
    db_session.add(user)
    db_session.commit()

    return jsonify(user.serialize), 201


if __name__ == '__main__':
	app.secret_key = '03uklsjadf09'
	app.debug = True
	app.run(host='0.0.0.0', port=5001)
