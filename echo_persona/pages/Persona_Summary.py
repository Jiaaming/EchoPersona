import os
from dotenv import load_dotenv
import sys
import streamlit as st
import openai, langchain, pinecone
from langchain.llms.openai import OpenAI
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone

sys.path.insert(1, os.environ.get("PROJECT_PATH"))

from echo_persona.logic import utils, chains, models, prompts


if 'openai_api_key' not in st.session_state:
	st.session_state.openai_api_key = os.environ.get("OPENAI_API_KEY")

if 'CATEGORIES' not in st.session_state:
    st.session_state.CATEGORIES = {}

if 'HOBBIES' not in st.session_state:
    st.session_state.HOBBIES = []

if 'PERSONALITIES' not in st.session_state:
    st.session_state.PERSONALITIES = {}
# Set API keys from session state
openai_api_key = st.session_state.openai_api_key
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Streamlit app
st.subheader('Weibo User analysis')
source_doc = st.file_uploader("Upload Source Document", type="json")


classify_chain = chains.JsonScoreChain(openai_api_key=openai_api_key,
                                       p_text=prompts.get_classify_prompt(),
                                       pydantic_object=models.SpeechCategoryScore)
personality_chain = chains.JsonScoreChain(openai_api_key=openai_api_key,
                                          p_text=prompts.get_personality_prompt(),
                                          pydantic_object=models.PersonalityScore)
hobby_chain = chains.ListStrChain(openai_api_key=openai_api_key, p_text=prompts.get_hobby_prompt())

def analysis_and_report(category: str, text: str, score: int, i: int):
    # 根据分类结果选择相应的分析chain
    # 这里仅为示例，您需要根据实际情况实现
    if category == 'opinions_and_views':
        """
        return a dict like:
            {
            openness: int,
            conscientiousness: int,
            extraversion: int,
            agreeableness: int, 
            neuroticism: int
            }
        """
        report = personality_chain.run(text)
        print(report)
        res = {'res': report, 'score': score}
        st.session_state.PERSONALITIES[i] = res
        return None
    elif category == 'personal_life_sharing':
        """
        return a list of hobbies
        """
        hobby_list = hobby_chain.run(text)
        st.session_state.HOBBIES[i] = hobby_list
        return None
    # 添加其他分类对应的chain
    else:
        return None

pinecone_index = st.text_input("Pinecone index name")
# If the 'Summarize' button is clicked
if pinecone_index and st.button("Let Analyze!"):
    # Validate inputs
    if not openai_api_key:
        st.error("Please provide the missing API keys in Settings.")
    elif not source_doc:
        st.error("Please provide the source document.")
    else:
        try:
            with st.spinner('Please wait...'):
                # 使用read_json_file函数读取上传的JSON文件
                json_data = utils.read_json_file(source_doc)

                # 提取用户信息
                user_info = utils.extract_user_info(json_data.get("user", {}))
                # st.write("User Info:", user_info)

                # 提取微博信息
                weibo_texts = utils.extract_weibo_texts(json_data.get("weibo", []))

                #weibo_texts = ["今天上午踢了足球，下午打了篮球，晚上看了书，真开心", "2"]
                for i, text in enumerate(weibo_texts[:5]):  # 假设只展示前5条微博
                    # st.write(text)
                    # classify the text
                    print(i, text)
                    result = utils.filter_and_sort_categories(classify_chain.run(text), min_portion=0.25)
                    # result: {'opinions_and_views': 75, 'others': 25}
                    st.session_state.CATEGORIES[i] = result
                    for category, score in result:
                        print(f"{category}: {score} %")
                        st.write(f"{category}: {score} %")
                        # Start with the highest score, analyze the text
                        analysis_and_report(category, text, score, i)
                # st.success(summary)
                utils.save_to_json(st.session_state.CATEGORIES, st.session_state.HOBBIES, st.session_state.PERSONALITIES)
        except Exception as e:
            utils.save_to_json(st.session_state.CATEGORIES, st.session_state.HOBBIES, st.session_state.PERSONALITIES)
            st.error(f"An error occurred: {str(e)}")
            # 或者
            st.error(f"An error occurred: {e.__class__.__name__}: {e}")
