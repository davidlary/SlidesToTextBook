import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from slides_to_textbook.modules.pdf_analyzer import PDFAnalyzer

class MockPage:
    def extract_text(self):
        return "Slide Text"
    def to_image(self, resolution):
        m = Mock()
        m.original = "ImageObject"
        return m

class MockPDF:
    def __init__(self, path):
        self.pages = [MockPage(), MockPage()]
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

@pytest.fixture
def analyzer():
    return PDFAnalyzer()

@patch('slides_to_textbook.modules.pdf_analyzer.pdfplumber.open')
def test_extract_content_simple(mock_open, analyzer):
    mock_open.return_value = MockPDF("dummy")
    
    result = analyzer.extract_content(Path("dummy.pdf"))
    
    assert len(result["pages"]) == 2
    assert result["pages"][0]["text"] == "Slide Text"
    assert result["pages"][0]["page_number"] == 1

@patch('slides_to_textbook.modules.pdf_analyzer.pdfplumber.open')
@patch('slides_to_textbook.modules.pdf_analyzer.pytesseract.image_to_string')
def test_extract_content_ocr_fallback(mock_ocr, mock_open, analyzer):
    # Setup page with empty text
    mock_page = MockPage()
    mock_page.extract_text = Mock(return_value="") # Empty text
    
    mock_pdf = MagicMock()
    mock_pdf.pages = [mock_page]
    mock_open.return_value.__enter__.return_value = mock_pdf
    
    mock_ocr.return_value = "OCR Text"
    
    result = analyzer.extract_content(Path("dummy.pdf"))
    
    assert result["pages"][0]["text"] == "OCR Text"
    mock_ocr.assert_called_once()

@patch('slides_to_textbook.modules.pdf_analyzer.AIClient')
@patch('slides_to_textbook.modules.pdf_analyzer.pdfplumber.open')
def test_analyze_pdf_integration(mock_open, mock_ai_client, analyzer):
    # Mock PDF
    mock_open.return_value = MockPDF("dummy")
    
    # Mock AI response
    mock_client_instance = mock_ai_client.return_value
    mock_client_instance.generate_text.return_value = '''
    {
        "title": "Test Chapter",
        "description": "A test description",
        "sections": ["Intro", "Conclusion"],
        "concepts": ["AI", "ML"],
        "people": ["Turing"],
        "equations": ["E=mc2"]
    }
    '''
    # We need to set the instance on the analyzer because it's created in __init__
    # But checking implementation: analyzer = PDFAnalyzer() creates AIClient()
    # So we should patch the class before init or mock the attribute
    analyzer.ai_client = mock_client_instance

    with patch('pathlib.Path.exists', return_value=True):
        result = analyzer.analyze_pdf("dummy.pdf")
    
    assert result["file_name"] == "dummy.pdf"
    assert result["analysis"]["title"] == "Test Chapter"
    assert len(result["analysis"]["sections"]) == 2
