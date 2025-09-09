import nltk
import spacy
import json
import re
from datetime import datetime
from collections import defaultdict

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag


class SupermarketChatbot:
    def __init__(self):
        """Initialize the chatbot with product database and NLP tools"""
        # Product database with shelf locations
        self.product_database = {
            # Fruits & Vegetables - Shelf 1
            'apple': 1, 'apples': 1, 'banana': 1, 'bananas': 1, 'orange': 1, 'oranges': 1,
            'tomato': 1, 'tomatoes': 1, 'onion': 1, 'onions': 1, 'carrot': 1, 'carrots': 1,
            'potato': 1, 'potatoes': 1, 'lettuce': 1, 'spinach': 1,

            # Dairy Products - Shelf 2
            'milk': 2, 'cheese': 2, 'butter': 2, 'yogurt': 2, 'yoghurt': 2, 'cream': 2,
            'eggs': 2, 'egg': 2,

            # Beverages - Shelf 3
            'water': 3, 'juice': 3, 'soda': 3, 'coffee': 3, 'tea': 3, 'beer': 3,
            'wine': 3, 'cola': 3, 'pepsi': 3, 'sprite': 3,

            # Meat & Seafood - Shelf 4
            'chicken': 4, 'beef': 4, 'pork': 4, 'fish': 4, 'salmon': 4, 'tuna': 4,
            'shrimp': 4, 'meat': 4,

            # Cleaning Products - Shelf 5
            'detergent': 5, 'soap': 5, 'shampoo': 5, 'toothpaste': 5, 'tissue': 5,
            'tissues': 5, 'towel': 5, 'towels': 5, 'bleach': 5,

            # Bread & Bakery - Shelf 6
            'bread': 6, 'cake': 6, 'cookies': 6, 'cookie': 6, 'muffin': 6, 'muffins': 6,
            'bagel': 6, 'bagels': 6,

            # Snacks & Candy - Shelf 7
            'chips': 7, 'chocolate': 7, 'candy': 7, 'nuts': 7, 'crackers': 7,
            'popcorn': 7, 'gum': 7,

            # Pasta & Rice - Shelf 8
            'pasta': 8, 'rice': 8, 'noodles': 8, 'spaghetti': 8, 'macaroni': 8,
            'quinoa': 8, 'beans': 8, 'lentils': 8,

            # Frozen Foods - Shelf 9
            'ice': 9, 'icecream': 9, 'pizza': 9, 'vegetables': 9, 'fries': 9,
            'burger': 9, 'burgers': 9,

            # Spices & Condiments - Shelf 10
            'salt': 10, 'pepper': 10, 'sugar': 10, 'oil': 10, 'vinegar': 10,
            'sauce': 10, 'ketchup': 10, 'mustard': 10, 'mayo': 10, 'mayonnaise': 10
        }

        # Initialize stop words
        self.stop_words = set(stopwords.words('english'))

        # Load spaCy model for advanced NLP (optional)
        try:
            self.nlp = spacy.load('en_core_web_sm')
            self.use_spacy = True
        except OSError:
            print("spaCy model not found. Using NLTK only.")
            self.use_spacy = False

    def preprocess_text(self, text):
        """Clean and preprocess input text"""
        # Convert to lowercase
        text = text.lower()

        # Remove extra whitespace and special characters except commas and 'and'
        text = re.sub(r'[^\w\s,]', '', text)

        # Replace common separators with commas
        text = re.sub(r'\s+and\s+', ', ', text)
        text = re.sub(r'\s*,\s*', ', ', text)

        return text

    def extract_items_nltk(self, text):
        """Extract items using NLTK techniques"""
        # Tokenize the text
        tokens = word_tokenize(text)

        # POS tagging
        pos_tags = pos_tag(tokens)

        # Extract nouns (potential product names)
        items = []
        for word, pos in pos_tags:
            # Focus on nouns and ignore stop words
            if (pos in ['NN', 'NNS', 'NNP', 'NNPS'] and
                    word.lower() not in self.stop_words and
                    len(word) > 2):
                items.append(word.lower())

        return items

    def extract_items_spacy(self, text):
        """Extract items using spaCy NER and POS tagging"""
        doc = self.nlp(text)
        items = []

        # Extract named entities (products)
        for ent in doc.ents:
            if ent.label_ in ['PRODUCT', 'ORG']:
                items.append(ent.text.lower())

        # Also extract nouns
        for token in doc:
            if (token.pos_ == 'NOUN' and
                    not token.is_stop and
                    len(token.text) > 2 and
                    token.text.lower() not in [item.lower() for item in items]):
                items.append(token.text.lower())

        return items

    def extract_items(self, text):
        """Main item extraction function"""
        # Preprocess the text
        clean_text = self.preprocess_text(text)

        # Try spaCy first, fallback to NLTK
        if self.use_spacy:
            items = self.extract_items_spacy(clean_text)
        else:
            items = self.extract_items_nltk(clean_text)

        # Also try simple comma/and splitting as backup
        simple_split = [item.strip() for item in re.split(r'[,\s]+and\s+|\s*,\s*', clean_text) if item.strip()]

        # Combine results and remove duplicates
        all_items = list(set(items + simple_split))

        # Filter out very common words that aren't products
        filtered_items = [item for item in all_items if item not in ['want', 'buy', 'need', 'get', 'purchase']]

        return filtered_items

    def find_shelf_locations(self, items):
        """Find shelf locations for extracted items"""
        results = {}
        not_found = []

        for item in items:
            item_lower = item.lower().strip()
            if item_lower in self.product_database:
                results[item] = self.product_database[item_lower]
            else:
                # Try to find partial matches
                found = False
                for product_key in self.product_database.keys():
                    if item_lower in product_key or product_key in item_lower:
                        results[item] = self.product_database[product_key]
                        found = True
                        break

                if not found:
                    not_found.append(item)

        return results, not_found

    def generate_shopping_list(self, results):
        """Generate formatted shopping list"""
        if not results:
            return "No items found in our database."

        # Group items by shelf
        shelf_groups = defaultdict(list)
        for item, shelf in results.items():
            shelf_groups[shelf].append(item)

        # Generate formatted list
        shopping_list = []
        shopping_list.append("=" * 50)
        shopping_list.append("SUPERMARKET SHOPPING LIST")
        shopping_list.append("=" * 50)
        shopping_list.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        shopping_list.append("")

        # Sort by shelf number
        for shelf in sorted(shelf_groups.keys()):
            shopping_list.append(f"SHELF {shelf}:")
            for item in shelf_groups[shelf]:
                shopping_list.append(f"  • {item.capitalize()}")
            shopping_list.append("")

        shopping_list.append("=" * 50)
        shopping_list.append("Happy Shopping!")
        shopping_list.append("=" * 50)

        return "\n".join(shopping_list)

    def save_shopping_list(self, shopping_list_text, filename=None):
        """Save shopping list to file"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"shopping_list_{timestamp}.txt"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(shopping_list_text)
            return filename
        except Exception as e:
            print(f"Error saving file: {e}")
            return None

    def process_request(self, user_input):
        """Main function to process user request"""
        print("\n" + "=" * 60)
        print("PROCESSING YOUR REQUEST...")
        print("=" * 60)

        # Extract items using NLP
        print("🔍 Extracting items from your request...")
        extracted_items = self.extract_items(user_input)
        print(f"   Found potential items: {extracted_items}")

        # Find shelf locations
        print("\n📍 Looking up shelf locations...")
        results, not_found = self.find_shelf_locations(extracted_items)

        # Display results
        if results:
            print("\n✅ ITEMS FOUND:")
            for item, shelf in results.items():
                print(f"   {item.capitalize()} → Shelf {shelf}")

        if not_found:
            print("\n❌ ITEMS NOT FOUND:")
            for item in not_found:
                print(f"   {item.capitalize()} (not in our database)")

        # Generate shopping list
        shopping_list = self.generate_shopping_list(results)

        return shopping_list, results, not_found


def main():
    """Main function to run the chatbot"""
    print("🛒 WELCOME TO SUPERMARKET ASSISTANT CHATBOT 🛒")
    print("=" * 60)
    print("I can help you find shelf locations for your shopping items!")
    print("Just tell me what you want to buy, and I'll guide you to the right shelves.")
    print("\nExample: 'I want to buy apples, milk, and detergent'")
    print("Type 'quit' or 'exit' to end the conversation.")
    print("=" * 60)

    # Initialize chatbot
    chatbot = SupermarketChatbot()

    while True:
        try:
            # Get user input
            print("\n💬 What items would you like to buy today?")
            user_input = input("You: ").strip()

            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("\n👋 Thank you for using Supermarket Assistant! Happy shopping!")
                break

            if not user_input:
                print("Please enter some items you'd like to buy.")
                continue

            # Process the request
            shopping_list, results, not_found = chatbot.process_request(user_input)

            # Display shopping list
            print("\n" + shopping_list)

            # Ask if user wants to save the list
            if results:
                save_choice = input("\n💾 Would you like to save this shopping list? (y/n): ").strip().lower()
                if save_choice in ['y', 'yes']:
                    filename = chatbot.save_shopping_list(shopping_list)
                    if filename:
                        print(f"✅ Shopping list saved as: {filename}")
                    else:
                        print("❌ Failed to save shopping list.")

            print("\n" + "-" * 60)

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thank you for using Supermarket Assistant!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()