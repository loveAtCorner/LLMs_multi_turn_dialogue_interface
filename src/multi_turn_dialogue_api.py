from flask import Flask, request, jsonify
from multi_turn_dialogue_manager import BaseMultipleTurnConversationManager

app = Flask(__name__)
conversation_manager = BaseMultipleTurnConversationManager()

@app.route('/start_session', methods=['POST'])
def start_session():
    user_id = request.json.get('user_id')
    session = conversation_manager.session_manager.start_new_session(user_id)
    return jsonify({'session_id': session.session_id})

@app.route('/message', methods=['POST'])
def message():
    user_id = request.json.get('user_id')
    session_id = request.json.get('session_id')
    user_message = request.json.get('user_message')
    system_prompt = request.json.get('system_prompt')
    
    response = conversation_manager.handle_message(user_id, session_id, user_message, system_prompt)
    return jsonify({'response': response})

@app.route('/history', methods=['GET'])
def history():
    user_id = request.args.get('user_id')
    session_id = request.args.get('session_id')
    
    history = conversation_manager.history_manager.get_history(user_id, session_id)
    return jsonify({'history': history})

if __name__ == '__main__':
    app.run(debug=True)
