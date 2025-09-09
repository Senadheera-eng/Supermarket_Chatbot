#!/usr/bin/env python3
"""
Supermarket Assistant Chatbot Launcher
Choose between CLI and GUI interfaces
"""

import sys
import os
import subprocess


def show_banner():
    """Display application banner"""
    print("=" * 70)
    print("🛒 SUPERMARKET ASSISTANT CHATBOT")
    print("=" * 70)
    print("Natural Language Processing Assignment - CO3251")
    print("Find shelf locations for your shopping items!")
    print("=" * 70)


def check_dependencies():
    """Check if required dependencies are installed"""
    missing_deps = []

    try:
        import nltk
    except ImportError:
        missing_deps.append('nltk')

    try:
        import spacy
    except ImportError:
        missing_deps.append('spacy')

    try:
        import tkinter
    except ImportError:
        missing_deps.append('tkinter')

    return missing_deps


def install_dependencies():
    """Install missing dependencies"""
    print("📦 Installing required dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'nltk', 'spacy'])
        print("✅ Dependencies installed successfully!")

        # Try to download spaCy model
        try:
            subprocess.check_call([sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'])
            print("✅ spaCy English model downloaded!")
        except:
            print("⚠️  spaCy English model download failed (optional)")

        return True
    except Exception as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def run_cli():
    """Run the CLI version"""
    try:
        import supermarket_chatbot
        print("\n🚀 Starting CLI version...")
        print("Press Ctrl+C to exit at any time.\n")
        supermarket_chatbot.main()
    except ImportError:
        print("❌ supermarket_chatbot.py not found in current directory!")
        input("Press Enter to exit...")
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error running CLI: {e}")
        input("Press Enter to exit...")


def run_gui():
    """Run the GUI version"""
    try:
        import supermarket_chatbot_gui
        print("\n🚀 Starting GUI version...")
        supermarket_chatbot_gui.main()
    except ImportError:
        print("❌ supermarket_chatbot_gui.py not found in current directory!")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"❌ Error running GUI: {e}")
        input("Press Enter to exit...")


def main():
    """Main launcher function"""
    show_banner()

    # Check dependencies
    missing_deps = check_dependencies()

    if missing_deps:
        print(f"⚠️  Missing dependencies: {', '.join(missing_deps)}")
        print("These packages are required to run the application.")

        choice = input("\n📦 Would you like to install them now? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            if not install_dependencies():
                input("\nPress Enter to exit...")
                return
        else:
            print("❌ Cannot run without required dependencies.")
            input("Press Enter to exit...")
            return

    # Check if files exist
    has_cli = os.path.exists('supermarket_chatbot.py')
    has_gui = os.path.exists('supermarket_chatbot_gui.py')

    if not has_cli and not has_gui:
        print("❌ Neither CLI nor GUI version found!")
        print("Make sure supermarket_chatbot.py and/or supermarket_chatbot_gui.py")
        print("are in the same directory as this launcher.")
        input("Press Enter to exit...")
        return

    # Show interface selection menu
    while True:
        print("\n🎯 Choose your preferred interface:")
        print("-" * 40)

        options = []
        if has_cli:
            print("1. 💻 CLI Version (Command Line Interface)")
            options.append(('1', run_cli))

        if has_gui:
            print("2. 🖼️  GUI Version (Graphical User Interface)")
            options.append(('2', run_gui))

        print("3. ❓ Help & Information")
        print("4. 🚪 Exit")
        print("-" * 40)

        choice = input("Select option (1-4): ").strip()

        # Handle CLI option
        if choice == '1' and has_cli:
            run_cli()
            break

        # Handle GUI option
        elif choice == '2' and has_gui:
            run_gui()
            break

        # Handle help
        elif choice == '3':
            show_help()

        # Handle exit
        elif choice == '4':
            print("\n👋 Thank you for using Supermarket Assistant Chatbot!")
            break

        # Invalid choice
        else:
            print("❌ Invalid choice. Please try again.")


def show_help():
    """Show help information"""
    print("\n" + "=" * 60)
    print("📚 HELP & INFORMATION")
    print("=" * 60)

    print("\n🎯 About This Application:")
    print("The Supermarket Assistant Chatbot helps you find shelf locations")
    print("for your shopping items using Natural Language Processing (NLP).")

    print("\n🔧 Features:")
    print("• Natural language input processing")
    print("• Smart item recognition using NLP techniques")
    print("• 50+ supported products across 10 shelf categories")
    print("• Organized shopping lists grouped by shelf")
    print("• Save and print functionality")

    print("\n💻 Interface Options:")
    print("• CLI Version: Text-based interface in terminal")
    print("• GUI Version: Modern graphical interface with buttons")

    print("\n📝 Example Inputs:")
    print("• 'I want to buy apples, milk, and bread'")
    print("• 'apples, milk, bread'")
    print("• 'I need chicken, rice, and ice cream'")

    print("\n🛠️  Technical Details:")
    print("• Uses NLTK for tokenization and POS tagging")
    print("• Optional spaCy integration for enhanced NLP")
    print("• Supports partial matching and product variations")

    print("\n📞 Troubleshooting:")
    print("• Make sure Python 3.7+ is installed")
    print("• Install dependencies when prompted")
    print("• Keep all Python files in the same directory")

    input("\nPress Enter to return to main menu...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("Press Enter to exit...")