import streamlit as st
import save

# 실험 설명 페이지 함수
def intro_page():
    st.title("실험 참여 안내 🌟")
    st.divider()  # 구분선
    
    # 실험 설명 블록
    intro_explanation_block()
    
    # 개인정보 입력
    with st.form("personal_info_form"):
        user_name, user_age, user_gender, education_level, familiar_fields, additional_info = personal_information_block()
        submitted = st.form_submit_button("제출 🚀")
        
        if submitted:
            # 필수 항목 검증
            if user_name and user_age and user_gender and education_level:
                # 세션 상태에 데이터 저장
                st.session_state["personal_info"] = {
                    "name": user_name,
                    "age": user_age,
                    "gender": user_gender,
                    "education_level": education_level,
                    "familiar_fields": familiar_fields,
                    "additional_info": additional_info
                }
                st.success("정보가 성공적으로 제출되었습니다. 다음 세션으로 넘어가 주세요!")
            else:
                st.error("모든 필수 항목을 입력해주세요.")
    
    # 다음 세션으로 진행 버튼
    if st.button("다음 세션으로 진행 ➡️"):
        st.session_state["page"] = "experiment"


# 실험 설명 블록
def intro_explanation_block():
    st.subheader("실험 개요")
    st.markdown(
        """
        안녕하세요! 이번 실험에 참여해 주셔서 감사합니다.  
        이 실험은 **자연어 처리(NLP) 모델**을 활용하여 사람들이 익숙하지 않은 분야의 복잡한 텍스트를 보다 효과적으로 이해할 수 있도록 돕는 방법을 연구하기 위한 것입니다.

        ### 실험 목적
        - 복잡한 텍스트를 간단한 설명으로 이해도를 높이는 방식을 연구합니다.
        - 중요한 개념을 유지하며 이해하기 쉽게 만드는 것이 목표입니다.

        ### 실험 절차
        1. 복잡한 개념이 포함된 문장을 읽습니다.
        2. 제공된 간소화된 설명을 읽습니다.
        3. 각 텍스트에 대해 이해도와 만족도를 평가합니다.

        ### 예상 소요 시간
        - 약 15~20분  
        - 실험은 총 20개의 문장으로 구성되어 있습니다.

        **참고:**  
        - 실험은 익명으로 진행되며, 모든 데이터는 연구 목적으로만 사용됩니다.  
        - 중간에 실험을 종료하고 싶으시면 언제든 종료하실 수 있습니다.  
        """,
        unsafe_allow_html=False
    )

# 개인정보 입력 블록
def personal_information_block():
    user_name = st.text_input("*이름:", placeholder="예: 홍길동")
    user_age = st.number_input("*나이:", min_value=10, max_value=100, value=20)
    user_gender = st.radio("*성별:", ["남성", "여성", "기타"], horizontal=True)
    education_level = st.selectbox(
        "*최종 학력:",
        ["고등학교 졸업", "대학교 졸업", "대학원 석사 졸업", "대학원 박사 졸업"]
    )
    familiar_fields = st.multiselect(
        "잘 알고 있는 분야를 선택하세요:",
        ["음식과 음료", "공연 예술", "비즈니스와 경제", "정치와 정부", "생물학", "화학", "컴퓨팅", "지구와 환경", "수학", "의학과 건강", "물리학", "공학", "기술"]
    )
    additional_info = st.text_area("추가 정보:", placeholder="본인의 관심 분야나 특기 사항 등을 입력해주세요.")
    return user_name, user_age, user_gender, education_level, familiar_fields, additional_info

example = {
    "concept": "Hyperaemia",
    "difficult_term": "blood",
    "definition": "Hyperaemia is the increase of blood flow to different tissues in the body.",
    "rewrite": "Blood flow increases to different parts of the body."
}

def experiment_page():
    st.title("실험 진행 🧠")
    st.divider()  # 구분선
    
    # 실험 설명
    experiment_explanation_block()
    
    # 개별 실험 수행
    if "experiment_num" not in st.session_state:
        st.session_state["experiment_num"] = 1
        st.session_state["responses"] = []

    experiment_num = st.session_state["experiment_num"]

    if experiment_num <= 20:
        example = {
            "concept": "Hyperaemia",
            "difficult term": "blood",
            "definition": "Hyperaemia is the increase of blood flow to different tissues in the body.",
            "rewrite": "Blood flow increases to different parts of the body."
        }
        experiment_block(example)
        
        # 다음 실험으로 진행 버튼
        if st.button("다음 실험으로 진행 ➡️"):
            st.session_state["experiment_num"] += 1
    else:
        st.session_state["page"] = "completion"
        st.success("실험이 완료되었습니다! 완료 페이지로 이동합니다.")
        st.button("완료 페이지로 이동")


