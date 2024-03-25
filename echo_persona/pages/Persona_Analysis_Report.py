import streamlit as st
import json
import plotly.graph_objects as go


file_path = "hu_report_raw_data.json"

with open(file_path, "r") as f:
    test_data_updated = json.load(f)

st.subheader('Part1: 观点与看法分析')
with open(file_path, "r") as f:
    test_data_updated = json.load(f)
opinions_and_views_data = test_data_updated["opinions_and_views"]
opinions_and_views_dimensions = ['international_outlook','sociability', 'equity', 'cultural_outlook', 'technological_stance', 'lifestyle']

# 创建箱线图 - Opinions and Views
fig_opinions_views = go.Figure()

dimension_annotations = {
    "international_outlook": ["民族主义", "世界主义"],
    "sociability": ["个人主义", "集体主义"],
    "equity": ["平等主义", "精英主义"],
    "cultural_outlook": ["文化多元", "文化同质"],
    "technological_stance": ["技术乐观", "技术悲观"],
    "lifestyle": ["追求自律", "追求享乐"]
}

# You only need one loop here
for idx, dimension in enumerate(opinions_and_views_dimensions):
    dimension_data = opinions_and_views_data[dimension]
    fig_opinions_views.add_trace(go.Box(y=dimension_data, name=dimension))
    # Annotations for positive values
    fig_opinions_views.add_annotation(
        x=dimension, y=max(dimension_data), text=dimension_annotations[dimension][1],
        showarrow=False, yshift=10
    )
    # Annotations for negative values
    fig_opinions_views.add_annotation(
        x=dimension, y=min(dimension_data), text=dimension_annotations[dimension][0],
        showarrow=False, yshift=-10
    )

fig_opinions_views.update_layout(
    title="微博用户：胡锡进 观点与看法分析",
    yaxis_title="Scores",
    boxmode='group'
)

st.plotly_chart(fig_opinions_views, use_container_width=True)

st.subheader('Part2: 情感表达分析')

emotional_expression_dimensions = ["happiness", "sadness", "anger", "anxiety", "shock"]
emotional_expression_data = test_data_updated["emotional_expression"]
emotional_expression_scores = [emotional_expression_data[dimension] for dimension in emotional_expression_dimensions]

# 创建箱线图 - Emotional Expression
fig_emotional_expression = go.Figure()
for idx, dimension in enumerate(emotional_expression_dimensions):
    fig_emotional_expression.add_trace(go.Box(y=emotional_expression_scores[idx], name=dimension))

fig_emotional_expression.update_layout(
    title="Emotional Expression Scores",
    yaxis_title="Scores",
    boxmode='group'
)

st.plotly_chart(fig_emotional_expression, use_container_width=True)

st.subheader('Part3: 个人生活分享分析')
st.write("总结：用户关注社会问题，注重健康保健，喜欢观赏自然现象，展现出对生活多样性和社会公正的关注，以及对健康和自然的尊重。")

life_sharing_data = test_data_updated["personal_life_sharing"]
activities = [activity["activity"] for activity in life_sharing_data["frequent_activities"]]
frequency = [activity["frequency"] for activity in life_sharing_data["frequent_activities"]]

colors = ['lightblue' if freq == 0 else 'mediumseagreen' if freq == 1 else 'salmon' for freq in frequency]

# 创建柱状图
fig = go.Figure(go.Bar(x=activities, y=frequency, marker_color=colors))

# 更新布局
fig.update_layout(title="活动频率柱状图",
                  xaxis_title="活动",
                  yaxis_title="频率",
                  yaxis=dict(tickvals=[0, 1, 2], ticktext=['低频率', '中频率', '高频率']))

# 在Streamlit中显示柱状图
st.plotly_chart(fig, use_container_width=True)


# 互动性问答
interest = st.selectbox('选择你感兴趣的用户活动', activities)
# if interest == '购物':
#     st.write("购物活动分析...")
st.write("活动情境描述：" + life_sharing_data["activity_contexts"][interest])
st.write("活动动机：" + life_sharing_data["motivations"][interest])

# 生活方式和价值观的综述