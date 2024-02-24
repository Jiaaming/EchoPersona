from langchain_core.output_parsers import JsonOutputParser, CommaSeparatedListOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.output_parsers import StrOutputParser


class JsonScoreChain:
    """

    openai_api_key = "your_openai_api_key"
    instruction = "请仔细阅读以下用户在社交媒体上的发言，并分析其主要内容类别..."
    chain = SpeechCategoryChain(openai_api_key=openai_api_key, instruction=instruction)
    result = chain.run("这里是用户发言内容")
    print("分类结果：", result)

    """

    def __init__(self, openai_api_key: str, p_text: str, pydantic_object: BaseModel, temperature: float = 0.0):
        self.llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=temperature)
        self.p_text = p_text
        self.parser = JsonOutputParser(pydantic_object=pydantic_object)
        self.template = "{p_text}, {query}, {format_instructions}"
        self.prompt = PromptTemplate(
            template=self.template,
            input_variables=["query"],
            partial_variables={"format_instructions": self.parser.get_format_instructions(), "p_text": self.p_text}
        )
        self.chain = self.prompt | self.llm | self.parser

    def run(self, query: str):
        res = self.chain.invoke({"query": query})
        return res


class ListStrChain:
    def __init__(self, openai_api_key: str, p_text: str, temperature: float = 0.0):
        self.llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=temperature)
        self.p_text = p_text
        self.parser = CommaSeparatedListOutputParser()
        self.template = "{p_text} {query}, {format_instructions}"
        self.prompt = PromptTemplate(
            template=self.template,
            input_variables=["query"],
            partial_variables={"format_instructions": self.parser.get_format_instructions(), "p_text": self.p_text}
        )
        self.chain = self.prompt | self.llm | self.parser

    def run(self, query: str):
        res = self.chain.invoke({"query": query})
        return res


class CommonChain:
    def __init__(self, openai_api_key: str, p_text: str, temperature: float = 0.0):
        self.llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=temperature)
        self.p_text = p_text
        self.parser = StrOutputParser()
        self.template = "{p_text} {query}"
        self.prompt = PromptTemplate(
            template=self.template,
            input_variables=["query"],
            partial_variables={"p_text": self.p_text}
        )
        self.chain = self.prompt | self.llm | self.parser

    def run(self, query: str):
        res = self.chain.invoke({"query": query})
        return res
