# Main Flask app to handle API requests
from flask import Flask, request, jsonify
from ai import AIModel

app = Flask(__name__)
ai_model = AIModel()

# Store the conversation history
conversation_history = []

@app.route('/generate', methods=['POST'])
def generate_dialogue():
    global conversation_history
    
    data = request.json
    player_input = data['input']
    relationship_state = data['relationship_state']

    # Append the new player input to the conversation history
    conversation_history.append(f"Player: {player_input}")
    
    # Construct the prompt including the full conversation history
    prompt = f"Conversation so far:\n" + "\n".join(conversation_history) + f"\nThe hostage taker is {relationship_state}. The response is:"
    
    # Generate AI response
    response = ai_model.generate_response(prompt)
    
    # Append the AI response to the conversation history
    conversation_history.append(f"AI: {response}")
    
    # Return the AI response
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
