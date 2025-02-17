from flask import Flask, request, send_from_directory, render_template, redirect, url_for, flash, session
from models import db, Model, User, ModelRelation
import os
import uuid
from config import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///modelgraph.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = modelkey

db.init_app(app)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'h5', 'pt', 'pb'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/upload', methods=['POST'])
def upload_model():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(request.url)
    
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = f"{uuid.uuid4()}_{file.filename}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        new_model = Model(name=filename, file_path=filename, user_id=session['user_id'])
        db.session.add(new_model)
        db.session.commit()
        
        flash('Model uploaded successfully', 'success')
        return redirect(url_for('dashboard'))
    
    flash('Invalid file format', 'danger')
    return redirect(request.url)

@app.route('/download/<int:model_id>')
def download_model(model_id):
    model = Model.query.get_or_404(model_id)
    user = User.query.get(session['user_id'])
    
    if model.points_required > user.points:
        flash('Insufficient points', 'danger')
        return redirect(url_for('dashboard'))
    
    user.points -= model.points_required
    db.session.commit()

    owner = model.owner
    owner.points += model.points_required * 0.1  
    db.session.commit()

    return send_from_directory(app.config['UPLOAD_FOLDER'], model.file_path)

@app.route('/model_relation', methods=['POST'])
def add_model_relation():
    parent_model_id = request.form['parent_model_id']
    child_model_id = request.form['child_model_id']
    
    parent_model = Model.query.get(parent_model_id)
    child_model = Model.query.get(child_model_id)
    
    if parent_model and child_model:
        relation = ModelRelation(parent_model_id=parent_model.id, child_model_id=child_model.id)
        db.session.add(relation)
        db.session.commit()
        
        flash('Model relation added successfully', 'success')
    else:
        flash('Model not found', 'danger')
    
    return redirect(url_for('dashboard'))