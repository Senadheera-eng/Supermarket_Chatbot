# Supermarket Assistant Chatbot

## Overview
An intelligent chatbot application that helps supermarket customers find shelf locations for their shopping items using Natural Language Processing (NLP) techniques. Available in both CLI and GUI versions!

## Features
- **NLP-powered item extraction**: Uses NLTK and spaCy for tokenization, POS tagging, and named entity recognition
- **Smart product matching**: Handles various item names and finds partial matches
- **Organized shopping lists**: Groups items by shelf number for efficient shopping
- **Printable output**: Generates formatted shopping lists that can be saved to file
- **Dual interface**: Choose between CLI (command-line) or GUI (graphical) interface
- **Modern GUI**: Beautiful, intuitive graphical interface with real-time processing

## Interface Options

### 🖼️ GUI Version (Recommended)
- Modern, user-friendly graphical interface
- Real-time NLP processing with visual feedback
- Organized layout with input panel and results panel
- One-click save and print functionality
- Example buttons for quick testing
- Professional design with modern styling

### 💻 CLI Version
- Simple command-line interface
- Interactive text-based conversation
- Ideal for terminal users and automation

## Requirements
- Python 3.7 or higher
- NLTK library
- spaCy library (optional, for enhanced NLP)
- tkinter (usually included with Python, for GUI)

## Installation

### Step 1: Clone or Download
Download all the project files to a folder on your computer.

### Step 2: Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt

# Optional: Install spaCy English model for better NLP performance
python -m spacy download en_core_web_sm
```

### Step 3: Run the Application

#### Easy Way (Launcher):
```bash
python launcher.py
```
The launcher will let you choose between CLI and GUI versions and handle dependency installation.

#### Direct Launch:
```bash
# For GUI version:
python supermarket_chatbot_gui.py

# For CLI version:
python supermarket_chatbot.py
```

## Usage

1. **Start the chatbot**: Run `python supermarket_chatbot.py`
2. **Enter your shopping list**: Type items you want to buy in natural language
3. **Get shelf locations**: The chatbot will show you where each item is located
4. **Save your list**: Optionally save the formatted shopping list to a file
5. **Exit**: Type 'quit' or 'exit' to end the session

### Example Interactions

**Input:** "I want to buy apples, milk, and detergent"
**Output:**
```
✅ ITEMS FOUND:
   Apples → Shelf 1
   Milk → Shelf 2
   Detergent → Shelf 5

SHELF 1:
  • Apples

SHELF 2:
  • Milk

SHELF 5:
  • Detergent
```

**Input:** "I need bread, eggs, chicken, and orange juice"
**Output:**
```
✅ ITEMS FOUND:
   Bread → Shelf 6
   Eggs → Shelf 2
   Chicken → Shelf 4
   Orange → Shelf 1
   Juice → Shelf 3
```

## Supported Products
The chatbot recognizes over 50 different products across 10 shelf categories:

- **Shelf 1**: Fruits & Vegetables (apples, bananas, tomatoes, etc.)
- **Shelf 2**: Dairy Products (milk, cheese, eggs, etc.)
- **Shelf 3**: Beverages (water, juice, coffee, etc.)
- **Shelf 4**: Meat & Seafood (chicken, beef, fish, etc.)
- **Shelf 5**: Cleaning Products (detergent, soap, shampoo, etc.)
- **Shelf 6**: Bread & Bakery (bread, cake, cookies, etc.)
- **Shelf 7**: Snacks & Candy (chips, chocolate, nuts, etc.)
- **Shelf 8**: Pasta & Rice (pasta, rice, noodles, etc.)
- **Shelf 9**: Frozen Foods (ice cream, pizza, frozen vegetables, etc.)
- **Shelf 10**: Spices & Condiments (salt, pepper, oil, etc.)

## NLP Techniques Used

1. **Tokenization**: Breaking down input text into individual words
2. **POS Tagging**: Identifying parts of speech to find nouns (potential products)
3. **Stop Word Removal**: Filtering out common words that aren't products
4. **Named Entity Recognition**: Using spaCy to identify product entities
5. **Text Preprocessing**: Cleaning and normalizing input text
6. **Pattern Matching**: Finding partial matches for product variations

## File Structure
```
supermarket-chatbot/
│
├── launcher.py                    # Easy launcher (choose CLI/GUI)
├── supermarket_chatbot.py         # CLI version
├── supermarket_chatbot_gui.py     # GUI version  
├── requirements.txt               # Python dependencies
├── README.md                     # This file
├── user_guide.md                 # User documentation
├── test_chatbot.py               # Testing script
└── shopping_list_*.txt           # Generated shopping lists
```

## Troubleshooting

### Common Issues:

1. **NLTK Data Not Found**
   - The application will automatically download required NLTK data
   - If issues persist, run: `python -c "import nltk; nltk.download('all')"`

2. **spaCy Model Not Found**
   - Install with: `python -m spacy download en_core_web_sm`
   - The application works without spaCy, using NLTK only

3. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Use Python 3.7 or higher

## Development Notes
- The product database can be easily extended by adding items to the `product_database` dictionary
- The NLP pipeline can be customized by modifying the extraction methods
- Additional shelf categories can be added as needed

## License
This project is created for educational purposes as part of the CO3251 Natural Language Processing course assignment.