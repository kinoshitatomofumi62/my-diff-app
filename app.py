import streamlit as st
import pandas as pd
import random

# --- 問題生成関数 ---
def get_new_question():
    types = ["power", "const", "sin", "exp", "log"]
    t = random.choice(types)
    a, b, c = random.randint(2, 9), random.randint(2, 5), random.randint(1, 9)
    
    if t == "power":
        return {"q": f"{a}x^{{{b}}}", "a": f"{a*b}x^{{{b-1}}}"}
    elif t == "sin":
        return {"q": f"\\sin({a}x)", "a": f"{a}\\cos({a}x)"}
    elif t == "exp":
        return {"q": f"e^{{{a}x}}", "a": f"{a}e^{{{a}x}}"}
    elif t == "log":
        return {"q": f"\\log({a}x)", "a": f"\\frac{{1}}{{x}}"} # log(ax)の微分は1/x
    else:
        return {"q": f"x^{{{b}}} + {c}x", "a": f"{b}x^{{{b-1}}} + {c}"}

# --- アプリの初期化 ---
if 'count' not in st.session_state:
    st.session_state.count = 0
    st.session_state.q_data = get_new_question()

st.title("微分10本ノック（ランダム版）")

if st.session_state.count < 10:
    st.write(f"### 第 {st.session_state.count + 1} 問")
    st.latex(f"y = {st.session_state.q_data['q']}")

    if st.button("答えを見る"):
        st.latex(f"y' = {st.session_state.q_data['a']}")
        
        if st.button("正解！次の問題へ"):
            st.session_state.count += 1
            st.session_state.q_data = get_new_question() # ここで新しい問題を生成
            st.rerun() # 画面を強制更新
else:
    st.success("10問終了！お疲れ様でした！")
    if st.button("もう一度最初から"):
        st.session_state.count = 0
        st.session_state.q_data = get_new_question()
        st.rerun()
