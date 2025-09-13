/**
 * Supermarket Assistant Chatbot - Complete Fixed Version
 * Natural Language Processing Assignment - CO3251
 */

// Product-Location Database
const productDatabase = {
    // Fresh Produce - Shelf 1
    'apple': 1, 'apples': 1, 'banana': 1, 'bananas': 1, 'orange': 1, 'oranges': 1,
    'tomato': 1, 'tomatoes': 1, 'potato': 1, 'potatoes': 1, 'onion': 1, 'onions': 1,
    'carrot': 1, 'carrots': 1, 'lettuce': 1, 'spinach': 1,
    
    // Dairy Products - Shelf 2
    'milk': 2, 'cheese': 2, 'butter': 2, 'yogurt': 2, 'yoghurt': 2, 'cream': 2,
    'egg': 2, 'eggs': 2,
    
    // Bakery - Shelf 3
    'bread': 3, 'cake': 3, 'cookies': 3, 'biscuits': 3, 'muffin': 3, 'muffins': 3,
    'bagel': 3, 'bagels': 3, 'croissant': 3, 'croissants': 3,
    
    // Meat & Seafood - Shelf 4
    'chicken': 4, 'beef': 4, 'pork': 4, 'fish': 4, 'salmon': 4, 'tuna': 4,
    'shrimp': 4, 'prawns': 4, 'turkey': 4, 'ham': 4,
    
    // Cleaning Supplies - Shelf 5
    'detergent': 5, 'soap': 5, 'shampoo': 5, 'toothpaste': 5, 'tissue': 5, 'tissues': 5,
    'toilet paper': 5, 'paper towels': 5, 'bleach': 5, 'dishwasher': 5,
    
    // Pantry Items - Shelf 6
    'rice': 6, 'pasta': 6, 'flour': 6, 'sugar': 6, 'salt': 6, 'pepper': 6,
    'oil': 6, 'olive oil': 6, 'vinegar': 6, 'honey': 6,
    
    // Canned Goods - Shelf 7
    'beans': 7, 'soup': 7, 'tomato sauce': 7, 'corn': 7, 'tuna can': 7,
    'peas': 7, 'mushrooms': 7, 'pickles': 7,
    
    // Beverages - Shelf 8
    'water': 8, 'juice': 8, 'soda': 8, 'cola': 8, 'beer': 8, 'wine': 8,
    'coffee': 8, 'tea': 8, 'energy drink': 8,
    
    // Frozen Foods - Shelf 9
    'ice cream': 9, 'frozen pizza': 9, 'frozen vegetables': 9, 'frozen fruit': 9,
    'frozen chicken': 9, 'frozen fish': 9, 'frozen dinner': 9,
    
    // Snacks - Shelf 10
    'chips': 10, 'chocolate': 10, 'candy': 10, 'nuts': 10, 'crackers': 10,
    'popcorn': 10, 'pretzels': 10, 'granola bars': 10
};

let currentShoppingList = [];

// GREETING DETECTION SYSTEM
const GREETING_RESPONSES = {
    'hello': 'Hello there! Welcome to our smart supermarket assistant! How can I help you find items today?',
    'hi': 'Hi! Great to see you! What items are you looking for in our store?',
    'hey': 'Hey! Welcome! Tell me what products you need and I\'ll help you find them!',
    'greetings': 'Greetings! I\'m your friendly supermarket assistant. What can I help you locate today?',
    'good morning': 'Good morning! Ready to help you with your shopping. What items do you need?',
    'good afternoon': 'Good afternoon! How can I assist with your shopping list today?',
    'good evening': 'Good evening! Let me help you find everything you need!',
    'howdy': 'Howdy! What brings you to our store today? What items can I help you find?',
    'what\'s up': 'Not much, just here to help you find products! What are you shopping for?',
    'whats up': 'Not much, just here to help you find products! What are you shopping for?'
};

const THANKS_RESPONSES = {
    'thank you': 'You\'re very welcome! Happy to help with anything else you need!',
    'thanks': 'You\'re welcome! Let me know if you need help finding more items!',
    'thx': 'No problem! Anything else I can help you locate?',
    'thank u': 'You\'re so welcome! What else can I help you find?',
    'ty': 'You\'re welcome! Need help with anything else?',
    'cheers': 'Cheers to you too! Happy shopping!'
};

