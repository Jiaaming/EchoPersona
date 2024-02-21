from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from logic import utils, chains, models, prompts
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
query = "没有一个可驻扎的地方，到每一个地方那儿的人都对我说：你得走。就连回家妈妈都说：你不能留在这儿。每一刻看着那些离去的期限我就觉得孤立无依。 "

personality_chain = chains.JsonScoreChain(openai_api_key=openai_api_key,
                                       p_text=prompts.get_personality_prompt(),
                                       pydantic_object=models.PersonalityScore)


# 示例：新提取的兴趣爱好
a = personality_chain.run(query)

# 打印更新后的结果
print(a)

