import os
from typing import List, Dict
from openai import AzureOpenAI
from dotenv import load_dotenv
from chatbot.database import DatabaseManager

load_dotenv()


class Chatbot:
    """AI-powered chatbot using Azure OpenAI with database integration."""

    def __init__(self):
        # Initialize Azure OpenAI client
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

        # Initialize database manager
        self.db = DatabaseManager()
        self.db.connect()

        # Conversation history
        self.conversation_history: List[Dict[str, str]] = []

        # Get database context for AI
        self.db_context = self.db.get_database_context()

        # System prompt
        self.system_prompt = f"""You are a helpful AI assistant with access to a PostgreSQL database.
You can answer questions about the data in the database and help users query information.

{self.db_context}

When users ask about data, you can:
1. Describe what tables and data are available
2. Help them understand the database structure
3. Answer questions based on the database context
4. Suggest queries they might want to run

Be helpful, accurate, and concise in your responses."""

    def chat(self, user_message: str) -> str:
        """Send a message and get a response from the AI."""
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Prepare messages for API call
        messages = [
            {"role": "system", "content": self.system_prompt}
        ] + self.conversation_history

        try:
            # Call Azure OpenAI API
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                max_completion_tokens=800
            )

            # Extract assistant's response
            assistant_message = response.choices[0].message.content

            # Add to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            return assistant_message

        except Exception as e:
            error_message = f"Error: {str(e)}"
            print(error_message)
            return f"I encountered an error while processing your request: {str(e)}"

    def query_database(self, query: str) -> List[Dict]:
        """Execute a SQL query on the database."""
        return self.db.execute_query(query)

    def get_tables(self) -> List[str]:
        """Get list of all tables."""
        return self.db.get_tables()

    def get_table_schema(self, table_name: str) -> List[Dict]:
        """Get schema for a specific table."""
        return self.db.get_table_schema(table_name)

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []

    def close(self):
        """Close database connection."""
        self.db.disconnect()
