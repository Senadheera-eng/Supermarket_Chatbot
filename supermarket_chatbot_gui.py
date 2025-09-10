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
        
        # Initialize transaction logging first
        self.transactions = []
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        self.setup_window()
        self.setup_chatbot_engine()
        self.setup_ui()
        self.setup_bindings()
        
        # Welcome message
        self.add_message("assistant", "Hello! I'm your Supermarket Assistant 🛒\nI can help you find shelf locations for your shopping items. Just tell me what you'd like to buy!")

    def setup_window(self):
        """Configure the main window"""
        self.root.title("Supermarket Assistant")
        self.root.geometry("450x700")
        self.root.minsize(400, 600)
        
        # Modern color scheme matching the design
        self.colors = {
            'primary': '#4285F4',          # Google Blue
            'primary_dark': '#1976D2',     # Darker Blue
            'background': '#F8F9FA',       # Light Gray Background
            'surface': '#FFFFFF',          # White
            'user_bubble': '#4285F4',      # Blue for user messages
            'assistant_bubble': '#F1F3F4', # Light gray for assistant
            'text_dark': '#202124',        # Dark text
            'text_light': '#5F6368',       # Light text
            'border': '#DADCE0',           # Border color
            'success': '#34A853',          # Green
            'accent': '#EA4335'            # Red for location pins
        }
        
        self.root.configure(bg=self.colors['background'])

    def setup_chatbot_engine(self):
        """Initialize the chatbot engine"""
        # Product database with shelf locations and categories
        self.product_database = {
            # Fruits & Vegetables - Shelf 1
            'apple': (1, 'Fruits & Vegetables'), 'apples': (1, 'Fruits & Vegetables'),
            'banana': (1, 'Fruits & Vegetables'), 'bananas': (1, 'Fruits & Vegetables'),
            'orange': (1, 'Fruits & Vegetables'), 'oranges': (1, 'Fruits & Vegetables'),
            'tomato': (1, 'Fruits & Vegetables'), 'tomatoes': (1, 'Fruits & Vegetables'),
            'onion': (1, 'Fruits & Vegetables'), 'onions': (1, 'Fruits & Vegetables'),
            'carrot': (1, 'Fruits & Vegetables'), 'carrots': (1, 'Fruits & Vegetables'),
            'potato': (1, 'Fruits & Vegetables'), 'potatoes': (1, 'Fruits & Vegetables'),
            'lettuce': (1, 'Fruits & Vegetables'), 'spinach': (1, 'Fruits & Vegetables'),

            # Dairy Products - Shelf 2
            'milk': (2, 'Dairy Products'), 'cheese': (2, 'Dairy Products'),
            'butter': (2, 'Dairy Products'), 'yogurt': (2, 'Dairy Products'),
            'yoghurt': (2, 'Dairy Products'), 'cream': (2, 'Dairy Products'),
            'eggs': (2, 'Dairy Products'), 'egg': (2, 'Dairy Products'),

            # Beverages - Shelf 3
            'water': (3, 'Beverages'), 'juice': (3, 'Beverages'),
            'soda': (3, 'Beverages'), 'coffee': (3, 'Beverages'),
            'tea': (3, 'Beverages'), 'beer': (3, 'Beverages'),
            'wine': (3, 'Beverages'), 'cola': (3, 'Beverages'),

            # Meat & Seafood - Shelf 4
            'chicken': (4, 'Meat & Seafood'), 'beef': (4, 'Meat & Seafood'),
            'pork': (4, 'Meat & Seafood'), 'fish': (4, 'Meat & Seafood'),
            'salmon': (4, 'Meat & Seafood'), 'tuna': (4, 'Meat & Seafood'),
            'shrimp': (4, 'Meat & Seafood'), 'meat': (4, 'Meat & Seafood'),

            # Cleaning Products - Shelf 5
            'detergent': (5, 'Cleaning Products'), 'soap': (5, 'Cleaning Products'),
            'shampoo': (5, 'Cleaning Products'), 'toothpaste': (5, 'Cleaning Products'),
            'tissue': (5, 'Cleaning Products'), 'tissues': (5, 'Cleaning Products'),

            # Bread & Bakery - Shelf 6
            'bread': (6, 'Bread & Bakery'), 'cake': (6, 'Bread & Bakery'),
            'cookies': (6, 'Bread & Bakery'), 'cookie': (6, 'Bread & Bakery'),
            'muffin': (6, 'Bread & Bakery'), 'muffins': (6, 'Bread & Bakery'),
            'bagel': (6, 'Bread & Bakery'), 'bagels': (6, 'Bread & Bakery'),

            # Snacks & Candy - Shelf 7
            'chips': (7, 'Snacks & Candy'), 'chocolate': (7, 'Snacks & Candy'),
            'candy': (7, 'Snacks & Candy'), 'nuts': (7, 'Snacks & Candy'),

            # Pasta & Rice - Shelf 8
            'pasta': (8, 'Pasta & Rice'), 'rice': (8, 'Pasta & Rice'),
            'noodles': (8, 'Pasta & Rice'), 'spaghetti': (8, 'Pasta & Rice'),

            # Frozen Foods - Shelf 9
            'ice': (9, 'Frozen Foods'), 'icecream': (9, 'Frozen Foods'),
            'pizza': (9, 'Frozen Foods'), 'fries': (9, 'Frozen Foods'),

            # Spices & Condiments - Shelf 10
            'salt': (10, 'Spices & Condiments'), 'pepper': (10, 'Spices & Condiments'),
            'sugar': (10, 'Spices & Condiments'), 'oil': (10, 'Spices & Condiments'),
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
        # Header
        self.create_header()
        
        # Main chat area
        self.create_chat_area()
        
        # Input area
        self.create_input_area()

    def create_header(self):
        """Create the header section"""
        header_frame = tk.Frame(self.root, bg=self.colors['surface'], height=80)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Add subtle shadow
        shadow_frame = tk.Frame(self.root, bg=self.colors['border'], height=1)
        shadow_frame.pack(fill='x')
        
        # Header content
        header_content = tk.Frame(header_frame, bg=self.colors['surface'])
        header_content.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Shopping cart icon and title
        title_frame = tk.Frame(header_content, bg=self.colors['surface'])
        title_frame.pack(anchor='w')
        
        # Icon circle
        icon_frame = tk.Frame(title_frame, bg=self.colors['primary'], width=50, height=50)
        icon_frame.pack(side='left', pady=5)
        icon_frame.pack_propagate(False)
        
        icon_label = tk.Label(icon_frame, text="🛒", font=('Segoe UI', 20),
                             bg=self.colors['primary'], fg='white')
        icon_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title and subtitle
        text_frame = tk.Frame(title_frame, bg=self.colors['surface'])
        text_frame.pack(side='left', padx=(15, 0), fill='y')
        
        title_label = tk.Label(text_frame, text="Supermarket Assistant",
                              font=('Segoe UI', 18, 'bold'),
                              bg=self.colors['surface'],
                              fg=self.colors['text_dark'])
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(text_frame, text="Find shelf locations for your items",
                                 font=('Segoe UI', 11),
                                 bg=self.colors['surface'],
                                 fg=self.colors['text_light'])
        subtitle_label.pack(anchor='w')

    def create_chat_area(self):
        """Create the main chat area"""
        # Chat container
        chat_container = tk.Frame(self.root, bg=self.colors['background'])
        chat_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Scrollable chat area
        self.chat_canvas = tk.Canvas(chat_container, bg=self.colors['background'], 
                                   highlightthickness=0, bd=0)
        self.chat_scrollbar = ttk.Scrollbar(chat_container, orient="vertical", 
                                          command=self.chat_canvas.yview)
        self.chat_frame = tk.Frame(self.chat_canvas, bg=self.colors['background'])
        
        self.chat_canvas.configure(yscrollcommand=self.chat_scrollbar.set)
        self.chat_canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")
        
        # Pack scrollbar and canvas
        self.chat_scrollbar.pack(side="right", fill="y")
        self.chat_canvas.pack(side="left", fill="both", expand=True)
        
        # Bind canvas events
        self.chat_frame.bind('<Configure>', self._on_frame_configure)
        self.chat_canvas.bind('<Configure>', self._on_canvas_configure)

    def create_input_area(self):
        """Create the input area"""
        # Input container with rounded border effect
        input_container = tk.Frame(self.root, bg=self.colors['background'])
        input_container.pack(fill='x', padx=15, pady=(0, 15))
        
        # Input frame with border
        input_frame = tk.Frame(input_container, bg=self.colors['border'], relief='solid', bd=1)
        input_frame.pack(fill='x')
        
        # Inner frame
        inner_frame = tk.Frame(input_frame, bg=self.colors['surface'])
        inner_frame.pack(fill='x', padx=1, pady=1)
        
        # Message input and send button in same row
        message_frame = tk.Frame(inner_frame, bg=self.colors['surface'])
        message_frame.pack(fill='x', padx=15, pady=12)
        
        # Message input
        self.message_entry = tk.Text(message_frame, height=1, font=('Segoe UI', 12),
                                   wrap='word', relief='flat', bd=0,
                                   bg=self.colors['surface'],
                                   fg=self.colors['text_dark'])
        self.message_entry.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Placeholder
        self.placeholder_text = "Ask me about shelf locations... (e.g., 'I need milk and bread')"
        self.message_entry.insert('1.0', self.placeholder_text)
        self.message_entry.configure(fg=self.colors['text_light'])
        
        # Send button (arrow icon)
        self.send_btn = tk.Button(message_frame, text="➤", font=('Segoe UI', 16),
                                bg=self.colors['text_light'], fg=self.colors['surface'],
                                relief='flat', width=3, height=1, cursor='hand2',
                                command=self.send_message)
        self.send_btn.pack(side='right')

    def setup_bindings(self):
        """Setup event bindings"""
        # Input focus events
        self.message_entry.bind('<FocusIn>', self.on_input_focus_in)
        self.message_entry.bind('<FocusOut>', self.on_input_focus_out)
        
        # Enter key binding
        self.message_entry.bind('<Return>', self.on_enter_key)
        
        # Mouse wheel scrolling
        self.chat_canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.chat_frame.bind("<MouseWheel>", self._on_mousewheel)

    def _on_frame_configure(self, event=None):
        """Reset the scroll region to encompass the inner frame"""
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        self._scroll_to_bottom()

    def _on_canvas_configure(self, event):
        """Reset the canvas window to encompass inner frame when required"""
        canvas_width = event.width
        self.chat_canvas.itemconfig(self.chat_canvas.find_all()[0], width=canvas_width)

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        try:
            if event.delta:
                delta = -1 * (event.delta / 120)
            else:
                delta = -1 if event.num == 4 else 1
            self.chat_canvas.yview_scroll(int(delta), "units")
        except:
            pass

    def _scroll_to_bottom(self):
        """Scroll to the bottom of the chat"""
        self.root.after(100, lambda: self.chat_canvas.yview_moveto(1.0))

    def on_input_focus_in(self, event):
        """Handle input focus in"""
        if self.message_entry.get('1.0', 'end-1c') == self.placeholder_text:
            self.message_entry.delete('1.0', 'end')
            self.message_entry.configure(fg=self.colors['text_dark'])

    def on_input_focus_out(self, event):
        """Handle input focus out"""
        current_text = self.message_entry.get('1.0', 'end-1c').strip()
        if not current_text:
            self.message_entry.delete('1.0', 'end')
            self.message_entry.insert('1.0', self.placeholder_text)
            self.message_entry.configure(fg=self.colors['text_light'])

    def on_enter_key(self, event):
        """Handle Enter key press"""
        current_text = self.message_entry.get('1.0', 'end-1c').strip()
        if current_text and current_text != self.placeholder_text:
            self.send_message()
        return 'break'

    def add_message(self, sender, message, timestamp=None):
        """Add a message to the chat area"""
        if timestamp is None:
            timestamp = datetime.now().strftime('%I:%M %p')
        
        # Message container
        msg_container = tk.Frame(self.chat_frame, bg=self.colors['background'])
        msg_container.pack(fill='x', pady=8)
        
        if sender == "user":
            # User message (right aligned, blue bubble)
            user_frame = tk.Frame(msg_container, bg=self.colors['background'])
            user_frame.pack(anchor='e', fill='x')
            
            # User message bubble
            msg_bubble = tk.Frame(user_frame, bg=self.colors['user_bubble'],
                                relief='flat', bd=0)
            msg_bubble.pack(anchor='e', padx=(60, 0), pady=2)
            
            # Add rounded corner effect with padding
            msg_label = tk.Label(msg_bubble, text=message, font=('Segoe UI', 11),
                               bg=self.colors['user_bubble'], fg='white',
                               wraplength=250, justify='left', padx=16, pady=12)
            msg_label.pack()
            
            # Timestamp
            time_label = tk.Label(user_frame, text=timestamp, font=('Segoe UI', 9),
                                bg=self.colors['background'], fg=self.colors['text_light'])
            time_label.pack(anchor='e', padx=(0, 10), pady=(2, 0))
            
        else:
            # Assistant message (left aligned with icon)
            assistant_frame = tk.Frame(msg_container, bg=self.colors['background'])
            assistant_frame.pack(anchor='w', fill='x')
            
            # Icon and message container
            content_frame = tk.Frame(assistant_frame, bg=self.colors['background'])
            content_frame.pack(anchor='w', fill='x')
            
            # Assistant icon
            icon_frame = tk.Frame(content_frame, bg=self.colors['success'], width=32, height=32)
            icon_frame.pack(side='left', padx=(0, 12), pady=2)
            icon_frame.pack_propagate(False)
            
            icon_label = tk.Label(icon_frame, text="🛒", font=('Segoe UI', 16),
                                bg=self.colors['success'], fg='white')
            icon_label.place(relx=0.5, rely=0.5, anchor='center')
            
            # Message content
            msg_content_frame = tk.Frame(content_frame, bg=self.colors['background'])
            msg_content_frame.pack(side='left', fill='both', expand=True)
            
            # Message bubble
            msg_bubble = tk.Frame(msg_content_frame, bg=self.colors['assistant_bubble'],
                                relief='flat', bd=0)
            msg_bubble.pack(anchor='w', fill='x', padx=(0, 60), pady=2)
            
            msg_label = tk.Label(msg_bubble, text=message, font=('Segoe UI', 11),
                               bg=self.colors['assistant_bubble'], fg=self.colors['text_dark'],
                               wraplength=280, justify='left', padx=16, pady=12)
            msg_label.pack(anchor='w')
            
            # Timestamp
            time_label = tk.Label(msg_content_frame, text=timestamp, font=('Segoe UI', 9),
                                bg=self.colors['background'], fg=self.colors['text_light'])
            time_label.pack(anchor='w', padx=(0, 0), pady=(2, 0))
        
        # Update scroll region and scroll to bottom
        self.chat_frame.update_idletasks()
        self._on_frame_configure()

    def send_message(self):
        """Send a message"""
        message = self.message_entry.get('1.0', 'end-1c').strip()
        
        if message == self.placeholder_text or not message:
            return
        
        # Add user message
        self.add_message("user", message)
        
        # Clear input
        self.message_entry.delete('1.0', 'end')
        self.message_entry.configure(fg=self.colors['text_dark'])
        
        # Disable send button
        self.send_btn.configure(state='disabled', bg=self.colors['border'])
        
        # Log transaction
        transaction = {
            'timestamp': datetime.now().isoformat(),
            'user_input': message,
            'session_id': self.session_id
        }
        
        # Process in separate thread
        def process_request():
            try:
                response, results = self.process_shopping_request(message)
                transaction['response'] = response
                transaction['items_found'] = results
                self.transactions.append(transaction)
                
                self.root.after(0, lambda: self.handle_response(response))
                
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                transaction['response'] = error_msg
                transaction['error'] = True
                self.transactions.append(transaction)
                
                self.root.after(0, lambda: self.handle_response(error_msg))
        
        thread = threading.Thread(target=process_request)
        thread.daemon = True
        thread.start()

    def handle_response(self, response):
        """Handle the assistant's response"""
        self.add_message("assistant", response)
        
        # Re-enable send button and show placeholder
        self.send_btn.configure(state='normal', bg=self.colors['text_light'])
        if not self.message_entry.get('1.0', 'end-1c').strip():
            self.message_entry.insert('1.0', self.placeholder_text)
            self.message_entry.configure(fg=self.colors['text_light'])

    def process_shopping_request(self, user_input):
        """Process the shopping request using NLP"""
        user_lower = user_input.lower().strip()
        
        # Handle greetings
        greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']
        if user_lower in greetings:
            return "Hello! I'm here to help you find items in the supermarket. What would you like to buy today?", {}
        
        # Handle thanks
        thanks = ['thanks', 'thank you', 'thanks!', 'thank you!']
        if any(thank in user_lower for thank in thanks):
            return "You're welcome! Is there anything else you'd like to find? 😊", {}
        
        # Extract items
        extracted_items = self.extract_items(user_input)
        
        if not extracted_items:
            return "I didn't detect any shopping items in your message. Could you tell me what products you're looking for?\n\nFor example: 'apples', 'milk', 'bread', etc.", {}
        
        # Find shelf locations
        results, not_found = self.find_shelf_locations(extracted_items)
        
        if results:
            response = "Great! I found these items for you:\n\n"
            
            # Group by shelf and category
            shelf_groups = defaultdict(list)
            shelf_categories = {}
            
            for item, (shelf, category) in results.items():
                shelf_groups[shelf].append(item.capitalize())
                shelf_categories[shelf] = category
            
            # Format response with location pins and categories
            for shelf in sorted(shelf_groups.keys()):
                items_list = ", ".join(shelf_groups[shelf])
                category = shelf_categories[shelf]
                response += f"📍 **Shelf {shelf}** ({category}):\n• {items_list}\n\n"
            
            if not_found:
                response += f"❌ Sorry, I couldn't find: {', '.join(not_found)}\n\n"
            
            response += "Is there anything else you'd like to find?"
        else:
            response = f"I couldn't find any of these items in our database: {', '.join(extracted_items)}\n\nCould you try different item names? For example: 'apples', 'milk', 'bread', etc."
        
        return response, results

    def extract_items(self, text):
        """Main item extraction function"""
        clean_text = self.preprocess_text(text)
        
        # Check for greetings
        greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'thanks', 'thank you']
        if clean_text.strip() in greetings:
            return []
        
        # Remove helper phrases
        helper_phrases = ['i need', 'i want', 'i would like', 'can you find', 'where is', 'where are', 'looking for', 'buy']
        for phrase in helper_phrases:
            clean_text = re.sub(r'\b' + phrase + r'\b', '', clean_text)
        
        if self.use_spacy:
            items = self.extract_items_spacy(clean_text)
        else:
            items = self.extract_items_nltk(clean_text)
        
        simple_split = [item.strip() for item in re.split(r'[,\s]+and\s+|\s*,\s*', clean_text) if item.strip()]
        all_items = list(set(items + simple_split))
        
        # Enhanced filtering
        filtered_items = [item for item in all_items if item not in [
            'want', 'buy', 'need', 'get', 'purchase', 'find', 'looking', 'for', 'can', 'you', 
            'where', 'is', 'are', 'the', 'some', 'any', 'would', 'like', 'to', 'do', 'have',
            'hi', 'hello', 'hey', 'thanks', 'thank', 'please', 'yes', 'no', 'ok', 'okay'
        ] and len(item) > 1]
        
        return filtered_items

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
            for word, pos in pos_tags:
                if (pos in ['NN', 'NNS', 'NNP', 'NNPS'] and
                        word.lower() not in self.stop_words and
                        len(word) > 2):
                    items.append(word.lower())
            return items
        except:
            return [item.strip() for item in text.split(',') if item.strip()]

    def extract_items_spacy(self, text):
        """Extract items using spaCy NER and POS tagging"""
        doc = self.nlp(text)
        items = []
        for ent in doc.ents:
            if ent.label_ in ['PRODUCT', 'ORG']:
                items.append(ent.text.lower())
        for token in doc:
            if (token.pos_ == 'NOUN' and not token.is_stop and len(token.text) > 2 and
                    token.text.lower() not in [item.lower() for item in items]):
                items.append(token.text.lower())
        return items

    def find_shelf_locations(self, items):
        """Find shelf locations for extracted items"""
        results = {}
        not_found = []
        for item in items:
            item_lower = item.lower().strip()
            if item_lower in self.product_database:
                results[item] = self.product_database[item_lower]
            else:
                found = False
                for product_key in self.product_database.keys():
                    if item_lower in product_key or product_key in item_lower:
                        results[item] = self.product_database[product_key]
                        found = True
                        break
                if not found:
                    not_found.append(item)
        return results, not_found

    def save_transaction_log(self):
        """Save transaction log to file"""
        if not self.transactions:
            messagebox.showinfo("No Data", "No transactions to save yet!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Chat Log",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("JSON files", "*.json")],
            initialfile=f"supermarket_chat_log_{self.session_id}.txt"
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(self.transactions, f, indent=2, ensure_ascii=False)
                else:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write("="*60 + "\n")
                        f.write("SUPERMARKET ASSISTANT CHAT LOG\n")
                        f.write("="*60 + "\n")
                        f.write(f"Session ID: {self.session_id}\n")
                        f.write(f"Total Transactions: {len(self.transactions)}\n")
                        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write("="*60 + "\n\n")
                        
                        for i, transaction in enumerate(self.transactions, 1):
                            f.write(f"TRANSACTION {i}\n")
                            f.write("-" * 20 + "\n")
                            f.write(f"Time: {transaction['timestamp']}\n")
                            f.write(f"User: {transaction['user_input']}\n")
                            f.write(f"Assistant: {transaction['response']}\n")
                            if 'items_found' in transaction:
                                f.write(f"Items Found: {transaction['items_found']}\n")
                            f.write("\n")
                
                messagebox.showinfo("Success", f"Chat log saved!\n\nFile: {os.path.basename(filename)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")


def main():
    """Main function to run the enhanced GUI application"""
    root = tk.Tk()
    
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