import random
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="국어 표준 발음 평가",
    layout="centered"
)

# 기본 원본 데이터 (영역/카테고리별 분리)
RAW_QUIZ_DATA = {
    "1. 표준 발음의 개념과 원칙": [
        {
            "id": 1,
            "type": "short",
            "question": "사람마다 발음하는 법이 달라서 [      ]에 지장이 생기는 것을 막기 위해 발음의 표준을 정해 놓은 것을 '표준 발음'이라고 합니다. 빈칸에 들어갈 알맞은 단어를 쓰시오.",
            "answer": "의사소통",
            "explanation": "표준 발음은 국어를 쓰는 사람들 사이에서 발음이 달라 의사소통에 지장이 생기는 것을 막기 위해 정한 약속입니다."
        },
        {
            "id": 2,
            "type": "short",
            "question": "표준 발음은 '표준어의 실제 발음을 따르되, 국어의 전통성과 [      ]을 고려하여 정함을 원칙으로 한다.'에서 빈칸에 들어갈 단어를 쓰시오.",
            "answer": "합리성",
            "explanation": "표준 발음의 3대 원칙은 ① 표준어의 실제 발음, ② 국어의 전통성, ③ 합리성입니다."
        },
        {
            "id": 3,
            "type": "choice",
            "question": "다음 중 표준 발음의 원칙에 대한 설명으로 알맞은 것을 고르세요.",
            "options": [
                "1. 현실 발음에서 모음의 장단(길이)이 구별되지 않으므로, 장단 구분 규정은 전통성을 고려해 마련되어 있다.",
                "2. 'ㅢ'는 항상 예외 없이 단하나의 발음인 [ㅢ]로만 발음해야 한다."
            ],
            "answer": "1. 현실 발음에서 모음의 장단(길이)이 구별되지 않으므로, 장단 구분 규정은 전통성을 고려해 마련되어 있다.",
            "explanation": "현실 발음에서 모음의 장단이 잘 구별되지 않더라도 오랜 기간 뜻을 변별해 온 역사성을 고려하여 '전통성' 측면에서 장단 규정을 두고 있습니다."
        }
    ],
    "2. 홑받침과 쌍받침의 발음": [
        {
            "id": 4,
            "type": "short",
            "question": "어말이나 자음 앞에서 'ㅅ, ㅆ, ㅈ, ㅊ, ㅌ, ㅎ' 받침이 바뀐 대표음 한 글자를 쓰시오.",
            "answer": "ㄷ",
            "explanation": "음절의 끝소리 규칙에 따라 ㅅ, ㅆ, ㅈ, ㅊ, ㅌ, ㅎ은 모두 대표음 [ㄷ]으로 바뀌어 발음됩니다."
        },
        {
            "id": 5,
            "type": "choice",
            "question": "홑받침이나 쌍받침 뒤에 '모음으로 시작하는 형식 형태소(조사, 어미, 접사)'가 연결될 때의 발음 원칙은?",
            "options": [
                "1. 대표음으로 바꾼 뒤 뒤 음절 첫소리로 옮겨 발음한다.",
                "2. 대표음으로 바꾸지 않고 제 음가대로 뒤 음절 첫소리로 옮겨 발음한다(연음)."
            ],
            "answer": "2. 대표음으로 바꾸지 않고 제 음가대로 뒤 음절 첫소리로 옮겨 발음한다(연음).",
            "explanation": "형식 형태소가 올 때는 음절의 끝소리 규칙을 적용하지 않고 받침 제 음가대로 넘겨 발음(연음)합니다."
        },
        {
            "id": 6,
            "type": "choice",
            "question": "홑받침이나 쌍받침 뒤에 '모음으로 시작하는 실질 형태소'가 올 때는 받침을 무엇으로 바꾸어서 뒤 음절의 첫소리로 옮겨 발음하나요?",
            "options": ["1. 대표음", "2. 기본형"],
            "answer": "1. 대표음",
            "explanation": "뜻을 가진 실질 형태소가 뒤에 오면, 먼저 받침을 7개 대표음 중 하나로 바꾼 뒤에 연음시킵니다."
        },
        {
            "id": 7,
            "type": "choice",
            "question": "그 사람은 얼굴에서 빛이 [ 1. 비시 / 2. 비치 ] 난다.",
            "options": ["1. 비시", "2. 비치"],
            "answer": "2. 비치",
            "explanation": "'이'는 모음으로 시작하는 형식 형태소(조사)이므로, 'ㅊ' 받침을 대표음으로 바꾸지 않고 제 음가대로 연음하여 [비치]로 발음합니다."
        },
        {
            "id": 8,
            "type": "choice",
            "question": "등산을 했더니 무릎이 [ 1. 무르비 / 2. 무르피 ] 아프다.",
            "options": ["1. 무르비", "2. 무르피"],
            "answer": "2. 무르피",
            "explanation": "'이'는 조사(형식 형태소)이므로 'ㅍ' 받침이 제 음가대로 연음되어 [무르피]가 됩니다."
        },
        {
            "id": 9,
            "type": "choice",
            "question": "이 소설의 끝을 [ 1. 끄슬 / 2. 끄츨 / 3. 끄틀 ] 다시 써 보려 해.",
            "options": ["1. 끄슬", "2. 끄츨", "3. 끄틀"],
            "answer": "3. 끄틀",
            "explanation": "'을'은 조사(형식 형태소)이므로 'ㅌ' 받침을 그대로 연음하여 [끄틀]로 발음합니다."
        },
        {
            "id": 10,
            "type": "choice",
            "question": "꽃 아래 [ 1. 꼬다래 / 2. 꼬사래 / 3. 꼬차래 ] 그늘이 있다.",
            "options": ["1. 꼬다래", "2. 꼬사래", "3. 꼬차래"],
            "answer": "1. 꼬다래",
            "explanation": "'아래'는 뜻을 가진 실질 형태소입니다. 따라서 '꽃'의 'ㅊ'을 먼저 대표음 [ㄷ]으로 바꾸고 연음시켜 [꼬다래]로 발음합니다."
        },
        {
            "id": 11,
            "type": "choice",
            "question": "나는 빵을 매우 좋아한다 [ 1. 조아한다 / 2. 조하한다 ].",
            "options": ["1. 조아한다", "2. 조하한다"],
            "answer": "1. 조아한다",
            "explanation": "받침 'ㅎ' 뒤에 모음으로 시작하는 형식 형태소가 오면 'ㅎ'은 발음되지 않고 탈락하므로 [조아한다]가 맞습니다."
        }
    ],
    "3. 겹받침의 발음": [
        {
            "id": 12,
            "type": "short",
            "question": "음절 끝에 두 개의 자음이 놓일 때, 둘 중 하나의 자음만 남고 나머지 자음은 탈락하는 음운 현상의 명칭을 쓰시오.",
            "answer": "자음군 단순화",
            "explanation": "겹받침이 어말이나 자음 앞에서 하나만 발음되고 하나는 탈락하는 현상을 '자음군 단순화'라고 합니다."
        },
        {
            "id": 13,
            "type": "choice",
            "question": "이 선을 밟지 [ 1. 발찌 / 2. 밥찌 ] 마라.",
            "options": ["1. 발찌", "2. 밥찌"],
            "answer": "2. 밥찌",
            "explanation": "겹받침 'ㄼ'은 대부분 [ㄹ]로 발음되지만, 동사 '밟-'은 자음 앞에서 예외적으로 [밥-]으로 발음하므로 [밥찌]가 맞습니다."
        },
        {
            "id": 14,
            "type": "choice",
            "question": "강당은 교실보다 넓다 [ 1. 넙따 / 2. 널따 ].",
            "options": ["1. 넙따", "2. 널따"],
            "answer": "2. 널따",
            "explanation": "겹받침 'ㄼ'의 원칙적인 발음은 [ㄹ]이므로 [널따]가 맞습니다."
        },
        {
            "id": 15,
            "type": "choice",
            "question": "오늘은 날씨가 어제보다 맑다 [ 1. 막따 / 2. 말따 ].",
            "options": ["1. 막따", "2. 말따"],
            "answer": "1. 막따",
            "explanation": "겹받침 'ㄺ'은 어말이나 자음 앞에서 대표음 [ㄱ]으로 발음하므로 [막따]가 맞습니다."
        },
        {
            "id": 16,
            "type": "choice",
            "question": "밥값은 [ 1. 밥깝슨 / 2. 밥까븐 ] 누가 내는 거냐?",
            "options": ["1. 밥깝슨", "2. 밥까븐"],
            "answer": "1. 밥깝슨",
            "explanation": "'은'은 조사(형식 형태소)입니다. 겹받침 'ㅄ'에서 첫째 받침 'ㅂ'은 남고, 둘째 받침 'ㅅ'이 연음되어 된소리 [ㅆ]으로 발음되므로 [밥깝슨]이 맞습니다."
        },
        {
            "id": 17,
            "type": "choice",
            "question": "흙 위에 [ 1. 흘귀에 / 2. 흐귀에 / 3. 흙위에 ] 쏟아졌다.",
            "options": ["1. 흘귀에", "2. 흐귀에", "3. 흙위에"],
            "answer": "1. 흘귀에",
            "explanation": "'위'는 실질 형태소이므로 겹받침 'ㄺ'에서 자음군 단순화가 일어나 대표음 [ㄱ]이 남고, 이것이 연음되어 [흘귀에]가 됩니다."
        },
        {
            "id": 18,
            "type": "choice",
            "question": "하늘에 구름이 많아서 [ 1. 마나서 / 2. 만하서 ] 달을 못 보았다.",
            "options": ["1. 마나서", "2. 만하서"],
            "answer": "1. 마나서",
            "explanation": "겹받침 'ㄶ' 뒤에 모음으로 시작하는 어미 '-아서'가 오면 'ㅎ'이 탈락하고 'ㄴ'만 넘어가 [마나서]로 발음됩니다."
        }
    ]
}

