from pprint import pprint
import openai
import sys
import os
import locale
import json
import azure.cognitiveservices.speech as speechsdk

speech_key = os.environ['AZURE_SPEECH_KEY']
service_region = "brazilsouth"
openai.api_key = os.environ['OPENAI_API_KEY']
language, _ = locale.getdefaultlocale()

# language = "en_US"
# language = "pt_BR"

with open("resources.json") as f:
    r = json.load(f)

lang = language if language in r else "en"
system_content = r[lang]["content_system"].format(r[lang]["username"])
system_contentAnalysis = r[lang]["system_contentAnalysis"]
_messages = [{"role": "system", "content": system_content}]
_usage = []
_analysisMessages = [{"role": "system", "content": system_contentAnalysis}, {
    "role": "assistant", "content": r[lang]["dolores_start"]}]

run = True
analysis = False
talkToMe = False


def request_chat(prompt):
    global _messages, _usage
    _messages.append({"role": "user", "content": prompt})

    result = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                          messages=_messages)

    item = result["choices"][0]["message"]
    resp = result["choices"][0]["message"]["content"]

    _messages.append(item)

    _usage.append({
        "role": result["choices"][0]["message"]["role"],
        "content": result["choices"][0]["message"]["content"],
        "prompt_tokens": result["usage"]["prompt_tokens"],
        "completion_tokens": result["usage"]["completion_tokens"],
        "total_tokens": result["usage"]["total_tokens"]
    })

    return resp


def requestAnalysis_chat(prompt):
    global _messages, _usage
    _analysisMessages.append({"role": "user", "content": prompt})

    result = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                          messages=_analysisMessages)

    item = result["choices"][0]["message"]
    resp = result["choices"][0]["message"]["content"]

    _analysisMessages.append(item)

    return resp


def recognize_from_microphone(mock):
    if (mock):
        return input("type: ")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key,
                                           region=service_region)
    speech_config.speech_recognition_language = r[lang]['azure_lang']

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,
                                                   audio_config=audio_config)
    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return speech_recognition_result.text

    return "Azure error"


def talk(text):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key,
                                           region=service_region)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_config.speech_synthesis_voice_name = r[lang]['azure_voice']
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config)
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()


def clear_terminal():
    if sys.platform.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')


def total_tokens():
    if (len(_usage) == 0):
        return "0"

    return _usage[-1]["total_tokens"]


def run_talkToMe():
    global talkToMe, analysis, _analysisMessages
    print(r[lang]['dolores_start'])
    talk(r[lang]['dolores_start'])
    while (talkToMe):
        print(f"[{r[lang]['msg_prompt']} | {r[lang]['menu_back']}]")
        question = recognize_from_microphone(False).replace(".", "")
        print(f"[{question}]")
        if (question.lower() == r[lang]['menu_back']):
            talkToMe = False
            analysis = False
            clear_terminal()
            print(f"[{r[lang]['msg_back']}]")
        else:
            result = requestAnalysis_chat(question)
            print(f"[Dolores: {result}]")
            talk(result)
            print("\n")


def run_analysis():
    global analysis, run, _messages, _usage, talkToMe
    while (analysis):
        print(
            f"[:: {r[lang]['menu_tokens']} | {r[lang]['menu_list']} | {r[lang]['menu_restart']} | {r[lang]['menu_back']} | {r[lang]['menu_exit']} | {r[lang]['menu_talk']} ::]")

        opt = recognize_from_microphone(False).replace(".", "")

        if (opt.lower() == r[lang]['menu_tokens']):
            clear_terminal()
            print("-------\n")
            pprint(_usage)
            print(f"\n[Total Tokens: {total_tokens()}]")
            print("\n-------")

        if (opt.lower() == r[lang]['menu_list']):
            clear_terminal()
            print("-------\n")
            pprint(_messages)
            print("\n-------")

        if (opt.lower() == r[lang]['menu_restart']):
            clear_terminal()
            print(f"[{r[lang]['msg_restart']}]")
            _usage = []
            _messages = [{"role": "system", "content": system_content}]

        if (opt.lower() == r[lang]['menu_back']):
            analysis = False
            clear_terminal()
            print(f"[{r[lang]['msg_back']}]")

        if (opt.lower() == r[lang]['menu_exit']):
            analysis = False
            run = False
            clear_terminal()
            print(r[lang]['msg_end'])

        if (opt.lower() == r[lang]['menu_talk']):
            talkToMe = True
            run_talkToMe()


clear_terminal()
print(f"[{r[lang]['msg_welcome']}]\n")
print(f"[Dolores: {r[lang]['msg_hi'].format(r[lang]['username'])}]")
talk(r[lang]['msg_hi'].format(r[lang]['username']))

while (run):
    print(f"[{r[lang]['msg_prompt']}]")
    phrase = recognize_from_microphone(False).replace(".", "")
    print(phrase)

    if (phrase.casefold() == r[lang]['cmd_analysis']):
        analysis = True

    if (analysis):
        clear_terminal()
        print(f"[:: {r[lang]['cmd_analysis']} :: ]")
        run_analysis()
    else:
        if (phrase.lower() == r[lang]['cmd_end']):
            run = False
            print(r[lang]['msg_end'])
        else:
            result = request_chat(phrase)
            print(f"[Dolores: {result}]")
            talk(result)
            print("\n")
