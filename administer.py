# coding : utf-8
# professor : Helin Gong
# author : Lizhan Hong

# from .Workspace.Train import *
from flask import Flask
from flask import request, render_template, session, redirect, url_for
import numpy as np
import os
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = 'VIVE_LA_SPEIT'  # Set a secret key for session management

# Mock user data (Replace with your actual authentication logic)
users = {
    "Apollo": "20040601",
    "Coline": "20010209"
}

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('Home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Process the registration form
        username = request.form['username']
        password = request.form['password']
        
        # Perform your registration logic here, e.g., store the username and password
        # in a database or file
        
        return redirect('/login')
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'user' in session:
        username = session['user']
        return f"Welcome, {username}! This is your dashboard."
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    # Clear the session and redirect to the login page
    session.pop('user', None)
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            # Authentication successful
            return redirect(url_for('plot'))
        else:
            # Authentication failed
            error = "Invalid credentials. Please try again."
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/plot')
def plot():
    # Generate some random data for plotting
    x = np.linspace(0, 2*np.pi, 100)
    y = np.sin(x)

    # Create the plot
    plt.figure(figsize=(8, 6))
    plt.plot(x, y)
    plt.title('Sine Wave')
    plt.xlabel('x')
    plt.ylabel('sin(x)')

    # # Myplot
    # Plot2D3D(1)

    # Save the plot to a temporary file
    plot_path = os.path.join('static', 'plot.png')
    plt.savefig(plot_path)
    plt.close()

    return render_template('plot.html', plot_path=plot_path)


@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><input name="password" type="password"></p>
              <p><button type="submit">Sign In</button></p>
              </form>'''

@app.route('/signin', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    if request.form['username']=='Apollo' and request.form['password']=='password':
        return f'<h3>Hello, Apollo!</h3>'
    return '<h3>Bad username or password.</h3>'

if __name__ == '__main__':
    app.run(debug=True) 
