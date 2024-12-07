import streamlit as st

def intro_page():
    '''
    Intro 페이지 구성
    
    실험 설명, 개인정보 수집, 다음 페이지로 이동
    필수 정보를 모두 수집했을 경우에만 다음 페이지로 이동
    
    Args: None
        
    Returns: None
        
    '''
    # 제목
    st.title("🌟 실험 참여 안내 🌟")
    st.divider()  # 구분선

    # 실험 설명
    intro_explanation_block()
    
    # 개인정보 수집
    personal_information_block()

    # 제출
    submitted = st.button("제출 및 다음 세션으로 진행 ➡️")
    if submitted:
        # 필수 항목 검증
        user = st.session_state["personal_information"]
        if user["name"] and user["age"] and user["gender"] and user["education_level"]:
            # 성공 및 페이지 이동
            st.success("정보가 성공적으로 제출되었습니다. 다음 세션으로 이동합니다.")
            st.session_state["page"] = "experiment"
            st.rerun()
        else:
            # 오류 메시지 출력
            st.error("모든 필수 항목을 입력해주세요.")

        st.rerun()

def intro_explanation_block():
    '''
    개요 설명 블록
    
    주어진 텍스트 출력
    
    Args: None
        
    Returns: None
        
    '''
    st.markdown(
        """
        ### 🌟 실험 개요
        안녕하세요! 이번 실험에 참여해 주셔서 감사합니다.<br>
        이 실험은 **자연어 처리(NLP) 모델**을 활용하여 사람들이 익숙하지 않은 분야의 복잡한 텍스트를 보다 효과적으로 이해할 수 있도록 돕는 방법을 연구하기 위한 것입니다.

        ### 🎯 실험 목적
        - 🧩 어려운 개념을 다양한 방식으로 설명했을 때 텍스트 이해도가 얼마나 향상되는지 연구합니다.<br>
        - 📝 중요한 정보와 원래 의미를 유지하면서 텍스트를 쉽게 풀어 쓰는 효과를 분석하는 것이 목표입니다.

        ### 🛠️ 실험 절차
        1️⃣ **복잡한 개념이 포함된 문장을 읽습니다.**<br>
        2️⃣ **해당 문장을 다른 방식으로 서술한 문장을 읽습니다.**<br>
        3️⃣ **각 텍스트에 대해 이해도와 만족도를 평가합니다.**

        ### ⏳ 예상 소요 시간
        - ⌛ 약 15~20분<br>
        - 실험은 총 **20개의 문장**으로 구성되어 있습니다.

        **📌 참고:**<br>
        - 🛡️ 실험에서 수집한 모든 데이터는 연구 목적으로만 사용됩니다.<br>
        - ⛔ 중간에 실험을 종료하고 싶으시면 언제든 종료하실 수 있습니다.
        """,
        unsafe_allow_html=True
    )

def personal_information_block():
    '''    
    개인 정보 수집 블록

    개인 정보 수집 후 st.session_state["personal_information"]에 저장
    이름, 나이, 성별, 최종 학력, 관련 경험 또는 친숙한 분야, 추가 정보
    
    Args: None
        
    Returns: None
        
    '''
    # 개인정보 수집
    container = st.container(border=True)
    user_name = container.text_input("*이름:", placeholder="예: 홍길동")
    user_age = container.number_input("*나이:", min_value=10, max_value=100, value=20)
    user_gender = container.radio("*성별:", ["남성", "여성", "기타"], horizontal=True)
    education_level = container.selectbox(
        "*최종 학력:",
        ["고등학교 졸업", "대학교 졸업", "대학원 석사 졸업", "대학원 박사 졸업"], index=1
    )
    familiar_fields = container.multiselect(
        "관련 경험 또는 친숙한 분야:",
        ["음식과 음료", "공연 예술", "비즈니스와 경제", "정치와 정부", "생물학", "화학", "컴퓨팅", "지구와 환경", "수학", "의학과 건강", "물리학", "공학", "기술"]
    )
    additional_info = container.text_area("추가 정보:", placeholder="본인의 특기 사항이나 취미 등을 입력해주세요.")

    # session_state에 저장
    st.session_state["personal_information"] = {
        "name": user_name,
        "age": user_age,
        "gender": user_gender,
        "education_level": education_level,
        "familiar_fields": familiar_fields,
        "additional_info": additional_info
    }
    