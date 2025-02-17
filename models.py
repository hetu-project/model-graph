from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    points = db.Column(db.Integer, default=0)
    models = db.relationship('Model', backref='owner', lazy=True)

# model file save
class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    file_path = db.Column(db.String(120), nullable=False)
    points_required = db.Column(db.Integer, default=0) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    related_models = db.relationship('ModelRelation', backref='model', lazy=True)

# model relation
class ModelRelation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_model_id = db.Column(db.Integer, db.ForeignKey('model.id'), nullable=False)
    child_model_id = db.Column(db.Integer, db.ForeignKey('model.id'), nullable=False)