from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)

# Example 1
@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

# Example 2
@app.route('/hello/<name>')
def hello_name(name):
    return '<h2>Hello {}<h2>'.format(name)

@app.route('/blog/<int:postID>')
def show_blog(postID):
    return '<h2>Showing Post with ID: {}</h2>'.format(postID+1)

# Example 3
@app.route('/admin')
def hello_admin():
    return '<h1>Hello Admin</h1>'

@app.route('/python/')
def hello_python():
    return '<h1>Hello Python</h1>'

# Example 4
@app.route('/guest/<guest>')
def hello_guest(guest):
    return '<h1>Hello {} as Guest</h1>'.format(guest)

@app.route('/user/<name>')
def hello_user(name):
    if name == 'admin':
        return redirect(url_for('hello_admin')) #call hello_admin function 
    else:
        return redirect(url_for('hello_guest', guest=name)) #call hello_guest function

# Example 5 - login.html posting data.
@app.route('/success/<name>')
def success(name):
    return '<h1>Welcome, {}!</h1>'.format(name)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name=user))

# Example 6 - rendering template
@app.route('/from_html/<user>')
def index2(user):
    return render_template('hello.html', name = user)

# Example 7 - If else in HTML
@app.route('/score/<int:score>')
def show_score(score):
    return render_template('score.html', marks = score)

# Example 8 - Loop in HTML
@app.route('/result/')
def result():
    dict = {'phy':50, 'che':60, 'maths':70}
    return render_template('result.html', result = dict)

@app.route('/try_static/')
def try_static():
    return render_template('try_static.html')

@app.route('/student')
def student():
    return render_template('student.html')

@app.route('/student_result', methods=['POST', 'GET'])
def student_result():
    if request.method == 'POST':
        result = request.form
        return render_template('result.html', result = result )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')