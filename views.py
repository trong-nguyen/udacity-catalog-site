import json
from flask import (Flask, jsonify,
	request, url_for, abort, g,
	make_response, render_template
	)
from models import (
	Sport, Gear, User,
	session,
	)

app = Flask(__name__)

@app.route('/')
@app.route('/catalog')
def show_catalog():
	categories = session.query(Sport).all()

	num_latest = 10
	items = session.query(Gear).order_by(Gear.added_on.desc())
	latest_items = items.limit(num_latest).all()
	latest_items = [item.serialize for item in items]
	return render_template(
		'catalog_latest.html',
		categories=categories,
		items=latest_items,
		)

@app.route('/catalog/<string:sport_name>/items')
def show_gears(sport_name):
	sport = session.query(Sport).filter_by(title=sport_name).first()
	if sport is None:
		return make_response(
			json.dumps('Invalid sport name: {}'.format(sport_name)),
			404
			)

	categories = session.query(Sport).all()
	items = session.query(Gear).filter_by(sport_id=sport.id).all()
	return render_template(
		'catalog_items.html',
		categories=categories,
		items=items,
		category=sport.title
		)

@app.route('/catalog/<string:sport_name>/<string:gear_name>')
def show_gear(sport_name, gear_name):
	sport = session.query(Sport).filter_by(title=sport_name).first()
	if sport is None:
		return make_response(
			json.dumps('Invalid sport name: {}'.format(sport_name)),
			404
			)

	q = session.query(Gear)
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
		category=sport.title
		)


@app.route('/catalog/<string:sport>', methods=['POST'])
def add_gear(sport):
	item = request.json
	print 'adding item {}'.format(gear, item)
	response = make_response(json.dumps('Added {}'.format(item)), 200)
	return response

@app.route('/catalog/<string:sport>/<string:gear>/edit', methods=['PUT'])
def edit_gear(sport, gear):
	print 'editing item {} with values {}'.format(gear, request.json)
	response = make_response(json.dumps('Item {} edited'.format(gear)), 200)
	return response

@app.route('/catalog/<string:sport>/<string:gear>/edit', methods=['DELETE'])
def delete_gear(sport, gear):
	response = make_response(json.dumps('Deleted gear {}'.format(gear)), 204)
	return response


@app.route('/api/<string:version>')
@app.route('/api/<string:version>/catalog')
def api_show_catalog(version):
	response = make_response(jsonify([
		{
			'name': "Soccer",
			'items': ['a', 'b', 'c']
		},
		{
			'name': "Basketball",
			'items': ['a', 'e', 'f', 'g']
		}
	]), 200)
	return response


@app.route('/api/<string:version>/catalog/<string:sport>')
def api_show_gears(version, sport):
	response = make_response(jsonify([
		'gloves',
		'balls',
		'socks'
	]), 200)
	return response

@app.route('/api/<string:version>/catalog/<string:sport>/<string:gear>')
def api_show_gear(version, sport, gear):
	response = make_response(jsonify({
		'title': 'gloves',
		'description': 'wear it and catch balls',
		'category': 'Soccer'
	}), 200)
	return response

@app.route('/register', methods=['POST'])
def register():
    body = request.json
    creds = map(body.get, ['email', 'name', 'password'])
    print creds
    if not all(creds):
        return make_response(
            json.dumps('Please provide valid email, name, AND password'),
            400,
            )
    email, name, password = creds
    user = User(email=email, name=name)
    user.hash_password(password)
    session.add(user)
    session.commit()

    return jsonify(user.serialize), 201


if __name__ == '__main__':
	app.secret_key = '03uklsjadf09'
	app.debug = True
	app.run(host='0.0.0.0', port=5001)
