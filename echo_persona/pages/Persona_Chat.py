import os
from langchain.chains.question_answering import load_qa_chain

from dotenv import load_dotenv
import sys
import streamlit as st
import openai, langchain, pinecone
from langchain.llms.openai import OpenAI
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

sys.path.insert(1, os.environ.get("PROJECT_PATH"))
from echo_persona.logic import utils, chains, models, prompts

# Set API keys from session state
openai_api_key = st.session_state.openai_api_key

st.subheader('Persona Q&A')
st.markdown(
"""
本交互模块是我们社交媒体用户画像分析系统的核心组成部分，旨在为使用者提供一个直观、高效的工具，通过对话交互形式探索特定用户的多维度画像。
该模块允许使用者深入了解用户的性格特征、心理状态、兴趣爱好等，从而获得细致丰富的用户洞见。


##### 功能概述
- **个性化查询**：使用者可以基于用户的特定维度（如心理状态、兴趣爱好）提出查询，系统将提供相关的详细信息。
- **深度探索**：针对生成的用户画像，使用者可进行深入的问询，系统能够根据之前的交互历史和用户画像数据，提供更加个性化的回答。
- **选择分析文本的数量**：允许您根据需要调整分析的深度和广度。           
- **设置生成文本的创造性**：值越低，生成的文本越倾向于保守和预测性高；值越高，文本则越新颖和多样化。

##### 使用步骤
1. **问前准备**：首先，请确定您在Analysis模块以及进行分析。
2. **提交查询**：通过输入框提交您的具体询问或探索要点，例如“该用户最感兴趣的活动是什么？”
3. **查看回答**：系统将基于LangChain框架和LLM技术分析您的查询，并提供详细且个性化的回答。

##### 最佳实践
- **明确查询目的**：在提问前，明确您希望了解的用户维度，有助于系统提供更精准的信息。
- **多角度探索**：鼓励从不同角度和维度进行用户画像的探索，以获得全面的用户理解。
"""
)

# Get OpenAI API key, Pinecone API key and environment, and source document input
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
pinecone_env = os.environ.get("PINECONE_ENV")
embed_model = "text-embedding-ada-002"
index_name = "echopersona"
# with st.sidebar:
#     pinecone_index = st.text_input("Pinecone index name")

number = st.slider('选择分析文本的数量', min_value=3, max_value=10, value=5, step=1)
temperature = st.slider('设置生成文本的创造性', min_value=0.0, max_value=1.0, value=0.5, step=0.1)
namespace = st.text_input("输入命名空间", value="hu")

if 'docsearch' not in st.session_state:
    st.session_state.docsearch = None

query = st.text_input("Enter your query")
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
keywords_chain = chains.ListStrChain(openai_api_key=openai_api_key, p_text=prompts.get_keywords_prompt())
summary_chain = chains.CommonChain(openai_api_key=openai_api_key, p_text=prompts.get_summary_prompt(), temperature=temperature)

if st.button("Submit") and namespace:
    from pinecone import Pinecone

    # initialize connection to pinecone (get API key at app.pinecone.io)
    # configure client
    pc = Pinecone(api_key=pinecone_api_key)
    # Validate inputs
    if not openai_api_key or not pinecone_api_key or not pinecone_env or not index_name or not query:
        st.warning(f"Please upload the document and provide the missing fields.")
    elif 'docsearch' not in st.session_state:
        st.warning(f"Please analyze the data first.")
    else:
        try:
            from langchain.vectorstores import Pinecone

            # Save uploaded file temporarily to disk, load and split the file into pages, delete temp file
            index = pc.Index(index_name)

            docsearch = Pinecone.from_texts([], embeddings, index_name = index_name,namespace=namespace)

            keywords_list = keywords_chain.run(query=query)
            keywords_str = ' '.join(keywords_list)
            st.write("关键词：")
            st.write(keywords_str)

            docs = docsearch.similarity_search(keywords_str, k=number)

            docs_str = "用户发言：" + '\n'.join([t.page_content for t in docs])
            q = "提问：" + query + "\n" + docs_str
            res = summary_chain.run(query=docs_str)
            print(res)
            st.write(res)
        except Exception as e:
            st.error(f"An error occurred: {e}")