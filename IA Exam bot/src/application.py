"""
Application management for DHS IA Exam Bot
"""

from datetime import datetime
from database import Database
from config.settings import APPLICATION_STATES


class ApplicationManager:
    """Manages DHS applications"""
    
    def __init__(self):
        self.db = Database()
    
    def create_application(self, user_id, name, email):
        """Create a new application"""
        if not self._validate_email(email):
            return {"success": False, "message": "Invalid email format"}
        
        if self.db.add_application(user_id, name, email):
            return {
                "success": True,
                "message": "Application created successfully",
                "user_id": user_id
            }
        else:
            return {
                "success": False,
                "message": "User already has an application"
            }
    
    def get_application(self, user_id):
        """Retrieve application details"""
        app = self.db.get_application(user_id)
        if app:
            return {"success": True, "data": app}
        return {"success": False, "message": "Application not found"}
    
    def submit_application(self, user_id):
        """Submit an application for review"""
        app = self.db.get_application(user_id)
        if not app:
            return {"success": False, "message": "Application not found"}
        
        if app['status'] != 'DRAFT':
            return {"success": False, "message": f"Cannot submit application in {app['status']} state"}
        
        self.db.update_application_status(user_id, 'SUBMITTED')
        return {"success": True, "message": "Application submitted successfully"}
    
    def approve_application(self, user_id):
        """Approve an application"""
        app = self.db.get_application(user_id)
        if not app:
            return {"success": False, "message": "Application not found"}
        
        self.db.update_application_status(user_id, 'APPROVED')
        self.db.update_application_status(user_id, 'PENDING_EXAM')
        return {"success": True, "message": "Application approved. User can now take IA exam"}
    
    def reject_application(self, user_id, reason):
        """Reject an application"""
        app = self.db.get_application(user_id)
        if not app:
            return {"success": False, "message": "Application not found"}
        
        self.db.update_application_status(user_id, 'REJECTED')
        self.db.log_action(user_id, "APPLICATION_REJECTED", reason)
        return {"success": True, "message": "Application rejected"}
    
    def get_application_status(self, user_id):
        """Get current application status"""
        app = self.db.get_application(user_id)
        if app:
            return {"success": True, "status": app['status']}
        return {"success": False, "message": "Application not found"}
    
    def _validate_email(self, email):
        """Validate email format"""
        return "@" in email and "." in email.split("@")[1]
    
    def close(self):
        """Close database connection"""
        self.db.close()
