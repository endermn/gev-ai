"""
Terminal History RAG Service

This service implements Retrieval Augmented Generation (RAG) for terminal history.
Instead of returning a fixed number of recent commands, it:
1. Stores terminal history commands in a database with embeddings
2. Retrieves semantically relevant commands based on the user's query
"""

import json
import os
from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import desc

from google import genai
from google.genai import types

try:
    # Relative imports for when running as a module
    from database.config.database_manager import database_manager
    from database.models.terminal_history import TerminalHistory
    from services.logger import GevaiLogger
except ImportError:
    # Absolute imports for when importing from tests or external code
    from gev_ai.database.config.database_manager import database_manager
    from gev_ai.database.models.terminal_history import TerminalHistory
    from gev_ai.services.logger import GevaiLogger

logger = GevaiLogger(name=__name__, file="gevai.log").get_logger()


class TerminalHistoryRAG:
    """RAG service for terminal history management and retrieval."""

    def __init__(self, api_key: str):
        """Initialize the RAG service with Google GenAI client."""
        self.client = genai.Client(api_key=api_key)
        self.embedding_model = "models/text-embedding-004"

    def _get_session(self) -> Session:
        """Get a database session."""
        from sqlalchemy.orm import sessionmaker
        SessionLocal = sessionmaker(bind=database_manager.engine)
        return SessionLocal()

    def _generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding for a text using Google GenAI."""
        try:
            response = self.client.models.embed_content(
                model=self.embedding_model,
                content=text
            )
            if response and hasattr(response, 'embedding'):
                return response.embedding.values
            return None
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return None

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)

    def store_commands(self, commands: List[str]) -> int:
        """
        Store terminal commands in the database with embeddings.
        
        Args:
            commands: List of terminal commands to store
            
        Returns:
            Number of commands successfully stored
        """
        session = self._get_session()
        stored_count = 0
        
        try:
            for command in commands:
                # Skip empty commands
                command = command.strip()
                if not command:
                    continue
                
                # Check if command already exists (avoid duplicates)
                existing = session.query(TerminalHistory).filter(
                    TerminalHistory.command == command
                ).first()
                
                if existing:
                    continue
                
                # Generate embedding
                embedding = self._generate_embedding(command)
                embedding_json = json.dumps(embedding) if embedding else None
                
                # Store in database
                history_entry = TerminalHistory(
                    command=command,
                    timestamp=datetime.now(timezone.utc),
                    embedding=embedding_json
                )
                session.add(history_entry)
                stored_count += 1
            
            session.commit()
            logger.info(f"Stored {stored_count} terminal history commands")
            return stored_count
            
        except Exception as e:
            logger.error(f"Error storing commands: {e}")
            session.rollback()
            return stored_count
        finally:
            session.close()

    def retrieve_relevant_commands(self, query: str, top_k: int = 10) -> str:
        """
        Retrieve relevant terminal commands based on semantic similarity to the query.
        
        Args:
            query: User's query or context
            top_k: Number of most relevant commands to retrieve
            
        Returns:
            String containing the most relevant commands
        """
        session = self._get_session()
        
        try:
            # Generate embedding for the query
            query_embedding = self._generate_embedding(query)
            if not query_embedding:
                logger.warning("Could not generate query embedding, falling back to recent commands")
                return self._get_recent_commands(session, top_k)
            
            # Get all commands with embeddings
            all_commands = session.query(TerminalHistory).filter(
                TerminalHistory.embedding.isnot(None)
            ).all()
            
            if not all_commands:
                logger.info("No commands with embeddings found, returning empty")
                return ""
            
            # Calculate similarity scores
            scored_commands = []
            for cmd in all_commands:
                try:
                    cmd_embedding = json.loads(cmd.embedding)
                    similarity = self._cosine_similarity(query_embedding, cmd_embedding)
                    scored_commands.append((cmd.command, similarity))
                except Exception as e:
                    logger.error(f"Error processing command embedding: {e}")
                    continue
            
            # Sort by similarity and get top_k
            scored_commands.sort(key=lambda x: x[1], reverse=True)
            top_commands = [cmd for cmd, _ in scored_commands[:top_k]]
            
            return "\n".join(top_commands) if top_commands else ""
            
        except Exception as e:
            logger.error(f"Error retrieving relevant commands: {e}")
            return self._get_recent_commands(session, top_k)
        finally:
            session.close()

    def _get_recent_commands(self, session: Session, limit: int = 10) -> str:
        """Fallback method to get most recent commands."""
        try:
            recent = session.query(TerminalHistory).order_by(
                desc(TerminalHistory.timestamp)
            ).limit(limit).all()
            
            return "\n".join([cmd.command for cmd in recent]) if recent else ""
        except Exception as e:
            logger.error(f"Error getting recent commands: {e}")
            return ""

    def sync_from_history_file(self, history_file_path: str) -> int:
        """
        Sync commands from terminal history file to database.
        
        Args:
            history_file_path: Path to terminal history file
            
        Returns:
            Number of commands synced
        """
        try:
            history_file = os.path.expanduser(history_file_path)
            with open(history_file, "r", errors="ignore") as f:
                lines = f.readlines()
            
            # Filter for commands starting with hyphen (as per original logic)
            commands = [line.strip() for line in lines if line.strip().startswith("-")]
            
            if commands:
                return self.store_commands(commands)
            return 0
            
        except FileNotFoundError:
            logger.error(f"History file not found at '{history_file_path}'")
            return 0
        except Exception as e:
            logger.error(f"Error syncing from history file: {e}")
            return 0
