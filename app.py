"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, flash, redirect, jsonify

from models import db, connect_db, Cupcake


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"

connect_db(app)

@app.route('/')
def home_page():
    
    return render_template('index.html')



@app.route('/api/cupcakes')
def list_cupcakes():
    cupcakes= [c.serialize() for c in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>')
def cake_detail(cupcake_id):
    cupcake=Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    cupcake= Cupcake(
                flavor=request.json['flavor'],
                rating=request.json['rating'],
                size=request.json['size'],
                image=request.json['image'] or None)
    
    db.session.add(cupcake)
    db.session.commit()
    response_json=jsonify(cupcake=cupcake.serialize())
    return(response_json,201)

   


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    cupcake=Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor= request.json.get('flavor',cupcake.flavor)
    cupcake.rating= request.json.get('rating',cupcake.rating)
    cupcake.size=request.json.get('size', cupcake.size)
    cupcake.image=request.json.get('image',cupcake.image)

    db.session.add(cupcake)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    cupcake= Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message='deleted')