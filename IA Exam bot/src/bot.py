"""
Main Bot logic for DHS IA Exam Bot
"""

from application import ApplicationManager
from exam import IAExam
from database import Database


class DHSBot:
    """Main DHS Application and Exam Bot"""
    
    def __init__(self):
        self.app_manager = ApplicationManager()
        self.exam = IAExam()
        self.db = Database()
    
    def process_user_request(self, request_type, user_id, **kwargs):
        """Process user requests based on type"""
        
        if request_type == "create_application":
            return self.app_manager.create_application(
                user_id, kwargs.get('name'), kwargs.get('email')
            )
        
        elif request_type == "get_application":
            return self.app_manager.get_application(user_id)
        
        elif request_type == "submit_application":
            return self.app_manager.submit_application(user_id)
        
        elif request_type == "get_status":
            return self.app_manager.get_application_status(user_id)
        
        elif request_type == "start_exam":
            return self.exam.start_exam(user_id)
        
        elif request_type == "submit_exam":
            return self.exam.submit_exam(user_id, kwargs.get('answers', []))
        
        elif request_type == "get_exam_results":
            return self.exam.get_exam_results(user_id)
        
        else:
            return {"success": False, "message": f"Unknown request type: {request_type}"}
    
    def get_bot_help(self):
        """Get available bot commands"""
        return {
            "commands": {
                "create_application": "Create a new DHS application",
                "get_application": "Get your application details",
                "submit_application": "Submit your application for review",
                "get_status": "Check your application status",
                "start_exam": "Start the IA exam",
                "submit_exam": "Submit exam answers",
                "get_exam_results": "View your exam results"
            }
        }
    
    def close(self):
        """Clean up resources"""
        self.app_manager.close()
        self.exam.close()
        self.db.close()
