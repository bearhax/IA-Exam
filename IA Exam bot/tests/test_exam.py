"""
Unit tests for IA Exam
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from exam import IAExam
from application import ApplicationManager


def test_start_exam():
    """Test starting an exam"""
    # First create and approve an application
    app_mgr = ApplicationManager()
    app_mgr.create_application("exam_user001", "Exam Test", "exam@example.com")
    app_mgr.submit_application("exam_user001")
    app_mgr.approve_application("exam_user001")
    
    # Now start exam
    exam = IAExam()
    result = exam.start_exam("exam_user001")
    assert result['success'] == True
    assert 'exam_session' in result
    
    exam.close()
    app_mgr.close()


def test_submit_exam():
    """Test submitting exam answers"""
    # Setup
    app_mgr = ApplicationManager()
    app_mgr.create_application("exam_user002", "Submit Exam Test", "examsubmit@example.com")
    app_mgr.submit_application("exam_user002")
    app_mgr.approve_application("exam_user002")
    
    exam = IAExam()
    
    # Submit answers
    answers = [
        {"question_id": 1, "answer": "B"},
        {"question_id": 2, "answer": "B"},
        {"question_id": 3, "answer": "C"}
    ]
    
    result = exam.submit_exam("exam_user002", answers)
    assert result['success'] == True
    assert 'score' in result
    
    exam.close()
    app_mgr.close()


def test_get_exam_results():
    """Test retrieving exam results"""
    # Setup
    app_mgr = ApplicationManager()
    app_mgr.create_application("exam_user003", "Results Test", "results@example.com")
    app_mgr.submit_application("exam_user003")
    app_mgr.approve_application("exam_user003")
    
    exam = IAExam()
    
    # Submit exam first
    answers = [
        {"question_id": 1, "answer": "B"},
        {"question_id": 2, "answer": "B"}
    ]
    exam.submit_exam("exam_user003", answers)
    
    # Get results
    result = exam.get_exam_results("exam_user003")
    assert result['success'] == True
    assert 'results' in result
    assert len(result['results']) > 0
    
    exam.close()
    app_mgr.close()


if __name__ == "__main__":
    test_start_exam()
    print("✓ test_start_exam passed")
    
    test_submit_exam()
    print("✓ test_submit_exam passed")
    
    test_get_exam_results()
    print("✓ test_get_exam_results passed")
    
    print("\nAll exam tests passed!")
