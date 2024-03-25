from langchain_core.pydantic_v1 import BaseModel, Field, conint

from typing import List, Dict


class FrequentActivity(BaseModel):
    activity: str
    frequency: conint(ge=0, le=2) = Field(default=0, description="活动频率，0表示低频率，1表示中等频率，2表示高频率")


class LifeSharing(BaseModel):
    frequent_activities: List[FrequentActivity] = Field(default=[], description="用户频繁进行的活动及其频率")
    activity_contexts: Dict[str, str] = Field(default={}, description="活动发生的典型情境描述")
    motivations: Dict[str, str] = Field(default={}, description="活动背后的主要动机分析")
    lifestyle_implications: str = Field(default="", description="这些活动对用户生活方式和价值观的反映")

class ViewpointScore(BaseModel):
    international_outlook: float = Field(
        0.0,
        description="世界观"
    )
    sociability: float = Field(
        0.0,
        description="社会性向"
    )
    equity: float = Field(
        0.0,
        description="平等观"
    )
    cultural_outlook: float = Field(
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
        0.0,
        description="个人生活分享"
    )
    opinions_and_views: float = Field(
        0.0,
        description="观点和看法"
    )
    emotional_expression: float = Field(
        0.0,
        description="情感表达"
    )
    others: float = Field(
        0.0,
        description="其它"
    )