# 1. 세션 변수 안전 초기화
if "student_id" not in st.session_state:
    st.session_state.student_id = ""
if "student_name" not in st.session_state:
    st.session_state.student_name = ""
if "user_info_submitted" not in st.session_state:
    st.session_state.user_info_submitted = False

if "quiz_list" not in st.session_state:
    shuffled_list = []
    for category_name, items in RAW_QUIZ_DATA.items():
        category_items = items.copy()
        random.shuffle(category_items)  # 영역 내부 순서만 무작위 섞기
        for item in category_items:
            item_copy = item.copy()
            item_copy["category"] = category_name
            shuffled_list.append(item_copy)
            
    st.session_state.quiz_list = shuffled_list
    st.session_state.current_index = 0
    st.session_state.user_answers = {}
    st.session_state.checked_status = {}
    st.session_state.quiz_finished = False

st.title("✏️ [국어] 표준 발음과 받침의 발음 형성 평가")

# 2. 정보 입력 단계 (시작 화면)
if not st.session_state.user_info_submitted:
    st.subheader("👤 학생 정보를 입력하고 평가를 시작하세요.")
    
    s_id = st.text_input("학번 (예: 10101)", key="input_s_id")
    s_name = st.text_input("이름", key="input_s_name")
    
    if st.button("🚀 평가 시작하기", use_container_width=True):
        if s_id.strip() and s_name.strip():
            st.session_state.student_id = s_id.strip()
            st.session_state.student_name = s_name.strip()
            st.session_state.user_info_submitted = True
            st.rerun()
        else:
            st.warning("⚠️ 학번과 이름을 모두 입력해 주세요!")

