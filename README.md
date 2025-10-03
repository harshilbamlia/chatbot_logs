# AI-Powered Database Chatbot

An intelligent chatbot that connects to your PostgreSQL database and answers questions using Azure OpenAI's o4-mini model with RAG (Retrieval-Augmented Generation) capabilities.

## Features

- **Natural Language Database Queries**: Ask questions in plain English, get answers from your database
- **RAG-Enabled**: Automatically generates and executes SQL queries based on your questions
- **Interactive Web Interface**: Clean Streamlit-based chat interface
- **Database Exploration**: View tables, schemas, and data structure
- **Conversation Memory**: Maintains context throughout the conversation
- **Azure OpenAI Integration**: Powered by o4-mini model for intelligent responses

## Project Structure

```
chatbot_logs/
├── .env                      # Environment configuration (API keys, DB connection)
├── requirements.txt          # Python dependencies
├── app.py                    # Streamlit web application
├── chatbot/
│   ├── __init__.py
│   ├── bot.py               # Basic chatbot with AI integration
│   ├── database.py          # Database connection and query management
│   └── rag.py               # RAG-enabled chatbot with SQL generation
└── README.md                # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

The `.env` file is already configured with your credentials:
- Azure OpenAI API Key
- Azure OpenAI Endpoint (o4-mini deployment)
- PostgreSQL Database URL (Supabase)

### 3. Run the Application

```bash
streamlit run app.py
```

The chatbot will open in your browser at `http://localhost:8501`

## Usage

### Example Questions

- "What tables are available?"
- "Show me the first 10 rows from [table_name]"
- "How many records are in [table_name]?"
- "What columns does [table_name] have?"
- "Find all records where [condition]"

### Features in the Interface

- **Show Tables**: View all available tables in your database
- **Clear Conversation**: Reset the chat history
- **Chat Input**: Type your questions naturally

## How It Works

1. **User Input**: You ask a question in natural language
2. **SQL Generation**: The AI analyzes your database schema and generates an appropriate SQL query
3. **Query Execution**: The query is safely executed on your PostgreSQL database
4. **Response Generation**: Results are formatted into a natural language response
5. **Display**: The answer is shown in the chat interface

## Components

### `chatbot/database.py`
Manages PostgreSQL connections, executes queries, and retrieves database schema information.

### `chatbot/bot.py`
Basic chatbot with Azure OpenAI integration and conversation management.

### `chatbot/rag.py`
Advanced RAG implementation that:
- Generates SQL queries from natural language
- Executes queries safely (read-only)
- Formats results into natural language responses

### `app.py`
Streamlit web interface providing an interactive chat experience.

## Security Notes

- All SQL queries are generated as read-only (SELECT statements only)
- Database credentials are stored in `.env` (not committed to version control)
- Connection uses SSL through Supabase pooler

## Dependencies

- `openai==1.58.1` - Azure OpenAI Python SDK
- `psycopg2-binary==2.9.9` - PostgreSQL adapter
- `sqlalchemy==2.0.36` - SQL toolkit
- `python-dotenv==1.0.1` - Environment variable management
- `streamlit==1.41.1` - Web interface framework
- `pandas==2.2.3` - Data manipulation (optional)

## Troubleshooting

### Connection Issues
- Verify your database URL in `.env`
- Check network connectivity to Supabase
- Ensure your IP is allowed in Supabase settings

### API Issues
- Verify Azure OpenAI API key is correct
- Check API endpoint and deployment name
- Ensure you have quota available

### Query Errors
- The AI will fallback to general conversation if it can't generate a valid query
- Check that table names in your questions match actual table names

## Future Enhancements

- Add query result caching
- Implement user authentication
- Add visualization for query results
- Support for more complex multi-table queries
- Export conversation history
- Add query explanation mode

## License

MIT License
