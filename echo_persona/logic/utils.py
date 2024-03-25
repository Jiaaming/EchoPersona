import json
import os

from langchain_core.pydantic_v1 import BaseModel, Field
# -*- coding: utf-8 -*-

# 文件路径

# 从文件中读取JSON数据
def read_json_file(file_obj):
    """读取并解析上传的JSON文件内容

    Args:
        file_obj (UploadedFile): Streamlit上传的文件对象

    Returns:
        dict: 解析后的JSON数据
    """
    # 确保文件对象不为空
    if file_obj is not None:
        return json.load(file_obj)
    else:
        return None

# 提取用户信息
def extract_user_info(user_data):
    user_info = {
        "id": user_data.get("id", ""),
        "screen_name": user_data.get("screen_name", ""),
        "gender": user_data.get("gender", ""),
        "description": user_data.get("description", ""),
        "followers_count": user_data.get("followers_count", 0)
    }
    return user_info

# 提取微博信息
def extract_weibo_texts(weibo_data):
    # "created_at": "2024-01-11T20:36:22",
    weibo_texts = ["text: "+ weibo.get("text", "") + " time: " + weibo.get("created_at", "") for weibo in weibo_data]
    return weibo_texts


def filter_and_sort_categories(distribution, min_portion=25):
    """
    过滤并排序分类

    Args:
    - distribution (dict): 分类及其对应的百分比
    - min_portion (int): 最小百分比阈值

    Returns:
    - list of tuples: 按百分比从大到小排列且值大于等于min_portion的分类
    """
    # 过滤出大于等于min_portion的项
    filtered = {k: v for k, v in distribution.items() if v >= min_portion}

    # 按值从大到小排序
    sorted_filtered = sorted(filtered.items(), key=lambda x: x[1], reverse=True)

    return sorted_filtered



# 定义保存为JSON文件的函数
def save_to_json(opinions_and_views, personal_life_sharing, emotional_expression, file_path="zoufan_analysis_result.json"):

    data = {
        "opinions_and_views": opinions_and_views,
        "personal_life_sharing": personal_life_sharing,
        "emotional_expression": emotional_expression
    }
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
