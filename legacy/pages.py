import streamlit as st
import save
import legacy.data as data
import pandas as pd
import random

# 실험 설명 페이지 함수
def intro_page():
    st.title("🌟 실험 참여 안내 🌟")
    st.divider()  # 구분선

    # 실험 설명 블록
    intro_explanation_block()
    
    # 개인정보 입력
    with st.form("personal_info_form"):
        # 입력 항목
        user_name, user_age, user_gender, education_level, familiar_fields, additional_info = personal_information_block()
        
        # "제출 및 진행" 버튼
        submitted = st.form_submit_button("제출 및 다음 세션으로 진행 ➡️")
        
        # 제출 시 동작
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
                # 성공 메시지와 페이지 이동
                st.success("정보가 성공적으로 제출되었습니다. 다음 세션으로 이동합니다.")
                st.session_state["page"] = "experiment"
                st.rerun()
            else:
                st.error("모든 필수 항목을 입력해주세요.")

def intro_explanation_block():
    st.subheader("🌟 실험 개요")
    st.markdown(
        """
        안녕하세요! 이번 실험에 참여해 주셔서 감사합니다.  
        이 실험은 **자연어 처리(NLP) 모델**을 활용하여 사람들이 익숙하지 않은 분야의 복잡한 텍스트를 보다 효과적으로 이해할 수 있도록 돕는 방법을 연구하기 위한 것입니다.

        ### 🎯 실험 목적
        - 🧩 복잡한 텍스트를 간단한 설명으로 이해도를 높이는 방식을 연구합니다.  
        - 📝 중요한 개념을 유지하며 이해하기 쉽게 만드는 것이 목표입니다.

        ### 🛠️ 실험 절차
        1️⃣ **복잡한 개념이 포함된 문장을 읽습니다.**  
        2️⃣ **제공된 간소화된 설명을 읽습니다.**  
        3️⃣ **각 텍스트에 대해 이해도와 만족도를 평가합니다.**

        ### ⏳ 예상 소요 시간
        - ⌛ 약 15~20분  
        - 실험은 총 **20개의 문장**으로 구성되어 있습니다.

        **📌 참고:**  
        - 🛡️ 실험에서 수집한 모든 데이터는 연구 목적으로만 사용됩니다.  
        - ⛔ 중간에 실험을 종료하고 싶으시면 언제든 종료하실 수 있습니다.
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
        ["고등학교 졸업", "대학교 졸업", "대학원 석사 졸업", "대학원 박사 졸업"], index=1
    )
    familiar_fields = st.multiselect(
        "관련 경험 또는 친숙한 분야:",
        ["음식과 음료", "공연 예술", "비즈니스와 경제", "정치와 정부", "생물학", "화학", "컴퓨팅", "지구와 환경", "수학", "의학과 건강", "물리학", "공학", "기술"]
    )
    additional_info = st.text_area("추가 정보:", placeholder="본인의 특기 사항이나 취미 등을 입력해주세요.")

    return user_name, user_age, user_gender, education_level, familiar_fields, additional_info

def experiment_page():
    st.title("🧠 실험 진행 🧠")
    st.divider()  # 구분선

    # 실험 설명
    experiment_explanation_block()

    if "random_state" not in st.session_state:
        st.session_state["random_state"] = random.randint(1, 100)

        # 데이터 불러오기
        file_path = "dataset.csv"  # 파일 경로
        df = pd.read_csv(file_path)
        st.session_state["experiment_data"] = df

    # 랜덤하게 20개 행 선택
    experiment_data = st.session_state["experiment_data"].sample(n=20, random_state=st.session_state["random_state"])

    unshuffled_examples = process_example(experiment_data)

    # 데이터프레임 행 셔플
    examples = unshuffled_examples.sample(frac=1, random_state=st.session_state["random_state"]).reset_index(drop=True)

    # 세션 상태 초기화
    if "experiment_num" not in st.session_state:
        st.session_state["experiment_num"] = 1
        st.session_state["experiment"] = {}

    experiment_num = st.session_state["experiment_num"]
        
    if experiment_num <= 20:
        example = examples.iloc[experiment_num-1]
        # 실험 블록
        experiment_content_block(example, experiment_num)
        Hmp, Hru, Hre = question_block(experiment_num)

        # 버튼 표시: 다음 또는 완료
        if experiment_num < 20:
            button_label = "다음 실험으로 진행 ➡️"
        else:
            button_label = "완료 페이지로 이동 ✅"

        # 버튼 클릭 처리
        if st.button(button_label):

            # 실험 결과 저장
            st.session_state["experiment"][f"experiment_{experiment_num}"] = {
                "term": example['term'],
                "difficult_concept": example['difficult_concept'],
                "original": example['original'],
                "rewrite": example['rewrite'],
                "rewrite_type": example['rewrite_type'],
                "term_domain": example['term_domain'],
                "Hmp": Hmp,
                "Hru": Hru,
                "Hre": Hre
            }

            # 다음 실험으로 이동 또는 완료 처리
            if experiment_num < 20:
                st.session_state["experiment_num"] += 1
            else:
                st.session_state["page"] = "completion"
            st.rerun()

    else:
        # 모든 실험 완료 후 처리
        st.session_state["page"] = "completion"
        st.rerun()

def experiment_explanation_block():
    st.subheader("실험 설명")
    st.markdown(
        """
        아래는 특정 개념(**"CONCEPT"**)과 그 정의를 포함한 텍스트입니다.  
        원본 정의(**"ORIGINAL"**)와 간소화된 정의(**"REWRITE"**)를 비교하고, 각 질문에 답변해 주세요.
        """
    )

def experiment_content_block(example, experiment_num):
    # 현재 실험 번호 표시
    st.subheader(f"실험 {experiment_num} / 20")

    # 현재 실험 내용 표시
    st.markdown(f"**Term**: {example['term']}")
    st.markdown(f"**Difficult Concept**: {example['difficult_concept']}")
    st.markdown(f"**ORIGINAL**: {example['original']}")
    st.markdown(f"**REWRITE**: {example['rewrite']}")

def question_block(experiment_num):

    # 질문 1. Hmp (Meaning Preservation)
    Hmp = st.radio(
        "1. 수정된 정의가 원본 정의의 의미를 얼마나 보존하고 있습니까?",
        options=[1, 2, 3, 4, 5],
        format_func=lambda x: f"{x}: " + (
            "전혀 보존되지 않음" if x == 1 else
            "조금 보존됨" if x == 2 else
            "보통" if x == 3 else
            "대부분 보존됨" if x == 4 else
            "완벽하게 보존됨"
        ),
    )

    # 질문 2. Hru (Rewrite Understanding)
    Hru = st.radio(
        "2. 수정된 정의를 이해한 사람이 원래의 어려운 개념을 알지 못한다고 해도, 수정된 정의를 이해할 수 있을까요?",
        options=[1, 0],
        format_func=lambda x: "예" if x == 1 else "아니오",
    )

    # 질문 3. Hre (Rewrite Easier)
    Hre = st.radio(
        "3. 수정된 정의가 원본 정의보다 이해하기 더 쉬운가요?",
        options=[1, 0],
        format_func=lambda x: "예" if x == 1 else "아니오",
    )

    # 값들을 리턴
    return Hmp, Hru, Hre


def process_example(experiment_data):
    df = experiment_data
    rewrite_options = ['simplify', 'explain', 'define', 'personalize']
    rows = []

    # 5개씩 데이터를 묶어 처리
    for i in range(0, len(df), 5):
        batch = df.iloc[i:i+5].copy()  # 5개씩 묶어서 처리
        for index, row in batch.iterrows():
            rewrite_type = rewrite_options[i//4]  # rewrite_type 선택
            rewrite_value = row[rewrite_type]  # 해당 열의 값 가져오기
            rows.append({
                'term': row['term'],
                'difficult_concept': row['difficult_concept'],
                'term_domain': row['term_domain'],
                'original': row['original'],
                'rewrite': rewrite_value,
                'rewrite_type': rewrite_type
            })

    df = pd.DataFrame(rows)

    return df

def completion_page():
    st.title("🎉 실험 완료 🎉")  # 제목을 표시
    st.balloons()  # 애니메이션 효과

    # 실험 완료 메시지
    st.subheader("🙏 감사합니다! 🙏")
    st.markdown(
        """
        실험에 참여해주셔서 진심으로 감사드립니다.  
        여러분의 소중한 응답이 연구에 큰 도움이 됩니다.
        궁금한 점이 있으시면 [연락처](mailto:sanjunah@snu.ac.kr)로 문의해주세요.
        """
    )
    # "응답 제출 및 인트로 페이지로 돌아가기" 버튼
    if st.button("🏠 응답 제출 및 인트로 페이지로 돌아가기"):

        st.write(st.session_state)

        # 응답을 저장
        responses = process_response()
        save.record_to_sheets(responses)

        # 세션 상태 초기화
        st.session_state.clear()  # 세션 상태 초기화

        # 새로고침
        st.session_state["page"] = "intro"
        st.rerun()
        
def process_response():
    responses = []
    
    # personal_info에서 각 값을 꺼내서 responses에 추가
    responses.append(st.session_state["personal_info"]['name'])
    responses.append(st.session_state["personal_info"]['age'])
    responses.append(st.session_state["personal_info"]['gender'])
    responses.append(st.session_state["personal_info"]['education_level'])
    responses.append('/'.join(map(str, st.session_state["personal_info"]['familiar_fields'])))
    responses.append(st.session_state["personal_info"]['additional_info'])
    
    for experiment_num in range(1, 21):
        if f"experiment_{experiment_num}" in st.session_state["experiment"]:
            experiment_data = st.session_state["experiment"][f"experiment_{experiment_num}"]
            responses.append(experiment_data['term'])
            responses.append(experiment_data['difficult_concept'])
            responses.append(experiment_data['original'])
            responses.append(experiment_data['rewrite'])
            responses.append(experiment_data['rewrite_type'])
            responses.append(experiment_data['term_domain'])
            responses.append(experiment_data['Hmp'])
            responses.append(experiment_data['Hru'])
            responses.append(experiment_data['Hre'])
    
    return responses

