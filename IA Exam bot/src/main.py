"""
Main entry point for DHS IA Exam Bot
"""

import sys
from bot import DHSBot
from config.settings import APP_NAME, APP_VERSION


def print_welcome():
    """Print welcome message"""
    print(f"\n{'='*60}")
    print(f"Welcome to {APP_NAME} v{APP_VERSION}")
    print(f"{'='*60}\n")


def print_menu():
    """Print main menu"""
    print("\nAvailable Commands:")
    print("1. create_application - Create a new application")
    print("2. get_application - View your application")
    print("3. submit_application - Submit your application")
    print("4. get_status - Check application status")
    print("5. start_exam - Begin the IA exam")
    print("6. submit_exam - Submit exam answers")
    print("7. get_exam_results - View exam results")
    print("8. help - Show available commands")
    print("9. exit - Exit the bot")
    print()


def interactive_mode():
    """Run bot in interactive mode"""
    bot = DHSBot()
    print_welcome()
    
    try:
        while True:
            print_menu()
            choice = input("Enter command (1-9): ").strip()
            
            if choice == "1":
                # Create application
                user_id = input("Enter user ID: ").strip()
                name = input("Enter your name: ").strip()
                email = input("Enter your email: ").strip()
                result = bot.process_user_request("create_application", user_id, name=name, email=email)
                print(f"\nResult: {result['message']}")
            
            elif choice == "2":
                # Get application
                user_id = input("Enter user ID: ").strip()
                result = bot.process_user_request("get_application", user_id)
                if result['success']:
                    print(f"\nApplication Details:")
                    for key, value in result['data'].items():
                        print(f"  {key}: {value}")
                else:
                    print(f"\nError: {result['message']}")
            
            elif choice == "3":
                # Submit application
                user_id = input("Enter user ID: ").strip()
                result = bot.process_user_request("submit_application", user_id)
                print(f"\nResult: {result['message']}")
            
            elif choice == "4":
                # Get status
                user_id = input("Enter user ID: ").strip()
                result = bot.process_user_request("get_status", user_id)
                if result['success']:
                    print(f"\nApplication Status: {result['status']}")
                else:
                    print(f"\nError: {result['message']}")
            
            elif choice == "5":
                # Start exam
                user_id = input("Enter user ID: ").strip()
                result = bot.process_user_request("start_exam", user_id)
                if result['success']:
                    print(f"\nExam Started!")
                    print(f"Time Limit: {result['exam_session']['time_limit_minutes']} minutes")
                    print(f"Number of Questions: {len(result['exam_session']['questions'])}")
                else:
                    print(f"\nError: {result['message']}")
            
            elif choice == "6":
                # Submit exam
                user_id = input("Enter user ID: ").strip()
                # Demo: submit sample answers
                answers = [
                    {"question_id": 1, "answer": "B"},
                    {"question_id": 2, "answer": "B"},
                    {"question_id": 3, "answer": "C"}
                ]
                result = bot.process_user_request("submit_exam", user_id, answers=answers)
                print(f"\nExam Results:")
                print(f"  Score: {result.get('score', 'N/A')}%")
                print(f"  Passed: {result.get('passed', False)}")
                print(f"  Correct: {result.get('correct_answers', 0)}/{result.get('total_questions', 0)}")
                print(f"  Message: {result['message']}")
            
            elif choice == "7":
                # Get exam results
                user_id = input("Enter user ID: ").strip()
                result = bot.process_user_request("get_exam_results", user_id)
                if result['success']:
                    print(f"\nExam Results:")
                    for exam in result['results']:
                        print(f"  Score: {exam['score']}% | Passed: {exam['passed']} | Attempt: {exam['attempt_number']}")
                else:
                    print(f"\nError: {result['message']}")
            
            elif choice == "8":
                # Help
                help_info = bot.get_bot_help()
                print("\nAvailable Commands:")
                for cmd, desc in help_info['commands'].items():
                    print(f"  {cmd}: {desc}")
            
            elif choice == "9":
                # Exit
                print("\nThank you for using DHS IA Exam Bot. Goodbye!")
                break
            
            else:
                print("\nInvalid choice. Please try again.")
    
    finally:
        bot.close()


if __name__ == "__main__":
    interactive_mode()
