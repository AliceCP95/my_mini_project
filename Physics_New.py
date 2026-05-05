import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# --- 1. 设置页面布局 ---
st.set_page_config(
    page_title="黑客实验室: 物理与几何",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 注入 CSS
st.markdown("""
    <style>
    .main { background-color: #00FFAA; }
    h1 { color: #00FFAA; text-shadow: 2px 2px 5px #00FFAA55; }

    </style>
    """, unsafe_allow_html=True)

st.title("📟 未来科学家：深色实验室")

# --- 2. 侧边栏 ---
with st.sidebar:
    st.header("🛸 实验室控制台")
    mode = st.radio("选择实验设备", ["原子碰撞模拟 (物理)", "3D 几何建模"])
    st.markdown("---")
    if st.button("🔴 重置实验状态"):
        for key in ['pos', 'vel']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# --- 3. 物理碰撞实验模块 ---
if mode == "原子碰撞模拟 (物理)":
    st.header("⚛️ 2D 弹性碰撞模拟")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        speed_val = st.slider("初始速度", 0.5, 3.0, 1.5)
        size = st.slider("原子大小", 10, 30, 20)

         # --- 这里是新加的重启按钮 ---
        if st.button("🔄 重启实验"):
            if 'pos' in st.session_state:
                del st.session_state['pos']
            if 'vel' in st.session_state:
                del st.session_state['vel']
            st.rerun()
        # ------------------------
        
    
    # 【关键修复】：使用 session_state 存储位置和速度，防止每一帧都被重置
    if 'pos' not in st.session_state:
        st.session_state.pos = np.array([[20.0, 50.0], [80.0, 50.0]])
        # 给 Y 轴速度加一个随机偏移量
        y_vel = 0.5 + np.random.uniform(-0.2, 0.2) 
        st.session_state.vel = np.array([[speed_val, y_vel], [-speed_val, -y_vel * 1.1]])

    # --- 初始化计时变量 ---
    if "start_collision_time" not in st.session_state:
        st.session_state.start_collision_time = None

    # 创建容器
    plot_spot = st.empty()
    countdown_text = st.empty() # 用来显示倒计时文字
    
    # 模拟循环for _ in range(300):

    # 使用 while 循环实现动态结束
    
    while True:

        r=size/18.0
        
        # 更新位置让小球按照当前速度向量移动。
        st.session_state.pos += st.session_state.vel
        st.session_state.pos += np.random.normal(0, 0.05, size=(2, 2)) 
        
        # 1. 边界碰撞检测 (0-100范围)
        for i in range(2): # 遍历两个小球
            if st.session_state.pos[i, 0] <= r: # 检测左边界
                st.session_state.vel[i, 0] *= -1 # 速度取反，实现反弹
                st.session_state.pos[i, 0] = r   # 【位置修正】：将球强行拉回边界，防止由于速度太快穿出墙外
            elif st.session_state.pos[i, 0] >= 100 - r:
                st.session_state.vel[i, 0] *= -1
                st.session_state.pos[i, 0] = 100 - r
                
            # Y轴碰撞
            if st.session_state.pos[i, 1] <= r:
                st.session_state.vel[i, 1] *= -1
                st.session_state.pos[i, 1] = r
            elif st.session_state.pos[i, 1] >= 100 - r:
                st.session_state.vel[i, 1] *= -1
                st.session_state.pos[i, 1] = 100 - r
        
        # 2. 核心：两个小球之间的碰撞检测 (简单动量交换)
        dist = np.linalg.norm(st.session_state.pos[0] - st.session_state.pos[1])
        if dist < (2*r): # 根据球大小判断碰撞
            # 交换速度向量
            # st.session_state.vel[0], st.session_state.vel[1] = \
            #     st.session_state.vel[1].copy(), st.session_state.vel[0].copy()
            
            st.session_state.vel[0], st.session_state.vel[1] = st.session_state.vel[1].copy(), st.session_state.vel[0].copy()


            # 【记录第一次碰撞的时间】
            if st.session_state.start_collision_time is None:
                st.session_state.start_collision_time = time.time()
                st.toast("💥 发生碰撞！实验将在10秒后结束")

               # 防止重叠卡死：碰撞后稍微推开一点
            overlap = (2 * r) - dist
            direction = (st.session_state.pos[0] - st.session_state.pos[1]) / (dist + 0.01)
            st.session_state.pos[0] += direction * (overlap / 2)
            st.session_state.pos[1] -= direction * (overlap / 2)             

        # 3. 检查时间是否该结束循环
        if st.session_state.start_collision_time is not None:
            elapsed = time.time() - st.session_state.start_collision_time
            remaining = 10 - elapsed
            if remaining <= 0:
                countdown_text.write("✨ 实验结束")
                
                # 重置时间，方便下次实验
                st.session_state.start_collision_time = None
                break # 退出循环
            else:
                countdown_text.write(f"⏳ 碰撞后倒计时: {remaining:.1f} 秒")                


        # 4.绘制
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=st.session_state.pos[:, 0], 
            y=st.session_state.pos[:, 1], 
            mode='markers',
            marker=dict(
                size=size, 
                color=['#00FFAA', '#FF007F'], 
                line=dict(width=2, color='white')
            )
        ))

        # 【布局优化】：修复边线消失
        fig.update_layout(
            template="plotly_dark",
            xaxis=dict(
                range=[0, 100], # 留出 5 个单位的边距，确保边框线可见
                showticklabels=False,
                showline=True,
                mirror=True,     # 关键：开启镜像，显示右侧和上方的线
                linecolor='#444',# 墙的颜色
                linewidth=4,
                zeroline=False,
                title="空间 X 轴"
            ),
            yaxis=dict(
                range=[0, 100],
                showticklabels=False,
                showline=True,
                mirror=True,
                linecolor='#444',
                linewidth=4,
                zeroline=False,
                scaleanchor="x", # 保持 1:1 比例
                title="空间 Y 轴"
            ),
            width=500, 
            height=500,
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10), # 增加内边距防止裁剪
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )

        # 【关键】：use_container_width 设为 False，避免 Streamlit 拉伸导致边框被添加固定 key，让 Streamlit 知道这是同一个组件的更新切
        plot_spot.plotly_chart(fig, use_container_width=False)
        time.sleep(0.01)
        
    # --- 解决抖动：循环结束后，最后再稳定画一次 ---

elif mode == "3D 几何建模":
    st.header("🧊 高精度空间建模")
    res = st.slider("模型精细度", 20, 100, 60)
    u, v = np.mgrid[0:2*np.pi:complex(0, res), 0:np.pi:complex(0, res//2)]
    x, y, z = np.cos(u)*np.sin(v), np.sin(u)*np.sin(v), np.cos(v)
    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y, colorscale='Magma')])
    fig.update_layout(template="plotly_dark", height=600)
    st.plotly_chart(fig, use_container_width=True)
