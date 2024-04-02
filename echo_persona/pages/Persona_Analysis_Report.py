import streamlit as st
import json
import plotly.graph_objects as go
import re
from datetime import datetime

name = "hu"
weibo_user = "胡锡进"
classify_path = name + "_classify.json"
score_path = name + "_score.json"
time_data_path = name + "_time_data.json"
classify_map = {
    "opinions_and_views": "观点与看法",
    "personal_life_sharing": "个人生活分享",
    "emotional_expression": "情感表达",
    "other": "其它无效发言"
}
opinions_and_views_map = {
    "international_outlook": "世界观(international_outlook)",
    "sociability": "社会性向(sociability)",
    "equity": "平等观(equity)",
    "cultural_outlook": "文化观(cultural_outlook)",
    "technological_stance": "技术态度(technological_stance)",
    "lifestyle": "生活方式(lifestyle)"
}
dimension_annotations = {
    "international_outlook": ["民族主义", "世界主义"],
    "sociability": ["个人主义", "集体主义"],
    "equity": ["平等主义", "精英主义"],
    "cultural_outlook": ["文化多元", "文化同质"],
    "technological_stance": ["技术乐观", "技术悲观"],
    "lifestyle": ["追求自律", "追求享乐"]
}


# if st.button("Generate detailed Report"):
#     with open(classify_path, "r") as f:
#         data = json.load(f)
#     time_regex = r"time: (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})"
#
#     res = {}
#     for key in data.keys():
#         times_list = [re.search(time_regex, text).group(1) for text in data[key] if
#                                     re.search(time_regex, text)]
#         res[key] = times_list
#
#     with open(time_data_path, 'w') as json_file:
#         json.dump(res, json_file, ensure_ascii=False, indent=4)

with open(classify_path, "r") as f:
    data = json.load(f)

with open(time_data_path, "r") as f:
    time_data = json.load(f)

with open(score_path, "r") as f:
    score_data = json.load(f)

# 计算各个分类的发言数
category_counts = {category: len(posts) for category, posts in data.items()}
total_posts = sum(category_counts.values())
categories = list(category_counts.keys())
values = list(category_counts.values())

earliest_time = datetime.max
latest_time = datetime.min

for category in time_data:
    times = [datetime.strptime(time, "%Y-%m-%dT%H:%M:%S") for time in time_data[category]]
    if times:
        category_earliest = min(times)
        category_latest = max(times)
        earliest_time = min(earliest_time, category_earliest)
        latest_time = max(latest_time, category_latest)

time_span_days = (latest_time - earliest_time).days

# 创建饼状图
fig = go.Figure(data=[go.Pie(labels=categories, values=values)])

# 使用columns布局
col1, col2 = st.columns(2)

with col1:
    st.subheader('总体分析')
    st.write(f"共分析了 '{weibo_user}' 从\n {earliest_time} 到 {latest_time}，共 {time_span_days} 天的 {total_posts} 条发言。")
    for category, count in category_counts.items():
        st.write(f"  其中'{classify_map[category]}'占{(count / total_posts * 100):.2f}%。")

with col2:
    st.plotly_chart(fig, use_container_width=True)


st.subheader('观点与看法分析')

opinions_and_views_data = score_data["opinions_and_views"]

opinions_and_views_dimensions = ['international_outlook','sociability', 'equity', 'cultural_outlook', 'technological_stance', 'lifestyle']

# 创建箱线图 - Opinions and Views
fig_opinions_views = go.Figure()

# You only need one loop here
for idx, dimension in enumerate(opinions_and_views_dimensions):
    print(dimension)
    dimension_data = opinions_and_views_data[dimension]
    fig_opinions_views.add_trace(go.Box(y=dimension_data, name=opinions_and_views_map[dimension]))
    # Annotations for positive values
    fig_opinions_views.add_annotation(
        x=opinions_and_views_map[dimension], y=max(dimension_data), text=dimension_annotations[dimension][1],
        showarrow=False, yshift=10
    )
    # Annotations for negative values
    fig_opinions_views.add_annotation(
        x=opinions_and_views_map[dimension], y=min(dimension_data), text=dimension_annotations[dimension][0],
        showarrow=False, yshift=-10
    )

fig_opinions_views.update_layout(
    title=f"微博用户：{weibo_user} 观点与看法分析",
    yaxis_title="Scores",
    boxmode='group'
)

st.plotly_chart(fig_opinions_views, use_container_width=True)

dimension = st.selectbox('查看所有发言中观点与看法指定维度变化趋势', opinions_and_views_dimensions)
data = opinions_and_views_data[dimension]

batch_size = 5  # Assuming each batch consists of 3 messages
# Assuming hu_time_data is loaded with your timestamps data
time_stamps = time_data["opinions_and_views"]

