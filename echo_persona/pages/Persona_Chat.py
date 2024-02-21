import os
from langchain.chains.question_answering import load_qa_chain

from dotenv import load_dotenv
import sys
import streamlit as st
import openai, langchain, pinecone
from langchain.llms.openai import OpenAI
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

sys.path.insert(1, os.environ.get("PROJECT_PATH"))
from echo_persona.logic import utils, chains, models, prompts

# Set API keys from session state
openai_api_key = st.session_state.openai_api_key

st.subheader('Persona Q&A')

# Get OpenAI API key, Pinecone API key and environment, and source document input
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
pinecone_env = os.environ.get("PINECONE_ENV")
embed_model = "text-embedding-ada-002"
pinecone_index = "echopersona"
# with st.sidebar:
#     pinecone_index = st.text_input("Pinecone index name")

query = st.text_input("Enter your query")
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

if st.button("Submit"):
    # Validate inputs
    if not openai_api_key or not pinecone_api_key or not pinecone_env or not pinecone_index or not query:
        st.warning(f"Please upload the document and provide the missing fields.")
    else:
        try:
            # Save uploaded file temporarily to disk, load and split the file into pages, delete temp file
            pc = Pinecone(api_key=pinecone_api_key, environment=pinecone_env)
            docsearch = Pinecone.from_texts(query, embeddings, index_name=pinecone_index)
            llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
            chain = load_qa_chain(llm, chain_type="stuff")
            docs = docsearch.similarity_search(query)
            chain.invoke(input_documents=docs, question=query)

        except Exception as e:
            st.error(f"An error occurred: {e}")