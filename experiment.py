import streamlit as st
import pandas as pd
import random

def experiment_page():
    st.title("🧠 실험 진행 🧠")
    st.divider()  # 구분선

    # 실험 설명
    experiment_explanation_block()

    # 실험에 사용할 데이터 불러오기
    random_select_examples()
    examples = st.session_state["experiment_data"]

    # 세션 상태 초기화
    if "experiment_num" not in st.session_state:
        st.session_state["experiment_num"] = 1
        st.session_state["experiment"] = {}

    experiment_num = st.session_state["experiment_num"]
        
    if experiment_num <= 20:
        # 실험 블록
        experiment_content_block()
        question_block()

        # 버튼 표시: 다음 또는 완료
        if experiment_num < 20:
            button_label = "다음 실험으로 진행 ➡️"
        else:
            button_label = "완료 페이지로 이동 ✅"

        # 버튼 클릭 처리
        if st.button(button_label):

            # 다음 실험으로 이동 또는 완료 처리
            if experiment_num < 20:
                st.session_state["experiment_num"] += 1
            else:
                st.session_state["page"] = "completion"
            st.rerun()

def experiment_explanation_block():
    st.subheader("실험 설명")
    st.markdown(
        """
        아래는 특정 단어(**"Term"**)과 그 정의를 포함한 텍스트입니다.\n
        원본 정의(**"ORIGINAL"**)와\n
        해당 문장의 어려운 개념(**"Difficult Concept"**)에 대한 설명을 덧붙여 재서술된 정의(**"REWRITE"**)를 비교하고,\n
        각 질문에 답변해 주세요.
        """
    )

def random_select_examples():
    '''
    실험에 사용할 데이터를 제공
    
    초기화 시, 데이터를 불러옴/20개를 선택/5개씩 분리/셔플
    st.session_state["experiment_data"]에 저장
    
    Args: None
        
    Returns: None
        
    '''
    if "is_data_loaded" not in st.session_state:
        st.session_state["is_data_loaded"] = True

        # 데이터 불러오기
        file_path = "dataset.csv"  # 파일 경로
        df = pd.read_csv(file_path)
        # 20개 선택
        df = df.sample(n=20)

        # rewrite_type 후보
        rewrite_options = ['simplify', 'explain', 'define', 'personalize']
        rows = []

        # rewrite type 결정
        for i in range(0, len(df)):
            row = df.iloc[i]
            rewrite_type = rewrite_options[i%4]
            rewrite_value = row[rewrite_type]
            rows.append({
                'term': row['term'],
                'difficult_concept': row['difficult_concept'],
                'term_domain': row['term_domain'],
                'original': row['original'],
                'rewrite': rewrite_value,
                'rewrite_type': rewrite_type
            })
        examples = pd.DataFrame(rows)

        # shuffle
        examples = examples.sample(frac=1).reset_index(drop=True)
        st.session_state["experiment_data"] = examples

def experiment_content_block():
    '''
    실험 번호 및 내용 표시
    
    Args:
        
    Returns:
        
    '''
    experiment_num = st.session_state["experiment_num"]
    example = st.session_state["experiment_data"].iloc[experiment_num - 1]

    # 현재 실험 번호 표시
    st.subheader(f"실험 {experiment_num} / 20")

    # 현재 실험 내용 표시
    st.markdown(f"**Term**: {example['term']}")
    st.markdown(f"**Difficult Concept**: {example['difficult_concept']}")
    st.markdown(f"**ORIGINAL**: {example['original']}")
    st.markdown(f"**REWRITE**: {example['rewrite']}")

    st.session_state["experiment"][f"experiment_{experiment_num}"] = {
            "term": example['term'],
            "difficult_concept": example['difficult_concept'],
            "original": example['original'],
            "rewrite": example['rewrite'],
            "rewrite_type": example['rewrite_type'],
            "term_domain": example['term_domain'],
            "Hmp": None,
            "Hru": None,
            "Hre": None
        }

def question_block():
    '''
    질문 출력 및 응답 수집, 응답 반환
    
    Args: None
        
    Returns: int, Hmp, Hre, Hru
        
    '''
    experiment_num = st.session_state["experiment_num"]
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

    st.session_state["experiment"][f"experiment_{experiment_num}"]["Hmp"] = Hmp

    # 질문 2. Hru (Rewrite Understanding)
    Hru = st.radio(
        "2. 수정된 정의를 이해한 사람이 원래의 어려운 개념을 알지 못한다고 해도, 수정된 정의를 이해할 수 있을까요?",
        options=[1, 0],
        format_func=lambda x: "예" if x == 1 else "아니오",
    )

    st.session_state["experiment"][f"experiment_{experiment_num}"]["Hru"] = Hru

    # 질문 3. Hre (Rewrite Easier)
    Hre = st.radio(
        "3. 수정된 정의가 원본 정의보다 이해하기 더 쉬운가요?",
        options=[1, 0],
        format_func=lambda x: "예" if x == 1 else "아니오",
    )

    st.session_state["experiment"][f"experiment_{experiment_num}"]["Hre"] = Hre