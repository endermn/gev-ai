"""
Unit tests for the Tool interface.
"""
import pytest
from gev_ai.tools.agent_tools.interfaces import Tool


class TestToolInterface:
    """Test the Tool abstract base class."""

    def test_tool_interface_is_abstract(self):
        """Test that Tool cannot be instantiated directly."""
        with pytest.raises(TypeError):
            Tool()

    def test_tool_implementation(self):
        """Test that a proper Tool implementation works correctly."""
        
        class ConcreteTool(Tool):
            @property
            def name(self) -> str:
                return "TestTool"
            
            @property
            def description(self) -> str:
                return "A test tool for unit testing"
        
        tool = ConcreteTool()
        assert tool.name == "TestTool"
        assert tool.description == "A test tool for unit testing"

    def test_tool_requires_name_implementation(self):
        """Test that Tool implementations must provide a name property."""
        
        class InvalidTool(Tool):
            @property
            def description(self) -> str:
                return "Missing name property"
        
        with pytest.raises(TypeError):
            InvalidTool()

    def test_tool_requires_description_implementation(self):
        """Test that Tool implementations must provide a description property."""
        
        class InvalidTool(Tool):
            @property
            def name(self) -> str:
                return "MissingDescription"
        
        with pytest.raises(TypeError):
            InvalidTool()
