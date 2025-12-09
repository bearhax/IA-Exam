"""
IA Exam management for DHS IA Exam Bot
"""

import random
from datetime import datetime, timedelta
from database import Database
from config.settings import IA_EXAM_CONFIG, EXAM_CATEGORIES


class IAExam:
    """Information Assurance Exam Management"""
    
    def __init__(self):
        self.db = Database()
        self.exam_questions = self._load_sample_questions()
    
    def _load_sample_questions(self):
        """Load sample exam questions"""
        return [
            {
                "id": 1,
                "category": "Security Fundamentals",
                "question": "What is the primary goal of information security?",
                "options": [
                    "A) To encrypt all data",
                    "B) To ensure confidentiality, integrity, and availability of information",
                    "C) To prevent all access to systems",
                    "D) To maximize system performance"
                ],
                "correct_answer": "B",
                "difficulty": "Easy"
            },
            {
                "id": 2,
                "category": "Network Security",
                "question": "What does a firewall primarily protect against?",
                "options": [
                    "A) Virus infections",
                    "B) Unauthorized network access",
                    "C) Hardware failures",
                    "D) Power outages"
                ],
                "correct_answer": "B",
                "difficulty": "Easy"
            },
            {
                "id": 3,
                "category": "Cryptography",
                "question": "Which of the following is a symmetric encryption algorithm?",
                "options": [
                    "A) RSA",
                    "B) ECC",
                    "C) AES",
                    "D) DSA"
                ],
                "correct_answer": "C",
                "difficulty": "Medium"
            },
            {
                "id": 4,
                "category": "Access Control",
                "question": "What is the principle of least privilege?",
                "options": [
                    "A) Give users maximum access",
                    "B) Grant users only the access they need to perform their job",
                    "C) Allow all system access",
                    "D) Restrict all access"
                ],
                "correct_answer": "B",
                "difficulty": "Easy"
            },
            {
                "id": 5,
                "category": "Incident Response",
                "question": "What is the first step in incident response?",
                "options": [
                    "A) Eradication",
                    "B) Detection and analysis",
                    "C) Recovery",
                    "D) Post-incident activities"
                ],
                "correct_answer": "B",
                "difficulty": "Medium"
            }
        ]
    
    def start_exam(self, user_id):
        """Start a new exam session"""
        app = self.db.get_application(user_id)
        if not app:
            return {"success": False, "message": "Application not found"}
        
        if app['status'] != 'PENDING_EXAM':
            return {"success": False, "message": "User not eligible for exam"}
        
        # Check if user has exceeded max attempts
        exam_history = self.db.get_exam_history(user_id)
        failed_attempts = sum(1 for exam in exam_history if not exam['passed'])
        
        if failed_attempts >= IA_EXAM_CONFIG['max_attempts']:
            return {"success": False, "message": "Maximum exam attempts exceeded"}
        
        # Select random questions for the exam
        selected_questions = random.sample(self.exam_questions, min(5, len(self.exam_questions)))
        
        return {
            "success": True,
            "message": "Exam started",
            "exam_session": {
                "user_id": user_id,
                "start_time": datetime.now().isoformat(),
                "time_limit_minutes": IA_EXAM_CONFIG['time_limit_minutes'],
                "questions": selected_questions
            }
        }
    
    def submit_exam(self, user_id, answers):
        """Submit exam answers and calculate score"""
        if not answers:
            return {"success": False, "message": "No answers provided"}
        
        # Calculate score
        correct = 0
        detailed_answers = []
        
        for answer in answers:
            question_id = answer['question_id']
            user_answer = answer['answer']
            
            # Find correct answer
            question = next((q for q in self.exam_questions if q['id'] == question_id), None)
            if not question:
                continue
            
            correct_answer = question['correct_answer']
            is_correct = user_answer == correct_answer
            
            if is_correct:
                correct += 1
            
            detailed_answers.append({
                "question_id": question_id,
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct
            })
        
        # Calculate percentage
        total_questions = len(detailed_answers)
        score = int((correct / total_questions * 100)) if total_questions > 0 else 0
        passed = score >= IA_EXAM_CONFIG['min_passing_score']
        
        # Get attempt number
        exam_history = self.db.get_exam_history(user_id)
        attempt_num = len(exam_history) + 1
        
        # Save results
        result_id = self.db.save_exam_result(
            user_id, score, passed, 0, attempt_num, "General"
        )
        self.db.save_exam_answers(result_id, detailed_answers)
        
        # Update application status if passed
        if passed:
            self.db.update_application_status(user_id, 'APPROVED')
        
        return {
            "success": True,
            "score": score,
            "passed": passed,
            "correct_answers": correct,
            "total_questions": total_questions,
            "message": "Exam passed!" if passed else "Exam failed. Please review and try again."
        }
    
    def get_exam_results(self, user_id):
        """Get exam results for a user"""
        results = self.db.get_exam_history(user_id)
        if results:
            return {"success": True, "results": results}
        return {"success": False, "message": "No exam results found"}
    
    def close(self):
        """Close database connection"""
        self.db.close()