def experiment_explanation_block():
    st.subheader("정의 이해도 평가")
    st.markdown(
        "아래는 특정 개념과 그 정의를 포함한 텍스트입니다. 원본 정의와 간소화된 정의를 비교하고, 각 질문에 답변해 주세요."
    )

def experiment_block(example):
    # 실험 번호 추적
    if "experiment_num" not in st.session_state:
        st.session_state["experiment_num"] = 1
        st.session_state["responses"] = []

    experiment_num = st.session_state["experiment_num"]

    if experiment_num <= 20:
        st.subheader(f"실험 {experiment_num}번째")
        
        # 개념 및 정의 표시
        st.markdown(f"**Concept**: {example['concept']}")
        st.markdown(f"**Difficult term**: {example['difficult term']}")
        st.markdown(f"**ORIGINAL**: {example['definition']}")
        st.markdown(f"**REWRITE**: {example['rewrite']}")
        
        # 질문 처리
        Hmp, Hru, Hre = question_block(experiment_num)
        
        # 실험이 끝난 후 응답을 세션에 저장
        if st.button("다음 실험으로 진행"):
            st.session_state["responses"].append({
                "experiment_num": experiment_num,
                "concept": example["concept"],
                "difficult_term": example["difficult term"],
                "original_definition": example["definition"],
                "rewrite_definition": example["rewrite"],
                "Hmp": Hmp, 
                "Hru": Hru, 
                "Hre": Hre,
            })
            st.session_state["experiment_num"] += 1

    if experiment_num > 20:
        st.session_state["page"] = "completion"  # 페이지 상태 업데이트
        st.write("실험이 완료되었습니다! 완료 페이지로 이동합니다.")
        st.button("완료 페이지로 이동")


def question_block(experiment_num):
    # Q1. Hmp (Meaning Preservation)
    Hmp = st.radio(
        "1. 수정된 정의가 원본 정의의 의미를 얼마나 보존하고 있습니까?",
        options=[1, 2, 3, 4, 5],  # 숫자만 저장되도록 설정
        format_func=lambda x: f"{x}: " + (
            "전혀 보존되지 않음" if x == 1 else
            "조금 보존됨" if x == 2 else
            "보통" if x == 3 else
            "대부분 보존됨" if x == 4 else
            "완벽하게 보존됨"
        ),
        key=f"Hmp_{experiment_num}"
    )

    # Q2. Hru (Rewrite Understanding)
    Hru = st.radio(
        "2. 수정된 정의를 이해한 사람이 원래의 어려운 개념을 알지 못한다고 해도, 수정된 정의를 이해할 수 있을까요?",
        options=[1, 0],  # 숫자로 옵션 설정
        format_func=lambda x: "예" if x == 1 else "아니오",
        key=f"Hru_{experiment_num}"
    )

    # Q3. Hre (Rewrite Easier)
    Hre = st.radio(
        "3. 수정된 정의가 원본 정의보다 이해하기 더 쉬운가요?",
        options=[1, 0],  # 숫자로 옵션 설정
        format_func=lambda x: "예" if x == 1 else "아니오",
        key=f"Hre_{experiment_num}"
    )

    return Hmp, Hru, Hre

def completion_page():
    st.markdown("<h1 style='text-align: center; color: #FF5722;'>🎉 실험 완료 🎉</h1>", unsafe_allow_html=True)
    st.balloons()  # 애니메이션 효과
    st.markdown(
        """
        ## 🙏 감사합니다! 🙏  
        실험에 참여해주셔서 진심으로 감사드립니다.  
        여러분의 소중한 응답이 연구에 큰 도움이 됩니다.
        """, unsafe_allow_html=True
    )
    st.markdown(
        """
        궁금한 점이 있으시면 [연락처](mailto:sanjunah@snu.ac.kr)로 문의해주세요.
        """
    )
    if st.button("🏠 응답 제출 및 인트로 페이지로 돌아가기"):
        st.session_state["page"] = "intro"
        responses = st.session_state.get("responses", [])
        save.record_to_sheets(responses)

def process_response():
    personal_info = st.session_state.get("personal_info", {})
    if personal_info:
        # 개인정보와 실험 응답을 하나의 리스트로 결합
        responses = [
            personal_info.get("name"),
            personal_info.get("age"),
            personal_info.get("gender"),
            personal_info.get("education_level"),
            # personal_info.get("familiar_fields"),
            personal_info.get("additional_info"),
            # 여기에 실험 응답을 추가 (예시로 response_1, response_2, response_3)
            st.session_state.get("response_1"),
            st.session_state.get("response_2"),
            st.session_state.get("response_3")
        ]
    return responses