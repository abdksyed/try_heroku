Link to the app: [Classify MobileNetV3](https://classify-mobilenetv3.herokuapp.com/)

# Building ML Apps using Flask and Heroku

## REST APIs
When a client `request` is made via a RESTful API, it transfers a representation of the state of the resource to the requester or `endpoint`. This transformation, or representation, is delivered in one of the several formats via HTTP: JSON, HTML, Python, PHP, or plain text. `JSON` is the most generally popular file format

Each URL is called a `request` while the data sent back to you is called a `response`.

Request are made of four things.
#### Endpoint
The Endpoint - is the url you request for. It follows this structure: root-endpoint/path/?.  
Example: https://api.github.com/users/abdksyed/repos

#### Method
The Method is the type of request you send to the server. You can choose from these five types below:  
`GET`, `POST`, `PUT`, `PATCH`, `DELETE`.

#### Header
Headers are used to provide information to both the client and server. It can be used for many purposes, such as authentification and providing information about the body content

HTTP Headers are property-value pairs that are separated by a colon. Example: "Content-Type: application/json"

#### Data/Body
The Data (or body) contains information you want to be sent to the server. This option is only used with POST, PUT, PATCH or DELETE requests. To send data through cURL, you can use the `-d` or `--data` option:

## FLASK

### Getting Started

Always better to start in a virtual enviroment.
```bash
mkdir <project-name>
cd <project-name>
python3.x -m venv venv

source venv/bin/activate # To activate the virtual env.

pip install Flask
```

Importing flask module in the project is mandatory. An object of Flask class is our WSGI application.
```python
from flask import Flask
app = Flask(__name__)
```

### Diving In

#### route()
`@app.route(url-path)` decorator bounds the URL to the function being decorated.  
Example:
```python
@app.route('/')
def hello_world():
   return 'Hello World’
```
When running the app and going go index page of url '/' will display `Hello World`. We can also return HTML tagged content such as <h1>hello World</h1> which will render it as Heading.

We can also have dynamic URLs, by having variable part which is marked as <variable-name>, which than needs to be passed as keyword argument to the function with which the rule is associated.

Example:
```
@app.route('/hello/<type:name>')
def hello_name(name):
   return 'Hello %s!' % name
```
By default the type is str, we can neglect type if we need str, but can give `int`, `float` and `path` types too.

#### run()
The `app.run(host, port, debug)` method of the Flask class runs the application on the local development server.

#### url_for()
The `url_for` function is very useful for dynamically building a URL for a specific function. The function accepts the name of a function as the first argument, and one or more keyword arguments, each corresponding to the variable part of the URL.

```python
@app.route('/admin')
def hello_admin():
   return 'Hello Admin'

@app.route('/guest/<guest>')
def hello_guest(guest):
   return 'Hello %s as Guest' % guest

@app.route('/user/<name>')
def hello_user(name):
   if name =='admin':
      return redirect(url_for('hello_admin'))
   else:
      return redirect(url_for('hello_guest',guest = name))
```

#### render_template()

We saw that we can pass HTML tags from python itselv, but generating HTML content from Python code is cumbersome, especially when variable data and Python language elements like conditionals or loops need to be put. This would require frequent escaping from HTML.

This is where one can take advantage of Jinja2 template engine, on which Flask is based on. Instead of returning hardcode HTML from the function, a HTML file can be rendered by the `render_template` function.

```python
@app.route('/')
def index():
   return render_template(‘hello.html’)
```

We can also pass data to the HTML file from python using the `render_template`
```python
@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html",result = result)
```

## Heroku
Heroku is a cloud platform as a service supporting several programming languages. We will use `heroku` to deploy our Flask application to predict images into 1000 ImageNet classes using `pretrained MobileNet-V3` model from Google.

For production we want to have a proper web server, so we install gunicorn:
```
pip install gunicorn
```

We can create a python file to call the app and we can use this script to call in `heroku` Procfile
```python
#wsgi.py
from app.main import app
```

```
# Procfile
web: gunicorn wsgi:app
```

Logging in herko
```bash
heroku login -i
heroku create <app-name>
```

Now we can push the code to heroku git.
```bash
git init
heroku git:remote -a your-app-name
git add .
git commit -m "initial commit"
git push heroku
```

Now our app is ready!!!
