import streamlit as st

# ✅ 세션 상태 초기화
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

# ✅ animate_slide 속성 초기화
if "animate_slide" not in st.session_state:
    st.session_state.animate_slide = True  # 슬라이드 애니메이션 트리거

cards = st.session_state.cards
current_index = st.session_state.current_index
current_card = cards[current_index]

st.title("🧠 MEDanki")

# ✅ CSS 추가 (카드 스타일 및 애니메이션)
st.markdown("""
    <style>
    .card-container {
        perspective: 1000px;
        animation: slide-in 0.5s ease-out;
    }
    .card {
        width: 100%;
        max-width: 400px;
        height: 200px;
        margin: 20px auto;
        position: relative;
        transform-style: preserve-3d;
        transition: transform 0.6s;
    }
    .card.flipped {
        transform: rotateY(180deg);
    }
    .card-face {
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #ddd;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 20px;
        font-size: 15px;
        background-color: #fefefe;
    }
    .card-face.back {
        transform: rotateY(180deg);
    }
    @keyframes slide-in {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ✅ 카드 표시
with st.container():
    st.markdown("### 📘 문제")
    # 슬라이드 애니메이션 클래스 추가
    slide_class = "slide-in" if st.session_state.animate_slide else ""
    card_class = "card flipped" if st.session_state.flipped else "card"
    st.markdown(f"""
    <div class="card-container {slide_class}">
        <div class="{card_class}">
            <div class="card-face front">
                {current_card["question"]}
            </div>
            <div class="card-face back">
                {current_card["answer"]}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 버튼 동작 즉시 반영되도록 rerun 사용
    if st.button("⬅ 문제로 돌아가기" if st.session_state.flipped else "정답 보기 ➡"):
        st.session_state.flipped = not st.session_state.flipped
        st.session_state.animate_slide = False  # 뒤집기 시 슬라이드 애니메이션 비활성화
        st.rerun()

# ✅ 난이도 평가 함수 수정
def rate_and_next(difficulty):
    current_card["difficulty"] = difficulty
    current_card["reviewed"] = True
    if st.session_state.current_index < len(cards) - 1:
        st.session_state.current_index += 1  # 다음 문제로 이동
    st.session_state.flipped = False
    st.session_state.animate_slide = True  # 슬라이드 애니메이션 활성화
    st.session_state.trigger_rerun = True  # 상태 변수로 rerun 트리거

# ✅ 난이도 평가 버튼
if st.session_state.flipped:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("**이 문제의 난이도는 어땠나요?**")

    col1, col2, col3 = st.columns(3)

    col1.button("😄 쉬움", on_click=lambda: rate_and_next(1))
    col2.button("😐 보통", on_click=lambda: rate_and_next(2))
    col3.button("😵 어려움", on_click=lambda: rate_and_next(3))

# ✅ rerun 트리거 처리
if "trigger_rerun" in st.session_state and st.session_state.trigger_rerun:
    st.session_state.trigger_rerun = False  # 트리거 초기화
    st.rerun()

# ✅ 카드 넘기기
col1, col2 = st.columns(2)
if col1.button("⬅ 이전", disabled=current_index == 0):
    st.session_state.current_index -= 1
    st.session_state.flipped = False
    st.session_state.animate_slide = True  # 슬라이드 애니메이션 활성화
    st.rerun()

if col2.button("다음 ➡", disabled=current_index == len(cards) - 1):
    st.session_state.current_index += 1
    st.session_state.flipped = False
    st.session_state.animate_slide = True  # 슬라이드 애니메이션 활성화
    st.rerun()

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
        st.rerun()

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
            st.rerun()
        else:
            st.warning("⚠️ 문제와 정답을 모두 입력해주세요.")
