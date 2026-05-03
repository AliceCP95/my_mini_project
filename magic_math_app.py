import streamlit as st
import random
import time
import math

st.set_page_config(page_title="超级算法百宝箱", page_icon="🚀")
st.title("🚀 十岁程序员的超级算法百宝箱")

# 侧边栏菜单：增加到10个
menu = st.sidebar.selectbox("请选择一个算法魔法", [
    "1. 阶乘计算器 (循环)", 
    "2. 数字排排队 (排序)", 
    "3. 奇偶小侦探 (余数逻辑)",
    "4. 质数搜寻镜 (素数判定)",
    "5. 斐波那契兔子 (递归序列)",
    "6. 秘密消息加密 (凯撒密码)",
    "7. 圆形大揭秘 (几何计算)",
    "8. 倒计时发射 (循环控制)",
    "9. 猜数字游戏 (二分法思想)",
    "10. 随机幸运星 (概率算法)"
])

# --- 1 & 2 保持原样 (省略部分描述以节省空间) ---
if menu == "1. 阶乘计算器 (循环)":
    st.header("🔢 阶乘计算")
    num = st.slider("选个数", 1, 20, 5)
    res = math.factorial(num)
    st.success(f"{num}! = {res}")
    st.balloons() # 撒花效果

elif menu == "2. 数字排排队 (排序)":
    st.header("📊 自动排序")
    nums = st.text_input("输入几个数字（用空格隔开）", "34 12 5 89 2").split()
    if st.button("开始排序"):
        sorted_list = sorted([int(x) for x in nums])
        st.write("从小到大：", sorted_list)
        st.snow() # 降雪效果

# --- 新增的 8 个算法 ---

elif menu == "3. 奇偶小侦探 (余数逻辑)":
    st.header("🔍 奇数还是偶数？")
    n = st.number_input("输入一个数字", value=0)
    if n % 2 == 0:
        st.success(f"{n} 是【偶数】，它是2的好朋友！")
        st.snow() # 降雪效果
    else:
        st.warning(f"{n} 是【奇数】，它总是多出一个1！")

elif menu == "4. 质数搜寻镜 (素数判定)":
    st.header("💎 寻找质数宝藏")
    st.write("质数是只能被1和它自己整除的数。")
    p = st.number_input("测测这个数是不是质数", value=7)
    is_prime = True
    if p < 2: is_prime = False
    for i in range(2, int(p**0.5) + 1):
        if p % i == 0:
            is_prime = False
            break
    st.write("结果：" + ("✅ 它是质数！" if is_prime else "❌ 它不是质数。"))
    st.balloons() # 撒花效果

elif menu == "5. 斐波那契兔子 (递归序列)":
    st.header("🐰 兔子数列")
    st.write("每一项都等于前两项之和：1, 1, 2, 3, 5, 8...")
    count = st.slider("你想看前几项？", 2, 20, 10)
    fib = [1, 1]
    while len(fib) < count:
        fib.append(fib[-1] + fib[-2])
    st.write(fib)
    st.balloons() # 撒花效果

elif menu == "6. 秘密消息加密 (凯撒密码)":
    st.header("🔐 特工加密器")
    text = st.text_input("输入英文密信", "Hello")
    shift = st.slider("加密位移", 1, 10, 3)
    secret = "".join([chr(ord(c) + shift) for c in text])
    st.info(f"加密后的电报：{secret}")

elif menu == "7. 圆形大揭秘 (几何计算)":
    st.header("⭕ 圆圆的秘密")
    r = st.number_input("输入圆的半径", value=1.0)
    area = math.pi * (r**2)
    perimeter = 2 * math.pi * r
    st.write(f"面积是：{area:.2f}")
    st.write(f"周长是：{perimeter:.2f}")
    st.snow() # 降雪效果

elif menu == "8. 倒计时发射 (循环控制)":
    st.header("🚀 火箭倒计时")
    t = st.slider("设置倒计时秒数", 3, 10, 5)
    if st.button("点火！"):
        placeholder = st.empty()
        for i in range(t, 0, -1):
            placeholder.header(f"倒计时：{i}")
            time.sleep(1)
        placeholder.header("🚀 轰！发射成功！")
        st.balloons()
        
elif menu == "9. 猜数字游戏 (二分法思想)":
    st.header("🎯 猜猜我的数字")
    if 'target' not in st.session_state:
        st.session_state.target = random.randint(1, 100)
    guess = st.number_input("猜一个 1-100 的数", min_value=1, max_value=100)
    if st.button("我猜！"):
        if guess < st.session_state.target: st.write("太小了，往大点猜！")
        elif guess > st.session_state.target: st.write("太大了，往小点猜！")
        else: 
            st.success("🎉 猜对啦！")
            st.session_state.target = random.randint(1, 100)

elif menu == "10. 随机幸运星 (概率算法)":
    st.header("🎲 幸运大抽奖")
    names = st.text_area("输入名单（用逗号隔开）", "小明, 小红, 小刚, 小亮")
    if st.button("抽一个幸运儿"):
        name_list = names.split(",")
        winner = random.choice(name_list)
        st.snow()
        st.subheader(f"✨ 今天的幸运星是：{winner.strip()}！")

st.markdown("---")
st.caption("小朋友，你已经掌握了10个超级算法啦！")
