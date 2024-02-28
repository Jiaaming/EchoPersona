import json
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
    st.session_state.HOBBIES = {}

if 'PERSONALITIES' not in st.session_state:
    st.session_state.PERSONALITIES = {}
# Set API keys from session state
openai_api_key = st.session_state.openai_api_key
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
pinecone_env = os.environ.get("PINECONE_ENV")
index_name = "echopersona"
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Streamlit app
st.subheader('Weibo User analysis')
source_doc = st.file_uploader("Upload Source Document", type="json")
namespace = st.text_input("Enter namespace")


classify_chain = chains.JsonScoreChain(openai_api_key=openai_api_key,
                                       p_text=prompts.get_classify_prompt(),
                                       pydantic_object=models.SpeechCategoryScore)
emotional_expression_chain = chains.JsonScoreChain(openai_api_key=openai_api_key,
                                                   p_text=prompts.get_emotional_prompt(),
                                                   pydantic_object=models.EmotionalScore)
life_sharing_chain = chains.ListStrChain(openai_api_key=openai_api_key, p_text=prompts.get_life_sharing_prompt())
opinions_and_views_chain = chains.JsonScoreChain(openai_api_key=openai_api_key,
                                                 p_text=prompts.get_viewpoint_prompt(),
                                                 pydantic_object=models.ViewpointScore)
opinions_and_views = []
personal_life_sharing = []
emotional_expression = []



def store_text(category: str, text: str):
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
        opinions_and_views.append(text)
    elif category == 'personal_life_sharing':
        """
        return a list of hobbies
        """
        personal_life_sharing.append(text)
    # 添加其他分类对应的chain
    elif category == 'emotional_expression':
        emotional_expression.append(text)

# If the 'Summarize' button is clicked

def analyze_category(category, text_list, chain_function, result_sum, n):
    """
    分析特定类别的文本列表，并更新结果汇总。

    :param category: 分析的类别名称
    :param text_list: 待分析的文本列表
    :param chain_function: 分析函数
    :param result_sum: 结果汇总字典
    """
    print(f"Analyzing {category}...")
    combined_texts = [" ".join(text_list[i:i + n]) for i in range(0, len(text_list), n)]

    for combined_text in combined_texts:
        result = chain_function.run(combined_text)
        print(result)  # 假设每个chain_function的输出是一个字典
        if isinstance(result, list):
            for keyword in result:
                result_sum.append(keyword)
        else:
            for key, value in result.items():
                result_sum[key].append(value)  # 对于非列表类型的结果处理

n = st.slider('k value', min_value=1, max_value=40, value=20, step=1)

if st.button("Classify first!") and namespace:
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


                # Pinecone.from_texts(weibo_texts, embeddings, index_name=index_name, namespace=namespace)
                # for i, text in enumerate(weibo_texts[:5]):  # 假设只展示前5条微博
                #     # st.write(text)
                #     # classify the text
                #     print(i, text)
                #
                #     result = utils.filter_and_sort_categories(classify_chain.run(text), min_portion=0.25)
                #     # result: {'opinions_and_views': 75, 'others': 25}
                #     for category, score in result:
                #         print(f"{category}: {score}")
                #         st.write(f"{category}: {score}")
                #         # Start with the highest score, analyze the text
                #         store_text(category, text)
                # # st.success(summary)
                # utils.save_to_json(opinions_and_views, personal_life_sharing, emotional_expression)
                st.write("Finished classify! Now let's analyze user text")

        except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                # 或者
                st.error(f"An error occurred: {e.__class__.__name__}: {e}")

if st.button("Let's Analyze!"):
    try:
        with st.spinner('Please wait...'):
            # 读取分析结果
            with open("analysis_result.json", "r") as f:
                texts = json.load(f)

            results_sum = {
                "opinions_and_views": {
                    "sociability": [],
                    "equity": [],
                    "cultural_Outlook": [],
                    "technological_stance": [],
                    "lifestyle": []
                },
                "personal_life_sharing": [],
                "emotional_expression": {
                    "happiness": [],
                    "sadness": [],
                    "anger": [],
                    "anxiety": [],
                    "shock": []
                }
            }
            print("analyzing~~~")

            # 分析每个类别
            analyze_category("opinions_and_views", texts["opinions_and_views"],
                             opinions_and_views_chain, results_sum["opinions_and_views"], n)
            analyze_category("personal_life_sharing", texts["personal_life_sharing"],
                             life_sharing_chain, results_sum["personal_life_sharing"], n)
            analyze_category("emotional_expression", texts["emotional_expression"],
                             emotional_expression_chain, results_sum["emotional_expression"], n)

            # 结果处理，例如输出或保存
            print(results_sum)
            file_path = "report_raw_data.json"
            with open(file_path, 'w') as json_file:
                json.dump(results_sum, json_file, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"An error occurred: {e}")
