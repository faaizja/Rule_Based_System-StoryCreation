import random
import re
from collections import defaultdict

# Define an enhanced generative grammar for structured stories
story_grammar = {
    "story": [["intro", "conflict", "climax", "resolution"]],
    "intro": [["Long ago, in", "setting", ",", "character", "was", "action", ".\n"]],
    "conflict": [["One fateful day,", "event", "This turned their world upside down.\n"]],
    "climax": [["As the stakes grew higher,", "character", "was forced to", "challenge", ".\n"]],
    "resolution": [["Against all odds,", "character", "chose to", "decision", "."]],
    "setting": ["an enchanted valley", "a futuristic metropolis", "a hidden underground city", "a floating island", "a war-torn empire", "a cursed temple", "a realm beyond time"],
    "character": ["a fearless warrior", "a brilliant engineer", "a rogue mercenary", "a lost royal heir", "a mystical oracle", "a daring explorer", "a seasoned bounty hunter"],
    "action": ["uncovering ancient relics", "developing groundbreaking technology", "escaping from captors", "seeking vengeance", "defying the laws of magic", "charting unknown territories", "mastering a forgotten art"],
    "event": ["a cataclysmic event shook the land", "a long-lost artifact resurfaced", "a powerful nemesis emerged", "a forbidden ritual was performed", "a celestial being descended", "a cryptic message was deciphered", "a rift between dimensions opened"],
    "challenge": ["face their ultimate rival", "decipher an impossible enigma", "sacrifice their deepest desire", "navigate a treacherous labyrinth", "stand against an unstoppable force", "forge an uneasy alliance", "defend the innocent at great cost"],
    "decision": ["embrace their newfound power", "leave behind everything they knew", "rebuild what was lost", "walk the path of redemption", "pass on their legacy", "safeguard the balance of worlds", "fade into legend"]
}

def generate(idea, grammar):
    """
    Recursively generate a story based on the given grammar.
    """
    if idea in grammar:
        production = random.choice(grammar[idea])
        return " ".join(generate(sym, grammar) for sym in production)
    return idea

# Markov Chain Model for Story Generation
class MarkovChain:
    def __init__(self):
        self.chain = defaultdict(list)
    
    def train(self, text):
        words = re.findall(r'\b\w+[\w\']*|[.,!?;]', text.lower())  # Capture words and punctuation
        for i in range(len(words) - 1):
            self.chain[words[i]].append(words[i + 1])
    
    def generate(self, start_word, length=150):
        if start_word not in self.chain:
            return "No data to generate story."
        
        word = start_word
        story = [word.capitalize()]
        count = 1
        # sentence_length = random.randint(8, 15)

        for _ in range(length - 1):
            if word not in self.chain or not self.chain[word]:
                break  # Prevent infinite loops when no next word exists
            
            word = random.choice(self.chain[word])
            if word in ['.', '!', '?']:
                story.append(word + "\n")  # Properly format sentence breaks
                count = 0
                # sentence_length = random.randint(8, 15)
            else:
                story.append(word)
            count += 1
        
        return ' '.join(story).replace(" .", ".").replace(" !", "!").replace(" ?", "?")  # Clean formatting


# Load a larger training text
training_text = """
Once upon a time in a distant kingdom, a young apprentice set out to prove himself.
He trained under the watchful eyes of the wise masters, learning the ways of combat and strategy.
One fateful night, an old prophecy was revealed, foretelling a hero would rise.
The kingdom fell into darkness as an evil sorcerer seized power, enslaving the people.
Bravely, the apprentice ventured into the forbidden lands, battling foes and solving ancient riddles.
With newfound allies, he confronted the sorcerer in a climactic duel.
In the end, justice prevailed, and peace was restored to the land.
"""

markov = MarkovChain()
markov.train(training_text)

# Generate a story using Markov Chain
start_word = "once"
generated_story = markov.generate(start_word)

# Generate a story using generative grammar
story = generate("story", story_grammar)

print("\nGenerated Story using Grammar:\n")
print(story)
print("\nGenerated Story using Markov Chain:\n")
print(generated_story)
