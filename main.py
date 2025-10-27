import streamlit as st
from agents_setup import the_quiz_room,QuizList
import asyncio


st.set_page_config(page_title="The Quiz Room" , page_icon="💡")
st.title("💡 The Quiz Room")
st.text("Developed by Muhammad Taha")

if "quiz_dict" not in st.session_state:
    st.session_state.quiz_dict = {}

if "quiz_response" not in st.session_state:
    st.session_state.quiz_response = {}

if "result" not in st.session_state:
    st.session_state.result = False

if not st.session_state.quiz_response and not st.session_state.result:
    quiz_prompt:str = st.text_input("Enter a prompt or your whole syllabus: ")
    limit:int = st.radio("Select Questions Limit: ",[5,10,20])
    difficulty:str  =st.radio("Select Difficulty Level: ",["Easy Level","Hard Level","Graduate Level"])
    if st.button("Generate Quiz",type="primary"):
        st.toast("Your quiz is generating please wait for few seconds...")
        quiz_response = asyncio.run(the_quiz_room(
            Qlimit=limit,
            Qdifficulty=difficulty,
            Qinput=quiz_prompt
        ))
        st.session_state.quiz_response = quiz_response
        st.rerun()

elif st.session_state.quiz_response and not st.session_state.result:
    if isinstance(st.session_state.quiz_response,str):
        st.warning(st.session_state.quiz_response)
        if st.button("Try Again",type="primary"):
            st.session_state.quiz_response = {}
            st.session_state.result = False
            st.rerun()

    elif isinstance(st.session_state.quiz_response,QuizList):
        question_num:int = 0
        for q in st.session_state.quiz_response.quiz:
            question_num = question_num + 1
            st.session_state.quiz_dict[question_num] = {}
            st.info(q.question)
            st.session_state.quiz_dict[question_num]["selected"] = st.radio(label="",options=[q.option_1,q.option_2,q.option_3,q.option_4],key=question_num)
            st.session_state.quiz_dict[question_num]["correct"] = q.correct_answer
            st.session_state.quiz_dict[question_num]["question"] = q.question
            
    
        if st.button("Submit Quiz",type="primary"):
            st.session_state.result = True
            st.rerun()
            

elif st.session_state.result:
    total_marks = len(st.session_state.quiz_response.quiz)*10
    user_marks = 0
    for q in st.session_state.quiz_dict:
        if st.session_state.quiz_dict[q]["selected"] == st.session_state.quiz_dict[q]["correct"]:
            user_marks = user_marks + 10
    percentage = ((user_marks/total_marks)*100)/100
    st.progress(percentage,f"You scored {user_marks} out of {total_marks} and got {percentage*100}%")
    st.subheader("Correct Answers")
    for q in st.session_state.quiz_dict:
        st.info(f"Question: {st.session_state.quiz_dict[q]["question"]}")
        st.success(f"Answer: {st.session_state.quiz_dict[q]["correct"]}")
        
    if st.button("Generate More Quiz", type="primary"):
        st.session_state.result = False
        st.session_state.quiz_dict = {}
        st.session_state.quiz_response = {}
        st.rerun()            

