import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List

class ProgressTracker:
    DEFAULT_PHASES = {
        "topic_analysis": {
            "status": "pending",
            "lectures_total": 0,
            "lectures_processed": 0,
            "topics_identified": 0,
            "user_approved": False
        },
        "content_generation": {
            "status": "pending",
            "chapters_completed": 0,
            "chapters_total": 0,
            "figures_created": 0,
            "figures_total": 0,
            "portraits_created": 0,
            "portraits_total": 0
        },
        "validation": {
            "status": "pending"
        },
        "finalization": {
            "status": "pending"
        }
    }

    def __init__(self, book_name: str, base_dir: Path):
        self.book_name = book_name
        self.base_dir = Path(base_dir)
        self.progress_file = self.base_dir / self.book_name / "progress.json"
        
        self.data = self._load_or_create()
        self._setup_logging()

    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(f"ProgressTracker-{self.book_name}")

    def _load_or_create(self) -> Dict[str, Any]:
        if self.progress_file.exists():
            try:
                return json.loads(self.progress_file.read_text())
            except json.JSONDecodeError:
                self.logger.error("Failed to decode progress.json, creating new.")
        
        # Create default
        now = datetime.utcnow().isoformat() + "Z"
        data = {
            "book_name": self.book_name,
            "version": "1.0",
            "started": now,
            "updated": now,
            "status": "not_started",
            "current_phase": "planning",
            "current_chunk": "",
            "phases": self.DEFAULT_PHASES.copy(),
            "chapters": [],
            "errors": [],
            "warnings": [],
            "recovery_checkpoint": {
                "module": None,
                "chapter": None,
                "section": None,
                "timestamp": now
            }
        }
        
        # Ensure directory exists
        self.progress_file.parent.mkdir(parents=True, exist_ok=True)
        self.save(data)
        return data

    def save(self, data: Optional[Dict[str, Any]] = None):
        if data:
            self.data = data
        
        # Update timestamp
        self.data["updated"] = datetime.utcnow().isoformat() + "Z"
        
        self.progress_file.parent.mkdir(parents=True, exist_ok=True)
        self.progress_file.write_text(json.dumps(self.data, indent=2))

    def update_phase(self, phase: str, **kwargs):
        if phase not in self.data["phases"]:
            self.data["phases"][phase] = {}
        
        self.data["phases"][phase].update(kwargs)
        if "status" in kwargs:
             # Basic status update logic could go here
             pass
        self.save()

    def add_chapter(self, name: str):
        # Check if exists
        for ch in self.data["chapters"]:
            if ch["name"] == name:
                return
        
        new_chapter = {
            "name": name,
            "file": f"Chapter-{name.replace(' ', '')}.tex",
            "status": "not_started",
            "word_count": 0,
            "figures": 0,
            "portraits": 0,
            "citations": 0,
            "started": datetime.utcnow().isoformat() + "Z"
        }
        self.data["chapters"].append(new_chapter)
        self.save()

    def update_chapter(self, name: str, **kwargs):
        found = False
        for ch in self.data["chapters"]:
            if ch["name"] == name:
                ch.update(kwargs)
                if kwargs.get("status") == "completed":
                    ch["completed"] = datetime.utcnow().isoformat() + "Z"
                found = True
                break
        if not found:
            self.logger.warning(f"Chapter {name} not found.")
        self.save()

    def log_error(self, message: str, details: Optional[Dict] = None):
        error_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "message": message,
            "details": details or {}
        }
        self.data["errors"].append(error_entry)
        self.logger.error(message)
        self.save()

    def update_chunk(self, chunk_name: str):
        self.data["current_chunk"] = chunk_name
        self.save()
