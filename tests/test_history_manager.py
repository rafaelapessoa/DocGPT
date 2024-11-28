import pytest
from app.models.history_manager import HistoryManager

def test_log_action_success():
    history_manager = HistoryManager()
    history_manager.log_action(1, "upload", {"filename": "test.txt"})
    assert len(history_manager.history) == 1

def test_retrieve_logs_for_specific_user():
    history_manager = HistoryManager()
    history_manager.log_action(1, "upload", {"filename": "test1.txt"})
    history_manager.log_action(2, "upload", {"filename": "test2.txt"})
    logs = history_manager.retrieve_logs(user_id=1)
    assert len(logs) == 1
    assert logs[0]["details"]["filename"] == "test1.txt"

def test_delete_logs_for_specific_user():
    history_manager = HistoryManager()
    history_manager.log_action(1, "upload", {"filename": "test1.txt"})
    history_manager.log_action(2, "upload", {"filename": "test2.txt"})
    history_manager.delete_logs(user_id=1)
    logs = history_manager.retrieve_logs()
    assert len(logs) == 1
    assert logs[0]["details"]["filename"] == "test2.txt"

def test_delete_all_logs():
    history_manager = HistoryManager()
    history_manager.log_action(1, "upload", {"filename": "test1.txt"})
    history_manager.delete_logs()
    assert len(history_manager.history) == 0
