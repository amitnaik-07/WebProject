from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
import json

app = Flask(__name__, template_folder='.')
app.secret_key = 'supersecretkey'  # For session management

USER_FILE = 'user.json'

def load_users():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, 'w') as f:
            json.dump({}, f)
    with open(USER_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f)

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('amit.html', username=session['username'])

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = load_users()
        email = request.form['email']
        password = request.form['password']
        if email in users:
            return 'User already exists!'
        users[email] = password
        save_users(users)
        return redirect(url_for('login'))
    return '''
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Poppins&display=swap" rel="stylesheet">
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(to right, #f4c27a, #d19451);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                color: #333;
            }

            .form-container {
                background-color: #fff8f0;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
                width: 100%;
                max-width: 400px;
                text-align: center;
            }

            h2 {
                font-family: 'Playfair Display', serif;
                font-size: 28px;
                color: #5d4c39;
                margin-bottom: 25px;
            }

            input[type="email"],
            input[type="password"] {
                width: 100%;
                padding: 12px 15px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 8px;
                font-size: 16px;
                transition: border-color 0.3s;
            }

            input[type="email"]:focus,
            input[type="password"]:focus {
                border-color: #d19451;
                outline: none;
            }

            button {
                background-color: #5d4c39;
                color: white;
                padding: 12px 25px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                margin-top: 15px;
                transition: background-color 0.3s ease;
            }

            button:hover {
                background-color: #7b3f00;
            }

            .link {
                margin-top: 15px;
                display: block;
                font-size: 14px;
                color: #337ab7;
                text-decoration: none;
            }

            .link:hover {
                text-decoration: underline;
                color: #23527c;
            }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h2>Register</h2>
            <form method="POST">
                <input type="email" name="email" placeholder="Email" required><br>
                <input type="password" name="password" placeholder="Password" maxlength="15" required><br>
                <button type="submit">Create Account</button>
            </form>
            <a class="link" href="/login">Already have an account? Login</a>
        </div>
    </body>
    </html>
    '''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            session['username'] = username
            return redirect(url_for('home'))
        return 'Invalid credentials!'
    return '''
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Poppins&display=swap" rel="stylesheet">
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(to right, #f4c27a, #d19451);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                color: #333;
            }

            .form-container {
                background-color: #fff8f0;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
                width: 100%;
                max-width: 400px;
                text-align: center;
            }

            h2 {
                font-family: 'Playfair Display', serif;
                font-size: 28px;
                color: #5d4c39;
                margin-bottom: 25px;
            }

            input[type="text"],
            input[type="password"] {
                width: 100%;
                padding: 12px 15px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 8px;
                font-size: 16px;
                transition: border-color 0.3s;
            }

            input[type="text"]:focus,
            input[type="password"]:focus {
                border-color: #d19451;
                outline: none;
            }

            button {
                background-color: #5d4c39;
                color: white;
                padding: 12px 25px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                margin-top: 15px;
                transition: background-color 0.3s ease;
            }

            button:hover {
                background-color: #7b3f00;
            }

            .link {
                margin-top: 15px;
                display: block;
                font-size: 14px;
                color: #337ab7;
                text-decoration: none;
            }

            .link:hover {
                text-decoration: underline;
                color: #23527c;
            }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h2>Login</h2>
            <form method="POST">
                <input type="text" name="username" placeholder="Username" required><br>
                <input type="password" name="password" placeholder="Password" required maxlength="15"><br>
                <button type="submit">Login</button>
            </form>
            <a class="link" href="/register">Don’t have an account? Register</a>
        </div>
    </body>
    </html>
    '''


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# File serving routes
@app.route('/<filename>.js')
def serve_js(filename):
    return send_from_directory('.', f"{filename}.js")

@app.route('/<filename>.css')
def serve_css(filename):
    return send_from_directory('.', f"{filename}.css")

@app.route('/<folder>/<path:filename>')
def serve_subfolder(folder, filename):
    return send_from_directory(os.path.join('.', folder), filename)

@app.route('/<path:filename>')
def page(filename):
    return render_template(filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