const HELP_RESPONSES = {
    'help': 'I\'d love to help! Just tell me what items you\'re looking for. For example: "I need apples and milk" or "Where can I find bread?" I know over 40 products!',
    'help me': 'Of course! I can help you find products in our supermarket. Just tell me what you\'re shopping for!',
    'i need help': 'I\'m here to help! Tell me what items you want to find and I\'ll show you exactly which shelf they\'re on!',
    'can you help': 'Absolutely! I can help you locate any products in our store. What are you looking for?',
    'assistance': 'Happy to provide assistance! What items do you need help finding today?'
};

/**
 * Check for conversational intents (greetings, thanks, help)
 */
function checkForGreeting(input) {
    const cleanInput = input.toLowerCase().trim();
    
    if (GREETING_RESPONSES[cleanInput]) {
        return {
            type: 'greeting',
            response: GREETING_RESPONSES[cleanInput]
        };
    }
    
    if (THANKS_RESPONSES[cleanInput]) {
        return {
            type: 'thanks',
            response: THANKS_RESPONSES[cleanInput]
        };
    }
    
    if (HELP_RESPONSES[cleanInput]) {
        return {
            type: 'help',
            response: HELP_RESPONSES[cleanInput]
        };
    }
    
    return null;
}

/**
 * Calculate Levenshtein distance for fuzzy matching
 */
function levenshteinDistance(str1, str2) {
    const matrix = [];
    
    for (let i = 0; i <= str2.length; i++) {
        matrix[i] = [i];
    }
    
    for (let j = 0; j <= str1.length; j++) {
        matrix[0][j] = j;
    }
    
    for (let i = 1; i <= str2.length; i++) {
        for (let j = 1; j <= str1.length; j++) {
            if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
                matrix[i][j] = matrix[i - 1][j - 1];
            } else {
                matrix[i][j] = Math.min(
                    matrix[i - 1][j - 1] + 1,
                    matrix[i][j - 1] + 1,
                    matrix[i - 1][j] + 1
                );
            }
        }
    }
    
    return matrix[str2.length][str1.length];
}

/**
 * Find fuzzy match for misspelled words
 */
function findFuzzyMatch(word, productList) {
    if (word.length < 3) return null;
    
    let bestMatch = null;
    let bestDistance = Infinity;
    const maxDistance = Math.floor(word.length / 3);
    
    for (const product of productList) {
        const distance = levenshteinDistance(word, product);
        if (distance <= maxDistance && distance < bestDistance) {
            bestDistance = distance;
            bestMatch = product;
        }
    }
    
    return bestMatch;
}

/**
 * Extract product names from user input with fuzzy matching
 */
function extractProducts(text) {
    const extractedProducts = [];
    const lowercaseText = text.toLowerCase();
    
    const commonWords = ['i', 'need', 'want', 'to', 'buy', 'and', 'the', 'some', 'a', 'an', 
                        'can', 'you', 'help', 'me', 'find', 'where', 'is', 'are', 'do', 'have'];
    
    const words = lowercaseText.split(/[,\s]+/).filter(word => 
        word.length > 0 && !commonWords.includes(word)
    );
    
    // Check for compound products first
    const compoundProducts = ['toilet paper', 'paper towels', 'olive oil', 'tomato sauce', 
                             'energy drink', 'ice cream', 'frozen pizza', 'frozen vegetables', 
                             'frozen fruit', 'frozen chicken', 'frozen fish', 'frozen dinner', 
                             'granola bars', 'tuna can'];
    
    compoundProducts.forEach(compound => {
        if (lowercaseText.includes(compound)) {
            extractedProducts.push(compound);
        }
    });
    
    // Check individual words
    words.forEach(word => {
        const cleanWord = word.replace(/[^\w\s]/g, '');
        
        if (cleanWord.length < 2) return;
        if (extractedProducts.some(product => product.includes(cleanWord))) return;
        
        // Exact match first
        if (productDatabase.hasOwnProperty(cleanWord)) {
            extractedProducts.push(cleanWord);
            return;
        }
        
        // Fuzzy matching for misspellings
        const fuzzyMatch = findFuzzyMatch(cleanWord, Object.keys(productDatabase));
        if (fuzzyMatch) {
            extractedProducts.push(fuzzyMatch);
            console.log(`Fuzzy match: "${cleanWord}" → "${fuzzyMatch}"`);
        } else {
            // Add as unknown product
            extractedProducts.push(cleanWord);
        }
    });
    
    return extractedProducts;
}

/**
 * Main processing function
 */
