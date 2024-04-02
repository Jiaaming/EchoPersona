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
import re

sys.path.insert(1, os.environ.get("PROJECT_PATH"))

from echo_persona.logic import utils, chains, models, prompts



if 'openai_api_key' not in st.session_state:
	st.session_state.openai_api_key = os.environ.get("OPENAI_API_KEY")

# Set API keys from session state
openai_api_key = st.session_state.openai_api_key
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
pinecone_env = os.environ.get("PINECONE_ENV")
index_name = "echopersona"
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Streamlit app
st.subheader('用户画像分析')
source_doc = st.file_uploader("上传微博json数据", type="json")
namespace = st.text_input("输入命名空间（可选）")


time_data_path = namespace + "_time_data.json"
classify_path = namespace + "_classify.json"
score_path = namespace + "_score.json"

opinions_and_views = []
personal_life_sharing = []
emotional_expression = []

def is_format(res):
    if isinstance(res, dict) and all(isinstance(value, (int, float)) for value in res.values()):
        return True
    return False

def store_text(category: str, text: str):
    # 根据分类结果选择相应的分析chain
    if category == 'opinions_and_views':

        opinions_and_views.append(text)
    elif category == 'personal_life_sharing':

        personal_life_sharing.append(text)
    # 添加其他分类对应的chain
    elif category == 'emotional_expression':
        emotional_expression.append(text)

# If the 'Summarize' button is clicked

def analyze_category_life_sharing(category, texts, chain_function, result_sum, n):
    """
    分析特定类别的文本列表，并更新结果汇总。

    :param category: 分析的类别名称
    :param text_list: 待分析的文本列表
    :param chain_function: 分析函数
    :param result_sum: 结果汇总字典
    """
    print(f"Analyzing {category}...")
    text_list = texts[category]

    combined_texts = [" ".join(text_list[i:i + n]) for i in range(0, len(text_list), n)]

    for combined_text in combined_texts:
        results = chain_function.run(combined_text)
        for key, value in results.items():
            if isinstance(value, list):
                result_sum[category][key] += value  # 对于非列表类型的结果处理
            elif isinstance(value, str):
                result_sum[category][key].append(value)
            else:
                for activity, context in value.items():
                    result_sum[category][key][activity] = context

def analyze_category(category, texts, chain_function, result_sum, batch_size):
    """
    分析特定类别的文本列表，并更新结果汇总。

    :param category: 分析的类别名称
    :param text_list: 待分析的文本列表
    :param chain_function: 分析函数
    :param result_sum: 结果汇总字典
    """
    print(f"Analyzing {category}...")
    text_list = texts[category]
    combined_texts = [" ".join(text_list[i:i + batch_size]) for i in range(0, len(text_list), batch_size)]

    for combined_text in combined_texts:
        result = chain_function.run(combined_text)
        print(result)  # 假设每个chain_function的输出是一个字典
        for key, value in result.items():
            result_sum[category][key].append(value)  # 对于非列表类型的结果处理


classify_chain = chains.JsonChain(openai_api_key=openai_api_key,
                                  p_text=prompts.get_classify_prompt(),
                                  pydantic_object=models.SpeechCategoryScore)
emotional_expression_chain = chains.JsonChain(openai_api_key=openai_api_key,
                                              p_text=prompts.get_emotional_prompt(),
                                              pydantic_object=models.EmotionalScore)
life_sharing_chain = chains.JsonChain(openai_api_key=openai_api_key,
                                      p_text=prompts.get_life_sharing_prompt(),
                                      pydantic_object=models.LifeSharing)

if st.button("存入向量数据库 (可选)") and namespace:
    try:
        with st.spinner('Please wait...'):
            # 使用read_json_file函数读取上传的JSON文件
            json_data = utils.read_json_file(source_doc)

            # 提取用户信息
            user_info = utils.extract_user_info(json_data.get("user", {}))
            # st.write("User Info:", user_info)

            # 提取微博信息
            weibo_texts = utils.extract_weibo_texts(json_data.get("weibo", []))

            Pinecone.from_texts(weibo_texts, embeddings, index_name=index_name, namespace=namespace)

    except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                # 或者


