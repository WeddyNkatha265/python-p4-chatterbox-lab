from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def messages():
    messages = Message.query.order_by(Message.created_at).all()  # Fetch all messages
    return jsonify([message.to_dict() for message in messages])  # Return messages as JSON

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()  # Get the JSON data from the request
    new_message = Message(body=data['body'], username=data['username'])  # Create a new message
    db.session.add(new_message)  # Add it to the session
    db.session.commit()  # Commit the session to save the message
    return jsonify(new_message.to_dict()), 201  # Return the created message as JSON

@app.route('/messages/<int:id>', methods=['PATCH'])
def messages_by_id(id):
    data = request.get_json()  # Get the JSON data from the request
    message = Message.query.get_or_404(id)  # Fetch the message by ID, return 404 if not found
    message.body = data['body']  # Update the message body
    db.session.commit()  # Commit the changes
    return jsonify(message.to_dict())  # Return the updated message as JSON

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)  # Fetch the message by ID, return 404 if not found
    db.session.delete(message)  # Delete the message
    db.session.commit()  # Commit the changes
    return jsonify({'message': 'Deleted successfully'})  # Return a success message


if __name__ == '__main__':
    app.run(port=5555)
