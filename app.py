from flask import Flask, render_template, redirect, url_for, request, session, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy user storage (use a database in production)
users = {}

# Folder to save uploaded PPT files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            flash('Login Successful!', 'success')
            return redirect(url_for('home'))
        flash('Invalid Credentials', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users:
            users[username] = password
            flash('Registration Successful!', 'success')
            return redirect(url_for('login'))
        flash('Username already exists', 'danger')
    return render_template('register.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/videos')
def videos():
    return render_template('videos.html')

@app.route('/quizzes')
def quizzes():
    return render_template('quizzes.html')

@app.route('/add_ppt')
def add_ppt():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('add_ppt.html')

@app.route('/upload_ppt', methods=['POST'])
def upload_ppt():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if 'ppt_file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('add_ppt'))
    
    file = request.files['ppt_file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('add_ppt'))
    
    if file and (file.filename.endswith('.ppt') or file.filename.endswith('.pptx')):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        flash('PPT Uploaded Successfully!', 'success')
    else:
        flash('Invalid file type. Please upload a .ppt or .pptx file.', 'danger')

    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    flash('Logged out successfully.', 'success')  # Flash message to indicate successful logout
    return redirect(url_for('login'))  # Redirect to login page

if __name__ == '__main__':
    app.run(debug=True)
