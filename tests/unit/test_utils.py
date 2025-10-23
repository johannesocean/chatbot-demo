"""Unit tests for app/utils.py module."""

import pytest
from pydantic import ValidationError

from app.utils import Message, get_history_str, construct_source_material, TEMPLATE


class TestMessage:
    """Tests for the Message Pydantic model."""

    def test_message_creation_with_valid_data(self):
        """Test creating a Message with valid role and content."""
        message = Message(role="user", content="Hello, world!")
        assert message.role == "user"
        assert message.content == "Hello, world!"

    def test_message_creation_with_assistant_role(self):
        """Test creating a Message with assistant role."""
        message = Message(role="assistant", content="How can I help you?")
        assert message.role == "assistant"
        assert message.content == "How can I help you?"

    def test_message_creation_with_empty_content(self):
        """Test creating a Message with empty content."""
        message = Message(role="user", content="")
        assert message.role == "user"
        assert message.content == ""

    def test_message_creation_missing_role(self):
        """Test that creating a Message without role raises ValidationError."""
        with pytest.raises(ValidationError):
            Message(content="Hello")

    def test_message_creation_missing_content(self):
        """Test that creating a Message without content raises ValidationError."""
        with pytest.raises(ValidationError):
            Message(role="user")


class TestGetHistoryStr:
    """Tests for the get_history_str function."""

    def test_get_history_str_with_empty_list(self):
        """Test get_history_str with an empty message list."""
        result = get_history_str([])
        assert result == "No chat history yet."

    def test_get_history_str_with_none(self):
        """Test get_history_str with None (falsy value)."""
        result = get_history_str(None)
        assert result == "No chat history yet."

    def test_get_history_str_with_single_message(self):
        """Test get_history_str with a single message."""
        messages = [Message(role="user", content="Hello")]
        result = get_history_str(messages)
        assert result == "user: Hello"

    def test_get_history_str_with_multiple_messages(self):
        """Test get_history_str with multiple messages."""
        messages = [
            Message(role="user", content="Hello"),
            Message(role="assistant", content="Hi there!"),
            Message(role="user", content="How are you?"),
        ]
        result = get_history_str(messages)
        expected = "user: Hello\nassistant: Hi there!\nuser: How are you?"
        assert result == expected

    def test_get_history_str_preserves_message_order(self):
        """Test that get_history_str preserves the order of messages."""
        messages = [
            Message(role="user", content="First"),
            Message(role="assistant", content="Second"),
            Message(role="user", content="Third"),
        ]
        result = get_history_str(messages)
        lines = result.split("\n")
        assert lines[0] == "user: First"
        assert lines[1] == "assistant: Second"
        assert lines[2] == "user: Third"

    def test_get_history_str_with_multiline_content(self):
        """Test get_history_str with messages containing multiline content."""
        messages = [
            Message(role="user", content="Line 1\nLine 2"),
        ]
        result = get_history_str(messages)
        assert result == "user: Line 1\nLine 2"


class TestConstructSourceMaterial:
    """Tests for the construct_source_material function."""

    def test_construct_source_material_with_single_document(self):
        """Test construct_source_material with a single document."""
        db_material = {
            "documents": [["This is a recipe for pasta."]]
        }
        result = construct_source_material(db_material)
        assert result == "This is a recipe for pasta."

    def test_construct_source_material_with_multiple_documents(self):
        """Test construct_source_material with multiple documents."""
        db_material = {
            "documents": [["Recipe 1: Pasta", "Recipe 2: Pizza", "Recipe 3: Salad"]]
        }
        result = construct_source_material(db_material)
        expected = "Recipe 1: Pasta\n Recipe 2: Pizza\n Recipe 3: Salad"
        assert result == expected

    def test_construct_source_material_with_empty_documents(self):
        """Test construct_source_material with empty documents list."""
        db_material = {
            "documents": [[]]
        }
        result = construct_source_material(db_material)
        assert result == ""

    def test_construct_source_material_format(self):
        """Test that construct_source_material uses correct separator."""
        db_material = {
            "documents": [["Doc1", "Doc2"]]
        }
        result = construct_source_material(db_material)
        # The function uses "\n " (newline + space) as separator
        assert "\n " in result
        assert result == "Doc1\n Doc2"


class TestTemplate:
    """Tests for the TEMPLATE constant."""

    def test_template_exists(self):
        """Test that TEMPLATE constant is defined."""
        assert TEMPLATE is not None
        assert isinstance(TEMPLATE, str)

    def test_template_contains_placeholders(self):
        """Test that TEMPLATE contains the expected placeholders."""
        assert "{context_str}" in TEMPLATE
        assert "{history_str}" in TEMPLATE

    def test_template_contains_system_info(self):
        """Test that TEMPLATE contains system information section."""
        assert "### System information ###" in TEMPLATE
        assert "master chef chatbot" in TEMPLATE.lower()

    def test_template_format_with_values(self):
        """Test that TEMPLATE can be formatted with actual values."""
        formatted = TEMPLATE.format(
            context_str="Recipe context here",
            history_str="user: What's for dinner?"
        )
        assert "Recipe context here" in formatted
        assert "user: What's for dinner?" in formatted
        assert "{context_str}" not in formatted
        assert "{history_str}" not in formatted