if st.button("文本分类"):
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

                start = 0
                # end = 200

                for i, text in enumerate(weibo_texts):  # 假设只展示前5条微博
                    # st.write(text)
                    # classify the text
                    st.write("第" + str(i+start) + "条：" + text[:60] + "...")
                    print("第" + str(i+start) + "条：" + text[:60])
                    res = classify_chain.run(text)
                    print(res)
                    if (not is_format(res)):
                        continue
                    result = utils.filter_and_sort_categories(res, min_portion=0.25)
                    # result: {'opinions_and_views': 75, 'others': 25}
                    for category, score in result:
                        print(f"{category}: {score}")
                        st.write(f"{category}: {score}")
                        # Start with the highest score, analyze the text
                        store_text(category, text)
                # st.success(summary)
                utils.save_to_json(opinions_and_views, personal_life_sharing, emotional_expression, classify_path)


                st.write("Finished classify! Now let's analyze user text")

        except Exception as e:
                utils.save_to_json(opinions_and_views, personal_life_sharing, emotional_expression, classify_path)

                st.error(f"An error occurred: {str(e)}")
                # 或者

k_opinions_and_views = st.slider('k value: 观点与看法 (opinions_and_views)的batch size', min_value=1, max_value=40, value=20, step=1)
k_emotional_expression = st.slider('k value: 情感表达 (emotional_expression)的batch size', min_value=1, max_value=40, value=20, step=1)
k_life_sharing = st.slider('k value: 个人生活分享 (personal_life_sharing)的batch size', min_value=10, max_value=80, value=40, step=1)

temperature_life_sharing = st.slider('设置个人生活分享分析的创造性', min_value=0.0, max_value=1.0, value=0.5, step=0.1)

opinions_and_views_chain = chains.JsonChain(openai_api_key=openai_api_key,
                                            p_text=prompts.get_viewpoint_prompt(),
                                            pydantic_object=models.ViewpointScore,temperature=temperature_life_sharing)
if st.button("分析"):
    try:
        with st.spinner('Please wait...'):
            # 读取分析结果
            with open(classify_path, "r") as f:
                texts = json.load(f)

            results_sum = {
                "opinions_and_views": {
                    "international_outlook": [],
                    "sociability": [],
                    "equity": [],
                    "cultural_outlook": [],
                    "technological_stance": [],
                    "lifestyle": []
                },
                "personal_life_sharing": {
                    "frequent_activities": [],
                    "activity_contexts": {},
                    "motivations": {},
                    "lifestyle_implications": []
                },
                "emotional_expression": {
                    "happiness": [],
                    "sadness": [],
                    "anger": [],
                    "anxiety": [],
                    "shock": []
                }
            }
            print("analyzing~~~")
            analyze_category_life_sharing("personal_life_sharing", texts,
                             life_sharing_chain, results_sum, k_life_sharing)
            # 分析每个类别
            analyze_category("opinions_and_views", texts,
                             opinions_and_views_chain, results_sum, k_opinions_and_views)
            #
            analyze_category("emotional_expression", texts,
                             emotional_expression_chain, results_sum, k_emotional_expression)
            # print(texts["personal_life_sharing"])

            with open(classify_path, "r") as f:
                data = json.load(f)
            time_regex = r"time: (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})"

            res = {}
            for key in data.keys():
                times_list = [re.search(time_regex, text).group(1) for text in data[key] if
                              re.search(time_regex, text)]
                res[key] = times_list

            with open(time_data_path, 'w') as json_file:
                json.dump(res, json_file, ensure_ascii=False, indent=4)

            # 结果处理，例如输出或保存
            print(results_sum)
            with open(score_path, 'w') as json_file:
                json.dump(results_sum, json_file, ensure_ascii=False, indent=4)
    except Exception as e:
        with open(score_path, 'w') as json_file:
            json.dump(results_sum, json_file, ensure_ascii=False, indent=4)
        st.error(f"An error occurred: {e}")

# if st.button("Generate detailed Report"):
#     with open("zoufan_classify.json", "r") as f:
#         data = json.load(f)
#     time_regex = r"time: (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})"
#
#     res = {}
#     for key in data.keys():
#         times_list = [re.search(time_regex, text).group(1) for text in data[key] if
#                                     re.search(time_regex, text)]
#         res[key] = times_list
#
#     print("okk")
#     with open("zoufan_time_data.json", 'w') as json_file:
#         json.dump(res, json_file, ensure_ascii=False, indent=4)