# Generate a list of timestamps representing each batch
# Using the first timestamp of each batch as representative
representative_timestamps = time_stamps[::batch_size]

# 创建折线图
fig = go.Figure(go.Scatter(x=representative_timestamps[:len(data)], y=data, mode='lines+markers'))

# 更新布局
fig.update_layout(title=f"用户发言中'{opinions_and_views_map[dimension]}'的变化趋势",
                  xaxis_title="时间",
                  yaxis_title="评分",
                  yaxis=dict(range=[min(data)-1, max(data)+1]),
                  xaxis = dict(
                        tickmode='auto',  # 根据实际数据量调整
                        nticks=10  # 根据实际需要调整显示的刻度数量
                      ),
                  annotations=[
                      dict(
                          xref='paper',  # 使用'paper'来参照整个图表的比例
                          yref='paper',  # 同上
                          x=0,  # x位置，-0.05表示稍微在y轴的左侧
                          y=1,  # y位置，1表示在图表的顶部
                          text=dimension_annotations[dimension][0],  # 你想要显示的文本
                          showarrow=False,  # 不显示箭头
                          xanchor='right',  # 文本对齐方式
                          yanchor='bottom',  # 文本垂直对齐方式
                      ),
                      dict(
                          xref='paper',
                          yref='paper',
                          x=0,
                          y=0,  # y位置，0表示在图表的底部
                          text=dimension_annotations[dimension][1],
                          showarrow=False,
                          xanchor='right',
                          yanchor='top',
                      )
                  ]
                )

# 在Streamlit中显示折线图
st.plotly_chart(fig, use_container_width=True)


st.subheader('情感表达分析')

emotional_expression_dimensions = ["happiness", "sadness", "anger", "anxiety", "shock"]
emotional_expression_data = score_data["emotional_expression"]
emotional_expression_scores = [emotional_expression_data[dimension] for dimension in emotional_expression_dimensions]

# 创建箱线图 - Emotional Expression
fig_emotional_expression = go.Figure()
for idx, dimension in enumerate(emotional_expression_dimensions):
    fig_emotional_expression.add_trace(go.Box(y=emotional_expression_scores[idx], name=dimension))

fig_emotional_expression.update_layout(
    title=f"微博用户：{weibo_user} 情感表达分析",
    yaxis_title="Scores",
    boxmode='group'
)

st.plotly_chart(fig_emotional_expression, use_container_width=True)


dimension = st.selectbox('查看所有发言中情感表达指定维度变化趋势', emotional_expression_dimensions)
data = emotional_expression_data[dimension]

emotion_expression_k = 3  # Assuming each batch consists of 3 messages
# Assuming hu_time_data is loaded with your timestamps data
time_stamps = time_data["emotional_expression"]

# Generate a list of timestamps representing each batch
# Using the first timestamp of each batch as representative
representative_timestamps = time_stamps[::emotion_expression_k]

# 创建折线图
fig = go.Figure(go.Scatter(x=representative_timestamps[:len(data)], y=data, mode='lines+markers'))

# 更新布局
fig.update_layout(title=f"用户发言中'{dimension}'的变化趋势",
                  xaxis_title="时间",
                  yaxis_title="评分",
                  yaxis=dict(range=[min(data)-1, max(data)+1]),
                  xaxis = dict(
                        tickmode='auto',  # 根据实际数据量调整
                        nticks=10  # 根据实际需要调整显示的刻度数量
                      )
                )

# 在Streamlit中显示折线图
st.plotly_chart(fig, use_container_width=True)


st.subheader('个人生活分享分析')


life_sharing_data = score_data["personal_life_sharing"]

for tip in life_sharing_data["lifestyle_implications"]:
    st.write(tip)
activities = [activity["activity"] for activity in life_sharing_data["frequent_activities"]]
frequency = [activity["frequency"] for activity in life_sharing_data["frequent_activities"]]

colors = ['lightblue' if freq == 0 else 'mediumseagreen' if freq == 1 else 'salmon' for freq in frequency]

# 创建柱状图
fig = go.Figure(go.Bar(x=activities, y=frequency, marker_color=colors))

# 更新布局
fig.update_layout(title="活动频率柱状图",
                  xaxis=dict(
                    tickangle=-45  # 或者其他你认为合适的角度
                  ),
                  xaxis_title="活动",
                  yaxis_title="频率",
                  yaxis=dict(tickvals=[1, 2, 3], ticktext=['低频率', '中频率', '高频率']))

# 在Streamlit中显示柱状图
st.plotly_chart(fig, use_container_width=True)


# 互动性问答
interest = st.selectbox('选择你感兴趣的用户活动', activities)
# if interest == '购物':
#     st.write("购物活动分析...")
st.write("活动情境描述：" + life_sharing_data["activity_contexts"][interest])
st.write("活动动机：" + life_sharing_data["motivations"][interest])

# 生活方式和价值观的综述