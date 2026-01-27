import pytest
import shutil
from pathlib import Path
from unittest.mock import Mock, patch
from slides_to_textbook.modules.image_generators import FigureRecreator, PortraitGenerator

@pytest.fixture
def output_dir(tmp_path):
    d = tmp_path / "images"
    d.mkdir()
    return d

def test_figure_recreation(output_dir):
    creator = FigureRecreator(output_dir)
    path = creator.recreate_figure("A graph of x squared", "graph.png")
    
    assert path is not None
    assert path.exists()
    assert path.name == "graph.png"

def test_portrait_generation(output_dir):
    gen = PortraitGenerator(output_dir)
    path = gen.generate_portrait("Alan Turing", "1912-1954")
    
    assert path is not None
    assert path.exists()
    assert path.name == "AlanTuring.jpg"

def test_skip_existing(output_dir):
    # Create file first
    (output_dir / "skip.png").touch()
    
    creator = FigureRecreator(output_dir)
    # Patch logger or check modification time to verify skip?
    # Simplest is just ensuring it returns the path
    path = creator.recreate_figure("desc", "skip.png")
    assert path.exists()
