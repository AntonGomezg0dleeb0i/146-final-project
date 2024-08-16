# Core game logic, input handling, state management
import requests
from relationships import RelationshipManager

class Game:
    def __init__(self):
        self.relationship = RelationshipManager()

    def get_ai_response(self, player_input):
        url = 'http://localhost:5000/generate'
        data = {
            'input': player_input,
            'relationship_state': self.relationship.current_state()
        }
        response = requests.post(url, json=data)
        return response.json()['response']

    def run(self):
        print("Welcome to Hostage Negotiator!")
        while True:
            player_input = input("You: ")
            ai_response = self.get_ai_response(player_input)
            print(f"AI: {ai_response}")
            self.relationship.update(player_input, ai_response)

if __name__ == "__main__":
    game = Game()
    game.run()
