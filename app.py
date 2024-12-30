import streamlit as st
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder
import io

# Initialize the recognizer
recognizer = sr.Recognizer()

# Define the list of affirmations
affirmations = [
    "I am confident",
    "I am worthy",
    "I am loved",
    "I am happy",
    "I am grateful",
    "I am enough",
    "I deserve to be happy",
    "I am enough because I am me",
    "I love myself for who I am",
    "My feelings matter",
    "I am worthy of respect",
    "I love my body just the way it is",
    "I am ready for what comes next.",
    "No one can make me feel inferior without my consent",
    "I deserve happiness and fulfillment"
]

# Initialize score array in session state
if "score_array" not in st.session_state:
    st.session_state.score_array = [0] * len(affirmations)  # Initialize an array to keep track of scores

# Initialize page state
if "page" not in st.session_state:
    st.session_state.page = "Affirmation Recognition"  # Default to the recognition page

def recognize_affirmation(audio_data):
    try:
        # Use speech_recognition's Google API to recognize speech
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Sorry, could you be a bit louder?"
    except sr.RequestError:
        return "Sorry, the service is down."

# Display the current page content based on the session state
if st.session_state.page == "Affirmation Recognition":
    st.title("Affirmation Speech Recognition")
    st.markdown("<h3 style='text-align: center; font-size: 16px;'>Boost your confidence and positivity with our Affirmation Speech Recognition App! Practicing affirmations helps strengthen self-belief and reduce stress. Simply say each affirmation aloud, and the app will recognize and confirm it. Track your progress and see how many affirmations you’ve mastered. Start building a more positive mindset today! </h3>", unsafe_allow_html=True)

    # Process each affirmation
    for idx, affirmation in enumerate(affirmations):
        st.subheader(f"Please say: '{affirmation}'")

        # Record audio using audio_recorder_streamlit, providing a unique key
        audio_data = audio_recorder(
            pause_threshold=2.0,
            key=f"audio_recorder_{idx}",
        )
        if audio_data:
            # Convert the raw audio data (which is in bytes) into an AudioData object
            audio_file = io.BytesIO(audio_data)  # Wrap the byte data in a BytesIO object

            # Now use SpeechRecognition to process the audio
            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)

            # Recognize the audio using Google Speech API
            recognized_text = recognize_affirmation(audio_data)
            audio_data = None

            if recognized_text.lower() == affirmation.lower():
                st.success(f"Affirmation detected: '{affirmation}'")
                st.session_state.score_array[idx] = 1  # Set score for this affirmation to 1 (correct)
            else:
                st.warning(f"Detected: '{recognized_text}'. Please try again.")

    # Button to go to the Score page
    if st.button("Go to Score"):
        st.session_state.page = "Score"

elif st.session_state.page == "Score":
    st.title("Your Score")

    # Calculate the total score (number of correctly recognized affirmations)
    total_score = sum(st.session_state.score_array)

    st.subheader(f"Total Affirmations Correct: {total_score}/{len(affirmations)}")

    # Button to go back to the Affirmation Recognition page
    if st.button("Back to Affirmations"):
        st.session_state.page = "Affirmation Recognition"

    st.markdown("<h1 style='text-align: center; color: white;'>Thank you for participating :) </h1>", unsafe_allow_html=True)