async function processUserInput(userInput) {
    showLoading(true);
    
    try {
        console.log('Processing input:', userInput);
        
        // Check for conversational intents first
        const greetingCheck = checkForGreeting(userInput);
        
        if (greetingCheck) {
            console.log('Greeting detected:', greetingCheck.type);
            addMessageToChat(userInput, 'user');
            addMessageToChat(greetingCheck.response, 'bot');
            showLoading(false);
            return;
        }
        
        // Look for products
        const extractedProducts = extractProducts(userInput);
        console.log('Extracted products:', extractedProducts);
        
        if (extractedProducts.length === 0) {
            addMessageToChat(userInput, 'user');
            addMessageToChat("I couldn't identify any specific products in your message. Could you try listing items like 'apples, milk, bread'?\n\nOr try saying 'hello' to start!", 'bot');
            showLoading(false);
            return;
        }
        
        // Find shelf locations
        const shelfResults = [];
        extractedProducts.forEach(product => {
            const shelfNumber = productDatabase[product];
            shelfResults.push({
                product: product,
                shelf: shelfNumber || null,
                found: shelfNumber !== undefined
            });
        });
        
        currentShoppingList = shelfResults;
        displayResults(shelfResults, userInput);
        
    } catch (error) {
        console.error('Error processing input:', error);
        addMessageToChat('Sorry, I encountered an error. Please try again.', 'bot');
    } finally {
        showLoading(false);
    }
}

/**
 * Display results in chat and results section
 */
function displayResults(results, originalInput) {
    addMessageToChat(originalInput, 'user');
    
    const foundItems = results.filter(r => r.found);
    const notFoundItems = results.filter(r => !r.found);
    
    let responseMessage = `I found ${foundItems.length} item(s) in our store:\n\n`;
    
    foundItems.forEach(item => {
        responseMessage += `• ${capitalizeFirst(item.product)} → Shelf ${item.shelf}\n`;
    });
    
    if (notFoundItems.length > 0) {
        responseMessage += `\nSorry, I couldn't locate these items:\n`;
        notFoundItems.forEach(item => {
            responseMessage += `• ${capitalizeFirst(item.product)} (not found)\n`;
        });
    }
    
    addMessageToChat(responseMessage, 'bot');
    displayShelfList(results);
}

/**
 * Display shelf list in results container
 */
function displayShelfList(results) {
    const resultsContainer = document.getElementById('resultsContainer');
    const shelfList = document.getElementById('shelfList');
    
    // Update statistics if elements exist
    const totalItems = document.getElementById('totalItems');
    const foundItems = document.getElementById('foundItems');
    const notFoundItems = document.getElementById('notFoundItems');
    
    if (totalItems && foundItems && notFoundItems) {
        const foundCount = results.filter(r => r.found).length;
        const notFoundCount = results.filter(r => !r.found).length;
        
        totalItems.textContent = `📦 ${results.length} Items`;
        foundItems.textContent = `✅ ${foundCount} Found`;
        notFoundItems.textContent = `❌ ${notFoundCount} Missing`;
    }
    
    shelfList.innerHTML = '';
    
    results.forEach(result => {
        const shelfItem = document.createElement('div');
        shelfItem.className = `shelf-item ${!result.found ? 'item-not-found' : ''}`;
        
        shelfItem.innerHTML = `
            <span class="item-name">${capitalizeFirst(result.product)}</span>
            <span class="shelf-number">${result.found ? `Shelf ${result.shelf}` : 'Not Found'}</span>
        `;
        
        shelfList.appendChild(shelfItem);
    });
    
    resultsContainer.style.display = 'block';
    resultsContainer.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Add message to chat interface
 */
function addMessageToChat(message, sender) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    // Check if we have the new avatar system
    const hasAvatars = document.querySelector('.message-avatar');
    
    if (hasAvatars) {
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = sender === 'bot' ? '🤖' : '👤';
        messageDiv.appendChild(avatar);
    }
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    if (sender === 'bot') {
        messageContent.innerHTML = `<strong>Smart Assistant:</strong> ${message.replace(/\n/g, '<br>')}`;
    } else {
        messageContent.innerHTML = `<strong>You:</strong> ${message}`;
    }
    
    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Send message function
 */
async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();
    
    if (message === '') return;
    
    userInput.value = '';
    await processUserInput(message);
}

/**
 * Handle Enter key press
 */
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

/**
 * Show/hide loading indicator
 */
function showLoading(show) {
    const loading = document.getElementById('loadingIndicator');
    if (loading) {
        loading.style.display = show ? 'block' : 'none';
    }
}

/**
 * Save transaction to file
 */
