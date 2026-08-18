import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
import json

# Load env
load_dotenv()

# Initialize Clients
client = genai.Client( api_key=st.secrets["API_KEY"]
                     )

# Define JSON Response Schema
class Question(BaseModel):
    question: str
    options: list[str] = Field(description="List of 4 multiple-choice options")
    correct_answer: str = Field(description="The exact text of the correct option")
    explanation: str = Field(description="A brief explanation of why the correct answer is correct")

class QuizResponse(BaseModel):
    quiz: list[Question]


# API Call Function
def generate_quiz(text_content: str, quiz_level: str, num_questions: int) -> QuizResponse:
    PROMPT_TEMPLATE = """ 
    Text: {text_content}
    You are an expert in generating multiple-choice question type quizzes on the basis of provided content.
    Given the above text, generate a quiz with {num_questions} multiple-choice questions keeping the difficulty level as {quiz_level}.
    Each question should have options labelled A, B, C, and D, and correct_answer must exactly match one of those options.Add a bit of True or False questions to each quiz.
    If the provided content is bulky or contains more than one topic, then split questions by themes or topic
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=PROMPT_TEMPLATE.format(
            num_questions=num_questions,
            quiz_level=quiz_level,
            text_content=text_content,
        ),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=QuizResponse,
        ),
    )

    return response.parsed 


def main():
    st.title("Quiz Generator")

    # Text inputs
    text_content = st.text_area("Paste content here:", height=200)
    quiz_level = st.selectbox("Select Quiz Level:", ["Easy", "Medium", "Hard"])
    num_questions = st.slider("Number of Questions:", min_value=1, max_value=10, value=5)

    # Initialize session state
    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = None

    # 1. Generate Quiz Button
    if st.button("Generate Quiz"):
        if text_content.strip():
            st.session_state.quiz_data = generate_quiz(
                text_content=text_content,
                quiz_level=quiz_level, 
                num_questions=num_questions
            )
        else:
            st.warning("Please paste some text content first!")

    # 2. Display Quiz & Submit Button ONLY if quiz_data exists
    if st.session_state.quiz_data is not None:
        quiz_data = st.session_state.quiz_data
        quiz_json = json.dumps(
            quiz_data.model_dump(),
            indent=4,
            ensure_ascii=False
            )
        st.download_button(
            label="Download Quiz as JSON",
            data=quiz_json,
            file_name="generated_quiz.json",
            mime="application/json",
            )

        # Render questions
        selected_options = [
            st.radio(f"**Q{i+1}: {q.question}**", q.options, index=None, key=f"q_{i}")
            for i, q in enumerate(quiz_data.quiz)
        ]

        # 3. Submit button
        if st.button("Submit"):
            score = 0
            st.header("Quiz Results")

            for i, (user_choice, question) in enumerate(zip(selected_options, quiz_data.quiz)):
                st.subheader(f"Question {i + 1}: {question.question}")
                st.write(f"You selected: **{user_choice or 'None'}**")
                st.write(f"Correct answer: **{question.correct_answer}**")
                st.write(f"Explanation: {question.explanation}")

                if user_choice == question.correct_answer:
                    score += 1
                    st.success("Correct!")
                else:
                    st.error("Incorrect!")

            st.divider()
            st.subheader(f"Your Score: {score}/{len(quiz_data.quiz)}")


if __name__ == "__main__":
    main()
