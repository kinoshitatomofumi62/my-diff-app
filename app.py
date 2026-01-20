import streamlit as st
import random

# --- 問題生成関数 ---
def get_new_question():
    types = ["power", "sin", "exp", "log", "composite"]
    t = random.choice(types)
    a, b, c = random.randint(2, 9), random.randint(2, 5), random.randint(1, 9)
    
    if t == "power":
        return {"q": f"{a}x^{{{b}}}", "a": f"{a*b}x^{{{b-1}}}"}
    elif t == "sin":
        return {"q": f"\\sin({a}x)", "a": f"{a}\\cos({a}x)"}
    elif t == "exp":
        return {"q": f"e^{{{a}x}}", "a": f"{a}e^{{{a}x}}"}
    elif t == "log":
        return {"q": f"\\log({a}x)", "a": f"\\frac{{1}}{{x}}"}
    else:
        return {"q": f"({a}x + {c})^{{{b}}}", "a": f"{a*b}({a}x + {c})^{{{b-1}}}"}

# --- アプリの状態管理（初期化） ---
if 'count' not in st.session_state:
    st.session_state.count = 0
    st.session_state.q_data = get_new_question()
    st.session_state.show_answer = False # 答えを表示しているかのフラグ

st.title("🔢 微分10本ノック")

if st.session_state.count < 10:
    st.write(f"### 第 {st.session_state.count + 1} 問 / 10問中")
    st.latex(f"y = {st.session_state.q_data['q']}")

    # 「答えを見る」ボタン
    if st.button("答えを見る"):
        st.session_state.show_answer = True

    # 答えを表示中なら、正解と「次の問題へ」ボタンを出す
    if st.session_state.show_answer:
        st.success("正解はこちら：")
        st.latex(f"y' = {st.session_state.q_data['a']}")
        
        if st.button("正解！次の問題へ"):
            st.session_state.count += 1
            st.session_state.q_data = get_new_question()
            st.session_state.show_answer = False # フラグをリセット
            st.rerun() # 画面を更新して次の問題へ
else:
    st.balloons()
    st.header("🎉 10問終了！お疲れ様でした！")
    if st.button("もう一度最初から挑戦する"):
        st.session_state.count = 0
        st.session_state.q_data = get_new_question()
        st.session_state.show_answer = False
        st.rerun()
