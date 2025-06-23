from flask import Flask, request, render_template, redirect, session, url_for, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from flask_session import Session
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Initialize Firebase
cred = credentials.Certificate('firebase_config.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# ---------- ROUTES ----------

@app.route('/')
def index():
    return render_template('index.html')  # Landing page

@app.route('/login-page')
def login_page():
    return render_template('login.html')

@app.route('/signup-page')
def signup_page():
    return render_template('signup.html')








@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('userType')

    user_ref = db.collection('users').where('email', '==', email).stream()
    if any(user_ref):
        return jsonify({'status': 'fail', 'message': 'Email already registered'}), 400

    user_id = str(uuid.uuid4())
    db.collection('users').document(user_id).set({
        'id': user_id,
        'firstName': first_name,
        'lastName': last_name,
        'email': email,
        'password': password,  # ⚠️ Don't forget to hash in production
        'userType': user_type
    })

    # Redirect based on user type
    if user_type == 'writer':
        return jsonify({'status': 'success', 'redirect': url_for('writer_dashboard')})
    else:
        return jsonify({'status': 'success', 'redirect': url_for('reader_dashboard')})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    users = db.collection('users').where('email', '==', email).where('password', '==', password).stream()
    user = next(users, None)

    if not user:
        return jsonify({'status': 'fail', 'message': 'Invalid credentials'}), 401

    user_data = user.to_dict()
    session['user'] = {
        'id': user_data['id'],
        'name': user_data['firstName'],
        'email': user_data['email'],
        'userType': user_data['userType']
    }

    if user_data['userType'] == 'reader':
        return jsonify({'status': 'success', 'redirect': url_for('reader_dashboard')})
    else:
        return jsonify({'status': 'success', 'redirect': url_for('writer_dashboard')})

@app.route('/reader')
def reader_dashboard():
    if 'user' not in session or session['user']['userType'] != 'reader':
        return redirect('/')
    return render_template('READER_profile.html', user=session['user'])

@app.route('/writer')
def writer_dashboard():
    if 'user' not in session or session['user']['userType'] != 'writer':
        return redirect('/')
    return render_template('writter_homedashbord.html', user=session['user'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
