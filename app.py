# import streamlit as st
# import speech_recognition as sr
# # import pyaudio 
#
# # Initialize the recognizer
# recognizer = sr.Recognizer()
#
#
# # Define the list of affirmations
# affirmations = [
#     "I am confident",
#     "I am worthy",
#     "I am loved",
#     "I am happy",
#     "I am grateful",
#     "I am enough",
#     "I deserve to be happy",
#     "I am enough because I am me",
#     "I love myself for who I am",
#     "My feelings matter",
#     "I am worthy of respect",
#     "I love my body just the way it is",
#     "I am ready for what comes next.",
#     "No one can make me feel inferior without my consent",
#     "I deserve happiness and fulfillment"
# ]
#
#
# # Score counter
# if "score" not in st.session_state:
#     st.session_state.score = 0  # Initialize the score in session state
#
#
# # Initialize page state
# if "page" not in st.session_state:
#     st.session_state.page = "Affirmation Recognition"  # Default to the recognition page
#
# def recognize_affirmation(audio_data):
#     try:
#         text = recognizer.recognize_google(audio_data)
#         return text
#     except sr.UnknownValueError:
#         return "Sorry, could you be a bit louder."
#     except sr.RequestError:
#         return "Sorry, the service is down."
#
#
# # Display the current page content based on the session state
# if st.session_state.page == "Affirmation Recognition":
#     st.title("Affirmation Speech Recognition")
#     st.markdown("<h3 style='text-align: center; font-size: 16px;'>Boost your confidence and positivity with our Affirmation Speech Recognition App! Practicing affirmations helps strengthen self-belief and reduce stress. Simply say each affirmation aloud, and the app will recognize and confirm it. Track your progress and see how many affirmations you’ve mastered. Start building a more positive mindset today! </h3>", unsafe_allow_html=True)
#
#
#     # Process each affirmation
#     for affirmation in affirmations:
#         st.subheader(f"Please say: '{affirmation}'")
#
#
#         if st.button(f"Listen for '{affirmation}'"):
#             with sr.Microphone() as source:
#                 status_placeholder = st.empty()  # Create a placeholder for status messages
#                 status_placeholder.write("Listening...")
#                 recognizer.adjust_for_ambient_noise(source, duration=1)
#                 audio = recognizer.listen(source)
#                 status_placeholder.empty()  # Clear the placeholder after recording is done
#
#
#             recognized_text = recognize_affirmation(audio)
#
#
#             if recognized_text.lower() == affirmation.lower():
#                 st.success(f"Affirmation detected: '{affirmation}'")
#                 st.session_state.score += 1  # Increment score if affirmation is correctly recognized
#             else:
#                 st.warning(f"Detected: '{recognized_text}'. Please try again.")
#
#
#     # Button to go to the Score page
#     if st.button("Go to Score"):
#         st.session_state.page = "Score"
#
# elif st.session_state.page == "Score":
#     st.title("Your Score")
#     st.subheader(f"Total Affirmations Correct: {st.session_state.score}/{len(affirmations)}")
#
#     # Button to go back to the Affirmation Recognition page
#     if st.button("Back to Affirmations"):
#         st.session_state.page = "Affirmation Recognition"
#
#     st.markdown("<h1 style='text-align: center; color: white;'>Thank you for paticipating :) </h1>", unsafe_allow_html=True)



import streamlit as st
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import io

# Initialize the recognizer
recognizer = sr.Recognizer()

# Streamlit app title
st.title("Speech to Text with Streamlit")

def recognize_audio(audio_data):
    """ Recognize the audio data using Google's speech recognition API """
    try:
        audio = sr.AudioData(audio_data, 16000, 2)
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError:
        return "Sorry, there was a problem with the speech recognition service."

def display_audio(audio_data):
    """ Display the audio as an audio player in Streamlit """
    audio_bytes = io.BytesIO(audio_data)  # Convert to bytes for Streamlit to display
    st.audio(audio_bytes, format="audio/wav")

# Record audio using the audio_recorder
audio_data = audio_recorder()

if audio_data is not None:
    st.write("Audio Recorded!")

    # Recognize and display the text
    recognized_text = recognize_audio(audio_data)
    st.write("You said:", recognized_text)

    # Display the audio as an audio player
    display_audio(audio_data)
