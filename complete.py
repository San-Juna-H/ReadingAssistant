import streamlit as st
import save

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
    
    # personal_information에서 각 값을 꺼내서 responses에 추가
    responses.append(st.session_state["personal_information"]['name'])
    responses.append(st.session_state["personal_information"]['age'])
    responses.append(st.session_state["personal_information"]['gender'])
    responses.append(st.session_state["personal_information"]['education_level'])
    responses.append('/'.join(map(str, st.session_state["personal_information"]['familiar_fields'])))
    responses.append(st.session_state["personal_information"]['additional_info'])
    
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

