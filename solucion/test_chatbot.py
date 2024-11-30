import pytest
from unittest.mock import Mock, patch
from chatbot import Chatbot

@pytest.fixture
def chatbot():
    return Chatbot()

def test_chatbot_initialization(chatbot):
    """Prueba la inicialización correcta del chatbot"""
    assert chatbot.conversation_history == []
    assert chatbot.sources == []
    assert chatbot.client is not None

@patch('requests.post')
def test_search_internet(mock_post, chatbot):
    """Prueba la funcionalidad de búsqueda en internet"""
    mock_response = Mock()
    mock_response.json.return_value = {
        'organic': [
            {'title': 'Test Title', 'link': 'http://test.com'},
            {'title': 'Test Title 2', 'link': 'http://test2.com'}
        ]
    }
    mock_post.return_value = mock_response

    results = chatbot.search_internet("test query")
    assert len(results) == 2
    assert results[0]['title'] == 'Test Title'
    assert results[0]['link'] == 'http://test.com'

@patch('requests.get')
def test_extract_text(mock_get, chatbot):
    """Prueba la extracción de texto de una URL"""
    mock_response = Mock()
    mock_response.text = """
    <html>
        <body>
            <script>JavaScript code</script>
            <p>Contenido de prueba</p>
        </body>
    </html>
    """
    mock_get.return_value = mock_response

    text = chatbot.extract_text("http://test.com")
    assert "Contenido de prueba" in text
    assert "JavaScript code" not in text

@patch('openai.OpenAI')
def test_generate_response(mock_openai, chatbot):
    """Prueba la generación de respuestas"""
    # Crear una estructura de mock que imite la respuesta de streaming de OpenAI
    class MockDelta:
        def __init__(self, content):
            self.content = content

    class MockChoice:
        def __init__(self, content):
            self.delta = MockDelta(content)

    class MockChunk:
        def __init__(self, content):
            self.choices = [MockChoice(content)]

    # Crear un iterador de chunks
    mock_chunks = [MockChunk("Respuesta "), MockChunk("de "), MockChunk("prueba")]
    
    # Configurar el mock del cliente
    mock_client = Mock()
    mock_client.chat.completions.create.return_value = mock_chunks
    chatbot.client = mock_client

    response = chatbot.generate_response("test query", "test context")
    assert "Respuesta de prueba" in response

def test_conversation_history(chatbot):
    """Prueba el manejo del historial de conversación"""
    with patch.object(chatbot, 'generate_response', return_value="Test response"):
        with patch.object(chatbot, 'search_internet', return_value=[]):
            chatbot.conversation_history.append({"role": "user", "content": "test question"})
            chatbot.conversation_history.append({"role": "assistant", "content": "test answer"})
            
            assert len(chatbot.conversation_history) == 2
            assert chatbot.conversation_history[0]["role"] == "user"
            assert chatbot.conversation_history[1]["role"] == "assistant"

def test_sources_management(chatbot):
    """Prueba el manejo de fuentes"""
    test_sources = [
        {'title': 'Test Source 1', 'link': 'http://test1.com'},
        {'title': 'Test Source 2', 'link': 'http://test2.com'}
    ]
    chatbot.sources = test_sources

    assert len(chatbot.sources) == 2
    assert chatbot.sources[0]['title'] == 'Test Source 1'
    assert chatbot.sources[1]['link'] == 'http://test2.com'

@patch('requests.post')
def test_search_internet_error_handling(mock_post, chatbot):
    """Prueba el manejo de errores en la búsqueda"""
    mock_post.side_effect = Exception("Error de conexión")
    results = chatbot.search_internet("test query")
    assert results == []

@patch('requests.get')
def test_extract_text_error_handling(mock_get, chatbot):
    """Prueba el manejo de errores en la extracción de texto"""
    mock_get.side_effect = Exception("Error de conexión")
    text = chatbot.extract_text("http://test.com")
    assert text == ""

def test_empty_conversation_history(chatbot):
    """Prueba el estado inicial del historial de conversación"""
    assert len(chatbot.conversation_history) == 0

if __name__ == '__main__':
    pytest.main(['-v'])
