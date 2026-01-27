import pytest
from unittest.mock import Mock, patch
from slides_to_textbook.modules.topic_researcher import TopicResearcher

@pytest.fixture
def researcher():
    return TopicResearcher()

@patch('slides_to_textbook.modules.topic_researcher.AIClient')
def test_research_topic_basic(mock_ai_client, researcher):
    # Setup AI mock
    mock_instance = mock_ai_client.return_value
    mock_instance.generate_text.return_value = "Historical Context Text"
    researcher.ai_client = mock_instance
    
    # Mock scholarly to avoid network calls
    with patch('slides_to_textbook.modules.topic_researcher.scholarly') as mock_scholarly:
        # Mock generator behavior
        mock_pub = {
            'bib': {
                'title': 'Seminal Paper',
                'author': ['A. Turing'],
                'pub_year': '1950'
            },
            'pub_url': 'http://example.com'
        }
        mock_scholarly.search_pubs.return_value = iter([mock_pub])
        
        input_data = {
            "title": "Machine Learning",
            "people": ["Turing"],
            "concepts": ["Neural Networks"]
        }
        
        result = researcher.research_topic(input_data)
        
        assert result["research"]["historical_context"] == "Historical Context Text"
        assert len(result["research"]["citations"]) > 0
        assert result["research"]["citations"][0]["title"] == "Seminal Paper"

@patch('slides_to_textbook.modules.topic_researcher.AIClient')
def test_research_topic_failure_handling(mock_ai_client, researcher):
    mock_instance = mock_ai_client.return_value
    mock_instance.generate_text.side_effect = Exception("AI Error")
    researcher.ai_client = mock_instance
    
    with patch('slides_to_textbook.modules.topic_researcher.scholarly') as mock_scholarly:
        mock_scholarly.search_pubs.side_effect = Exception("Network Error")
        
        input_data = {"title": "Test", "people": [], "concepts": []}
        result = researcher.research_topic(input_data)
        
        assert result["research"]["historical_context"] == "Historical context unavailable."
        assert len(result["research"]["citations"]) == 0
