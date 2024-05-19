from helpers import login_person, mongo_connection,display
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from bson import ObjectId
app = Flask(__name__)
CORS(app, origins=["https://davidbakalov21.github.io"]) 

db=mongo_connection.get_mongo_collection()
def default(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, bytes):
        return obj.decode('utf-8')
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)
@app.route('/signUp', methods=['POST'])
def add_user():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        name = data.get('first_name')
        lastname = data.get('last_name')
        result=db['Accounts'].find_one({"email":email})
        if result is None:
            db['Accounts'].insert_one({'name': name,'last_name': lastname, 'email': email, 'password':  password})
            return jsonify({
                'status': 'success'
            })
        else:
            return jsonify({
                'status': 'failure'
            })  
    except  Exception as e:
        return jsonify({
            'status': str(e)
        })
        
@app.route('/createCategory', methods=['POST'])
def create_category():
    try:
        data = request.json
        email = data.get('email')
        name = data.get('name')
        color = data.get('color')
        result = db['Categories'].find_one({"email": email, "name": name, "color": color})
        if result is None:
            db['Categories'].insert_one({'email': email, 'name': name, 'color': color})
            return jsonify({
                'status': 'success'
            })
        else:
            return jsonify({
                'status': 'failure'
            }) 
    except  Exception as e:
        return jsonify({
            'status': str(e)
        })
@app.route('/getCategory', methods=['POST'])
def get_categories():
    data = request.json
    info=display.display_all(db['Categories'],data.get('email'))
    converted_info = json.dumps(info, default=default)
    return converted_info

@app.route('/getNotes', methods=['POST'])
def get_notes():
    data = request.json
    info=display.display_all(db['Notes'],data.get('email'))
    converted_info = json.dumps(info, default=default)
    return converted_info

@app.route('/CreateNote', methods=['POST'])
def create_notes():
    try:
        data = request.json
        email = data.get('email')
        text = data.get('note')
        category = data.get('category')
        date = data.get('date')
        result=db['Notes'].find_one({"email":email,"text":text,"category":category})
        if result is None:
            db['Notes'].insert_one({"email":email,"text":text,"category":category,"date":date, "status":"active"})
            return jsonify({
                'status': 'success'
            })
        else:
            return jsonify({
                'status': 'failure'
            }) 
    except  Exception as e:
        return jsonify({
            'status': str(e)
        })
        
@app.route('/deleteNote', methods=['DELETE'])
def delete_notes():
    try:
        data = request.json
        email = data.get('email')
        text = data.get('note')
        category = data.get('category')
        date = data.get('date')
        status=data.get('status')
        db['Notes'].delete_one({"email":email,"text":text,"category":category,"date":date, "status":status})
        return jsonify({
            'status': 'success'
        })
    except  Exception as e:
        return jsonify({
            'status': str(e)
        })

@app.route('/signIn', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    return  jsonify({'status':login_person.login_user(email, password, db['Accounts'])})

@app.route('/UpdateNote', methods=['PATCH'])
def update_user():
    try:
        data = request.json.get('data')
        email = data.get('emailEdit')
        text = data.get('note')
        category = data.get('category')
        date = data.get('date')
        status=data.get('status')
        
        textE = data.get('noteEdit')
        categoryE = data.get('categoryEdit')
        dateE = data.get('dateEdit')
        statusE=data.get('statusEdit')
        search={"email":email,"text":text,"category":category,"date":date, "status":status}
        updated = {"$set": {'text':textE,'category':categoryE,'date':dateE,'status':statusE}}
        db['Notes'].update_one(search, updated)
        return jsonify({
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'status': str(e)
        })
if __name__ == '__main__':
    app.run(debug=True)