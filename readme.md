# Speech to Speech Translation

Using the services of Microsoft Azure, translate your speech into 63 diferent languages :3

# Deployment

1- Clone this repository into a folder.

    $ git clone https://github.com/RenatoCernades0107/SpeechToSpeechTranslation.git .

2- Create a virtual enviroment and install requirements.

    $ python -m venv venv
    (venv) $ pip install -r requirements.txt

3- Create and ``.env`` and put your api key and region of your ``Microsoft Cognitive Speech Service`` (https://portal.azure.com/#home).
    
    SPEECH_KEY=<your api key>
    SPEECH_REGION=<your region>

4- Run the program.

    $ python speech_translation.py

In the program, you can choose the language you talk and the language you desire translate to.

# Running the program

**Pick among these languages in order to recognize your voice**
![Recognizable Languages](/images/img1.png)

**Pick among these languages in order to translate your speech**
![Languages to translate](/images/img2.png)

**See and hear the result of the translation and the time that it took**
![End to the programe](/images/img3.png)