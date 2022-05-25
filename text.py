# importing libraries 
import os
import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
from moviepy.editor import VideoFileClip
import operator
from collections import defaultdict
import pandas as pd



class Video_to_Text:
   def __init__(self, video_name):
      self.video_name = video_name
      self.transcript = ""
      self.transcription()

   def from_mp4_to_mp3(self):
      """
      Converts video to audio using MoviePy library that uses `ffmpeg` 
      under the hood 
      """
      print("Starting to convert video to audio")
      output_ext="mp3"
      filename, ext = os.path.splitext(self.video_name)
      clip = VideoFileClip(self.video_name)
      clip.audio.write_audiofile(f"{filename}.{output_ext}")
      self.audio = f"{filename}.{output_ext}"

   def from_mp3_to_text(self):
      print("Starting to transcribe audio")
      # create a speech recognition object
      r = sr.Recognizer()
      # a function that splits the audio file into chunks
      # and applies speech recognition
      """
      Splitting the large audio file into chunks
      and apply speech recognition on each of these chunks
      """
      # open the audio file using pydub
      sound = AudioSegment.from_mp3(self.audio)  
      chunks = split_on_silence(sound,
         # experiment with this value for your target audio file
         min_silence_len = 1000,
         # adjust this per requirement
         silence_thresh = sound.dBFS-14,
         # keep the silence for 1 second, adjustable as well
         keep_silence=1000,
      )
      folder_name = "audio-chunks"
      # create a directory to store the audio chunks
      if not os.path.isdir(folder_name):
         os.mkdir(folder_name)
      # process each chunk 
      for i, audio_chunk in enumerate(chunks, start=1):
         # export audio chunk and save it in
         # the `folder_name` directory.
         chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
         audio_chunk.export(chunk_filename, format="wav")
         # recognize the chunk
         with sr.AudioFile(chunk_filename) as source:
               audio_listened = r.record(source)
               # try converting it to text
               try:
                  text = r.recognize_google(audio_listened, language='it-IT')
               except sr.UnknownValueError as e:
                  #print("Error:", str(e))
                  continue
               else:
                  text = f"{text.capitalize()}. "
                  #print(chunk_filename, ":", text)
                  self.transcript += text
      # return the text for all chunks detected
      return self.transcript

   def transcription(self):
      self.from_mp4_to_mp3()
      self.from_mp3_to_text()
      return self.transcript

class Text_Analizer:
   def __init__(self, transcript) -> None:
      self.stop_words = ['il', 'lo', 'la', 'le', 'gli', 'loro', 'i' ,'che', 'mi' ,'ti', 'voi' ,'vostro' , 'un', 'è', ' ', '', '  ' ]

      self.transcript = str(transcript)
      self.dictionary = self.unique_words().keys()
      self.count = len(self.dictionary)
      self.word_count = self.unique_words()
      self.ranking_words = sorted(self.word_count.items(), key=operator.itemgetter(1), reverse=True)

   def unique_words(self):
      """
      Counts the number of unique words in the transcript
      """
      # import stopwords from nltk
      

      # import the transcript from the video
      transcript = self.transcript
      # split the transcript into words
      words = transcript.split(' ')
      # remove stopwords from the words list
      words = [word.lower().strip('.,:"\!?;') for word in words if word.lower().strip('.,:"\!?;') not in self.stop_words]
      dictionary = {}
      for word in words:
         if word in dictionary:
            dictionary[word] += 1
         else:
            dictionary[word] = 1
      return dictionary

   def markov_chain(self):
      transcript = self.transcript
      from collections import defaultdict

      words = transcript.split(' ')
      
      # Initialize a default dictionary to hold all of the words and next words
      m_dict = defaultdict(list)
      
      # Create a zipped list of all of the word pairs and put them in word: list of next words format
      for current_word, next_word in zip(words[0:-1], words[1:]):
         m_dict[current_word].append(next_word)

      # Convert the default dict back into a dictionary
      m_dict = dict(m_dict)
      return m_dict

   def generate_sentence(self, count=15):
      chain = self.markov_chain() # it uses the transcript from the video
      import random
      '''Input a dictionary in the format of key = current word, value = list of next words
      along with the number of words you would like to see in your generated sentence.'''
 
      # Capitalize the first word
      word1 = random.choice(list(chain.keys()))
      sentence = word1.capitalize()

      # Generate the second word from the value list. Set the new word as the first word. Repeat.
      for i in range(count-1):
         word2 = random.choice(chain[word1])
         word1 = word2
         sentence += ' ' + word2

      # End it with a period
      sentence += '.'
      return(sentence)

   def words_list_overtime(self):
      words = self.transcript.split(' ')
      # remove stopwords from the words list
      words = [word.lower().strip('.,:"\!?;') for word in words if word.lower().strip('.,:"\!?;') not in self.stop_words]
      self.big_transcript = [word.lower() for word in words]
      self.big_dictionary_overtime = {}
      for i, _ in enumerate(self.big_transcript):

         dictionary = {}
         for word in self.big_transcript[:i]:
            if word in dictionary:
               dictionary[word] += 1
            else:
               dictionary[word] = 1
         self.big_dictionary_overtime[i] = dictionary
      return self.big_dictionary_overtime

   def create_matrix_frequency(self):  #### - > works fine
      '''At every word, it counts the number of times it appears in the transcript for all the words in the transcription'''
      import numpy as np
      # create zeros matrix
      self.df = np.zeros( (len(self.big_dictionary_overtime), len(self.unique_words().keys())) )
      # transform in a dataframe
      self.df = pd.DataFrame(self.df, columns = self.unique_words().keys())
      #polulate the matrix
      for i, (iteration, dict) in enumerate(self.big_dictionary_overtime.items()):
         for j, word in enumerate( dict.keys()):
            self.df[word].iloc[i] = list(dict.values())[j]
      # return the matrix
      return self.df
   
   def create_graphs(self):
      self.words_list_overtime()
      self.create_matrix_frequency()
      import plotly.express as px

      self.fig = px.line(self.df, x=self.df.index, y=self.df.columns)
      return self.fig

   def create_graphs_2(self):
      counter = self.unique_words()
      best_words = sorted(counter.items(), key=operator.itemgetter(1), reverse=True)[:10]
      words = pd.DataFrame([word[0] for word in best_words], columns=['word'])
      values = pd.DataFrame([word[1] for word in best_words], columns=['count'])
      frame = [words, values]
      self.df = pd.concat(frame, axis=1)
      import plotly.express as px
      self.fig1 = px.bar(self.df, x='word', y='count')
      return self.fig1