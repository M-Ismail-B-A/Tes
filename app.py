import streamlit as st
import speech_recognition as sr

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
    "I deserve happiness and fulfillment",
]

# Ensure all session state variables are initialized
if "page" not in st.session_state:
    st.session_state.page = "Affirmation Recognition"  # Default page
if "results" not in st.session_state:
    st.session_state.results = [None] * len(affirmations)  # Store results, None means no result yet
if "recorded_audio" not in st.session_state:
    st.session_state.recorded_audio = [None] * len(affirmations)  # Store recorded audio

def recognize_affirmation_from_audio(audio_bytes):
    try:
        # Convert the audio bytes to an audio file object for processing
        with sr.AudioFile(audio_bytes) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Sorry, could you be a bit louder."
    except sr.RequestError:
        return "Sorry, the service is down."

# Display the current page content
if st.session_state.page == "Affirmation Recognition":
    st.title("Affirmation Speech Recognition")
    st.markdown(
        "<h3 style='text-align: center; font-size: 16px;'>Boost your confidence and positivity with our Affirmation Speech Recognition App! Practicing affirmations helps strengthen self-belief and reduce stress. Simply record each affirmation aloud, and the app will recognize and confirm it. Track your progress and see how many affirmations you’ve mastered. Start building a more positive mindset today! </h3>",
        unsafe_allow_html=True,
    )

    # Process each affirmation
    for index, affirmation in enumerate(affirmations):
        st.subheader(f"Please say: '{affirmation}'")

        # Audio input widget for recording user input
        audio_input = st.audio_input(f"Record audio for '{affirmation}'", key=affirmation)

        # Run recognition only if new audio is recorded
        if audio_input and audio_input != st.session_state.recorded_audio[index]:
            st.session_state.recorded_audio[index] = audio_input  # Store the new audio
            recognized_text = recognize_affirmation_from_audio(audio_input)

            if recognized_text.lower() == affirmation.lower():
                st.session_state.results[index] = f"Affirmation detected: '{affirmation}'"
            else:
                st.session_state.results[index] = f"Detected: '{recognized_text}'. Please try again."

        # Display current result for this affirmation if it exists
        if st.session_state.results[index]:
            if "Affirmation detected" in st.session_state.results[index]:
                st.markdown(f"<p style='color: green; font-size: 18px;'>{st.session_state.results[index]}</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p style='color: yellow; font-size: 18px;'>{st.session_state.results[index]}</p>", unsafe_allow_html=True)

    # Button to go to the Score page
    if st.button("Go to Score"):
        st.session_state.page = "Score"

elif st.session_state.page == "Score":
    st.title("Your Progress")
    
    # Count correct affirmations
    correct = len([r for r in st.session_state.results if r and "Affirmation detected" in r])

    st.subheader(f"Total Affirmations Correct: {correct}/{len(affirmations)}")

    # Button to go back to the Affirmation Recognition page
    if st.button("Back to Affirmations"):
        st.session_state.page = "Affirmation Recognition"

    st.markdown("<h1 style='text-align: center; color: white;'>Thank you for participating :)</h1>", unsafe_allow_html=True)
