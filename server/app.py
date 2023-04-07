from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
import ipdb

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    
    if request.method == 'GET':
        all_messages = Message.query.order_by(Message.created_at).all()
        dict_messages = [m.to_dict() for m in all_messages]
        return make_response(dict_messages,200)
    elif request.method == 'POST':

        new_message = Message(
            body = request.get_json()['body'],
            username = request.get_json()['username']
        )
        db.session.add(new_message)
        db.session.commit()
        return make_response(new_message.to_dict(),201)

@app.route('/messages/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):

    selected_entry = Message.query.filter(Message.id == id).one()

    if request.method == 'GET':

        return make_response(selected_entry.to_dict(), 200)

    if request.method == 'PATCH':
        
        for key in request.get_json():
            setattr(selected_entry, key, request.get_json()[key])

        db.session.add(selected_entry)
        db.session.commit()

        return make_response(selected_entry.to_dict(),200)
    
    if request.method == 'DELETE':
        
        db.session.delete(selected_entry)
        db.session.commit()

        return make_response({'message':'message deleted successfully'},200)

if __name__ == '__main__':
    app.run(port=5555)
