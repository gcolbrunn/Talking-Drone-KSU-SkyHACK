# Conversational Drone with OpenAI GPT-3.5 Turbo

# Used as part of KSU SkyHACK

# Python script allows a drone to interact with users, providing comforting and concise responses. 
# It utilizes OpenAI's GPT-3.5 Turbo model to understand and generate text-based responses.
# The drone communicates through speech, receiving audio input from users and providing vocal responses.
# Speech-to-Text --> GPT-3.5 Generated response --> Text-to-Speech
# Users can terminate the interaction by saying "terminate."

import openai
import speech_recognition as sr
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Speak the initial message
initial_message = "Hello, I am a lifesaving drone. How can I help you today?"
engine.say(initial_message)
engine.runAndWait()

# Set up the OpenAI API key
# Replace "my-API-key" with an OpenAI Key
openai.api_key = "my-API-key"

# Initialize the speech recognizer
r = sr.Recognizer()

# Start the loop
while True:
    with sr.Microphone() as source:
        print("Listening...")  # Print a message to indicate listening
        audio = r.listen(source)

    # Convert the audio to text using speech recognition
    try:
        audio_text = r.recognize_google(audio, language='en-US')
        print("Speech to Text:", audio_text)

        # Check if the user said "terminate" to exit the loop
        if "terminate" in audio_text.lower():
            break

        # Use the recognized text and the last GPT-3.5 Turbo response in the request
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                # Describe the personality of the robot here, to run efficiently tell it to use minimal
                # amount of sentence or you will get really long wait times
                {"role": "system", "content": """Respond in minimal and short sentences. You are a comforting lifesaving-drone named rubble-buster.
                  Answer everything in a soft comforting and clear and concise way. Make sure the victim knows its gonna be okay."""},
                {"role": "user", "content": audio_text},
            ]
        )

        # Get the GPT-3.5 Turbo response text
        gpt_response = completion.choices[0].message.content

        # Speak the response text with the specified voice
        engine.say(gpt_response)
        engine.runAndWait()

    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
