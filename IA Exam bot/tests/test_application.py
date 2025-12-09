"""
Unit tests for Application Management
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from application import ApplicationManager


def test_create_application():
    """Test creating a new application"""
    app_mgr = ApplicationManager()
    result = app_mgr.create_application("user001", "John Doe", "john@example.com")
    assert result['success'] == True
    assert result['user_id'] == "user001"
    app_mgr.close()


def test_invalid_email():
    """Test application creation with invalid email"""
    app_mgr = ApplicationManager()
    result = app_mgr.create_application("user002", "Jane Doe", "invalid-email")
    assert result['success'] == False
    app_mgr.close()


def test_duplicate_user():
    """Test creating duplicate application"""
    app_mgr = ApplicationManager()
    # Create first
    app_mgr.create_application("user003", "Test User", "test@example.com")
    # Try to create duplicate
    result = app_mgr.create_application("user003", "Another User", "another@example.com")
    assert result['success'] == False
    app_mgr.close()


def test_submit_application():
    """Test submitting an application"""
    app_mgr = ApplicationManager()
    app_mgr.create_application("user004", "Submit Test", "submit@example.com")
    result = app_mgr.submit_application("user004")
    assert result['success'] == True
    app_mgr.close()


def test_get_application_status():
    """Test getting application status"""
    app_mgr = ApplicationManager()
    app_mgr.create_application("user005", "Status Test", "status@example.com")
    result = app_mgr.get_application_status("user005")
    assert result['success'] == True
    assert result['status'] == 'DRAFT'
    app_mgr.close()


if __name__ == "__main__":
    test_create_application()
    print("✓ test_create_application passed")
    
    test_invalid_email()
    print("✓ test_invalid_email passed")
    
    test_duplicate_user()
    print("✓ test_duplicate_user passed")
    
    test_submit_application()
    print("✓ test_submit_application passed")
    
    test_get_application_status()
    print("✓ test_get_application_status passed")
    
    print("\nAll tests passed!")
