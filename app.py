import streamlit as st
import requests

st.set_page_config(page_title="Nebius x NVIDIA AI Agent", page_icon="🤖")

st.title("🤖 Nebius x NVIDIA AI Agent")
with st.sidebar:
    st.header("⚙️ Hackathon Metadata")
    st.success("● API Status: Connected")
    st.info("Model: `nvidia/Nemotron-Mini-4B-Instruct`")
    st.write("Infrastructure: Nebius Cloud")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
st.caption("Powered by `nvidia/Nemotron-Mini-4B-Instruct` via Nebius Infrastructure & FastAPI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User prompt input
if prompt := st.chat_input("Ask your NVIDIA AI Agent..."):
    # Render user query
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call FastAPI server
    with st.chat_message("assistant"):
        with st.spinner("Agent is generating response..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/hackathon-agent",
                    json={"user_prompt": prompt},
                    timeout=30
                )
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("agent_response", "No response returned.")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error("Could not reach FastAPI server! Make sure Uvicorn is running in your other terminal.")