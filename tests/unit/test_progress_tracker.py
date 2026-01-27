import json
import tempfile
import pytest
from pathlib import Path
from slides_to_textbook.modules.progress_tracker import ProgressTracker

@pytest.fixture
def temp_project_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        d = Path(tmpdirname)
        # Create book directory
        (d / "TestBook").mkdir()
        yield d

def test_init_creates_default_progress(temp_project_dir):
    tracker = ProgressTracker(book_name="TestBook", base_dir=temp_project_dir)
    assert tracker.book_name == "TestBook"
    
    # Check if file created
    progress_file = temp_project_dir / "TestBook" / "progress.json"
    assert progress_file.exists()
    
    data = json.loads(progress_file.read_text())
    assert data["book_name"] == "TestBook"
    assert data["status"] == "not_started"
    assert "phases" in data

def test_load_existing_progress(temp_project_dir):
    # Setup existing
    progress_file = temp_project_dir / "TestBook" / "progress.json"
    initial_data = {
        "book_name": "TestBook",
        "version": "1.0",
        "status": "in_progress",
        "phases": {}
    }
    progress_file.write_text(json.dumps(initial_data))
    
    tracker = ProgressTracker(book_name="TestBook", base_dir=temp_project_dir)
    assert tracker.data["status"] == "in_progress"

def test_update_phase(temp_project_dir):
    tracker = ProgressTracker(book_name="TestBook", base_dir=temp_project_dir)
    tracker.update_phase("topic_analysis", status="in_progress")
    
    assert tracker.data["phases"]["topic_analysis"]["status"] == "in_progress"
    
    tracker.save()
    # Verify persistence
    data = json.loads((temp_project_dir / "TestBook" / "progress.json").read_text())
    assert data["phases"]["topic_analysis"]["status"] == "in_progress"

def test_add_chapter(temp_project_dir):
    tracker = ProgressTracker(book_name="TestBook", base_dir=temp_project_dir)
    tracker.add_chapter("Chapter 1")
    
    assert len(tracker.data["chapters"]) == 1
    assert tracker.data["chapters"][0]["name"] == "Chapter 1"
    assert tracker.data["chapters"][0]["status"] == "not_started"

def test_complete_chapter(temp_project_dir):
    tracker = ProgressTracker(book_name="TestBook", base_dir=temp_project_dir)
    tracker.add_chapter("Chapter 1")
    tracker.update_chapter("Chapter 1", status="completed", word_count=1000)
    
    assert tracker.data["chapters"][0]["status"] == "completed"
    assert tracker.data["chapters"][0]["word_count"] == 1000

def test_log_error(temp_project_dir):
    tracker = ProgressTracker(book_name="TestBook", base_dir=temp_project_dir)
    tracker.log_error("Something went wrong")
    
    assert len(tracker.data["errors"]) == 1
    assert tracker.data["errors"][0]["message"] == "Something went wrong"

def test_invalid_phase_update(temp_project_dir):
    tracker = ProgressTracker(book_name="TestBook", base_dir=temp_project_dir)
    # Start a non-existent phase - depending on implementation strictness
    # For now assuming we allow dynamic or preset phases.
    # If strict, this might raise error.
    # Let's assume strict validation against schema phases if possible, or just loose.
    # Creating a new phase entry for test
    tracker.update_phase("unknown_phase", status="pending")
    assert "unknown_phase" in tracker.data["phases"]
