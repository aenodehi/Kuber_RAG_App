import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader, DirectoryLoader
import openai
import time
from dotenv import load_dotenv

load_dotenv()

os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
os.environ['HF_TOKEN'] = os.getenv("HF_TOKEN")

from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Initialize the model
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

# Prompts
explorer_prompt = ChatPromptTemplate.from_template("""
    Explore the topic based on the provided context.
    Provide a detailed and comprehensive explanation to the query.
    <context>
    {context}
    <context>
    Question: {input}
    """)

evaluator_prompt = ChatPromptTemplate.from_template("""
    Critically evaluate the provided context and the query.
    Provide an analysis that highlights strengths, weaknesses, or key considerations.
    <context>
    {context}
    <context>
    Question: {input}
    """)

summary_prompt = ChatPromptTemplate.from_template("""
    Summarize the provided context and answer the query with a concise summary.
    Focus on key points and insights.
    <context>
    {context}
    <context>
    Question: {input}
    """)

# Vector embedding setup
def create_vector_embedding():
    """Creates vector embeddings and stores them in session state."""
    if "vectors" not in st.session_state:
        st.session_state.embeddings = embeddings
        st.session_state.loader = DirectoryLoader("./maintenance") 
        st.session_state.docs = st.session_state.loader.load()
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(
            st.session_state.docs[:50]
        )
        st.session_state.vectors = FAISS.from_documents(
            st.session_state.final_documents, st.session_state.embeddings
        )

# Streamlit interface
st.set_page_config(page_title="Predictive Maintenance (Dual Agent)", layout="wide")

st.title("Predictive Maintenance (Dual Agent)")
st.markdown("""
Analyze anomalies and receive insights from three different perspectives:
1. **Explorer Agent**: Provides a broad, exploratory response.
2. **Evaluator Agent**: Offers critical analysis and evaluation.
3. **Summary Agent**: Summarizes the key points and insights.
""")

st.sidebar.title("Settings")
model_name = st.sidebar.selectbox("Select Model", ["all-MiniLM-L6-v2", "other-model"])
chunk_size = st.sidebar.slider("Chunk Size", 500, 2000, 1000)

st.sidebar.image(
    "/home/ali/Projects/LLMs/RAG_Document_QA_GROQ_API_LLama3_20241102/images/02.png",
    caption="Predictive Maintenance",
    use_container_width=True
)

col1, col2 = st.columns(2)

with col1:
    user_prompt = st.text_input("Enter Anomaly Prediction Query")
    if st.button("Document Embedding"):
        with st.spinner('Creating vector embeddings...'):
            create_vector_embedding()
            st.success("Vector Database is ready!")

# Define the tabs for switching between different agent responses
tabs = ["Explorer Agent", "Evaluator Agent", "Summary Agent"]
selected_tab = st.selectbox("Select an Agent", tabs)

if user_prompt:
    if "vectors" not in st.session_state:
        st.warning("Please generate document embeddings first!")
    else:
        retriever = st.session_state.vectors.as_retriever()

        explorer_chain = create_stuff_documents_chain(llm, explorer_prompt)
        explorer_retrieval_chain = create_retrieval_chain(retriever, explorer_chain)

        evaluator_chain = create_stuff_documents_chain(llm, evaluator_prompt)
        evaluator_retrieval_chain = create_retrieval_chain(retriever, evaluator_chain)

        summary_chain = create_stuff_documents_chain(llm, summary_prompt)
        summary_retrieval_chain = create_retrieval_chain(retriever, summary_chain)

        start = time.process_time()

        try:
            explorer_response = explorer_retrieval_chain.invoke({'input': user_prompt})
            evaluator_response = evaluator_retrieval_chain.invoke({'input': user_prompt})
            summary_response = summary_retrieval_chain.invoke({'input': user_prompt})
            response_time = time.process_time() - start

            explorer_answer = explorer_response.get('answer', "No response generated.")
            evaluator_answer = evaluator_response.get('answer', "No response generated.")
            summary_answer = summary_response.get('answer', "No response generated.")

            if selected_tab == "Explorer Agent":
                st.subheader("Explorer Agent Response")
                st.write(explorer_answer)
            elif selected_tab == "Evaluator Agent":
                st.subheader("Evaluator Agent Response")
                st.write(evaluator_answer)
            elif selected_tab == "Summary Agent":
                st.subheader("Summary Agent Response")
                st.write(summary_answer)

            st.metric(label="Response Time", value=f"{response_time:.2f} seconds")

        except Exception as e:
            st.error(f"Error: {e}")

        with st.expander("Document Similarity Search"):
            st.subheader("Similar Documents")
            for i, doc in enumerate(explorer_response.get('context', [])):
                st.write(f"Document {i + 1}:")
                st.write(doc.page_content)
                st.write('------------------------')

# File upload handling
uploaded_file = st.file_uploader("Upload a document for analysis", type=["pdf", "txt"])
if uploaded_file:
    file_path = os.path.join("./uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.session_state.loader = PyPDFDirectoryLoader("./uploads")
    st.success("File uploaded and ready for processing!")
