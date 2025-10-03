import streamlit as st
from chatbot.rag import RAGChatbot

# Page configuration
st.set_page_config(
    page_title="AI Database Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if "chatbot" not in st.session_state:
    st.session_state.chatbot = RAGChatbot()

if "messages" not in st.session_state:
    st.session_state.messages = []


def main():
    # Title and description
    st.title("🤖 AI-Powered Database Chatbot")
    st.markdown("Ask me anything about your PostgreSQL database!")

    # Sidebar
    with st.sidebar:
        st.header("📊 Database Info")

        if st.button("Show Tables"):
            tables = st.session_state.chatbot.db.get_tables()
            st.write("**Available Tables:**")
            for table in tables:
                st.write(f"- {table}")

        st.divider()

        if st.button("Clear Conversation"):
            st.session_state.messages = []
            st.session_state.chatbot.clear_history()
            st.rerun()

        st.divider()
        st.markdown("### 💡 Example Questions")
        st.markdown("""
        - What tables are available?
        - Show me the first 5 rows from [table_name]
        - How many records are in [table_name]?
        - What columns does [table_name] have?
        """)

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about your database..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.chatbot.execute_and_respond(prompt)
                st.markdown(response)

        # Add assistant response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
