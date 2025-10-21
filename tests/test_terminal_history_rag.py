"""
Unit tests for Terminal History RAG functionality.
"""
import pytest
import tempfile
import os
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from gev_ai.services.terminal_history_rag import TerminalHistoryRAG
from gev_ai.database.models.terminal_history import TerminalHistory


class TestTerminalHistoryRAG:
    """Test the Terminal History RAG service."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock Google GenAI client."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.embedding.values = [0.1, 0.2, 0.3, 0.4, 0.5]
        mock_client.models.embed_content.return_value = mock_response
        return mock_client

    @pytest.fixture
    def rag_service(self, mock_client):
        """Create a RAG service with mocked client."""
        with patch('gev_ai.services.terminal_history_rag.genai.Client', return_value=mock_client):
            service = TerminalHistoryRAG(api_key="test_key")
            service.client = mock_client
            return service

    def test_rag_service_initialization(self):
        """Test that RAG service can be initialized."""
        with patch('gev_ai.services.terminal_history_rag.genai.Client'):
            service = TerminalHistoryRAG(api_key="test_key")
            assert service.embedding_model == "models/text-embedding-004"

    def test_cosine_similarity(self, rag_service):
        """Test cosine similarity calculation."""
        vec1 = [1.0, 0.0, 0.0]
        vec2 = [1.0, 0.0, 0.0]
        similarity = rag_service._cosine_similarity(vec1, vec2)
        assert similarity == 1.0

        vec3 = [1.0, 0.0, 0.0]
        vec4 = [0.0, 1.0, 0.0]
        similarity = rag_service._cosine_similarity(vec3, vec4)
        assert similarity == 0.0

    def test_cosine_similarity_edge_cases(self, rag_service):
        """Test cosine similarity with edge cases."""
        # Empty vectors
        assert rag_service._cosine_similarity([], []) == 0.0
        
        # Different lengths
        assert rag_service._cosine_similarity([1.0], [1.0, 2.0]) == 0.0
        
        # Zero magnitude
        assert rag_service._cosine_similarity([0.0, 0.0], [1.0, 1.0]) == 0.0

    def test_generate_embedding(self, rag_service):
        """Test embedding generation."""
        embedding = rag_service._generate_embedding("test command")
        assert embedding is not None
        assert len(embedding) == 5
        assert embedding == [0.1, 0.2, 0.3, 0.4, 0.5]

    def test_generate_embedding_error(self, rag_service):
        """Test embedding generation with error."""
        rag_service.client.models.embed_content.side_effect = Exception("API Error")
        embedding = rag_service._generate_embedding("test command")
        assert embedding is None

    @patch('gev_ai.services.terminal_history_rag.Session')
    def test_store_commands(self, mock_session_class, rag_service):
        """Test storing commands in the database."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        with patch.object(rag_service, '_get_session', return_value=mock_session):
            commands = ["- ls -la", "- cd /home", "- pwd"]
            count = rag_service.store_commands(commands)
            
            assert count == 3
            assert mock_session.add.call_count == 3
            assert mock_session.commit.called

    @patch('gev_ai.services.terminal_history_rag.Session')
    def test_store_commands_skip_duplicates(self, mock_session_class, rag_service):
        """Test that duplicate commands are not stored."""
        mock_session = Mock()
        mock_existing = Mock()
        mock_session.query.return_value.filter.return_value.first.return_value = mock_existing
        
        with patch.object(rag_service, '_get_session', return_value=mock_session):
            commands = ["- ls -la"]
            count = rag_service.store_commands(commands)
            
            assert count == 0
            assert not mock_session.add.called

    @patch('gev_ai.services.terminal_history_rag.Session')
    def test_store_commands_skip_empty(self, mock_session_class, rag_service):
        """Test that empty commands are skipped."""
        mock_session = Mock()
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        with patch.object(rag_service, '_get_session', return_value=mock_session):
            commands = ["", "  ", "- ls"]
            count = rag_service.store_commands(commands)
            
            assert count == 1

    def test_sync_from_history_file(self, rag_service):
        """Test syncing commands from a history file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("- command1\n")
            f.write("regular command\n")
            f.write("- command2\n")
            temp_file = f.name
        
        try:
            with patch.object(rag_service, 'store_commands', return_value=2) as mock_store:
                count = rag_service.sync_from_history_file(temp_file)
                assert count == 2
                mock_store.assert_called_once()
                stored_commands = mock_store.call_args[0][0]
                assert len(stored_commands) == 2
                assert "- command1" in stored_commands
                assert "- command2" in stored_commands
        finally:
            os.unlink(temp_file)

    def test_sync_from_history_file_not_found(self, rag_service):
        """Test syncing from non-existent file."""
        count = rag_service.sync_from_history_file("/nonexistent/file")
        assert count == 0

    @patch('gev_ai.services.terminal_history_rag.Session')
    def test_retrieve_relevant_commands(self, mock_session_class, rag_service):
        """Test retrieving relevant commands using RAG."""
        mock_session = Mock()
        
        # Create mock command objects with embeddings
        mock_cmd1 = Mock()
        mock_cmd1.command = "- git commit"
        mock_cmd1.embedding = "[0.1, 0.2, 0.3, 0.4, 0.5]"
        
        mock_cmd2 = Mock()
        mock_cmd2.command = "- git push"
        mock_cmd2.embedding = "[0.15, 0.25, 0.35, 0.45, 0.55]"
        
        mock_session.query.return_value.filter.return_value.all.return_value = [mock_cmd1, mock_cmd2]
        
        with patch.object(rag_service, '_get_session', return_value=mock_session):
            result = rag_service.retrieve_relevant_commands("git operations", top_k=2)
            
            assert "git commit" in result or "git push" in result

    @patch('gev_ai.services.terminal_history_rag.Session')
    def test_retrieve_relevant_commands_empty(self, mock_session_class, rag_service):
        """Test retrieving commands when database is empty."""
        mock_session = Mock()
        mock_session.query.return_value.filter.return_value.all.return_value = []
        
        with patch.object(rag_service, '_get_session', return_value=mock_session):
            result = rag_service.retrieve_relevant_commands("test query", top_k=10)
            assert result == ""

    @patch('gev_ai.services.terminal_history_rag.Session')
    def test_retrieve_relevant_commands_no_embedding(self, mock_session_class, rag_service):
        """Test fallback when query embedding cannot be generated."""
        mock_session = Mock()
        
        with patch.object(rag_service, '_get_session', return_value=mock_session):
            with patch.object(rag_service, '_generate_embedding', return_value=None):
                with patch.object(rag_service, '_get_recent_commands') as mock_recent:
                    mock_recent.return_value = "- recent command"
                    result = rag_service.retrieve_relevant_commands("test", top_k=10)
                    mock_recent.assert_called_once()