function saveTransactionToFile() {
    if (currentShoppingList.length === 0) {
        alert('No shopping list to save. Please search for items first.');
        return;
    }
    
    const timestamp = new Date().toLocaleString();
    const transactionId = 'TXN-' + Date.now();
    
    let transactionContent = `SUPERMARKET SHOPPING TRANSACTION\n`;
    transactionContent += `=====================================\n`;
    transactionContent += `Transaction ID: ${transactionId}\n`;
    transactionContent += `Date & Time: ${timestamp}\n`;
    transactionContent += `=====================================\n\n`;
    
    transactionContent += `SHOPPING LIST:\n`;
    currentShoppingList.forEach((item, index) => {
        transactionContent += `${index + 1}. ${capitalizeFirst(item.product)} - ${item.found ? `Shelf ${item.shelf}` : 'Not Available'}\n`;
    });
    
    transactionContent += `\n=====================================\n`;
    transactionContent += `Generated by: Supermarket Assistant Chatbot\n`;
    
    const blob = new Blob([transactionContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `shopping-list-${Date.now()}.txt`;
    link.style.display = 'none';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
    
    addMessageToChat('Transaction saved successfully!', 'bot');
}

/**
 * Print shopping list
 */
function printShelfList() {
    if (currentShoppingList.length === 0) {
        alert('No shopping list to print.');
        return;
    }
    
    const printContent = document.getElementById('printContent');
    if (printContent) {
        printContent.innerHTML = '';
        
        const timestamp = new Date().toLocaleString();
        printContent.innerHTML += `<p><strong>Generated:</strong> ${timestamp}</p><hr><br>`;
        
        currentShoppingList.forEach(item => {
            const printItem = document.createElement('div');
            printItem.className = 'print-shelf-item';
            printItem.innerHTML = `
                <span>${capitalizeFirst(item.product)}</span>
                <span>${item.found ? `Shelf ${item.shelf}` : 'Not Found'}</span>
            `;
            printContent.appendChild(printItem);
        });
    }
    
    window.print();
}

/**
 * Clear results
 */
function clearResults() {
    const resultsContainer = document.getElementById('resultsContainer');
    if (resultsContainer) {
        resultsContainer.style.display = 'none';
    }
    currentShoppingList = [];
    addMessageToChat("Results cleared. What else can I help you find?", 'bot');
}

/**
 * Share list function
 */
function shareList() {
    if (currentShoppingList.length === 0) {
        alert('No shopping list to share.');
        return;
    }
    
    const foundItems = currentShoppingList.filter(item => item.found);
    const shareText = `My Shopping List:\n\n${foundItems.map(item => 
        `• ${capitalizeFirst(item.product)} - Shelf ${item.shelf}`
    ).join('\n')}\n\nGenerated by Smart Supermarket Assistant`;
    
    if (navigator.share) {
        navigator.share({
            title: 'My Shopping List',
            text: shareText
        }).catch(err => console.log('Error sharing:', err));
    } else {
        navigator.clipboard.writeText(shareText).then(() => {
            alert('Shopping list copied to clipboard!');
        }).catch(() => {
            alert(shareText);
        });
    }
}

/**
 * Helper functions for UI
 */
function fillExample(text) {
    const userInput = document.getElementById('userInput');
    if (userInput) {
        userInput.value = text;
        userInput.focus();
    }
}

function clearChat() {
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) {
        chatMessages.innerHTML = '';
        setTimeout(() => {
            addMessageToChat('Chat cleared! Ready for a fresh start!', 'bot');
        }, 200);
    }
}

/**
 * Capitalize first letter
 */
function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

/**
 * Test function for debugging
 */
window.testGreeting = function(input) {
    const result = checkForGreeting(input);
    console.log(`Testing "${input}":`, result);
    return result;
};

window.testFuzzy = function(input) {
    const result = findFuzzyMatch(input, Object.keys(productDatabase));
    console.log(`Fuzzy match for "${input}":`, result);
    return result;
};

/**
 * Initialize the application
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('Bulletproof Chatbot Initialized');
    
    const userInput = document.getElementById('userInput');
    if (userInput) {
        userInput.focus();
    }
    
    addMessageToChat('System ready! Try saying "hello" or type your shopping list.', 'bot');
    
    console.log('Test functions available: testGreeting("hello"), testFuzzy("aples")');
});

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { 
        checkForGreeting, 
        extractProducts, 
        processUserInput,
        findFuzzyMatch,
        levenshteinDistance
    };
}