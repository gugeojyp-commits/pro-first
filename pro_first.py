import streamlit as st

st.set_page_config(
    page_title="국어 표준 발음과 받침의 발음 형성 평가",
    page_layout="centered"
)

# 퀴즈 데이터 정의 (교과서 바탕다지기 및 본문 개념 기반)
quiz_data = [
    {
        "id": 1,
        "type": "short",
        "question": "1. 사람마다 발음하는 법이 달라서 [      ]에 지장이 생기는 것을 막기 위해 발음의 표준을 정해 놓은 것을 '표준 발음'이라고 합니다. 빈칸에 들어갈 알맞은 단어를 쓰시오.",
        "answer": "의사소통",
        "explanation": "표준 발음은 국어를 쓰는 사람들 사이에서 발음이 달라 의사소통에 지장이 생기는 것을 막기 위해 정한 약속입니다."
    },
    {
        "id": 2,
        "type": "short",
        "question": "2. 표준 발음은 '표준어의 실제 발음을 따르되, 국어의 전통성과 [      ]을 고려하여 정함을 원칙으로 한다.'에서 빈칸에 들어갈 단어를 쓰시오.",
        "answer": "합리성",
        "explanation": "표준 발음의 3대 원칙은 ① 표준어의 실제 발음, ② 국어의 전통성, ③ 합리성입니다."
    },
    {
        "id": 3,
        "type": "choice",
        "question": "3. 다음 중 표준 발음의 원칙에 대한 설명으로 알맞은 것을 고르세요.",
        "options": [
            "1. 현실 발음에서 모음의 장단(길이)이 구별되지 않으므로, 장단 구분 규정은 전통성을 고려해 마련되어 있다.",
            "2. 'ㅢ'는 항상 예외 없이 단하나의 발음인 [ㅢ]로만 발음해야 한다."
        ],
        "answer": "1. 현실 발음에서 모음의 장단(길이)이 구별되지 않으므로, 장단 구분 규정은 전통성을 고려해 마련되어 있다.",
        "explanation": "현실 발음에서 모음의 장단이 잘 구별되지 않더라도 오랜 기간 뜻을 변별해 온 역사성을 고려하여 '전통성' 측면에서 장단 규정을 두고 있습니다. ('ㅢ'는 조건에 따라 [ㅣ], [ㅔ] 발음도 허용됩니다.)"
    },
    {
        "id": 4,
        "type": "short",
        "question": "4. 어말이나 자음 앞에서 'ㅅ, ㅆ, ㅈ, ㅊ, ㅌ, ㅎ' 받침이 바뀐 대표음 한 글자를 쓰시오.",
        "answer": "ㄷ",
        "explanation": "음절의 끝소리 규칙에 따라 ㅅ, ㅆ, ㅈ, ㅊ, ㅌ, ㅎ은 모두 대표음 [ㄷ]으로 바뀌어 발음됩니다."
    },
    {
        "id": 5,
        "type": "choice",
        "question": "5. 홑받침이나 쌍받침 뒤에 '모음으로 시작하는 형식 형태소(조사, 어미, 접사)'가 연결될 때의 발음 원칙은?",
        "options": [
            "1. 대표음으로 바꾼 뒤 뒤 음절 첫소리로 옮겨 발음한다.",
            "2. 대표음으로 바꾸지 않고 제 음가대로 뒤 음절 첫소리로 옮겨 발음한다(연음)."
        ],
        "answer": "2. 대표음으로 바꾸지 않고 제 음가대로 뒤 음절 첫소리로 옮겨 발음한다(연음).",
        "explanation": "형식 형태소가 올 때는 음절의 끝소리 규칙을 적용하지 않고 받침 제 음가대로 넘겨 발음(연음)합니다. (예: 꽃이 -> [꼬치])"
    },
    {
        "id": 6,
        "type": "choice",
        "question": "6. 홑받침이나 쌍받침 뒤에 '모음으로 시작하는 실질 형태소'가 올 때는 받침을 무엇으로 바꾸어서 뒤 음절의 첫소리로 옮겨 발음하나요?",
        "options": ["1. 대표음", "2. 기본형"],
        "answer": "1. 대표음",
        "explanation": "뜻을 가진 실질 형태소가 뒤에 오면, 먼저 받침을 7개 대표음 중 하나로 바꾼 뒤에 연음시킵니다."
    },
    {
        "id": 7,
        "type": "choice",
        "question": "7. 그 사람은 얼굴에서 빛이 [ 1. 비시 / 2. 비치 ] 난다.",
        "options": ["1. 비시", "2. 비치"],
        "answer": "2. 비치",
        "explanation": "'이'는 모음으로 시작하는 형식 형태소(조사)이므로, 'ㅊ' 받침을 대표음으로 바꾸지 않고 제 음가대로 연음하여 [비치]로 발음합니다."
    },
    {
        "id": 8,
        "type": "choice",
        "question": "8. 등산을 했더니 무릎이 [ 1. 무르비 / 2. 무르피 ] 아프다.",
        "options": ["1. 무르비", "2. 무르피"],
        "answer": "2. 무르피",
        "explanation": "'이'는 조사(형식 형태소)이므로 'ㅍ' 받침이 제 음가대로 연음되어 [무르피]가 됩니다."
    },
    {
        "id": 9,
        "type": "choice",
        "question": "9. 이 소설의 끝을 [ 1. 끄슬 / 2. 끄츨 / 3. 끄틀 ] 다시 써 보려 해.",
        "options": ["1. 끄슬", "2. 끄츨", "3. 끄틀"],
        "answer": "3. 끄틀",
        "explanation": "'을'은 조사(형식 형태소)이므로 'ㅌ' 받침을 그대로 연음하여 [끄틀]로 발음합니다."
    },
    {
        "id": 10,
        "type": "choice",
        "question": "10. 꽃 아래 [ 1. 꼬다래 / 2. 꼬사래 / 3. 꼬차래 ] 그늘이 있다.",
        "options": ["1. 꼬다래", "2. 꼬사래", "3. 꼬차래"],
        "answer": "1. 꼬다래",
        "explanation": "'아래'는 뜻을 가진 실질 형태소입니다. 따라서 '꽃'의 'ㅊ'을 먼저 대표음 [ㄷ]으로 바꾸고 연음시켜 [꼬다래]로 발음합니다."
    },
    {
        "id": 11,
        "type": "choice",
        "question": "11. 나는 빵을 매우 좋아한다 [ 1. 조아한다 / 2. 조하한다 ].",
        "options": ["1. 조아한다", "2. 조하한다"],
        "answer": "1. 조아한다",
        "explanation": "받침 'ㅎ' 뒤에 모음으로 시작하는 형식 형태소가 오면 'ㅎ'은 발음되지 않고 탈락하므로 [조아한다]가 맞습니다."
    },
    {
        "id": 12,
        "type": "short",
        "question": "12. 음절 끝에 두 개의 자음이 놓일 때, 둘 중 하나의 자음만 남고 나머지 자음은 탈락하는 음운 현상의 명칭을 쓰시오.",
        "answer": "자음군 단순화",
        "explanation": "겹받침이 어말이나 자음 앞에서 하나만 발음되고 하나는 탈락하는 현상을 '자음군 단순화'라고 합니다."
    },
    {
        "id": 13,
        "type": "choice",
        "question": "13. 이 선을 밟지 [ 1. 발찌 / 2. 밥찌 ] 마라.",
        "options": ["1. 발찌", "2. 밥찌"],
        "answer": "2. 밥찌",
        "explanation": "겹받침 'ㄼ'은 대부분 [ㄹ]로 발음되지만, 동사 '밟-'은 자음 앞에서 예외적으로 [밥-]으로 발음하므로 [밥찌]가 맞습니다."
    },
    {
        "id": 14,
        "type": "choice",
        "question": "14. 강당은 교실보다 넓다 [ 1. 넙따 / 2. 널따 ].",
        "options": ["1. 넙따", "2. 널따"],
        "answer": "2. 널따",
        "explanation": "겹받침 'ㄼ'의 원칙적인 발음은 [ㄹ]이므로 [널따]가 맞습니다."
    },
    {
        "id": 15,
        "type": "choice",
        "question": "15. 오늘은 날씨가 어제보다 맑다 [ 1. 막따 / 2. 말따 ].",
        "options": ["1. 막따", "2. 말따"],
        "answer": "1. 막따",
        "explanation": "겹받침 'ㄺ'은 어말이나 자음 앞에서 대표음 [ㄱ]으로 발음하므로 [막따]가 맞습니다."
    },
    {
        "id": 16,
        "type": "choice",
        "question": "16. 밥값은 [ 1. 밥깝슨 / 2. 밥까븐 ] 누가 내는 거냐?",
        "options": ["1. 밥깝슨", "2. 밥까븐"],
        "answer": "1. 밥깝슨",
        "explanation": "'은'은 조사(형식 형태소)입니다. 겹받침 'ㅄ'에서 첫째 받침 'ㅂ'은 남고, 둘째 받침 'ㅅ'이 연음되어 된소리 [ㅆ]으로 발음되므로 [밥깝슨]이 맞습니다."
    },
    {
        "id": 17,
        "type": "choice",
        "question": "17. 흙 위에 [ 1. 흘귀에 / 2. 흐귀에 / 3. 흙위에 ] 쏟아졌다.",
        "options": ["1. 흘귀에", "2. 흐귀에", "3. 흙위에"],
        "answer": "1. 흘귀에",
        "explanation": "'위'는 실질 형태소이므로 겹받침 'ㄺ'에서 자음군 단순화가 일어나 대표음 [ㄱ]이 남고, 이것이 연음되어 [흘귀에]가 됩니다."
    },
    {
        "id": 18,
        "type": "choice",
        "question": "18. 하늘에 구름이 많아서 [ 1. 마나서 / 2. 만하서 ] 달을 못 보았다.",
        "options": ["1. 마나서", "2. 만하서"],
        "answer": "1. 마나서",
        "explanation": "겹받침 'ㄶ' 뒤에 모음으로 시작하는 어미 '-아서'가 오면 'ㅎ'이 탈락하고 'ㄴ'만 넘어가 [마나서]로 발음됩니다."
    }
]

