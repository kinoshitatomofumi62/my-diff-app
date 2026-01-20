import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

st.set_page_config(page_title="微分計算マスター", layout="wide")
st.title("📊 微分計算・成長管理アプリ")

# 問題データ
questions = [
    {"q": "4x^3 - 5x + 2", "a": "12x^2 - 5", "tag": "基礎"},
    {"q": "(2x + 3)^5", "a": "10(2x + 3)^4", "tag": "合成関数"},
    {"q": "sin(2x + 1)", "a": "2cos(2x + 1)", "tag": "三角・合成"},
    {"q": "x^2 * cos(x)", "a": "2x * cos(x) - x^2 * sin(x)", "tag": "積の微分"},
    {"q": "log(x^2 + 1)", "a": "2x / (x^2 + 1)", "tag": "対数・合成"},
    {"q": "e^{x^2}", "a": "2x * e^{x^2}", "tag": "指数・合成"},
    {"q": "x * log(x)", "a": "log(x) + 1", "tag": "積の微分"}
]

# データの読み込み
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["日付", "問題", "結果", "理由"])

# メイン画面
tab1, tab2 = st.tabs(["今日のトレーニング", "伸び率レポート"])

with tab1:
    idx = st.selectbox("解く問題を選択してください", range(len(questions)), format_func=lambda i: f"問題 {i+1}")
    q = questions[idx]
    
    st.info(f"### 問題: y = {q['q']} を微分せよ")
    
    if st.button("答え合わせ"):
        st.success(f"正解: y' = {q['a']}")
        
        st.write("---")
        status = st.radio("結果を選択:", ["瞬殺！", "完答（遅め）", "ミスした..."])
        
        reason = "なし"
        if status == "ミスした...":
            reason = st.selectbox("ミス理由:", ["符号ミス", "中身の微分忘れ", "公式混同", "計算ミス"])
            
        if st.button("この結果を記録する"):
            new_data = pd.DataFrame([[datetime.date.today(), q['tag'], status, reason]], columns=st.session_state.history.columns)
            st.session_state.history = pd.concat([st.session_state.history, new_data], ignore_index=True)
            st.balloons()

with tab2:
    if not st.session_state.history.empty:
        st.subheader("ミスの傾向分析")
        fig = px.pie(st.session_state.history[st.session_state.history["理由"] != "なし"], names="理由", title="ミスの内訳")
        st.plotly_chart(fig)
        
        st.subheader("これまでの全記録")
        st.dataframe(st.session_state.history)
    else:
        st.write("まだ記録がありません。まずは問題を解いてみよう！")