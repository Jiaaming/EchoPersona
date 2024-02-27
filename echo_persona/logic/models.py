from langchain_core.pydantic_v1 import BaseModel, Field


class ViewpointScore(BaseModel):
    sociability: float = Field(
        0.0,
        description="社会性向"
    )
    equity: float = Field(
        0.0,
        description="平等观"
    )
    cultural_Outlook: float = Field(
        0.0,
        description="文化观"
    )
    technological_stance: float = Field(
        0.0,
        description="技术态度"
    )
    lifestyle: float = Field(
        0.0,
        description="生活方式"
    )


class EmotionalScore(BaseModel):
    happiness: float = Field(
        0.0,
        description="快乐/喜悦"
    )
    sadness: float = Field(
        0.0,
        description="悲伤/哀愁"
    )
    anger: float = Field(
        0.0,
        description="愤怒/生气"
    )
    anxiety: float = Field(
        0.0,
        description="恐惧/焦虑"
    )
    shock: float = Field(
        0.0,
        description="惊喜/震惊"
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

