from flask import Flask, Response, request
import requests
import hashlib
import redis

app = Flask(__name__)
cache = redis.StrictRedis(host='redis', port=6379, db=0)
salt = "sdfjdskfjsfkljlkn32i3o749028u389ry289yhdjksfhnskf"
default_name = 'Joe Bloggs'

@app.route('/', methods=['GET','POST'])
def mainpage():
	
	name = default_name
	if request.method == 'POST':
		name = request.form['name']
	
	salted_name = salt + name
	name_hash = hashlib.sha256(salted_name.encode()).hexdigest()
	
	header = '<html><head><title>Indentidock</title></head><body>'
	body =  '''<form method="POST">
		Hello <input type="text" name="name" value="{0}">
		<input type="submit" value="submit">
		</form>
		<p>You look like a:
		<img src="/monster/{1}"/>
		'''.format(name, name_hash)
	footer = '</body></html>'

	return header + body + footer
	
@app.route('/monster/<name>')
def get_identicon(name):
	
	image = cache.get(name)
	if image is None:
		print("cache miss", flush=True)
		r = requests.get('http://dnmonster:8080/monster/' + name + '?size=50')
		image = r.content
		cache.set(name, image)
	else:
		print("cache hit", flush=True)
	
	return Response(image, mimetype='image/png')
	
if __name__=='__main__':
	app.run(debug=True, host='0.0.0.0')