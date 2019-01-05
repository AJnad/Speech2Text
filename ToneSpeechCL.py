#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8

# In[19]:


#!/usr/bin/python

from __future__ import print_function
import json
import sys
import os
from os.path import join, dirname
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud.tone_analyzer_v3 import ToneInput
from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud.websocket import RecognizeCallback, AudioSource
import threading


def main():
    getAudiofilePath()
    transcription()

def getAudiofilePath():
    pathName = ''.join(sys.argv[1:])
    return pathName


def transcription():
    speech_service = SpeechToTextV1(
                             url='https://stream.watsonplatform.net/speech-to-text/api',
                             iam_apikey='T9sJMbCNwcShwX3piuvHO1n8CVfNJp7CdK_6IRt4Fdz-')

    tone_service = ToneAnalyzerV3(url='https://gateway.watsonplatform.net/tone-analyzer/api', iam_apikey='8JxzbihGNrwLnHyE_U0ehZy8yL9eEYGZZKxYRFneqofM', version='2017-09-21')

    #print(pathName) #prints "/users/ajay/Desktop/audio-file.flac"
    #print("\n", _file_) #prints "audio-file.flac"
    file = os.path.basename(str(getAudiofilePath()))

    with open(join(dirname(file), getAudiofilePath()), 'rb') as audio_file:
        jsonOutput = json.dumps(speech_service.recognize(audio=audio_file, content_type='audio/flac',
                                                timestaxxamps=True,word_confidence=True).get_result(),
                                indent=2)
        decoded_data = json.loads(jsonOutput)
    
        for data in decoded_data['results']:
            for word in data['alternatives']:
                transcript = word.get('transcript')
                confidence = word.get('confidence')

    utterances = [{
              'text': transcript,
              'user': 'user'
              }, {
              'text': 'It is a good day.',
              'user': 'user'
              }]
    tone_chat = tone_service.tone_chat(utterances).get_result()
    jsonOutput = json.dumps(tone_chat, indent=2)
    decoded_data = json.loads(jsonOutput)

    for data in decoded_data['utterances_tone']:
        print("\nStatement:", data.get('utterance_text'), )
        if not data['tones']:
            print('Tones Identified: None')
        else:
            for word in data['tones']:
                print('Tones Identified:', word.get('tone_id'))
        print("\n")
#print("\n", transcript + "\n")
# print("Accuracy is", round(confidence*100, 1))


if __name__ == "__main__":
    main()


# In[ ]:




