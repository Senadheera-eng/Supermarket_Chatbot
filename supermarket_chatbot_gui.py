import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import nltk
import spacy
import json
import re
from datetime import datetime
from collections import defaultdict
import sys
import os


# Download required NLTK data
def download_nltk_data():
    """Download required NLTK data if not present"""
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('taggers/averaged_perceptron_tagger')
        nltk.data.find('corpora/stopwords')
    except LookupError:
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            nltk.download('stopwords', quiet=True)
        except:
            pass


# Import NLTK components after download
try:
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from nltk.tag import pos_tag
except ImportError:
    pass


class SupermarketChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_chatbot_engine()
        self.setup_ui()
        self.setup_bindings()

    def setup_window(self):
        """Configure the main window"""
        self.root.title("🛒 Supermarket Assistant Chatbot")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)

        # Modern color scheme
        self.colors = {
            'primary': '#2563eb',  # Blue
            'secondary': '#10b981',  # Green
            'accent': '#f59e0b',  # Orange
            'background': '#f8fafc',  # Light gray
            'surface': '#ffffff',  # White
            'text': '#1f2937',  # Dark gray
            'text_light': '#6b7280',  # Medium gray
            'success': '#10b981',  # Green
            'error': '#ef4444',  # Red
            'warning': '#f59e0b'  # Orange
        }

        # Configure styles
        self.setup_styles()

        # Set window background
        self.root.configure(bg=self.colors['background'])

    def setup_styles(self):
        """Setup ttk styles for modern appearance"""
        style = ttk.Style()

        # Configure button styles
        style.configure('Primary.TButton',
                        font=('Segoe UI', 10, 'bold'),
                        padding=(15, 8))

        style.configure('Secondary.TButton',
                        font=('Segoe UI', 9),
                        padding=(10, 6))

        # Configure frame styles
        style.configure('Card.TFrame',
                        background=self.colors['surface'],
                        relief='flat',
                        borderwidth=1)

        style.configure('Header.TLabel',
                        font=('Segoe UI', 16, 'bold'),
                        background=self.colors['surface'],
                        foreground=self.colors['primary'])

        style.configure('Subheader.TLabel',
                        font=('Segoe UI', 11, 'bold'),
                        background=self.colors['surface'],
                        foreground=self.colors['text'])

        style.configure('Body.TLabel',
                        font=('Segoe UI', 9),
                        background=self.colors['surface'],
                        foreground=self.colors['text_light'])

    def setup_chatbot_engine(self):
        """Initialize the chatbot engine"""
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

        # Initialize NLP components
        download_nltk_data()
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            self.stop_words = set()

        # Try to load spaCy model
        try:
            self.nlp = spacy.load('en_core_web_sm')
            self.use_spacy = True
        except OSError:
            self.use_spacy = False

    def setup_ui(self):
        """Create the user interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header section
        self.create_header(main_frame)

        # Main content area
        content_frame = tk.Frame(main_frame, bg=self.colors['background'])
        content_frame.pack(fill='both', expand=True, pady=(20, 0))

        # Left panel - Input and controls
        self.create_input_panel(content_frame)

        # Right panel - Results and shopping list
        self.create_results_panel(content_frame)

        # Status bar
        self.create_status_bar(main_frame)

    def create_header(self, parent):
        """Create the header section"""
        header_frame = tk.Frame(parent, bg=self.colors['surface'], relief='flat', bd=1)
        header_frame.pack(fill='x', pady=(0, 10))

        # Add shadow effect
        shadow_frame = tk.Frame(parent, bg='#e5e7eb', height=2)
        shadow_frame.pack(fill='x')

        # Header content
        header_content = tk.Frame(header_frame, bg=self.colors['surface'])
        header_content.pack(fill='x', padx=30, pady=20)

        # Title and subtitle
        title_label = tk.Label(header_content,
                               text="🛒 Supermarket Assistant Chatbot",
                               font=('Segoe UI', 24, 'bold'),
                               bg=self.colors['surface'],
                               fg=self.colors['primary'])
        title_label.pack(anchor='w')

        subtitle_label = tk.Label(header_content,
                                  text="Find shelf locations for your shopping items using Natural Language Processing",
                                  font=('Segoe UI', 12),
                                  bg=self.colors['surface'],
                                  fg=self.colors['text_light'])
        subtitle_label.pack(anchor='w', pady=(5, 0))

    def create_input_panel(self, parent):
        """Create the input panel"""
        input_frame = tk.Frame(parent, bg=self.colors['background'])
        input_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))

        # Input card
        input_card = tk.Frame(input_frame, bg=self.colors['surface'], relief='flat', bd=1)
        input_card.pack(fill='both', expand=True)

        # Add shadow
        shadow = tk.Frame(input_frame, bg='#e5e7eb', height=2)
        shadow.place(in_=input_card, x=2, y=2, relwidth=1, relheight=1)
        input_card.lift()

        # Input card header
        input_header = tk.Frame(input_card, bg=self.colors['surface'])
        input_header.pack(fill='x', padx=20, pady=(20, 10))

        tk.Label(input_header,
                 text="📝 What would you like to buy?",
                 font=('Segoe UI', 14, 'bold'),
                 bg=self.colors['surface'],
                 fg=self.colors['text']).pack(anchor='w')

        tk.Label(input_header,
                 text="Enter your shopping items in natural language",
                 font=('Segoe UI', 10),
                 bg=self.colors['surface'],
                 fg=self.colors['text_light']).pack(anchor='w', pady=(2, 0))

        # Input area
        input_area = tk.Frame(input_card, bg=self.colors['surface'])
        input_area.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Text input
        self.input_text = scrolledtext.ScrolledText(input_area,
                                                    height=4,
                                                    font=('Segoe UI', 11),
                                                    wrap='word',
                                                    relief='solid',
                                                    borderwidth=1,
                                                    padx=10,
                                                    pady=10)
        self.input_text.pack(fill='x', pady=(0, 15))

        # Placeholder text
        self.input_placeholder = "Type your shopping list here... (e.g., 'I want to buy apples, milk, and bread')"
        self.input_text.insert('1.0', self.input_placeholder)
        self.input_text.configure(fg=self.colors['text_light'])

        # Button frame
        button_frame = tk.Frame(input_area, bg=self.colors['surface'])
        button_frame.pack(fill='x')

        # Process button
        self.process_btn = tk.Button(button_frame,
                                     text="🔍 Find Items",
                                     font=('Segoe UI', 11, 'bold'),
                                     bg=self.colors['primary'],
                                     fg='white',
                                     relief='flat',
                                     padx=20,
                                     pady=10,
                                     cursor='hand2',
                                     command=self.process_shopping_list)
        self.process_btn.pack(side='left')

        # Clear button
        clear_btn = tk.Button(button_frame,
                              text="🗑️ Clear",
                              font=('Segoe UI', 10),
                              bg='#f3f4f6',
                              fg=self.colors['text'],
                              relief='flat',
                              padx=15,
                              pady=8,
                              cursor='hand2',
                              command=self.clear_input)
        clear_btn.pack(side='left', padx=(10, 0))

        # Example buttons
        examples_frame = tk.Frame(input_area, bg=self.colors['surface'])
        examples_frame.pack(fill='x', pady=(15, 0))

        tk.Label(examples_frame,
                 text="💡 Try these examples:",
                 font=('Segoe UI', 10, 'bold'),
                 bg=self.colors['surface'],
                 fg=self.colors['text']).pack(anchor='w')

        examples = [
            "apples, milk, bread",
            "I need chicken, rice, and ice cream",
            "chocolate, cookies, cheese, pizza"
        ]

        for example in examples:
            btn = tk.Button(examples_frame,
                            text=f"✨ {example}",
                            font=('Segoe UI', 9),
                            bg='#f8fafc',
                            fg=self.colors['primary'],
                            relief='flat',
                            cursor='hand2',
                            padx=10,
                            pady=5,
                            command=lambda e=example: self.set_example(e))
            btn.pack(anchor='w', pady=2)

    def create_results_panel(self, parent):
        """Create the results panel"""
        results_frame = tk.Frame(parent, bg=self.colors['background'])
        results_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))

        # Results card
        results_card = tk.Frame(results_frame, bg=self.colors['surface'], relief='flat', bd=1)
        results_card.pack(fill='both', expand=True)

        # Add shadow
        shadow = tk.Frame(results_frame, bg='#e5e7eb', height=2)
        shadow.place(in_=results_card, x=2, y=2, relwidth=1, relheight=1)
        results_card.lift()

        # Results header
        results_header = tk.Frame(results_card, bg=self.colors['surface'])
        results_header.pack(fill='x', padx=20, pady=(20, 10))

        self.results_title = tk.Label(results_header,
                                      text="📋 Shopping List",
                                      font=('Segoe UI', 14, 'bold'),
                                      bg=self.colors['surface'],
                                      fg=self.colors['text'])
        self.results_title.pack(anchor='w')

        self.results_subtitle = tk.Label(results_header,
                                         text="Your items will appear here",
                                         font=('Segoe UI', 10),
                                         bg=self.colors['surface'],
                                         fg=self.colors['text_light'])
        self.results_subtitle.pack(anchor='w', pady=(2, 0))

        # Results display area
        results_display = tk.Frame(results_card, bg=self.colors['surface'])
        results_display.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Results text area
        self.results_text = scrolledtext.ScrolledText(results_display,
                                                      font=('Courier New', 10),
                                                      wrap='word',
                                                      relief='solid',
                                                      borderwidth=1,
                                                      padx=15,
                                                      pady=15,
                                                      state='disabled')
        self.results_text.pack(fill='both', expand=True)

        # Action buttons frame
        action_frame = tk.Frame(results_display, bg=self.colors['surface'])
        action_frame.pack(fill='x', pady=(15, 0))

        # Save button
        self.save_btn = tk.Button(action_frame,
                                  text="💾 Save List",
                                  font=('Segoe UI', 10, 'bold'),
                                  bg=self.colors['secondary'],
                                  fg='white',
                                  relief='flat',
                                  padx=15,
                                  pady=8,
                                  cursor='hand2',
                                  command=self.save_shopping_list,
                                  state='disabled')
        self.save_btn.pack(side='left')

        # Print button
        self.print_btn = tk.Button(action_frame,
                                   text="🖨️ Print List",
                                   font=('Segoe UI', 10),
                                   bg='#6b7280',
                                   fg='white',
                                   relief='flat',
                                   padx=15,
                                   pady=8,
                                   cursor='hand2',
                                   command=self.print_shopping_list,
                                   state='disabled')
        self.print_btn.pack(side='left', padx=(10, 0))

    def create_status_bar(self, parent):
        """Create the status bar"""
        self.status_frame = tk.Frame(parent, bg=self.colors['surface'], relief='flat', bd=1)
        self.status_frame.pack(fill='x', pady=(10, 0))

        self.status_label = tk.Label(self.status_frame,
                                     text="Ready to help you find your shopping items! 🛒",
                                     font=('Segoe UI', 9),
                                     bg=self.colors['surface'],
                                     fg=self.colors['text_light'],
                                     anchor='w')
        self.status_label.pack(side='left', padx=20, pady=8)

        # NLP status
        nlp_status = "NLP: NLTK"
        if self.use_spacy:
            nlp_status += " + spaCy"

        self.nlp_status_label = tk.Label(self.status_frame,
                                         text=nlp_status,
                                         font=('Segoe UI', 9),
                                         bg=self.colors['surface'],
                                         fg=self.colors['success'])
        self.nlp_status_label.pack(side='right', padx=20, pady=8)

    def setup_bindings(self):
        """Setup event bindings"""
        # Input text focus events
        self.input_text.bind('<FocusIn>', self.on_input_focus_in)
        self.input_text.bind('<FocusOut>', self.on_input_focus_out)

        # Enter key binding
        self.input_text.bind('<Control-Return>', lambda e: self.process_shopping_list())

        # Window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_input_focus_in(self, event):
        """Handle input focus in"""
        current_text = self.input_text.get('1.0', 'end-1c')
        if current_text == self.input_placeholder:
            self.input_text.delete('1.0', 'end')
            self.input_text.configure(fg=self.colors['text'])

    def on_input_focus_out(self, event):
        """Handle input focus out"""
        current_text = self.input_text.get('1.0', 'end-1c').strip()
        if not current_text:
            self.input_text.delete('1.0', 'end')  # Clear any whitespace
            self.input_text.insert('1.0', self.input_placeholder)
            self.input_text.configure(fg=self.colors['text_light'])

    def set_example(self, example):
        """Set example text in input"""
        # Clear the text widget completely
        self.input_text.delete('1.0', 'end')
        # Insert only the example text
        self.input_text.insert('1.0', example)
        # Set the text color to normal (not placeholder color)
        self.input_text.configure(fg=self.colors['text'])
        # Give focus to the text widget
        self.input_text.focus_set()

    def clear_input(self):
        """Clear input text"""
        self.input_text.delete('1.0', 'end')
        self.input_text.insert('1.0', self.input_placeholder)
        self.input_text.configure(fg=self.colors['text_light'])
        # Remove focus from the text widget to ensure placeholder behavior works correctly
        self.process_btn.focus_set()

    def update_status(self, message, color='text_light'):
        """Update status bar message"""
        self.status_label.configure(text=message, fg=self.colors[color])
        self.root.update_idletasks()

    def preprocess_text(self, text):
        """Clean and preprocess input text"""
        text = text.lower()
        text = re.sub(r'[^\w\s,]', '', text)
        text = re.sub(r'\s+and\s+', ', ', text)
        text = re.sub(r'\s*,\s*', ', ', text)
        return text

    def extract_items_nltk(self, text):
        """Extract items using NLTK techniques"""
        try:
            tokens = word_tokenize(text)
            pos_tags = pos_tag(tokens)

            items = []
            i = 0
            while i < len(pos_tags):
                word, pos = pos_tags[i]
                
                # Look for nouns that could be products
                if pos in ['NN', 'NNS', 'NNP', 'NNPS'] and len(word) > 2:
                    # Check for compound nouns (like "ice cream")
                    compound_noun = word
                    j = i + 1
                    while (j < len(pos_tags) and 
                        pos_tags[j][1] in ['NN', 'NNS', 'NNP', 'NNPS'] and 
                        j - i < 3):  # Limit compound to 3 words max
                        compound_noun += " " + pos_tags[j][0]
                        j += 1
                    
                    items.append(compound_noun.lower())
                    i = j - 1
                i += 1
                
            return items
        except:
            # Fallback to simple splitting
            return [item.strip() for item in text.split(',') if item.strip()]

    def extract_items_spacy(self, text):
        """Extract items using spaCy NER and POS tagging"""
        doc = self.nlp(text)
        items = []

        for ent in doc.ents:
            if ent.label_ in ['PRODUCT', 'ORG']:
                items.append(ent.text.lower())

        for token in doc:
            if (token.pos_ == 'NOUN' and
                    not token.is_stop and
                    len(token.text) > 2 and
                    token.text.lower() not in [item.lower() for item in items]):
                items.append(token.text.lower())

        return items

    def extract_items(self, text):
        """Main item extraction function"""
        clean_text = self.preprocess_text(text)
        
        # Words to filter out (common phrases that aren't products)
        filter_words = {
            'want', 'buy', 'need', 'get', 'purchase', 'looking', 'for', 'some', 
            'would', 'like', 'to', 'i', 'we', 'me', 'us', 'can', 'could', 
            'should', 'will', 'shall', 'do', 'does', 'did', 'have', 'has', 
            'had', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'the', 'a', 'an', 'and', 'or', 'but', 'so', 'if', 'then',
            'this', 'that', 'these', 'those', 'my', 'your', 'our', 'their'
        }

        if self.use_spacy:
            items = self.extract_items_spacy(clean_text)
        else:
            items = self.extract_items_nltk(clean_text)

        # Also try simple splitting on commas and "and"
        simple_split = [item.strip() for item in re.split(r'[,\s]+and\s+|\s*,\s*', clean_text) if item.strip()]

        # Combine items from both methods
        all_items = items + simple_split
        
        # Enhanced filtering
        filtered_items = []
        for item in all_items:
            # Clean the item by removing common prefixes
            item_cleaned = re.sub(r'^(i\s+want\s+|i\s+need\s+|we\s+want\s+|we\s+need\s+)', '', item.lower()).strip()
            
            # Skip if it's just a filter word
            words_in_item = item_cleaned.split()
            if len(words_in_item) == 1 and item_cleaned in filter_words:
                continue
                
            # Skip if more than half the words are filter words
            filter_word_count = sum(1 for word in words_in_item if word in filter_words)
            if len(words_in_item) > 1 and filter_word_count >= len(words_in_item) / 2:
                continue
                
            # Skip very short items or items that are just numbers
            if len(item_cleaned) < 3 or item_cleaned.isdigit():
                continue
            
            # Add the cleaned item if it's not empty and not already added
            if (item_cleaned and 
                item_cleaned not in [i.lower() for i in filtered_items]):
                filtered_items.append(item_cleaned)

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
                # Try partial matches
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
            return "No items found in our database.", {}

        # Group items by shelf
        shelf_groups = defaultdict(list)
        for item, shelf in results.items():
            shelf_groups[shelf].append(item)

        # Generate formatted list
        lines = []
        lines.append("=" * 60)
        lines.append("🛒 SUPERMARKET SHOPPING LIST")
        lines.append("=" * 60)
        lines.append(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        # Sort by shelf number
        for shelf in sorted(shelf_groups.keys()):
            lines.append(f"📍 SHELF {shelf}:")
            for item in shelf_groups[shelf]:
                lines.append(f"   • {item.capitalize()}")
            lines.append("")

        lines.append("=" * 60)
        lines.append("✨ Happy Shopping! ✨")
        lines.append("=" * 60)

        return "\n".join(lines), shelf_groups

    def process_shopping_list(self):
        """Process the shopping list input"""
        # Get input text
        user_input = self.input_text.get('1.0', 'end-1c').strip()

        if user_input == self.input_placeholder or not user_input:
            messagebox.showwarning("Input Required", "Please enter some items you'd like to buy!")
            return

        # Update UI state
        self.process_btn.configure(state='disabled', text="🔄 Processing...")
        self.update_status("🔍 Analyzing your shopping list...", 'primary')

        def process_in_thread():
            try:
                # Extract items
                self.root.after(0, lambda: self.update_status("🔍 Extracting items using NLP...", 'primary'))
                extracted_items = self.extract_items(user_input)

                # Find shelf locations
                self.root.after(0, lambda: self.update_status("📍 Looking up shelf locations...", 'primary'))
                results, not_found = self.find_shelf_locations(extracted_items)

                # Generate shopping list
                shopping_list, shelf_groups = self.generate_shopping_list(results)

                # Update UI on main thread
                self.root.after(0, lambda: self.update_results(shopping_list, results, not_found, shelf_groups))

            except Exception as e:
                self.root.after(0, lambda: self.show_error(f"An error occurred: {str(e)}"))

        # Run processing in separate thread
        thread = threading.Thread(target=process_in_thread)
        thread.daemon = True
        thread.start()

    def update_results(self, shopping_list, results, not_found, shelf_groups):
        """Update the results display"""
        # Enable text widget for updates
        self.results_text.configure(state='normal')
        self.results_text.delete('1.0', 'end')

        # Insert shopping list
        self.results_text.insert('end', shopping_list)

        # Add not found items if any
        if not_found:
            self.results_text.insert('end', "\n\n❌ ITEMS NOT FOUND:\n")
            for item in not_found:
                self.results_text.insert('end', f"   • {item.capitalize()} (not in our database)\n")

        # Disable text widget
        self.results_text.configure(state='disabled')

        # Update titles and status
        found_count = len(results)
        total_count = found_count + len(not_found)

        self.results_title.configure(text=f"📋 Shopping List ({found_count} items found)")
        if shelf_groups:
            shelf_count = len(shelf_groups)
            self.results_subtitle.configure(text=f"Items organized across {shelf_count} shelves")

        # Enable action buttons
        if results:
            self.save_btn.configure(state='normal')
            self.print_btn.configure(state='normal')

        # Update status
        if results:
            self.update_status(f"✅ Found {found_count} items across {len(shelf_groups)} shelves!", 'success')
        else:
            self.update_status("❌ No items found in database. Try different item names.", 'error')

        # Re-enable process button
        self.process_btn.configure(state='normal', text="🔍 Find Items")

        # Store current results for saving
        self.current_shopping_list = shopping_list

    def show_error(self, message):
        """Show error message"""
        messagebox.showerror("Error", message)
        self.process_btn.configure(state='normal', text="🔍 Find Items")
        self.update_status("❌ An error occurred. Please try again.", 'error')

    def save_shopping_list(self):
        """Save shopping list to file"""
        if not hasattr(self, 'current_shopping_list'):
            return

        # Ask for filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        default_filename = f"shopping_list_{timestamp}.txt"

        filename = filedialog.asksaveasfilename(
            title="Save Shopping List",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=default_filename
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.current_shopping_list)

                messagebox.showinfo("Success",
                                    f"Shopping list saved successfully!\n\nFile: {os.path.basename(filename)}")
                self.update_status(f"💾 Saved as {os.path.basename(filename)}", 'success')

            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")

    def print_shopping_list(self):
        """Print shopping list (opens in notepad/default text editor)"""
        if not hasattr(self, 'current_shopping_list'):
            return

        try:
            # Create temporary file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            temp_filename = f"temp_shopping_list_{timestamp}.txt"

            with open(temp_filename, 'w', encoding='utf-8') as f:
                f.write(self.current_shopping_list)

            # Open with default system application
            if sys.platform.startswith('win'):
                os.startfile(temp_filename)
            elif sys.platform.startswith('darwin'):
                os.system(f'open "{temp_filename}"')
            else:
                os.system(f'xdg-open "{temp_filename}"')

            self.update_status("🖨️ Shopping list opened for printing", 'success')

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file for printing:\n{str(e)}")

    def on_closing(self):
        """Handle window closing"""
        # Clean up any temporary files
        try:
            for filename in os.listdir('.'):
                if filename.startswith('temp_shopping_list_'):
                    try:
                        os.remove(filename)
                    except:
                        pass
        except:
            pass

        self.root.destroy()


def main():
    """Main function to run the GUI application"""
    # Create root window
    root = tk.Tk()

    # Set window icon (if available)
    try:
        # You can add an icon file here if you have one
        # root.iconbitmap('icon.ico')
        pass
    except:
        pass

    # Create and run the application
    app = SupermarketChatbotGUI(root)

    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()