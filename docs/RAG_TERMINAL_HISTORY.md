# RAG Terminal History

## Overview

Gev-AI now uses **Retrieval Augmented Generation (RAG)** for terminal history instead of returning a fixed number of recent commands. This intelligent approach retrieves semantically relevant commands based on your query context.

## What Changed?

### Before (Constant Number Approach)
- Always returned the **last 10 commands** from terminal history
- No relevance to the user's current query
- Limited context for the AI assistant

### After (RAG Approach)
- Stores terminal commands in a database with **semantic embeddings**
- Retrieves **relevant commands** based on your query
- Provides more useful context to the AI assistant
- Ranks commands by semantic similarity

## How It Works

1. **Storage**: Terminal commands are synced from your history file to a local database
2. **Embedding**: Each command is converted to a semantic vector using Google's embedding model
3. **Retrieval**: When you make a query, the system:
   - Converts your query to an embedding
   - Compares it with stored command embeddings
   - Returns the most semantically similar commands

## Example

**Your query:** "I need to commit and push my changes"

**RAG retrieves:**
```bash
- git status
- git add .
- git commit -m 'Initial commit'
- git push origin main
```

Instead of just the last 10 commands, you get commands **relevant to Git operations**.

## Benefits

1. **Smarter Context**: AI sees commands relevant to your current task
2. **Better Suggestions**: More accurate recommendations based on what you've done before
3. **Efficient**: No need to manually specify what commands to show
4. **Automatic Sync**: Your terminal history is automatically synced and embedded

## Technical Details

### Database Schema

```python
class TerminalHistory(Base):
    id: Integer (Primary Key)
    command: Text (Indexed)
    timestamp: DateTime (Indexed)
    embedding: Text (JSON-encoded vector)
```

### Components

1. **TerminalHistoryRAG Service** (`services/terminal_history_rag.py`)
   - Manages storage and retrieval of terminal commands
   - Generates embeddings using Google GenAI API
   - Implements cosine similarity for semantic search

2. **TerminalHistoryParser** (`tools/common_tools/history_parser.py`)
   - Enhanced to support RAG retrieval
   - Falls back to recent commands if RAG is unavailable
   - Accepts optional query parameter for context-aware retrieval

3. **Database Model** (`database/models/terminal_history.py`)
   - Stores commands with timestamps and embeddings
   - Indexed for efficient querying

### Embedding Model

The system uses Google's `text-embedding-004` model, which provides:
- High-quality semantic embeddings
- Support for multiple languages
- Efficient vector representations

## Configuration

The system automatically syncs your terminal history file. The default paths are:

- **Zsh**: `~/.zsh_history`
- **Fish**: `~/.local/share/fish/fish_history`
- **Bash**: `~/.bash_history`
- **PowerShell**: `%APPDATA%\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt`

You can configure a custom path:
```bash
gevai config history='path/to/your/history'
```

## Privacy & Data

- All data is stored **locally** in `gev-ai.db`
- Embeddings are generated using the Google GenAI API
- No raw commands are sent to external services (only embeddings)
- You can clear the history database at any time

## Performance

- **First run**: May take a few seconds to sync and embed history
- **Subsequent runs**: Fast retrieval using cached embeddings
- **Storage**: Minimal disk space (~1KB per command)

## Fallback Behavior

If the RAG service is unavailable (e.g., API issues), the system automatically falls back to:
1. Most recent commands from the database
2. Last 10 commands from the history file

This ensures Gev-AI always has context, even if embedding generation fails.

## Testing

Comprehensive test suite covering:
- Embedding generation and storage
- Semantic retrieval and ranking
- Cosine similarity calculations
- Database operations
- Error handling and fallbacks

Run tests:
```bash
pytest tests/test_terminal_history_rag.py -v
```

## Future Enhancements

Potential improvements for the RAG system:
- Support for command metadata (exit codes, timestamps, frequency)
- Personalized command ranking based on usage patterns
- Multi-language support for command descriptions
- Command clustering and categorization
- Integration with issue/solution database for learning from past problems
