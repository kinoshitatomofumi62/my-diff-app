import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# ページの設定
st.set_page_config(page_title="微分計算マスター", layout="wide")
st.title("📊 微分計算・成長管理アプリ")

# 問題データ（LaTeX形式で記述）
# \\ は Python でバックスラッシュを表示するために2つ重ねています
questions = [
    {"q": "4x^3 - 5x + 2", "a": "12x^2 - 5", "tag": "基礎"},
    {"q": "(2x + 3)^5", "a": "10(2x + 3)^4", "tag": "合成関数"},
    {"q": "\\sin(2x + 1)", "a": "2\\cos(2x + 1)", "tag": "三角・合成"},
    {"q": "x^2 \\cos x", "a": "2x \\cos x - x^2 \\sin x", "tag": "積の微分"},
    {"q": "\\frac{e^x}{x}", "a": "\\frac{(x-1)e^x}{x^2}", "tag": "商の微分"},
    {"q": "\\log(x^2 + 1)", "a": "\\frac{2x}{x^2 + 1}", "tag": "対数・合成"},
    {"q": "\\tan x", "a": "\\frac{1}{\\cos^2 x}", "tag": "三角関数"},
    {"q": "e^{x^2}", "a": "2x e^{x^2}", "tag": "指数・合成"},
    {"q": "\\sqrt{x}", "a": "\\frac{1}{2\\sqrt{x}}", "tag": "べき乗"},
    {"q": "x \\log x", "a": "\\log x + 1", "tag": "積の微分"}
]

# データの読み込み
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["日付", "単元", "結果", "理由"])

# メイン画面のタブ
tab1, tab2 = st.tabs(["今日のトレーニング", "伸び率レポート"])

with tab1:
    idx = st.selectbox("解く問題を選択してください", range(len(questions)), format_func=lambda i: f"問題 {i+1}")
    q = questions[idx]
    
    st.write("### 問題")
    st.latex(f"y = {q['q']}")
    st.write("を微分せよ。")
    
    if st.button("答え合わせ"):
        st.write("---")
        st.write("### 正解")
        st.latex(f"y' = {q['a']}")
        
        st.write("---")
        status = st.radio("結果はどうでしたか？", ["瞬殺！", "完答（遅め）", "ミスした..."])
        
        reason = "なし"
        if status == "ミスした...":
            reason = st.selectbox("ミス理由を教えてください:", ["符号ミス", "中身の微分忘れ", "公式混同", "計算ミス", "方針が立たず"])
            
        if st.button("この結果を記録する"):
            new_entry = pd.DataFrame([[datetime.date.today(), q['tag'], status, reason]], 
                                     columns=st.session_state.history.columns)
            st.session_state.history = pd.concat([st.session_state.history, new_entry], ignore_index=True)
            st.balloons()
            st.success("記録完了！「伸び率レポート」タブで確認しましょう。")

with tab2:
    st.header("📈 成長の記録")
    if not st.session_state.history.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("ミスの内訳")
            miss_df = st.session_state.history[st.session_state.history["理由"] != "なし"]
            if not miss_df.empty:
                fig_pie = px.pie(miss_df, names="理由", hole=0.3)
                st.plotly_chart(fig_pie)
            else:
                st.write("ミスなし！素晴らしい！")
        
        with col2:
            st.subheader("学習状況")
            fig_bar = px.bar(st.session_state.history, x="日付", color="結果")
            st.plotly_chart(fig_bar)

        st.subheader("履歴詳細")
        st.dataframe(st.session_state.history, use_container_width=True)
    else:
        st.write("まだデータがありません。まずは問題を解いて記録しましょう！")
