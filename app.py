
import streamlit as st
import pandas as pd
import datetime
import random

st.set_page_config(page_title="微分計算10本ノック", layout="wide")

# --- 問題生成ロジック ---
def generate_question(type_idx):
    a = random.randint(2, 9)
    b = random.randint(2, 5)
    c = random.randint(1, 9)
    
    if type_idx == 0: # べき乗
        return {"q": f"{a}x^{b} - {c}x", "a": f"{a*b}x^{b-1} - {c}", "tag": "基礎"}
    elif type_idx == 1: # 合成関数
        return {"q": f"({a}x + {c})^{b}", "a": f"{a*b}({a}x + {c})^{b-1}", "tag": "合成関数"}
    elif type_idx == 2: # 三角関数
        return {"q": f"\\sin({a}x + {c})", "a": f"{a}\\cos({a}x + {c})", "tag": "三角・合成"}
    elif type_idx == 3: # 指数
        return {"q": f"e^{{{a}x}}", "a": f"{a}e^{{{a}x}}", "tag": "指数"}
    elif type_idx == 4: # 対数
        return {"q": f"\\log({a}x^2 + {c})", "a": f"\\frac{{{2*a}x}}{{{a}x^2 + {c}}}", "tag": "対数・合成"}
    # 他のパターンも同様に追加可能（今回は5パターン×2セットで10問構成にします）
    return {"q": f"{a}x^{b}", "a": f"{a*b}x^{b-1}", "tag": "基礎"}

# --- アプリの状態管理 ---
if 'step' not in st.session_state:
    st.session_state.step = 0  # 現在何問目か
    st.session_state.score = {"瞬殺！": 0, "完答（遅め）": 0, "ミスした...": 0}
    st.session_state.current_q = generate_question(0)

# --- 画面表示 ---
st.title("🔢 微分計算10本ノック")

if st.session_state.step < 10:
    st.subheader(f"第 {st.session_state.step + 1} 問 / 全10問")
    st.latex(f"y = {st.session_state.current_q['q']}")
    
    if st.button("答えを表示"):
        st.latex(f"y' = {st.session_state.current_q['a']}")
        st.write("---")
        status = st.radio("自己採点:", ["瞬殺！", "完答（遅め）", "ミスした..."], key=f"radio_{st.session_state.step}")
        
        if st.button("次の問題へ"):
            # スコア記録
            st.session_state.score[status] += 1
            # 次の問題準備
            st.session_state.step += 1
            if st.session_state.step < 10:
                st.session_state.current_q = generate_question(st.session_state.step % 5) # 5パターンを2周
            st.rerun()

else:
    st.balloons()
    st.header("🎉 トレーニング終了！")
    st.write("本日のリザルト：")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("瞬殺（完璧！）", st.session_state.score["瞬殺！"])
    col2.metric("完答（あと一息）", st.session_state.score["完答（遅め）"])
    col3.metric("ミス（要復習）", st.session_state.score["ミスした..."])
    
    if st.button("もう一度挑戦する"):
        st.session_state.step = 0
        st.session_state.score = {"瞬殺！": 0, "完答（遅め）": 0, "ミスした...": 0}
        st.session_state.current_q = generate_question(0)
        st.rerun()
