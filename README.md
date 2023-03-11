# shellGPT
Terminal app for chatGPT voice control.

This program is a Python application that uses the chatGPT API and the Azure Speech service to generate voice responses to user voice input. The program prompts the user for input via microphone or keyboard and then uses the OpenAI API to generate a response. The program also includes an analysis option that allows users to view statistics about the usage of the application. The application can be customized using a resources.json file to personalize various settings, such as the system prompt,  language used, system messages or change voice to keyboard input. The program requires valid OpenAI API and Azure Speech subscription keys to function correctly.

# Basic usage
To use the application, simply run the Python file. The application will prompt the user for input via microphone, and then use the chatGPT API to generate a response based on the user input. 

# Usage analysis
The application includes an analysis option that allows you to view statistics about application usage. To access the analysis, speak 'analysis' or customize the voice command in resources.json file and follow the instructions to view information about tokens used and messages exchanged.

# Easter Egg: Talk to Dolores
The application includes an option to talk to Dolores (westworld emulation), a virtual assistant based on the OpenAI API. To access the emulation option, say 'analysis' and then 'talk to me'.

# Customizing the application
The application includes a "resources.json" file that allows you to customize various application settings, such as the language used, the initial greeting, and system messages. You can modify this file to customize the application according to your preferences.

# System requirements
The application requires a valid OpenAI API key and a valid Azure Speech subscription key to function correctly. Make sure you have configured these keys correctly before running the application.

# Dependencies
The application requires the following Python libraries to function correctly:

openai
azure.cognitiveservices.speech
pprint

Make sure you have installed these libraries before running the application.
