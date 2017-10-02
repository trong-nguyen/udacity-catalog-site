from flask import (Flask, jsonify,
	request, url_for, abort, g,
	make_response
	)

app = Flask(__name__)

@app.route('/')
@app.route('/catalog')
def show_catalog():
	return jsonify([
		{
			'name': "Soccer",
			'items': ['a', 'b', 'c']
		},
		{
			'name': "Basketball",
			'items': ['a', 'e', 'f', 'g']
		}
	])

@app.route('/catalog/<string:sport>/items')
def show_gears(sport):
	return jsonify([
		'gloves',
		'balls',
		'socks'
	])

@app.route('/catalog/<string:sport>/<string:gear>')
def show_gear(sport, gear):
	return jsonify({
		'title': 'gloves',
		'description': 'wear it and catch balls',
		'category': 'Soccer'
	})

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

if __name__ == '__main__':
	app.secret_key = '03uklsjadf09'
	app.debug = True
	app.run(host='0.0.0.0', port=5001)
