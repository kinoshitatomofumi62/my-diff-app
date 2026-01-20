import streamlit as st
import random

# --- 問題の種類と難易度を固定した生成ロジック ---
def get_fixed_step_question(step):
    # a, b, c は計算がほどよく面倒になる2以上の数値
    a = random.randint(2, 5)
    b = random.randint(2, 4)
    c = random.randint(2, 6)
    
    # ステップごとに問題の型を固定
    if step == 0: # 多項式
        return {"q": f"{a}x^{{{b+1}}} - {c}x^{{{b}}}", "a": f"{a*(b+1)}x^{{{b}}} - {c*b}x^{{{b-1}}}"}
    elif step == 1: # 合成関数（累乗）
        return {"q": f"({a}x + {c})^{{{b}}}", "a": f"{a*b}({a}x + {c})^{{{b-1}}}"}
    elif step == 2: # 三角関数（sin）
        return {"q": f"\\sin({a}x^2)", "a": f"{2*a}x\\cos({a}x^2)"}
    elif step == 3: # 三角関数（cos）
        return {"q": f"\\cos({c}x + {a})", "a": f"-{c}\\sin({c}x + {a})"}
    elif step == 4: # 指数関数
        return {"q": f"e^{{{a}x^2}}", "a": f"{2*a}xe^{{{a}x^2}}"}
    elif step == 5: # 対数関数
        return {"q": f"\\log({a}x + {c})", "a": f"\\frac{{{a}}}{{{a}x + {c}}}"}
    elif step == 6: # 分数関数（商の微分）
        return {"q": f"\\frac{{1}}{{{a}x + {c}}}", "a": f"-\\frac{{{a}}}{{({a}x + {c})^2}}"}
    elif step == 7: # 積の微分（x * e^x）
        return {"q": f"{a}x e^{{x}}", "a": f"{a}(x + 1)e^{{x}}"}
    elif step == 8: # 積の微分（x * sin x）
        return {"q": f"x \\sin({a}x)", "a": f"\\sin({a}x) + {a}x \\cos({a}x)"}
    elif step == 9: # ルート（べき乗）
        return {"q": f"\\sqrt{{{a}x + {c}}}", "a": f"\\frac{{{a}}}{{2\\sqrt{{{a}x + {c}}}}}"}
    return {"q": "x", "a": "1"}

# --- アプリの初期化 ---
if 'count' not in st.session_state:
    st.session_state.count = 0
    st.session_state.q_data = get_fixed_step_question(0)
    st.session_state.show_answer = False

st.title("🔢 微分10本ノック【実戦・数IIIレベル】")

if st.session_state.count < 10:
    st.write(f"### 第 {st.session_state.count + 1} 問：")
    st.latex(f"y = {st.session_state.q_data['q']}")

    if not st.session_state.show_answer:
        if st.button("答えを見る"):
            st.session_state.show_answer = True
            st.rerun()
    else:
        st.success("正解：")
        st.latex(f"y' = {st.session_state.q_data['a']}")
        
        if st.button("次の問題へ"):
            st.session_state.count += 1
            if st.session_state.count < 10:
                st.session_state.q_data = get_fixed_step_question(st.session_state.count)
            st.session_state.show_answer = False
            st.rerun()
else:
    st.balloons()
    st.header("🎉 10問終了！完璧です！")
    if st.button("もう一度最初から"):
        st.session_state.count = 0
        st.session_state.q_data = get_fixed_step_question(0)
        st.session_state.show_answer = False
        st.rerun()
