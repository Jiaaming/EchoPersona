from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel

chain_instances = {}


class AnalysisChain:
    """

    openai_api_key = "your_openai_api_key"
    instruction = "请仔细阅读以下用户在社交媒体上的发言，并分析其主要内容类别..."
    chain = SpeechCategoryChain(openai_api_key=openai_api_key, instruction=instruction)
    result = chain.run("这里是用户发言内容")
    print("分类结果：", result)

    """

    def __new__(cls, openai_api_key: str, p_text: str, pydantic_object: BaseModel):
        # 使用pydantic_object的类名作为唯一标识符
        identifier = pydantic_object.__class__.__name__
        if identifier in chain_instances:
            # 如果已经有实例，直接返回现有实例
            return chain_instances[identifier]
        else:
            # 创建新实例，并存储到全局字典中
            instance = super(AnalysisChain, cls).__new__(cls)
            chain_instances[identifier] = instance
            return instance

    def __init__(self, openai_api_key: str, p_text: str, pydantic_object: BaseModel):
        # 防止重复初始化
        if hasattr(self, 'initialized'):
            return
        self.initialized = True

        self.llm = ChatOpenAI(openai_api_key=openai_api_key)
        self.p_text = p_text
        self.parser = JsonOutputParser(pydantic_object=pydantic_object)
        self.template = "{p_text}, 用户发言：{query}, {format_instructions}"
        self.prompt = PromptTemplate(
            template=self.template,
            input_variables=["query"],
            partial_variables={"format_instructions": self.parser.get_format_instructions(), "p_text": self.p_text}
        )
        self.chain = self.prompt | self.llm | self.parser

    def run(self, query: str):
        res = self.chain.invoke({"query": query})
        return res

