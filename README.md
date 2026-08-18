# AI Quiz Generator

An interactive web application that automatically generates MCQ type quizzes from user provided text content. Built with Streamlit and the Google Gemini API (`gemini-3.5-flash-lite`), this tool allows users to customize quiz difficulty and length, take the quiz directly in the browser, and receive immediate feedback. 

## Screenshots

**Main Interface & Input Area**
![App Interface - Input Area](Screenshot%202026-08-18%20115227.png)

**Taking the Generated Quiz**
![Generated Quiz Questions](Screenshot%202026-08-18%20115246.png)

**Instant Grading (Correct & Incorrect Feedback)**
![Quiz Results - Correct Answer](Screenshot%202026-08-18%20115344.png)
![Quiz Results - Incorrect Answer](Screenshot%202026-08-18%20115428.png)

## Features

* **Dynamic Generation**: Paste bulky text or multi-topic content to automatically generate a tailored quiz.
* **Customizable Parameters**: Select between Easy, Medium, and Hard difficulty levels. Use the slider to choose anywhere from 1 to 10 questions per quiz.
* **Interactive Quiz Taking**: Answer questions directly in the app using radio buttons. The app includes a mix of multiple-choice and True/False questions.
* **Instant Grading**: Submit your answers to receive a final score, see the correct answers, and read brief explanations for why the answer is correct.
* **Export Data**: Download the generated quiz questions, options, and explanations as a cleanly formatted JSON file.

## Tech Stack & Requirements

This project relies on the following Python packages:
* `python-dotenv` (for environment variable management)
* `streamlit` (for the frontend web interface)
* `google-genai` (for accessing the Gemini models)
* `pydantic` (for structured JSON schema validation)

