import asyncio

import sys
sys.path.append('src')

import dotenv
dotenv.load_dotenv()

import util
util.cred_kluge()

import speech

def list_voices():
    """Lists the available voices."""
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    # Performs the list voices request
    voices = client.list_voices()

    for voice in voices.voices:
        # en-GB en=US en-AU en-IN en-CA en-IE en-ZA
        if not [c for c in voice.language_codes if c.startswith('en-')]:
            continue
        #if 'en-US' not in 
        #    continue
        if 'Wavenet' in voice.name:
            continue
        if 'Neural2' in voice.name:
            continue

        # Display the voice's name. Example: tpc-vocoded
        print(f"Name: {voice.name}")

        # # Display the supported language codes for this voice. Example: "en-US"
        # for language_code in voice.language_codes:
        #     print(f"Supported language: {language_code}")

        # ssml_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender)

        # # Display the SSML Voice Gender
        # print(f"SSML Voice Gender: {ssml_gender.name}")

        # # Display the natural sample rate hertz for this voice. Example: 24000
        # print(f"Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}\n")

list_voices()
