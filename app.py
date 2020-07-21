import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from pymongo import MongoClient

db_pass = os.environ.get('DB_PASS')

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'songbook'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb+srv://Lingvistik:'+str(db_pass)+'@prviklaster-v3qci.mongodb.net/songbook?retryWrites=true&w=majority')


mongo = PyMongo(app)

@app.route('/')
def route():
    return redirect(url_for('get_chords'))

@app.route('/get_chords')
def get_chords():
    return render_template('songbook.html', chords=mongo.db.chords.find())

@app.route('/show_chords/<chord_id>')
def show_chords(chord_id):
    the_chord = mongo.db.chords.find_one({"_id": ObjectId(chord_id)})
    return render_template('showchords.html', chords=the_chord)

@app.route('/add_chords')
def add_chords():
    return render_template('addchords.html', genre=mongo.db.genre.find())

@app.route('/insert_chords', methods=['POST'])
def insert_chords():
    chords = mongo.db.chords
    chords.insert_one(request.form.to_dict())
    return redirect(url_for('get_chords'))

@app.route('/edit_chords/<chord_id>')
def edit_chords(chord_id):
    the_chord = mongo.db.chords.find_one({"_id": ObjectId(chord_id)})
    return render_template('editchords.html', chords=the_chord,)

@app.route('/update_chords/<chord_id>', methods=['POST'])
def update_chords(chord_id):
    chords = mongo.db.chords
    chords.update({'_id': ObjectId(chord_id)},
    {
        'band_name':request.form.get('band_name'),
        'song_name':request.form.get('song_name'),
        'chords_text': request.form.get('chords_text'),
    })
    return redirect(url_for('get_chords'))

@app.route('/delete_chords/<chord_id>')
def delete_chords(chord_id):
    mongo.db.chords.remove({'_id': ObjectId(chord_id)})
    return redirect(url_for('get_chords'))

@app.route('/chords_diagram')
def chords_diagram():
    return render_template('chordsdiagram.html')