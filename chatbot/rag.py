import os
import sys
from typing import List, Dict, Any
from openai import AzureOpenAI
from dotenv import load_dotenv
from chatbot.database import DatabaseManager

# Load environment variables from .env for local development
load_dotenv()

# Support Streamlit Cloud secrets
try:
    import streamlit as st
    if hasattr(st, 'secrets'):
        # Running on Streamlit Cloud, use secrets
        for key in st.secrets:
            os.environ[key] = st.secrets[key]
except:
    pass

# Force stdout to flush immediately for debugging
sys.stdout.reconfigure(line_buffering=True)


class RAGChatbot:
    """RAG-enabled chatbot that queries database and generates contextual responses."""

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

        # Get database schema
        self.db_context = self.db.get_database_context()

    def generate_sql_query(self, user_question: str) -> str:
        """Generate SQL query based on user's natural language question."""
        prompt = f"""Given the following database schema:

{self.db_context}

Generate a SQL query to answer this question: {user_question}

CRITICAL RULES:
1. ALL column names MUST be wrapped in double quotes (e.g., "executionId", "userId", "createdAt")
2. PostgreSQL column names are case-sensitive - use exact case as shown in schema
3. Table names do NOT need quotes (they are lowercase)
4. Return ONLY the SQL query, nothing else
5. Make sure the query is safe and read-only (SELECT only)

Example: SELECT "id", "executionId", "message" FROM execution_logs LIMIT 5

If the question cannot be answered with the available data, return 'NO_QUERY_POSSIBLE'."""

        try:
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {"role": "system", "content": "You are a SQL expert. Generate safe, read-only SQL queries."},
                    {"role": "user", "content": prompt}
                ],
                max_completion_tokens=500
            )

            sql_query = response.choices[0].message.content

            if not sql_query:
                print("⚠️ Azure OpenAI returned empty SQL query")
                return "NO_QUERY_POSSIBLE"

            sql_query = sql_query.strip()
            # Remove markdown code blocks if present
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

            if not sql_query:
                print("⚠️ SQL query empty after processing")
                return "NO_QUERY_POSSIBLE"

            return sql_query

        except Exception as e:
            print(f"Error generating SQL: {e}")
            return "NO_QUERY_POSSIBLE"

    def execute_and_respond(self, user_question: str) -> str:
        """Generate SQL, execute it, and provide a natural language response."""
        # Check if question is about database structure
        if any(keyword in user_question.lower() for keyword in ["what tables", "show tables", "list tables", "available data"]):
            tables = self.db.get_tables()
            return f"The database contains the following tables: {', '.join(tables)}\n\nYou can ask me questions about the data in these tables!"

        # Generate SQL query
        sql_query = self.generate_sql_query(user_question)
        print(f"\n🔍 Generated SQL: {sql_query}")

        if sql_query == "NO_QUERY_POSSIBLE":
            return self.chat_without_query(user_question)

        # Execute query
        try:
            results = self.db.execute_query(sql_query)
            print(f"📊 Query returned {len(results)} rows")
            if results:
                print(f"📝 First row: {results[0]}")

            # Generate natural language response based on results
            response = self.generate_response_from_results(
                user_question,
                sql_query,
                results
            )
            print(f"💬 AI Response: {response[:200]}...")

            return response

        except Exception as e:
            print(f"❌ Query error: {str(e)}")
            return f"I had trouble querying the database. Error: {str(e)}\n\nLet me help you without running a query."

    def generate_response_from_results(
        self,
        question: str,
        sql_query: str,
        results: List[Dict[str, Any]]
    ) -> str:
        """Generate natural language response from query results."""
        print(f"🔄 Generating response for {len(results)} results...")

        # Prepare context
        results_text = str(results[:10])  # Limit to first 10 results
        prompt = f"""User asked: {question}

I executed this SQL query:
{sql_query}

Query results (showing up to 10 rows):
{results_text}

Total rows returned: {len(results)}

Please provide a clear, natural language answer to the user's question based on these results.
Be concise and helpful."""

        try:
            print("🤖 Calling Azure OpenAI for response generation...")
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that explains database query results clearly."},
                    {"role": "user", "content": prompt}
                ],
                max_completion_tokens=600
            )

            content = response.choices[0].message.content
            print(f"✅ Response generated: {len(content) if content else 0} chars")

            # Debug: check finish_reason
            finish_reason = response.choices[0].finish_reason
            print(f"🔍 Finish reason: {finish_reason}")

            if not content or len(content.strip()) == 0:
                print("⚠️ Azure OpenAI returned empty content, using fallback")
                # Create a simple, formatted response ourselves
                if len(results) == 0:
                    return "The query returned no results."
                elif len(results) == 1:
                    return f"Found 1 record:\n{self._format_result_row(results[0])}"
                else:
                    formatted = f"Here are the {len(results)} rows from the query:\n\n"
                    for i, row in enumerate(results[:10], 1):
                        formatted += f"**Row {i}:**\n{self._format_result_row(row)}\n\n"
                    if len(results) > 10:
                        formatted += f"... and {len(results) - 10} more rows"
                    return formatted

            return content

        except Exception as e:
            print(f"❌ Error generating response: {str(e)}")
            return f"Found {len(results)} results, but had trouble formatting the response. Raw results: {results[:5]}"

    def _format_result_row(self, row: Dict[str, Any]) -> str:
        """Format a single result row nicely."""
        formatted = ""
        for key, value in row.items():
            formatted += f"  - **{key}**: {value}\n"
        return formatted

    def chat_without_query(self, user_message: str) -> str:
        """Handle general conversation without database queries."""
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        messages = [
            {"role": "system", "content": f"""You are a helpful AI assistant with access to a database.

{self.db_context}

You can help users understand the data and answer questions."""}
        ] + self.conversation_history

        try:
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                max_completion_tokens=600
            )

            assistant_message = response.choices[0].message.content

            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            return assistant_message

        except Exception as e:
            return f"Error: {str(e)}"

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []

    def close(self):
        """Close database connection."""
        self.db.disconnect()
