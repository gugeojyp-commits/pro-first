import random
import requests
import json
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="국어 표준 발음 평가",
    page_icon="✏️",
    layout="centered"
)

# -----------------------------------------------------------------------------
# ⚠️ [필수] 이전 세션(40문항 및 깨진 CSS) 강제 박멸 루틴
# -----------------------------------------------------------------------------
APP_VERSION = "v30_clean_final"
if st.session_state.get("app_version") != APP_VERSION:
    st.session_state.clear()
    st.session_state.app_version = APP_VERSION

# -----------------------------------------------------------------------------
# 🔗 [설정] 구글 시트 배포 URL 및 교사용 테스트 비밀번호
# -----------------------------------------------------------------------------
GOOGLE_SHEET_WEBAPP_URL = "https://script.google.com/macros/sAKfycbymuGKCOqviCjqn3PEab4ubtf_m5cf1Gj184kGTgFqm0nBrOSKX7_oc9V_Wjv73AbGTAA/exec"
TEACHER_PASSWORD = "01063052122"

# -----------------------------------------------------------------------------
# 📚 원본 퀴즈 데이터 (정확히 30문항 고정)
# -----------------------------------------------------------------------------
RAW_QUIZ_DATA = {
    "1. 표준 발음의 개념과 원칙": [
        {
            "id": 1,
            "type": "short",
            "question": "사람마다 발음하는 법이 달라서 [     ]에 지장이 생기는 것을 막기 위해 발음의 표준을 정해 놓은 것을 '표준 발음'이라고 합니다. 빈칸에 들어갈 알맞은 단어를 쓰시오. (띄어쓰기 없이 작성할 것)",
            "answer": "의사소통",
            "explanation": "표준 발음은 국어를 쓰는 사람들 사이에서 발음이 달라 의사소통에 지장이 생기는 것을 막기 위해 정한 약속입니다."
        },
        {
            "id": 2,
            "type": "short",
            "question": "표준 발음은 '표준어의 실제 발음을 따르되, 국어의 전통성과 [     ]을 고려하여 정함을 원칙으로 한다.'에서 빈칸에 들어갈 단어를 쓰시오.",
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
        },
        {
            "id": 101,
            "type": "choice",
            "question": "자음을 첫소리로 가지고 있는 음절의 'ㅢ'는 어떻게 발음하는 것이 원칙인가요? (희망, 무늬)",
            "options": [
                "1. [ㅢ]로만 발음해야 한다.",
                "2. [ㅣ]로 발음한다."
            ],
            "answer": "2. [ㅣ]로 발음한다.",
            "explanation": "자음을 첫소리로 가지고 있는 음절의 'ㅢ'는 [ㅣ]로 발음합니다. (희망[히망], 무늬[무니])"
        },
        {
            "id": 102,
            "type": "choice",
            "question": "단어의 첫음절 이외의 'ㅢ' 발음 규정으로 올바른 것은? (주의, 협의)",
            "options": [
                "1. 원칙적으로 [ㅢ]로 발음하되, [ㅣ]로 발음함도 허용한다.",
                "2. 원칙적으로 [ㅣ]로 발음하되, [ㅢ]로 발음함도 허용한다."
            ],
            "answer": "1. 원칙적으로 [ㅢ]로 발음하되, [ㅣ]로 발음함도 허용한다.",
            "explanation": "첫음절 이외의 'ㅢ'는 원칙적으로 [ㅢ]로 발음하지만 현실 발음을 고려하여 [ㅣ]로 발음하는 것도 허용합니다. (주의[주의/주이])"
        },
        {
            "id": 103,
            "type": "choice",
            "question": "조사 '의'의 발음 규정으로 올바른 것은? (예: 우리의)",
            "options": [
                "1. 원칙적으로 [ㅢ]로 발음하되, [ㅔ]로 발음함도 허용한다.",
                "2. 원칙적으로 [ㅔ]로 발음하되, [ㅢ]로 발음함도 허용한다."
            ],
            "answer": "1. 원칙적으로 [ㅢ]로 발음하되, [ㅔ]로 발음함도 허용한다.",
            "explanation": "조사 '의'는 원칙적으로 [ㅢ]로 발음하되, [ㅔ]로 발음하는 것도 허용합니다. (예: 우리의[우리의/우리에])"
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
            "type": "short",
            "question": "홑받침이나 쌍받침 뒤에 '모음으로 시작하는 실질 형태소'가 올 때는 받침을 [        ]으로 바꾸어서 뒤 음절의 첫소리로 옮겨 발음합니다. 빈칸에 들어갈 알맞은 단어를 쓰시오.",
            "answer": "대표음",
            "explanation": "뜻을 가진 실질 형태소가 뒤에 오면, 먼저 받침을 7개 대표음(ㄱ,ㄴ,ㄷ,ㄹ,ㅁ,ㅂ,ㅇ) 중 하나로 바꾼 뒤에 연음시킵니다."
        },
        {
            "id": 104,
            "type": "short",
            "question": "단어 '낮', '낯', '낱'의 실제 발음을 순서대로 적으시오.",
            "answer": ["낟,낟,낟", "낟, 낟, 낟"], 
            "explanation": "'낮', '낯', '낱'은 모두 어말에서 음절의 끝소리 규칙이 적용되어 대표음 [ㄷ]으로 동일하게 발음됩니다. [낟], [낟], [낟]"
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
            "id": 105,
            "type": "choice",
            "question": "'맛있다'의 표준 발음으로 올바른 설명을 고르세요.",
            "options": [
                "1. 실질 형태소 '있다'가 결합하므로 원칙 발음 [마디따]와 현실 발음을 고려한 [마시따] 둘 다 표준 발음이다.",
                "2. 형식 형태소가 결합한 것이므로 [마시따]만 표준 발음으로 인정된다."
            ],
            "answer": "1. 실질 형태소 '있다'가 결합하므로 원칙 발음 [마디따]와 현실 발음을 고려한 [마시따] 둘 다 표준 발음이다.",
            "explanation": "'있다'는 실질 형태소이므로 대표음 [ㄷ]으로 바꾼 [마디따]가 원칙이나, 현실 발음에서 많이 쓰는 [마시따]도 표준 발음으로 함께 허용합니다."
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
            "answer": ["자음군 단순화", "자음군단순화"],
            "explanation": "겹받침이 어말이나 자음 앞에서 하나만 발음되고 하나는 탈락하는 현상을 '자음군 단순화'라고 합니다."
        },
        {
            "id": 112,
            "type": "short",
            "question": "우리 국어 선생님은 늘 시조를 한 수 읊고 시작하십니다. '읊고'의 올바른 표준 발음을 쓰시오.",
            "answer": "읍꼬",
            "explanation": "겹받침 'ㄿ'은 어말이나 자음 앞에서 대표음 [ㅂ]으로 발음되므로 '읊고'는 [읍꼬]가 맞습니다. (예: 읊다[읍따], 읊고[읍꼬])"
        },
        {
            "id": 106,
            "type": "short",
            "question": "'닭이'의 올바른 표준 발음을 쓰시오.",
            "answer": "달기",
            "explanation": "모음으로 시작하는 형식 형태소(조사 '이')가 오면 겹받침 'ㄺ' 중 첫째 받침 [ㄹ]은 남고 둘째 받침 [ㄱ]이 넘어가 [달기]로 발음합니다."
        },
        {
            "id": 107,
            "type": "short",
            "question": "'외곬'의 올바른 표준 발음을 쓰시오.",
            "answer": "외골",
            "explanation": "겹받침 'ㄽ'은 어말이나 자음 앞에서 'ㅅ'이 탈락하고 [ㄹ]로 발음되므로 [외골]이 맞습니다."
        },
        {
            "id": 108,
            "type": "short",
            "question": "'읽다'와 '읽고'의 올바른 표준 발음을 순서대로 적으시오.",
            "answer": ["익따, 일꼬", "익따,일꼬", "'익따', '일꼬'", "'익따','일꼬'"],
            "explanation": "'읽다'의 겹받침 'ㄺ'은 자음 앞에서 [ㄱ]으로 발음되어 [익따]가 되고, '읽고'처럼 뒤에 'ㄱ'으로 시작하는 어미가 오면 [ㄹ]로 발음되어 [일꼬]가 됩니다."
        },
        {
            "id": 109,
            "type": "short",
            "question": "'닳아'의 올바른 표준 발음을 쓰시오.",
            "answer": "달아",
            "explanation": "겹받침 'ㅀ' 뒤에 모음으로 시작하는 형식 형태소(어미 '-아')가 오면 'ㅎ'이 탈락하여 [달아]로 발음됩니다."
        },
        {
            "id": 110,
            "type": "short",
            "question": "'값있는'의 올바른 표준 발음을 쓰시오.",
            "answer": "가빈는",
            "explanation": "실질 형태소 '있는' 앞에서 겹받침 'ㅄ'이 자음군 단순화로 대표음 [ㅂ]이 된 후, 뒤의 '있는'과 만나 음운 변동(비음화)을 거쳐 [가빈는]으로 발음됩니다."
        },
        {
            "id": 111,
            "type": "short",
            "question": "'닭 앞에'의 올바른 표준 발음을 쓰시오. (띄어쓰기 없이 작성할 것)",
            "answer": "다가페",
            "explanation": "실질 형태소 '앞'이 올 때는 겹받침 'ㄺ'이 자음군 단순화로 대표음 [ㄱ]이 되어 연음[다가]되고, 조사 '에' 앞에서 'ㅍ'이 연음되어 최종 발음은 [다가페]가 됩니다."
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
            "question": "밥값은 [ 1. 밥깝쓴 / 2. 밥까븐 ] 누가 내는 거냐?",
            "options": ["1. 밥깝쓴", "2. 밥까븐"],
            "answer": "1. 밥깝쓴",
            "explanation": "'은'은 조사(형식 형태소)입니다. 겹받침 'ㅄ'에서 첫째 받침 'ㅂ'은 남고, 둘째 받침 'ㅅ'이 연음되어 된소리 [ㅆ]으로 발음되므로 [밥깝쓴]이 맞습니다."
        },
        {
            "id": 17,
            "type": "choice",
            "question": "흙 위에 [ 1. 흘귀에 / 2. 흐귀에 ] 쏟아졌다.",
            "options": ["1. 흘귀에", "2. 흐귀에"],
            "answer": "2. 흐귀에",
            "explanation": "'위'는 실질 형태소이므로 겹받침 'ㄺ'에서 자음군 단순화가 일어나 대표음 [ㄱ]이 남고, 이것이 연음되어 [흐귀에]가 됩니다."
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

def clean_text(text):
    if isinstance(text, list):
        return [t.replace(" ", "").replace("[", "").replace("]", "").replace(".", ",").replace("/", ",") for t in text]
    return text.replace(" ", "").replace("[", "").replace("]", "").replace(".", ",").replace("/", ",")

# -----------------------------------------------------------------------------
# 1. 초기 퀴즈 데이터 세팅
# -----------------------------------------------------------------------------
def reset_full_quiz():
    shuffled_list = []
    for category_name, items in RAW_QUIZ_DATA.items():
        category_items = items.copy()
        random.shuffle(category_items)
        for item in category_items:
            item_copy = item.copy()
            item_copy["category"] = category_name
            shuffled_list.append(item_copy)
            
    st.session_state.quiz_list = shuffled_list
    st.session_state.current_index = 0
    st.session_state.user_answers = {}
    st.session_state.passed_status = {}
    st.session_state.checked_status = {}
    st.session_state.first_attempt_status = {}
    st.session_state.quiz_finished = False
    st.session_state.sheet_submitted = False

if "student_id" not in st.session_state:
    st.session_state.student_id = ""
if "student_name" not in st.session_state:
    st.session_state.student_name = ""
if "user_info_submitted" not in st.session_state:
    st.session_state.user_info_submitted = False

if "quiz_list" not in st.session_state or len(st.session_state.quiz_list) != 30:
    reset_full_quiz()

st.title("✏️ [국어] 표준 발음과 받침 형성 평가")

# -----------------------------------------------------------------------------
# 2. 학생 정보 입력 단계
# -----------------------------------------------------------------------------
if not st.session_state.user_info_submitted:
    st.subheader("👤 학생 정보 입력")
    st.write("학번과 이름을 입력하고 시작하세요. (총 30문항)")
    
    s_id = st.text_input("학번을 입력하세요 (예: 20101)", key="input_s_id")
    s_name = st.text_input("이름을 입력하세요", key="input_s_name")
    
    if st.button("🚀 평가 시작하기", use_container_width=True):
        if s_id.strip() and s_name.strip():
            st.session_state.student_id = s_id.strip()
            st.session_state.student_name = s_name.strip()
            st.session_state.user_info_submitted = True
            st.rerun()
        else:
            st.warning("⚠️ 학번과 이름을 모두 입력해 주세요!")

# -----------------------------------------------------------------------------
# 3. 개별 문제 풀이 단계
# -----------------------------------------------------------------------------
elif not st.session_state.quiz_finished:
    quiz_list = st.session_state.quiz_list
    total_q = len(quiz_list)
    curr_idx = st.session_state.current_index
    curr_q = quiz_list[curr_idx]

    col_info, col_prog = st.columns([1, 1])
    with col_info:
        st.write(f"👤 **학생:** {st.session_state.student_name} ({st.session_state.student_id})")
    with col_prog:
        st.write(f"🎯 **진행:** {curr_idx + 1} / {total_q} 문항")
    
    st.progress((curr_idx + 1) / total_q)
    st.write("")

    # 1번 문제에서 바로 교사용 점프 기능 제공
    if curr_idx == 0:
        c1, c2 = st.columns([3, 1])
        with c1:
            pw_input = st.text_input("교사 비밀번호", type="password", key="quick_admin_pw", label_visibility="collapsed", placeholder="교사 비밀번호 입력시 바로 결과 확인")
        with c2:
            if st.button("결과화면 점프", key="quick_jump_btn", use_container_width=True):
                if pw_input == TEACHER_PASSWORD:
                    st.session_state.quiz_finished = True
                    st.rerun()
                else:
                    st.error("비밀번호 불일치")
        st.write("---")

    # 문제 카드 영역
    st.caption(f"📌 {curr_q['category']}")
    st.subheader(f"Q{curr_idx + 1}. {curr_q['question']}")

    saved_ans = st.session_state.user_answers.get(curr_q["id"], "")
    
    if curr_q["type"] == "short":
        user_input = st.text_input("정답 입력:", value=saved_ans, placeholder="답을 작성하세요...", key=f"q_input_{curr_q['id']}")
    else:
        opts = curr_q["options"]
        default_idx = opts.index(saved_ans) if saved_ans in opts else None
        user_input = st.radio("알맞은 답 선택:", opts, index=default_idx, key=f"q_input_{curr_q['id']}", label_visibility="collapsed")

    st.write("")

    if st.button("🔍 정답 확인 및 해설 보기", key=f"check_btn_{curr_q['id']}", use_container_width=True):
        if user_input:
            st.session_state.user_answers[curr_q["id"]] = user_input
            st.session_state.checked_status[curr_q["id"]] = True
            
            correct = curr_q["answer"]
            if curr_q["type"] == "short":
                cleaned_user = clean_text(user_input)
                cleaned_correct = clean_text(correct)
                is_correct = (cleaned_user in cleaned_correct) if isinstance(cleaned_correct, list) else (cleaned_user == cleaned_correct)
            else:
                is_correct = (user_input == correct)
            
            if curr_q["id"] not in st.session_state.first_attempt_status:
                st.session_state.first_attempt_status[curr_q["id"]] = is_correct

            st.session_state.passed_status[curr_q["id"]] = is_correct
            st.rerun()
        else:
            st.warning("⚠️ 먼저 정답을 입력하거나 선택해 주세요.")

    if st.session_state.checked_status.get(curr_q["id"], False):
        ans = st.session_state.user_answers.get(curr_q["id"], "")
        is_passed = st.session_state.passed_status.get(curr_q["id"], False)
        
        if is_passed:
            st.success("🎉 **정답입니다! 통과하셨습니다.**")
        else:
            st.error(f"❌ **오답입니다. 해설을 확인하고 정답을 맞춰 다음으로 이동하세요.** (내가 낸 답: {ans})")
        
        st.info(f"💡 **교과서 원리 해설:**\n\n{curr_q['explanation']}")

        st.write("")
        if st.session_state.passed_status.get(curr_q["id"], False):
            if curr_idx < total_q - 1:
                if st.button("➡️ 다음 문제로 이동", use_container_width=True):
                    st.session_state.current_index += 1
                    st.rerun()
            else:
                if st.button("🏁 모든 문제 완료! 최종 결과 확인하기", use_container_width=True):
                    st.session_state.quiz_finished = True
                    st.rerun()
        else:
            st.caption("🔒 **정답을 맞혀야 다음 문제로 넘어갈 수 있습니다.**")

# -----------------------------------------------------------------------------
# 4. 최종 완료 화면
# -----------------------------------------------------------------------------
else:
    wrong_q_list = [q for q in st.session_state.quiz_list if not st.session_state.first_attempt_status.get(q["id"], False)]
    total_count = len(st.session_state.quiz_list)
    correct_count = total_count - len(wrong_q_list)
    wrong_ids_str = ", ".join([str(q["id"]) for q in wrong_q_list]) if wrong_q_list else "없음"

    if st.session_state.student_id and not st.session_state.get("sheet_submitted", False):
        payload = {
            "student_id": st.session_state.student_id,
            "student_name": st.session_state.student_name,
            "score": correct_count,
            "total": total_count,
            "wrong_questions": wrong_ids_str
        }
        try:
            res = requests.post(
                GOOGLE_SHEET_WEBAPP_URL,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            if res.status_code == 200:
                st.session_state.sheet_submitted = True
        except Exception:
            pass

    st.balloons()
    st.header(f"🎉 {st.session_state.student_name or '선생님'} 님, 평가 완료!")
    st.subheader(f"첫 시도 정답: {total_count}문항 중 {correct_count}개")
    st.write("평가 결과는 **선생님 기록부에 자동 저장**되었습니다.")
    st.write("---")

    tab1, tab2 = st.tabs(["📊 나의 결과 & 오답노트", f"📚 전체 {total_count}문항 한눈에 다시 보기"])

    with tab1:
        if len(wrong_q_list) > 0:
            st.warning(f"⚠️ 처음 시도에서 틀렸던 문제가 **{len(wrong_q_list)}개** 있습니다.")
            if st.button("🔥 처음 틀렸던 문제만 오답노트로 다시 풀기", use_container_width=True):
                st.session_state.quiz_list = wrong_q_list.copy()
                st.session_state.current_index = 0
                st.session_state.user_answers = {}
                st.session_state.passed_status = {}
                st.session_state.checked_status = {}
                st.session_state.first_attempt_status = {}
                st.session_state.quiz_finished = False
                st.session_state.sheet_submitted = True
                st.rerun()
        else:
            st.success("💯 첫 번째 시도에서 모든 문제를 완벽하게 맞혔습니다!")

        st.write("")
        with st.expander("🔄 처음부터 전체 문제 다시 시작하기"):
            if st.button("초기화 후 새로 시작하기", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

    with tab2:
        st.info(f"💡 전체 {total_count}개 문항을 자율적으로 다시 연습하고, 아래 [정답 및 해설]을 열어 확인하세요.")
        
        all_questions = []
        for cat, items in RAW_QUIZ_DATA.items():
            for item in items:
                all_questions.append((cat, item))

        for idx, (category_name, q) in enumerate(all_questions):
            st.write(f"**[{category_name}] {idx + 1}. {q['question']}**")
            
            if q["type"] == "short":
                st.text_input("답안 연습:", placeholder="답안을 직접 적어보세요...", key=f"all_view_input_{q['id']}")
            else:
                st.radio("답안 연습:", q["options"], index=None, key=f"all_view_opt_{q['id']}", label_visibility="collapsed")
            
            with st.expander(f"Q{idx + 1} 정답 및 해설 확인"):
                ans_display = q['answer'] if isinstance(q['answer'], str) else q['answer'][0]
                st.write(f"**정답:** `{ans_display}`")
                st.write(f"**💡 해설:** {q['explanation']}")
            st.write("---")
