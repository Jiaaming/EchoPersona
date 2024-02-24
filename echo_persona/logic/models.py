from langchain_core.pydantic_v1 import BaseModel, Field


class ViewpointScore(BaseModel):
    sociability: float = Field(
        0,
        description="社会性向"
    )
    equity: float = Field(
        0,
        description="平等观"
    )
    cultural_Outlook: float = Field(
        0,
        description="文化观"
    )
    technological_stance: float = Field(
        0,
        description="技术态度"
    )
    lifestyle: float = Field(
        0,
        description="生活方式"
    )


class PersonalityScore(BaseModel):
    openness: float = Field(
        0,
        description="开放性"
    )
    conscientiousness: float = Field(
        0,
        description="责任心"
    )
    extraversion: float = Field(
        0,
        description="外向性"
    )
    agreeableness: float = Field(
        0,
        description="宜人性"
    )
    neuroticism: float = Field(
        0,
        description="情绪稳定性（神经质）"
    )


class SpeechCategoryScore(BaseModel):
    personal_life_sharing: float = Field(
        0,
        description="个人生活分享"
    )
    opinions_and_views: float = Field(
        0,
        description="观点和看法"
    )
    emotional_expression: float = Field(
        0,
        description="情感表达"
    )
    others: float = Field(
        0,
        description="其它"
    )

