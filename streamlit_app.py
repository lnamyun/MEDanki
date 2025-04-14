import streamlit as st

# 초기 카드 목록 설정
if "cards" not in st.session_state:
    st.session_state.cards = [
        {
            "question": "다음 중 객체지향 프로그래밍의 특징이 아닌 것은?",
            "answer": "정답: 4. 절차적 프로그래밍<br><br>해설: 절차적 프로그래밍은 객체지향 프로그래밍과 대조되는 패러다임입니다.",
            "difficulty": 0,
            "reviewed": False
        },
        {
            "question": "TCP와 UDP의 차이점에 대한 설명으로 옳은 것은?",
            "answer": "정답: TCP는 연결 지향적이고 신뢰성이 있으며, UDP는 비연결 지향적이고 신뢰성이 낮습니다.<br><br>해설: TCP는 3-way handshake로 신뢰성을 보장합니다.",
            "difficulty": 0,
            "reviewed": False
        }
    ]
    st.session_state.current_index = 0
    st.session_state.flipped = False

cards = st.session_state.cards
current_index = st.session_state.current_index
current_card = cards[current_index]

st.title("🧠 MEDanki")

# ✅ 진행률 표시
reviewed_count = sum(card["reviewed"] for card in cards)
st.progress(reviewed_count / len(cards) if cards else 0)
st.caption(f"진행률: {reviewed_count} / {len(cards)}")

# ✅ 카드 표시
with st.container():
    st.markdown("### " + ("문제" if not st.session_state.flipped else "정답 및 해설"))

    if st.session_state.flipped:
        st.markdown(current_card["answer"], unsafe_allow_html=True)
        st.button("⬅ 문제로 돌아가기", on_click=lambda: st.session_state.update(flipped=False))
    else:
        st.markdown(current_card["question"], unsafe_allow_html=True)
        st.button("정답 보기 ➡", on_click=lambda: st.session_state.update(flipped=True))

# ✅ 난이도 평가
if st.session_state.flipped:
    st.markdown("**이 문제의 난이도는 어땠나요?**")
    col1, col2, col3 = st.columns(3)

    def rate(difficulty):
        current_card["difficulty"] = difficulty
        current_card["reviewed"] = True
        st.session_state.flipped = False

    col1.button("😄 쉬움", on_click=lambda: rate(1))
    col2.button("😐 보통", on_click=lambda: rate(2))
    col3.button("😵 어려움", on_click=lambda: rate(3))

# ✅ 카드 넘기기
col1, col2 = st.columns(2)
if col1.button("⬅ 이전", disabled=current_index == 0):
    st.session_state.current_index -= 1
    st.session_state.flipped = False
if col2.button("다음 ➡", disabled=current_index == len(cards) - 1):
    st.session_state.current_index += 1
    st.session_state.flipped = False

# ✅ 문제 목록
st.markdown("---")
st.markdown("### 📋 문제 목록")

for i, card in enumerate(cards):
    label = f"{i+1}. " + card["question"].split("<")[0][:30]
    diff = ["미평가", "쉬움", "보통", "어려움"][card["difficulty"]]
    status = "✅ 완료" if card["reviewed"] else "🕒 학습 필요"

    if st.button(f"{label} ({diff} / {status})", key=f"goto_{i}"):
        st.session_state.current_index = i
        st.session_state.flipped = False

# ✅ PDF 추가
st.markdown("---")
st.markdown("### 📄 문제 추가하기 - PDF 파일")

with st.container():
    st.info("PDF 파일을 업로드하면 문제와 정답을 자동으로 추출할 수 있습니다. (이미지도 지원 예정)")

    uploaded_pdf = st.file_uploader(
        "📤 PDF 파일 업로드",
        type=["pdf"],
        accept_multiple_files=False,
        help="기출문제가 담긴 PDF 파일을 업로드하세요."
    )

    if uploaded_pdf:
        st.success(f"✅ 업로드 완료: `{uploaded_pdf.name}`")
        st.caption("🔧 추출 처리는 아직 구현되지 않았습니다. 추후 텍스트 및 이미지 자동 인식 기능이 추가됩니다.")

# ✅ 문제 수동 추가
st.markdown("---")
st.markdown("### ✏️ 문제 수동 추가")

with st.form("manual_add"):
    q = st.text_area("문제 입력", key="new_q")
    a = st.text_area("정답 및 해설 입력 (HTML 가능)", key="new_a")
    submitted = st.form_submit_button("➕ 문제 추가")

    if submitted:
        if q.strip() and a.strip():
            cards.append({
                "question": q.strip(),
                "answer": a.strip(),
                "difficulty": 0,
                "reviewed": False
            })
            st.success("✅ 문제가 추가되었습니다!")
        else:
            st.warning("⚠️ 문제와 정답을 모두 입력해주세요.")
