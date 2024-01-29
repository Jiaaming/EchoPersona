from langchain_core.pydantic_v1 import BaseModel, Field


class PersonalityScore(BaseModel):
    openness: int = Field(
        0,
        description="开放性分数"
    )
    conscientiousness: int = Field(
        0,
        description="责任心"
    )
    extraversion: int = Field(
        0,
        description="外向性"
    )
    agreeableness: int = Field(
        0,
        description="宜人性"
    )
    neuroticism: int = Field(
        0,
        description="情绪稳定性（神经质）"
    )


class SpeechCategoryScore(BaseModel):
    personal_life_sharing: int = Field(
        0,
        description="个人生活分享"
    )
    opinions_and_views: int = Field(
        0,
        description="观点和看法"
    )
    emotional_expression: int = Field(
        0,
        description="情感表达"
    )
    others: int = Field(
        0,
        description="其它"
    )

