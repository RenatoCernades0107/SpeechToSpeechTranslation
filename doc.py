# def text_to_speech(text):
#     # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
#     speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
#     audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

#     # The language of the voice that speaks.
#     # Other supported languages here: https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#prebuilt-neural-voices
#     speech_config.speech_synthesis_voice_name='es-MX-CecilioNeural'

#     speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

#     speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

#     if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
#         print("Speech synthesized for text [{}]".format(text))
#     elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
#         cancellation_details = speech_synthesis_result.cancellation_details
#         print("Speech synthesis canceled: {}".format(cancellation_details.reason))
#         if cancellation_details.reason == speechsdk.CancellationReason.Error:
#             if cancellation_details.error_details:
#                 print("Error details: {}".format(cancellation_details.error_details))
#                 print("Did you set the speech resource key and region values?")


# def recognize_from_microphone():
#     speech_translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
#     # Other recognition languages here: https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support?tabs=stt#prebuilt-neural-voices
#     speech_translation_config.speech_recognition_language="en-US"

#     # Other languages to translade here: https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support?tabs=speech-translation#speech-translation
#     target_language="es"
#     speech_translation_config.add_target_language(target_language)

#     audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
#     translation_recognizer = speechsdk.translation.TranslationRecognizer(translation_config=speech_translation_config, audio_config=audio_config)

#     print("Speak into your microphone.")
#     translation_recognition_result = translation_recognizer.recognize_once_async().get()

#     if translation_recognition_result.reason == speechsdk.ResultReason.TranslatedSpeech:
#         print("Recognized: {}".format(translation_recognition_result.text))
#         print("""Translated into '{}': {}""".format(
#             target_language, 
#             translation_recognition_result.translations[target_language]))
#         text_to_speech(translation_recognition_result.translations[target_language])
#     elif translation_recognition_result.reason == speechsdk.ResultReason.NoMatch:
#         print("No speech could be recognized: {}".format(translation_recognition_result.no_match_details))
#     elif translation_recognition_result.reason == speechsdk.ResultReason.Canceled:
#         cancellation_details = translation_recognition_result.cancellation_details
#         print("Speech Recognition canceled: {}".format(cancellation_details.reason))
#         if cancellation_details.reason == speechsdk.CancellationReason.Error:
#             print("Error details: {}".format(cancellation_details.error_details))
#             print("Did you set the speech resource key and region values?")


# References:
  #https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-text-to-speech?tabs=windows%2Cterminal&pivots=programming-language-python
  #https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-speech-translation?tabs=windows%2Cterminal&pivots=programming-language-python