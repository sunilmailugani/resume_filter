from flask import Flask,request,jsonify
from mongoengine import connect,Document,StringField

app=Flask(__name__)
@app.route('/',methods=['get'])
def home():
    return jsonify({'message':'this is home page'})
app.run(debug=True)