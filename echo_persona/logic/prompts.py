
def get_emotional_prompt():
    text = """
    请仔细阅读以下用户在社交媒体上的发言，从下面五个维度进行打分。
    使用0到5的分数范围，其中0分代表无法获取此信息。尝试从用户的社交媒体发言、互动和表现出的行为中寻找证据支持你的评分。

    1) 快乐/喜悦（happiness）：文本中经常通过积极的描述、感叹号、以及与幸福相关的事件或情感状态的讨论来表达。
    
    2) 悲伤/哀愁（sadness）：用户可能会分享失落感、挫折或其他负面事件来表达悲伤，通常伴随着消极的词汇和叙述。
    
    3) 愤怒/生气（anger）：文本中的愤怒可能通过批评性的语言、对不公或不满意的情况的强烈反应来体现。
    
    4) 恐惧/焦虑（anxiety）：用户可能会表达对未来的担忧、不确定性或某种威胁的恐惧。
    
    5) 惊喜/震惊（shock）：通常由不预期事件的提及或反应表达，可能会用到“惊讶”或“没想到”等词汇。
    
    返回json格式的数据，包括五个特质的评分。
    用户发言如下：
    """
    return text


def get_viewpoint_prompt():
    text = """
    请根据用户在社交媒体上的发言，对以下五个方面的立场进行量化评分，使用-5到5的分数范围。-5代表立场的一个极端，5代表另一个极端，0代表中立。

    1) 社会性向 (Sociability): 从个人主义 （Individualism，-5）到 集体主义（Collectivism，5）。个人主义强调个人目标和自由，而集体主义更重视集体和社会和谐。
    2) 平等观 (Equity): 从 平等主义（Egalitarianism，-5）到 精英主义（Elitism，5）。平等主义主张机会和资源的均等分配，而精英主义认为这些应基于个人能力和成就。
    3) 文化观 (Cultural Outlook): 从 多元化（Diversity，-5）到 同质化（Uniformity，5）。多元化赞赏文化差异和表达自由，同质化倾向于文化一致性和共同的价值观。
    4) 技术态度 (Technological Stance): 从 乐观（Optimism，-5）到 悲观（Pessimism，5）。技术乐观者相信科技进步带来积极变化，技术悲观者担忧其负面影响。
    5) 生活方式 (Lifestyle): 从 自律（Discipline，-5）到 享乐（Hedonism，5）。自律强调自我控制和规律性，享乐追求个人快乐和感官满足。
    
    返回json格式的数据，包括五个特质的评分。
    用户发言如下：
    
    """
    return text


def get_life_sharing_prompt():
    text = """
    仔细阅读用户发言，请列举用户透露出的兴趣爱好，关心或喜爱的事物。返回一个列表。
    用户发言如下：
    """
    return text

def get_classify_prompt():
    text = """
    请仔细阅读以下用户在社交媒体上的发言，并分析其主要内容类别。根据以下四个类别：
    
    1) 个人生活分享：用户倾向于分享他们的日常活动、旅行经历、美食体验、兴趣爱好等，这些内容反映了用户的生活方式和个人兴趣。这些内容反映了用户的个人兴趣，主要为客观经历和生活琐事的陈述，情感色彩较少。
    2) 观点和看法：表达对于时事、政治、社会问题、文化艺术等的看法。这些发言可以揭示用户的价值观念、思想倾向和社会意识。
    3) 情感表达：用户表达自己的情感、情绪、心情等。
    4) 其它：仅当用户发言完全不知所云，无法识别，无法理解时。
    
    判断每个类别在发言中所占的比例。如果某个类别不适用，请将其比例设为0.0。请提供一个总和应为1.0的分布，。返回json格式的数据。
    用户发言如下：
    """
    return text





def get_keywords_prompt():
    text = """
    请列举出与此问题密切相关的关键词。考虑到提问的主题和上下文，关键词应该涵盖主要实体、概念以及用户可能关注的视角或态度。
    关键词应该简洁且具有代表性，能够帮助理解提问的核心焦点，利于向量数据库查询。

    请列举出相关的关键词，返回一个列表：
    """
    return text


def get_summary_prompt():
    text = """
    
    你会阅读用户发言和一段提问，你需要并基于这些发言内容，提炼出用户对此问题的观点或看法。

    请总结该用户对于问题的看法，并尽量提炼出对于这个提问的具体的观点或态度，并给出最相关的发言内容（太长的话可以概括）。
    请注意，总结应尽量简洁明了，直接反映用户的立场或观点，正面回答提问。
    
    用户发言和提问分别如下：    
    """
    return text
