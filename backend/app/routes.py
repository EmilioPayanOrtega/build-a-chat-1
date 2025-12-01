from flask import Blueprint, request, jsonify
from .services import register_user, authenticate_user

main = Blueprint('main', __name__)

@main.route('/signup', methods=['POST', 'OPTIONS'])
def signup():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    data = request.json
    try:
        user = register_user(data.get('username'), data.get('email'), data.get('password'))
        return jsonify({'success': True, 'msg': 'User registered successfully'}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@main.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    data = request.json
    try:
        user = authenticate_user(data.get('username'), data.get('password'))
        return jsonify({'success': True, 'msg': 'Login successful', 'user_id': user.id}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 401
    except Exception as e:
        return jsonify({'success': False, 'error': 'Internal server error'}), 500
