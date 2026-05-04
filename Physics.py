import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time

# --- 1. 设置深色主题和页面布局 ---
st.set_page_config(
    page_title="黑客实验室: 物理与几何",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 使用 Markdown 注入一点 CSS 让界面更酷
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    h1 { color: #00FFAA; text-shadow: 2px 2px 5px #00FFAA55; }
    .stButton>button { width: 100%; border-radius: 20px; border: 1px solid #00FFAA; }
    </style>
    """, unsafe_allow_html=True)

st.title("📟 未来科学家：深色实验室")

# --- 2. 侧边栏 ---
with st.sidebar:
    st.header("🛸 实验室控制台")
    mode = st.radio("选择实验设备", ["原子碰撞模拟 (物理)", "3D 几何建模", "函数波动"])
    st.markdown("---")
    st.info("提示：在深色模式下，高饱和度的颜色（如青色、粉色）看起来最酷！")

# --- 3. 物理碰撞实验模块 ---
if mode == "原子碰撞模拟 (物理)":
    st.header("⚛️ 2D 弹性碰撞模拟")
    st.write("模拟在一个密闭容器中，两个粒子发生完全弹性碰撞的过程。")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        speed = st.slider("初始动量 (速度)", 0.1, 0.5, 0.2)
        size = st.slider("原子大小", 5, 20, 10)
        if st.button("重启实验"):
            st.rerun()

    # 物理引擎逻辑
    # 初始化位置和速度
    pos = np.array([[20.0, 50.0], [80.0, 50.0]])
    vel = np.array([[speed, 0.1], [-speed, -0.1]])
    
    frames = []
    # 模拟 50 个时间步长
    for _ in range(50):
        pos += vel
        # 边界碰撞检测 (X轴)
        for i in range(2):
            if pos[i, 0] <= 0 or pos[i, 0] >= 100: vel[i, 0] *= -1
            if pos[i, 1] <= 0 or pos[i, 1] >= 100: vel[i, 1] *= -1
        
        # 两个小球之间的碰撞检测
        dist = np.linalg.norm(pos[0] - pos[1])
        if dist < size:
            vel[0], vel[1] = vel[1], vel[0] # 动量交换
            
        frames.append(pd.DataFrame({'x': pos[:, 0], 'y': pos[:, 1], 'color': ['原子A', '原子B']}))

    # 绘制动画
    fig = go.Figure()
    # 添加初始状态
    fig.add_trace(go.Scatter(x=frames[0]['x'], y=frames[0]['y'], mode='markers',
                             marker=dict(size=size*2, color=['#00FFAA', '#FF007F'])))
    
    fig.update_layout(
        template="plotly_dark", # 核心：使用 Plotly 的深色主题
        xaxis=dict(range=[0, 100], showgrid=False),
        yaxis=dict(range=[0, 100], showgrid=False),
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    # 用动画展示
    plot_spot = st.empty()
    for frame in frames:
        fig.data[0].x = frame['x']
        fig.data[0].y = frame['y']
        plot_spot.plotly_chart(fig, use_container_width=True)
        time.sleep(0.05)

# --- 4. 3D 几何建模 (保留并优化) ---
elif mode == "3D 几何建模":
    st.header("🧊 高精度空间建模")
    res = st.slider("模型精细度", 20, 100, 60)
    
    u, v = np.mgrid[0:2*np.pi:complex(0, res), 0:np.pi:complex(0, res//2)]
    x = np.cos(u)*np.sin(v)
    y = np.sin(u)*np.sin(v)
    z = np.cos(v)
    
    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y, colorscale='Magma')])
    fig.update_layout(template="plotly_dark", height=700)
    st.plotly_chart(fig, use_container_width=True)

# --- 5. 函数波动 ---
elif mode == "函数波动":
    st.header("🌊 波动函数分析")
    t = np.linspace(0, 10, 100)
    freq = st.slider("频率", 1, 10, 2)
    y = np.sin(freq * t)
    
    fig = go.Figure(data=go.Scatter(x=t, y=y, line=dict(color='#00FFAA')))
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
