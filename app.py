import streamlit as st
import os, tempfile
import pandas as pd
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import CSVLoader
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_core.prompts import MessagesPlaceholder
from langchain_experimental.agents import create_pandas_dataframe_agent
import asyncio
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="CSV AI", layout="wide")
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

def home_page():
    st.write("""Select any one feature from above sliderbox: \n
    1. Chat with CSV \n
    2. Summarize CSV \n
    3. Analyze CSV  """)

@st.cache_resource()
def retrieve_func(uploaded_file):
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        try:
           loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8", csv_args={"delimiter": ","}) 
           data = loader.load()
        except:
            loader = CSVLoader(file_path=tmp_file_path, encoding="cp1252", csv_args={"delimiter": ";"})
            data = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200, add_start_index = True)
        all_splits = text_splitter.split_documents(data)

        vectorstore = FAISS.from_documents(documents = all_splits, embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"))
        retriever = vectorstore.as_retriever(search_type = "similarity", search_kwargs = {"k": 6})
    if not uploaded_file:
        st.info("Please upload CSV documents to continue.")
        st.stop()
    return retriever, vectorstore

def chat():
    st.write("# Talk to CSV")
    reset = st.sidebar.button("Reset Chat")
    uploaded_file = st.sidebar.file_uploader("Upload your CSV here 👇:", type="csv")
    retriever, vectorstore = retrieve_func(uploaded_file)
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.5,
    )
    def format_docs(docs):
        return "\n\n".join([doc.page_content for doc in docs])
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]

    store = {}

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", """Use the following pieces of context to answer the question at the end.
                  If you don't know the answer, just say that you don't know, don't try to make up an answer. Context: {context}"""),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")      
        ]
    )
    runnable = prompt | llm
    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        return store[session_id]
    
    with_message_history = RunnableWithMessageHistory(
        runnable,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    async def chat_message():
        if prompt := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            contextt = retriever.invoke(prompt)
            context = format_docs(contextt)
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                text_chunk = ""
                async for chunk in with_message_history.astream(
                        {"context": context, "input": prompt},
                        config={"configurable": {"session_id": "abc123"}},
                    ):
                    text_chunk += chunk.content
                    message_placeholder.markdown(text_chunk)
                    #st.chat_message("assistant").write(text_chunk)
                st.session_state.messages.append({"role": "assistant", "content": text_chunk})
        if reset:
            st.session_state["messages"] = []
    asyncio.run(chat_message())

def summarize():
    st.write("# Summarize CSV")
    st.write("Upload your document here:")
    uploaded_file = st.file_uploader("Upload source document", type="csv", label_visibility="collapsed")
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1024, chunk_overlap = 100, add_start_index = True)
        try:
            loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8", csv_args={"delimiter": ","}) 
            data = loader.load()
            texts = text_splitter.split_documents(data)
        except:
            loader = CSVLoader(file_path=tmp_file_path, encoding="cp1252", csv_args={"delimiter": ";"})
            data = loader.load()
            texts = text_splitter.split_documents(data)
        os.remove(tmp_file_path)
        gen_sum = st.button("Generate Summary")
        if gen_sum:
            llm = ChatGroq(
                model="llama-3.1-8b-instant",
                temperature=0.5,
            )
            chain = load_summarize_chain(
                llm = llm,
                chain_type = "map_reduce",
                return_intermediate_steps = True
            )
            result = chain.invoke({"input_documents": texts})
            st.success(result["output_text"])

def analyze():
    st.write("# Analyze CSV")
    #st.write("This is Page 3")
    # Add functionality for Page 3
    reset = st.sidebar.button("Reset Chat")
    uploaded_file = st.sidebar.file_uploader("Upload your CSV here 👇:", type="csv")
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        df = pd.read_csv(tmp_file_path)
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.5,
        )
        agent = create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True)
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
        if prompt := st.chat_input(placeholder="What are the names of the columns?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            msg = agent.invoke({"input": prompt, "chat_history": st.session_state.messages})
            st.session_state.messages.append({"role": "assistant", "content": msg["output"]})
            st.chat_message("assistant").write(msg["output"])
        if reset:
            st.session_state["messages"] = []
def main():
    st.markdown(
        """
        <div style='text-align: center;'>
            <h1>🧠 CSV AI</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div style='text-align: center;'>
            <h4>⚡️ Interacting, Analyzing and Summarizing CSV Files!</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )
    functions = [
        "home",
        "Chat with CSV",
        "Summarize CSV",
        "Analyze CSV",
    ]
    
    #st.subheader("Select any generator👇")
    # Create a selectbox with the function names as options
    selected_function = st.selectbox("Select a functionality", functions)
    if selected_function == "home":
        home_page()
    elif selected_function == "Chat with CSV":
        chat()
    elif selected_function == "Summarize CSV":
        summarize()
    elif selected_function == "Analyze CSV":
        analyze()
    else:
        st.warning("You haven't selected any AI Functionality!!")
    

    

if __name__ == "__main__":
    main()