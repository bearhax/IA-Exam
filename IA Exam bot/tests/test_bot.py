"""
Unit tests for DHS Bot
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from bot import DHSBot


def test_bot_initialization():
    """Test bot initialization"""
    bot = DHSBot()
    assert bot is not None
    assert bot.app_manager is not None
    assert bot.exam is not None
    bot.close()


def test_process_create_application():
    """Test bot processing create application request"""
    bot = DHSBot()
    result = bot.process_user_request(
        "create_application", 
        "bot_user001",
        name="Bot Test User",
        email="bottest@example.com"
    )
    assert result['success'] == True
    bot.close()


def test_process_unknown_request():
    """Test bot processing unknown request"""
    bot = DHSBot()
    result = bot.process_user_request("unknown_request", "user001")
    assert result['success'] == False
    assert "Unknown" in result['message']
    bot.close()


def test_get_bot_help():
    """Test getting bot help"""
    bot = DHSBot()
    help_info = bot.get_bot_help()
    assert 'commands' in help_info
    assert 'create_application' in help_info['commands']
    bot.close()


if __name__ == "__main__":
    test_bot_initialization()
    print("✓ test_bot_initialization passed")
    
    test_process_create_application()
    print("✓ test_process_create_application passed")
    
    test_process_unknown_request()
    print("✓ test_process_unknown_request passed")
    
    test_get_bot_help()
    print("✓ test_get_bot_help passed")
    
    print("\nAll bot tests passed!")
