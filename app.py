import streamlit as st
from groq import Groq

st.set_page_config(page_title="Kimi-K2-Instruct Chatbot", page_icon="🤖", layout="wide")


st.markdown("""
    <style>
    .main {
        background-color: #f6f8fa;
    }
    .stTextInput > div > div > input {
        font-size: 18px;
    }
    .stTextArea textarea {
        font-size: 16px;
    }
    .stButton button {
        font-size: 18px;
        background-color: #6c757d;  /* Soft gray button */
        color: white;
    }
    .chat-bubble-user {
        background: #000000;  /* Light gray background */
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 5px;
        border: 1px solid #d6d6d6;
    }
    .chat-bubble-assistant {
        background: #000000;  /* Very light gray */
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 5px;
        border: 1px solid #dcdcdc;
    }
    </style>
""", unsafe_allow_html=True)




with st.sidebar:
    st.image("https://kimik2.net/logo.png", width=48)
    st.header("Kimi-K2-Instruct Chatbot 🤖")
    st.markdown("Powered by Moonshot AI & Groq API")
    groq_api_key = st.text_input("Groq API Key", type="password", help="Get your API key from https://console.groq.com")
    st.markdown("---")
    st.markdown("**Instructions:**")
    st.markdown("- Enter your Groq API key.")
    st.markdown("- Start chatting with Kimi!")
    st.markdown("---")
    st.markdown("[Model Info](https://console.groq.com/docs/model/moonshotai/kimi-k2-instruct)")
    st.markdown("[Contact Support](mailto:support@moonshot.cn)")


if "messages" not in st.session_state:
    st.session_state.messages = []


st.title("Kimi-K2-Instruct Chatbot")
st.markdown("Chat with Moonshot AI's Kimi-K2-Instruct model using the Groq API.")


client = None
if groq_api_key:
    try:
        client = Groq(api_key=groq_api_key)
        st.success("Connected to Groq API!")
    except Exception as e:
        st.error(f"Failed to connect to Groq API: {str(e)}")


st.markdown("#### Your Message")
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_area("Type your message here...", height=80, label_visibility="collapsed")
with col2:
    send_clicked = st.button("Send", use_container_width=True, disabled=not groq_api_key or not user_input)


if send_clicked:
    if client and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        api_messages = [
            {"role": "system", "content": "You are Kimi, an AI assistant created by Moonshot AI."},
            {"role": "user", "content": user_input}
        ]
        try:
            completion = client.chat.completions.create(
                model="moonshotai/kimi-k2-instruct",
                messages=api_messages,
                temperature=0.6,
                max_completion_tokens=8192,
                top_p=1,
                stream=True,
                stop=None
            )
            assistant_response = ""
            response_container = st.empty()
            for chunk in completion:
                chunk_content = chunk.choices[0].delta.content or ""
                assistant_response += chunk_content
                response_container.markdown(
                    f'<div class="chat-bubble-assistant"><b>Assistant:</b> {assistant_response}</div>',
                    unsafe_allow_html=True
                )
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        except Exception as e:
            st.error(f"Error getting response from model: {str(e)}")
            st.warning("""
                If the Groq API is unavailable, try the following:
                - Verify your Groq API key at https://console.groq.com.
                - Check if Kimi-K2-Instruct is supported: https://console.groq.com/docs/model/moonshotai/kimi-k2-instruct.
                - Alternatively, explore community-hosted Hugging Face Spaces:
                  - https://huggingface.co/spaces/Jhawley/Kimi-K2-Instruct
                  - https://huggingface.co/spaces/philippotiger/Kimi-K2-Instruct
                - Contact support@moonshot.cn for model availability updates.
            """)


st.markdown("#### Chat History")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(
            f'<div class="chat-bubble-user"><b>You:</b> {message["content"]}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="chat-bubble-assistant"><b>Assistant:</b> {message["content"]}</div>',
            unsafe_allow_html=True
        )


with st.expander("How to Deploy on Hugging Face Spaces"):
    st.markdown("""
    1. Create a new Space on Hugging Face (select Streamlit as SDK).
    2. Add your GROQ_API_KEY as a secret in the Space settings.
    3. Upload this `app.py` file to your Space repository.
    4. Create a `requirements.txt` with:
    ```
    streamlit
    groq
    ```
    5. Deploy the Space and interact with your chatbot.
    """)

with st.expander("How to Get a Groq API Key"):
    st.markdown("""
    - Sign up for free at https://console.groq.com (no credit card required for free tier).
    - Generate an API key in the Groq Console.
    **Note**: The Groq API offers a free tier, but usage limits apply. Check https://console.groq.com for details.
    """)

    
