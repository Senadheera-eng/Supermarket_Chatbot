# Supermarket Assistant Chatbot

## CO3251 Natural Language Processing - Assignment 2

A web-based intelligent chatbot that helps supermarket customers find shelf locations for their shopping items using Natural Language Processing techniques.

## 🎯 Project Overview

This chatbot application is designed to be placed at supermarket entrances to assist customers in locating products. Customers can input their shopping lists in natural language, and the system will extract item names using NLP techniques and provide corresponding shelf numbers.

## 🚀 Features

- **Natural Language Understanding**: Uses NLP.js to process customer requests
- **Product Recognition**: Extracts product names from natural language input
- **Shelf Location Mapping**: Maps products to predefined shelf locations
- **Interactive Web Interface**: User-friendly chat-based interface
- **Print Functionality**: Generates printable shopping lists with shelf numbers
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Processing**: Instant responses with loading indicators

## 🛠 Technical Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **NLP Library**: NLP.js (Node Natural Language Processing)
- **Database**: JSON-based product-shelf mapping
- **Interface**: Web-based responsive design

## 📦 Installation & Setup

### Prerequisites

- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for NLP.js CDN)
- Optional: Node.js and npm for development server

### Quick Start (Browser-based)

1. **Download the project files**

   ```
   supermarket-chatbot/
   ├── index.html
   ├── script.js
   ├── style.css
   ├── package.json
   └── README.md
   ```

2. **Open in browser**
   - Simply open `index.html` in your web browser
   - The application will load automatically

### Development Setup (Optional)

1. **Install dependencies**

   ```bash
   npm install
   ```

2. **Start development server**

   ```bash
   npm start
   ```

   or use any local server:

   ```bash
   python -m http.server 8000
   # or
   npx live-server
   ```

3. **Access the application**
   - Open http://localhost:8000 in your browser

## 🎮 How to Use

### Basic Usage

1. **Start the Application**

   - Open the chatbot in your web browser
   - You'll see a welcome message from the assistant

2. **Input Your Shopping List**

   - Type your items in natural language
   - Examples:
     - "I need apples, milk, and bread"
     - "Where can I find tomatoes and cheese?"
     - "I want to buy eggs, rice, and shampoo"

3. **View Results**

   - The chatbot will display shelf locations for each item
   - Items are shown in an organized list with shelf numbers

4. **Save Shopping List**
   - Click the "Save Transaction" button
   - A detailed text file will be downloaded automatically

### Sample Interactions

**Input**: "I need apples, milk, and detergent"
**Output**:

```
• Apples → Shelf 1
• Milk → Shelf 2
• Detergent → Shelf 5
```

**Input**: "Where can I find bread and eggs?"
**Output**:

```
• Bread → Shelf 3
• Eggs → Shelf 2
```

## 🗃 Product Database

The system recognizes 40+ products across 10 different shelf categories:

- **Shelf 1**: Fresh Produce (apples, bananas, tomatoes, etc.)
- **Shelf 2**: Dairy Products (milk, cheese, eggs, etc.)
- **Shelf 3**: Bakery (bread, cakes, cookies, etc.)
- **Shelf 4**: Meat & Seafood (chicken, fish, beef, etc.)
- **Shelf 5**: Cleaning Supplies (detergent, soap, shampoo, etc.)
- **Shelf 6**: Pantry Items (rice, pasta, flour, etc.)
- **Shelf 7**: Canned Goods (beans, soup, corn, etc.)
- **Shelf 8**: Beverages (water, juice, coffee, etc.)
- **Shelf 9**: Frozen Foods (ice cream, frozen pizza, etc.)
- **Shelf 10**: Snacks (chips, chocolate, nuts, etc.)

## 🧠 NLP Implementation

### Techniques Used

1. **Tokenization**: Breaking input text into individual words
2. **Entity Recognition**: Identifying product names from input
3. **Intent Classification**: Understanding customer requests
4. **Text Normalization**: Converting to lowercase, removing punctuation
5. **Stop Word Removal**: Filtering out common words like "I", "need", "and"

### NLP Pipeline

```javascript
User Input → Tokenization → Entity Extraction → Database Lookup → Response Generation
```

### Key Functions

- `extractProducts()`: Extracts product names using pattern matching
- `processUserInput()`: Main NLP processing pipeline
- `initializeNLP()`: Initializes and trains the NLP model

## 🎨 User Interface

### Features

- **Clean, Modern Design**: Gradient backgrounds with card-based layout
- **Chat Interface**: Conversational interaction style
- **Responsive Layout**: Adapts to different screen sizes
- **Visual Feedback**: Loading indicators and animations
- **Print Support**: Optimized print stylesheet

### Accessibility

- Keyboard navigation support
- High contrast colors
- Clear typography
- Screen reader friendly

## 📁 File Structure

```
supermarket-chatbot/
├── index.html          # Main HTML file
├── script.js           # JavaScript logic and NLP processing
├── style.css           # Styling and responsive design
├── package.json        # Project configuration
├── README.md           # This documentation
└── user-guide.pdf      # User guide document
```

## 🧪 Testing

### Manual Testing Scenarios

1. **Basic Product Search**

   - Input: "apples and milk"
   - Expected: Shelf locations displayed

2. **Natural Language Variations**

   - "I need..." / "I want to buy..." / "Where can I find..."
   - All should work correctly

3. **Multiple Items**

   - Test with 2-10 items in one request
   - Verify all items are processed

4. **Unknown Items**

   - Input items not in database
   - Should show "not found" message

5. **Print Functionality**
   - Generate and verify printable list

### Browser Compatibility

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## 🚨 Troubleshooting

### Common Issues

1. **NLP Library Not Loading**

   - Check internet connection
   - Verify CDN link in HTML
   - Check browser console for errors

2. **Products Not Recognized**

   - Ensure products exist in database
   - Check spelling and variations
   - Try simpler input format

3. **Print Not Working**
   - Enable pop-ups in browser
   - Check print permissions
   - Try different browser

### Debug Mode

Enable debug mode by opening browser console and running:

```javascript
console.log("Product Database:", productDatabase);
console.log("Current Shopping List:", currentShoppingList);
```

## 📈 Performance Considerations

- **Loading Time**: ~2-3 seconds for NLP initialization
- **Response Time**: <1 second for product lookup
- **Memory Usage**: Minimal client-side storage
- **Scalability**: Can handle 100+ products efficiently

## 📄 License

This project is created for educational purposes as part of CO3251 Natural Language Processing course assignment.

## 👨‍💻 Developer

**Developer**-K.M.L.N.Senadheera (22/ENG/079)
**Assignment**: CO3251 Natural Language Processing - Assignment 2  
**Topic**: Supermarket Assistant Chatbot using NLP  
**Technology**: JavaScript with NLP.js
