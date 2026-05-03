import streamlit as st
import random

# 设置网页标题和图标
st.set_page_config(page_title="小小程序员的魔法盒", page_icon="🪄")

# --- 网页界面设计 ---
st.title("🌟 10岁程序员的魔法助手")
st.write("欢迎来到编程世界！在这里你可以体验算法的魔力。")

# 侧边栏导航
menu = st.sidebar.selectbox("选择一个魔法项目", ["算法1：阶乘计算器", "算法2：数字排序挑战"])

# --- 算法 1：阶乘计算器 (展示循环/迭代思想) ---
if menu == "算法1：阶乘计算器":
    st.header("🔢 阶乘计算魔法")
    st.info("阶乘就是从1一直乘到你选的那个数。比如 3 的阶乘是 1×2×3 = 6")
    
    number = st.slider("选一个数字看看效果", 1, 10, 5)
    
    # 算法逻辑：基础循环
    result = 1
    for i in range(1, number + 1):
        result *= i
    
    st.success(f"魔法结果：{number} 的阶乘是 **{result}**！")
    st.balloons() # 撒花效果

# --- 算法 2：数字排序 (展示数据处理) ---
elif menu == "算法2：数字排序挑战":
    st.header("📊 数字排排队")
    st.info("算法可以帮我们把乱七八糟的数字按从小到大排好。")
    
    # 生成 5 个随机数
    if st.button("生成一组乱序魔法数字"):
        random_list = [random.randint(1, 100) for _ in range(5)]
        st.session_state.numbers = random_list
    
    if 'numbers' in st.session_state:
        st.write("现在的数字：", st.session_state.numbers)
        
        # 算法逻辑：Python内置排序（也是算法的一种）
        sorted_list = sorted(st.session_state.numbers)
        
        if st.button("施展排序魔法"):
            st.write("排好序的数字：", sorted_list)
            st.snow() # 降雪效果

# 底部页脚
st.markdown("---")
st.caption("用 Python 创造你的第一个网页助手吧！🚀")