# 3. 문제 풀이 단계 (1문제씩 진행 + 즉시 해설)
elif not st.session_state.quiz_finished:
    quiz_list = st.session_state.quiz_list
    total_q = len(quiz_list)
    curr_idx = st.session_state.current_index
    curr_q = quiz_list[curr_idx]

    # 상단 학생 정보 및 진행 상황
    st.caption(f"학생: {st.session_state.student_name} ({st.session_state.student_id})")
    st.progress((curr_idx + 1) / total_q)
    st.write(f"**진행 상황: {curr_idx + 1} / {total_q} 문항**")
    
    # 영역 및 문제 안내
    st.markdown(f"### 📌 {curr_q['category']}")
    st.markdown(f"#### Q{curr_idx + 1}. {curr_q['question']}")

    # 기존 답안 복원
    saved_ans = st.session_state.user_answers.get(curr_q["id"], "")
    
    # 문제 양식
    if curr_q["type"] == "short":
        user_input = st.text_input("정답 입력:", value=saved_ans, key=f"q_input_{curr_q['id']}")
    else:
        opts = curr_q["options"]
        default_idx = opts.index(saved_ans) if saved_ans in opts else None
        user_input = st.radio("알맞은 답 선택:", opts, index=default_idx, key=f"q_input_{curr_q['id']}")

    # 답안 세션 실시간 기록
    if user_input:
        st.session_state.user_answers[curr_q["id"]] = user_input

    st.write("")
    
    # 정답 확인 버튼
    if st.button("🔍 정답 확인 및 해설 보기", key=f"check_btn_{curr_q['id']}"):
        if user_input:
            st.session_state.checked_status[curr_q["id"]] = True
        else:
            st.warning("⚠️ 먼저 정답을 입력하거나 선택해 주세요.")

    # 해설 출력
    if st.session_state.checked_status.get(curr_q["id"], False):
        ans = st.session_state.user_answers.get(curr_q["id"], "")
        correct = curr_q["answer"]
        
        is_correct = (ans.replace(" ", "") == correct.replace(" ", "")) if curr_q["type"] == "short" else (ans == correct)
        
        if is_correct:
            st.success("🎉 **정답입니다!**")
        else:
            st.error(f"❌ **오답입니다.** (내가 낸 답: {ans if ans else '미입력'})")
            st.write(f"👉 **바른 정답:** {correct}")
        
        st.info(f"💡 **교과서 원리 해설:**\n\n{curr_q['explanation']}")

    st.divider()

    # 이전 / 다음 이동 버튼
    btn_col1, btn_col2 = st.columns([1, 1])
    with btn_col1:
        if curr_idx > 0:
            if st.button("⬅️ 이전 문제"):
                st.session_state.current_index -= 1
                st.rerun()
                
    with btn_col2:
        if curr_idx < total_q - 1:
            if st.button("다음 문제 ➡️"):
                st.session_state.current_index += 1
                st.rerun()
        else:
            if st.button("🏁 최종 제출 및 평가 완료"):
                st.session_state.quiz_finished = True
                st.rerun()

# 4. 최종 완료 화면
else:
    st.header(f"📊 {st.session_state.student_name} 학생의 최종 결과")
    quiz_list = st.session_state.quiz_list
    total_q = len(quiz_list)
    score = 0

    for q in quiz_list:
        ans = st.session_state.user_answers.get(q["id"], "")
        correct = q["answer"]
        is_correct = (ans.replace(" ", "") == correct.replace(" ", "")) if q["type"] == "short" else (ans == correct)
        if is_correct:
            score += 1

    final_score = int((score / total_q) * 100)
    st.subheader(f"💯 최종 점수: {final_score}점 ({score} / {total_q} 문항 맞춤)")
    
    if final_score >= 80:
        st.balloons()
        st.success("🎉 수고하셨습니다! 개념을 완벽하게 이해했습니다.")
    else:
        st.warning("📖 수고하셨습니다! 틀렸던 문제의 교과서 해설을 다시 한번 복습해 보세요.")

    if st.button("🔄 다시 풀기"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
