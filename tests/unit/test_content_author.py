import pytest
from unittest.mock import Mock, patch
from slides_to_textbook.modules.content_author import ContentAuthor

@pytest.fixture
def author():
    return ContentAuthor()

@patch('slides_to_textbook.modules.content_author.AIClient')
def test_generate_chapter_content(mock_ai_client, author):
    # Setup AI mock
    mock_instance = mock_ai_client.return_value
    mock_instance.generate_text.return_value = "Lorem ipsum content."
    author.ai_client = mock_instance
    
    topic_data = {
        "title": "Machine Learning Intro",
        "description": "Basics of ML",
        "sections": ["Supervised", "Unsupervised"],
        "concepts": ["Regression", "Clustering"],
        "people": ["Samuel"],
        "equations": ["y = mx + b"],
        "research": {
            "historical_context": "Created in 1950s..."
        }
    }
    
    content = author.generate_chapter_content(topic_data)
    
    assert "\\section{Introduction}" in content
    assert "Lorem ipsum content." in content
    # Should call generate_text 3 times (Intro + 2 sections)
    assert mock_instance.generate_text.call_count == 3

@patch('slides_to_textbook.modules.content_author.AIClient')
def test_generate_section_failure(mock_ai_client, author):
    mock_instance = mock_ai_client.return_value
    mock_instance.generate_text.side_effect = Exception("AI Error")
    author.ai_client = mock_instance
    
    content = author._generate_section("Test Section", {})
    assert "% Error generating section" in content
