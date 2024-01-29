import json
import os

from langchain_core.pydantic_v1 import BaseModel, Field
# -*- coding: utf-8 -*-

# 文件路径
file_path = '../../media_source/hu.json'

# 从文件中读取JSON数据
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

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
    weibo_texts = [weibo.get("text", "") for weibo in weibo_data]
    return weibo_texts


def filter_and_sort_categories(distribution, min_portion):
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

print(os.environ.get('OPENAI_API_KEY'))
