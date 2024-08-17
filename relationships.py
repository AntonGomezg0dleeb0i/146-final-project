 # Logic for managing relationship states
 
from transformers import AutoTokenizer, TFAutoModelForTokenClassification
from transformers import pipeline

import random

class RelationshipManager:
    def __init__(self):
        self.states = {
            "trust": 0,
            "fear": 0,
            "hostility": 0,
            "empathy": 0,
        }
        # alliance, authority, threat from professor paper
        self.aat_states = {
            "alliance": 0,
            "authority": 0,
            "threat": 0
        }
        

        # Load a pre-trained model for NER
        self.tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
        self.model = TFAutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
        self.ner_pipeline = pipeline("ner", model=self.model, tokenizer=self.tokenizer)

        # Define AI's interests with core keywords
        self.interests = {
            "movies": {
                "keywords": ["movie", "film", "cinema", "hollywood", "netflix"],  # Core keywords
                "positive": 2,  # Trust increases by 2 for positive talk
                "neutral": 1,   # Trust increases by 1 for neutral talk
                "negative": -1  # Trust decreases by 1 for negative talk, hostility increases by 2
            },
            # Add more interests if needed
        }

    def current_state(self):
        if self.states["hostility"] > 5:
            return "hostile"
        elif self.states["trust"] > 5:
            return "friendly"
        else:
            return "neutral"

    def recognize_entities(self, text):
        ner_results = self.ner_pipeline(text)
        recognized_entities = [result['word'].lower() for result in ner_results if result['entity'].startswith('B-')]
        return recognized_entities

    def update_aat(self, player_input):
        # Alliance: Building rapport and trust
        if any(word in player_input.lower() for word in ["understand", "help", "together", "we"]):
            self.aat_states["alliance"] += 1
        
        # Authority: Asserting control and setting boundaries
        if any(word in player_input.lower() for word in ["must", "should", "law", "police"]):
            self.aat_states["authority"] += 1
        
        # Threat: Highlighting negative consequences
        if any(word in player_input.lower() for word in ["consequences", "danger", "risk", "harm"]):
            self.aat_states["threat"] += 1
        
        # Ensure values stay within 0-10 range
        for key in self.aat_states:
            self.aat_states[key] = max(0, min(self.aat_states[key], 10))

    def update(self, player_input, ai_response):
        # Analyze the sentiment of the player's input using TextBlob
        sentiment_analysis = TextBlob(player_input)
        polarity = sentiment_analysis.sentiment.polarity
        
        # Determine sentiment based on polarity
        if polarity > 0.1:
            sentiment = 'positive'
        elif polarity < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        # Update AAT states
        self.update_aat(player_input)

        # Update emotional states based on AAT
        self.states["trust"] += self.aat_states["alliance"] * 0.1
        self.states["fear"] += self.aat_states["threat"] * 0.1
        self.states["hostility"] += (self.aat_states["authority"] - self.aat_states["alliance"]) * 0.05
        self.states["empathy"] += self.aat_states["alliance"] * 0.1

        # Recognize named entities in the player's input
        recognized_entities = self.recognize_entities(player_input)

        # Ensure all states stay within 0-10 range
        for key in self.states:
            self.states[key] = max(0, min(self.states[key], 10))

        # Check if the input mentions any of the AI's interests or recognized entities
        for interest, details in self.interests.items():
            for keyword in details["keywords"]:
                # Check for direct keyword match or recognized entities
                if keyword in player_input.lower() or any(keyword in entity for entity in recognized_entities):
                    # Adjust relationship states based on the sentiment and interest
                    if sentiment == 'positive':
                        self.states["trust"] += details["positive"]
                    elif sentiment == 'negative':
                        self.states["trust"] += details["negative"]
                        self.states["hostility"] += 2  # Increase hostility for negative talk
                    else:
                        self.states["trust"] += details["neutral"]
                    break  # Stop after finding the first matching interest

        # General sentiment-based relationship update (if no interest was matched)
        if "calm" in player_input.lower():
            self.states["trust"] += 1
        if "threaten" in player_input.lower():
            self.states["hostility"] += 1

        # Optionally, update based on overall sentiment if no specific interest was triggered
        if sentiment == 'positive':
            self.states["trust"] += 1
        elif sentiment == 'negative':
            self.states["hostility"] += 1
        
        return self.get_dominant_state()

    
    def get_dominant_state(self):
        return max(self.states, key=self.states.get)

    def get_response_tone(self):
        dominant_state = self.get_dominant_state()
        if dominant_state == "trust":
            return "The hostage-taker sounds more open to negotiation."
        elif dominant_state == "fear":
            return "The hostage-taker sounds nervous and unpredictable."
        elif dominant_state == "hostility":
            return "The hostage-taker's voice is filled with anger."
        elif dominant_state == "empathy":
            return "The hostage-taker seems to be considering the situation from other perspectives."
        else:
            return "The hostage-taker's tone is neutral."
