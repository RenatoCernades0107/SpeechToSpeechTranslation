import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
import time
import pandas as pd


def record_time(function):
    def wrap(*args, **kwargs):
        start_time = time.time()
        function_return = function(*args, 62**kwargs)
        print(f"Run time of {function.__name__} {round(time.time() - start_time, 2)} seconds")
        return function_return
    return wrap

load_dotenv()

class Translate():
    def __init__(self, target_language, recognition_language, voice) -> None:
        self.speech_translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
        # Other recognition languages here: https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support?tabs=stt#prebuilt-neural-voices
        self.speech_translation_config.speech_recognition_language=recognition_language

        # Other languages to translade here: https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support?tabs=speech-translation#speech-translation
        self.target_language=target_language
        self.speech_translation_config.add_target_language(self.target_language)

        self.audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        self.translation_recognizer = speechsdk.translation.TranslationRecognizer(translation_config=self.speech_translation_config, audio_config=self.audio_config)
        self.synthesizer = self.Synthesizer(voice_name=voice)

    @record_time
    def speech_to_speech_translation(self):
        start_time = time.time()
        translation_recognition_result = self.translation_recognizer.recognize_once_async().get()
        print(f"Run time of translation {round(time.time() - start_time, 2)} seconds")
        
        if translation_recognition_result.reason == speechsdk.ResultReason.TranslatedSpeech:
            print("Recognized: {}".format(translation_recognition_result.text))
            print("""Translated into '{}': {}""".format(
                self.target_language, 
                translation_recognition_result.translations[self.target_language]))
            self.synthesizer.text_to_speech(translation_recognition_result.translations[self.target_language])

        elif translation_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(translation_recognition_result.no_match_details))

        elif translation_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = translation_recognition_result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))


    class Synthesizer():
        def __init__(self, voice_name) -> None:
            # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
            self.speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
            self.audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

            # The language of the voice that speaks.
            # Other supported languages here: https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#prebuilt-neural-voices
            self.speech_config.speech_synthesis_voice_name=voice_name

            self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)

        @record_time
        def text_to_speech(self, text):
            speech_synthesis_result = self.speech_synthesizer.speak_text_async(text).get()

            if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                print("Speech synthesized for text [{}]".format(text))

            elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = speech_synthesis_result.cancellation_details
                print("Speech synthesis canceled: {}".format(cancellation_details.reason))

                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    if cancellation_details.error_details:
                        print("Error details: {}".format(cancellation_details.error_details))


def show_languages(text, list):
    for (index, l) in enumerate(list):
        print(str(index) + ".",  l)
    print(text)

def get_languages():
    df = pd.read_csv('languages/voice_and_target_languages.csv', sep=',',header=0, index_col=0)
    return df["0"].unique()

def get_recognition_languages():
    df = pd.read_csv('languages/recognition_languages.csv', sep=',',header=0, index_col=0)
    return df["1"].unique()


def create_recognizable_languages_map():
    df = pd.read_csv('languages/recognition_languages.csv', sep=',',header=0, index_col=0)
    
    languages_map = {}

    for l in df["1"]:
        languages_map[l] = df[df["1"] == l]["0"].unique()[0]
    
    return languages_map


def create_languages_map():
    df = pd.read_csv('languages/voice_and_target_languages.csv', sep=',',header=0, index_col=0)
    
    languages_map = {}

    for l in df["0"]:
        languages_map[l] = {
            "target": df[df["0"] == l]["1"].unique()[0],
            "voice": df[df["0"] == l]["voice"].unique()[0]
        }
    
    return languages_map

def main():
    rec_lang_map = create_recognizable_languages_map()
    lang_map = create_languages_map()

    rec_lang_list = get_recognition_languages()
    lang_list = get_languages()

    show_languages("Indicate the index of the language you will talk: ", rec_lang_list)
    from_lang = int(input())

    show_languages("Indicate the index of the language you desire translate to: ", lang_list)
    to_lang = int(input())

    translate = Translate(target_language=lang_map[lang_list[to_lang]]['target'],recognition_language=rec_lang_map[rec_lang_list[from_lang]], voice=lang_map[lang_list[to_lang]]['voice'])

    print("Speak into your microphone.")
    translate.speech_to_speech_translation()

    
if __name__ == '__main__':
    main()