import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

st.set_page_config(page_title="未来科学家实验室", layout="wide")

st.title("🔬 15岁少年的科学探索实验室")
st.write("欢迎来到更高级的计算与可视化空间。这里你可以探索多维世界。")

# 侧边栏
st.sidebar.header("实验项目列表")
category = st.sidebar.radio("选择领域", ["立体几何 3D", "高级函数图像", "物理/数据模拟"])

# --- 模块 1：立体几何 3D ---
if category == "立体几何 3D":
    st.header("🧊 交互式立体几何")
    col1, col2 = st.columns([1, 3])
    
    with col1:
        shape = st.selectbox("选择几何体", ["球体", "甜甜圈 (环面)", "正弦波曲面"])
        color = st.color_picker("挑选颜色", "#00FFAA")
        opacity = st.slider("透明度", 0.1, 1.0, 0.8)

    # 3D 绘图算法
    fig = go.Figure()

    if shape == "球体":
        u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:30j]
        x = np.cos(u)*np.sin(v)
        y = np.sin(u)*np.sin(v)
        z = np.cos(v)
        fig.add_trace(go.Surface(x=x, y=y, z=z, colorscale=[[0, color], [1, color]], opacity=opacity))
    
    elif shape == "甜甜圈 (环面)":
        u, v = np.mgrid[0:2*np.pi:30j, 0:2*np.pi:20j]
        x = (2 + np.cos(v)) * np.cos(u)
        y = (2 + np.cos(v)) * np.sin(u)
        z = np.sin(v)
        fig.add_trace(go.Surface(x=x, y=y, z=z, colorscale=[[0, color], [1, color]], opacity=opacity))

    elif shape == "正弦波曲面":
        x, y = np.mgrid[-5:5:40j, -5:5:40j]
        z = np.sin(np.sqrt(x**2 + y**2))
        fig.add_trace(go.Surface(x=x, y=y, z=z, colorscale='Viridis'))

    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), scene_aspectmode='manual', 
                      scene_aspectratio=dict(x=1, y=1, z=1))
    col2.plotly_chart(fig, use_container_width=True)

# --- 模块 2：高级函数图像 ---
elif category == "高级函数图像":
    st.header("📈 函数解析镜")
    st.info("通过调整参数，观察函数曲线的实时变化（解析几何基础）。")
    
    formula_type = st.selectbox("选择函数类型", ["二次函数 y=ax²+bx+c", "三角正弦函数 y=a*sin(bx+c)", "三角余弦函数 y=a*cos(bx+c)"])
    
    c1, c2, c3 = st.columns(3)
    a = c1.slider("参数 a", -5.0, 5.0, 1.0)
    b = c2.slider("参数 b", -5.0, 5.0, 1.0)
    c = c3.slider("参数 c", -5.0, 5.0, 0.0)

    x = np.linspace(-10, 10, 400)
    if "二次函数" in formula_type:
        y = a * x**2 + b * x + c
        label = f"y = {a}x² + {b}x + {c}"
    elif "三角正弦函数" in formula_type:
        y = a * np.sin(b * x + c)
        label = f"y = {a}sin({b}x + {c})"
    elif "三角余弦函数" in formula_type:
        y = a * np.cos(b * x + c)
        label = f"y = {a}cos({b}x + {c})"

    df = pd.DataFrame({'x': x, 'y': y})
    st.line_chart(df.set_index('x'))
    st.latex(label) # 用专业的数学公式显示

# --- 模块 3：物理/数据模拟 ---
elif category == "物理/数据模拟":
    st.header("🎯 概率与统计实验：抛硬币大数定律")
    st.write("模拟抛掷硬币 1000 次，观察正面出现的概率如何趋近 0.5。")
    
    if st.button("开始模拟实验"):
        results = np.random.randint(0, 2, 1000)
        cumulative_heads = np.cumsum(results)
        attempts = np.arange(1, 1001)
        prob = cumulative_heads / attempts
        
        chart_data = pd.DataFrame({'次数': attempts, '正面概率': prob})
        st.line_chart(chart_data.set_index('次数'))
        st.success(f"最终模拟得到的概率: {prob[-1]:.4f}")

st.sidebar.markdown("---")
st.sidebar.write("💡 **15岁进阶建议：**")
st.sidebar.caption("尝试在代码中修改 `numpy` 的公式，看看 3D 模型会发生什么奇怪的形变！")
