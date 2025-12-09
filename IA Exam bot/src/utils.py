"""
Utility functions for DHS IA Exam Bot
"""

from datetime import datetime
from tabulate import tabulate


def format_timestamp(timestamp_str):
    """Format timestamp to readable format"""
    try:
        dt = datetime.fromisoformat(timestamp_str)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp_str


def display_table(headers, rows):
    """Display data in table format"""
    print(tabulate(rows, headers=headers, tablefmt="grid"))


def validate_user_id(user_id):
    """Validate user ID format"""
    if not user_id or len(user_id) < 3:
        return False
    return True


def validate_email(email):
    """Validate email format"""
    if "@" not in email or "." not in email.split("@")[1]:
        return False
    return True


def calculate_percentage(correct, total):
    """Calculate percentage"""
    if total == 0:
        return 0
    return round((correct / total) * 100, 2)


def generate_exam_report(user_id, exam_results):
    """Generate exam report"""
    if not exam_results:
        return "No exam results found."
    
    latest = exam_results[0]
    report = f"""
    ╔════════════════════════════════════════╗
    ║        EXAM REPORT - {user_id:25}║
    ╚════════════════════════════════════════╝
    
    Score: {latest['score']}%
    Status: {"PASSED ✓" if latest['passed'] else "FAILED ✗"}
    Attempt: {latest['attempt_number']}
    Date: {latest['exam_date']}
    Category: {latest['category']}
    
    """
    return report


def get_status_symbol(status):
    """Get symbol for status"""
    symbols = {
        "DRAFT": "📝",
        "SUBMITTED": "📤",
        "UNDER_REVIEW": "🔍",
        "APPROVED": "✓",
        "REJECTED": "✗",
        "PENDING_EXAM": "📋"
    }
    return symbols.get(status, "•")