# 화면 헤더
st.title("✏️ [국어] 표준 발음과 받침의 발음 형성 평가")
st.caption("수업 내용을 바탕으로 크롬북을 활용해 답안을 제출해 주세요. (제출 후 해설 확인 가능)")

# 학생 정보 입력 섹션
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        student_id = st.text_input("학번 (예: 10101)", key="student_id")
    with col2:
        student_name = st.text_input("이름", key="student_name")

st.divider()

# 폼 생성
with st.form("quiz_form"):
    user_answers = {}
    
    for item in quiz_data:
        st.markdown(f"#### {item['question']}")
        
        if item["type"] == "short":
            user_answers[item["id"]] = st.text_input(
                "정답을 입력하세요:", 
                key=f"q_{item['id']}"
            ).strip()
        elif item["type"] == "choice":
            user_answers[item["id"]] = st.radio(
                "알맞은 답을 선택하세요:", 
                options=item["options"], 
                index=None,
                key=f"q_{item['id']}"
            )
        st.write("---")
        
    submitted = st.form_submit_button("📝 형성 평가 제출하기", use_container_width=True)

# 결과 제출 처리 및 자동 채점
if submitted:
    if not student_id or not student_name:
        st.warning("⚠️ 학번과 이름을 반드시 입력해 주세요!")
    else:
        score = 0
        total = len(quiz_data)
        
        st.header(f"📊 {student_name} 학생의 평가 결과")
        
        for item in quiz_data:
            q_id = item["id"]
            user_ans = user_answers.get(q_id)
            correct_ans = item["answer"]
            
            is_correct = False
            if user_ans:
                if item["type"] == "short":
                    is_correct = (user_ans.replace(" ", "") == correct_ans.replace(" ", ""))
                else:
                    is_correct = (user_ans == correct_ans)
            
            if is_correct:
                score += 1
                st.success(f"**문항 {q_id}: 정답입니다! ⭕**")
            else:
                st.error(f"**문항 {q_id}: 오답입니다. ❌**")
                st.write(f"- **제출한 답:** {user_ans if user_ans else '미입력'}")
                st.write(f"- **바른 정답:** {correct_ans}")
            
            with st.expander("💡 교과서 개념 해설 보기"):
                st.info(item["explanation"])
            st.write("")
        
        final_score = int((score / total) * 100)
        st.metric(label="최종 점수", value=f"{final_score}점 / 100점", delta=f"{score}개 맞춤 ({total}문항 중)")
        
        if final_score >= 80:
            st.balloons()
            st.success("🎉 참 잘했습니다! 개념을 아주 잘 이해하고 있네요.")
        else:
            st.warning("📖 틀린 문제의 교과서 해설을 다시 읽고 복습해 보세요!")