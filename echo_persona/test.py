from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from logic import utils, chains, models, prompts
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
query = " "

personality_chain = chains.JsonScoreChain(openai_api_key=openai_api_key,
                                          p_text=prompts.get_emotional_prompt(),
                                          pydantic_object=models.PersonalityScore)


# 示例：新提取的兴趣爱好
a = personality_chain.run(query)

# 打印更新后的结果
print(a)

