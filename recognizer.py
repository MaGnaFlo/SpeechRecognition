import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from progressbar import ProgressBar
import time

""" Wrapper of speech recognition library.
	Allows to load, segment and transcribe and audio file."""
class SpeechRecognizer():
	def __init__(self, path, filename, recognizer_type="sphinx", verbose=True):
		try:
			self.audiofile = AudioSegment.from_wav(path+"/"+filename)
			self.path = path
			self.filename = filename
			if recognizer_type.lower() not in ["sphinx", "google"]:
				raise TypeError
			self.recognizer_type = recognizer_type.lower()
			self.recognizer = sr.Recognizer()
			self.use_chunks = False
			self.verbose = verbose
		except TypeError:
			print("Recognizer type not available.")
		except:
			print("Cannot read audio file.")
		finally:
			time.sleep(2)

	""" Chunks the audio based on silences in the discourse."""
	def chunkAudio(self, min_silence_length=400, silence_thresh=-50):
		if self.verbose:
			print("Chunking audio...")
		self.chunks = split_on_silence(self.audiofile, 
						  min_silence_len=min_silence_length, 
						  silence_thresh=silence_thresh)
		try:
			os.mkdir("audio_chunks")
		except(FileExistsError):
			pass
		os.chdir("audio_chunks")
		self.use_chunks = True
		if self.verbose:
			print(f"Audio has been chunked into {len(self.chunks)} parts.")
			time.sleep(2)

	""" Performs the transcription."""
	def transcribe(self, outfilepath="", added_silence=1000):
		if self.verbose:
			print("Initiating transcription...")
			time.sleep(1)
			errors = []

		transcript = open(outfilepath, "w+")
		if self.use_chunks:
			pbar = ProgressBar(len(self.chunks), width=30, prefix="Transcribing ")
			for i, ck in enumerate(self.chunks):
				chunksilent = AudioSegment.silent(duration=added_silence)
				audio_chunk = chunksilent + ck + chunksilent
				audio_chunk.export(f"./chunk_{i}.wav", bitrate='192k', format="wav")
				AUDIO_CHUNK = f"chunk_{i}.wav"
				with sr.AudioFile(AUDIO_CHUNK) as source:
				    audio = self.recognizer.record(source)
				try:
					if self.recognizer_type == "sphinx":
						text = self.recognizer.recognize_sphinx(audio) + " "
						transcript.write(text)
					elif self.recognizer_type == "google":
						text = self.recognizer.recognize_google(audio) + " "
						transcript.write(text)
				except sr.UnknownValueError:
				    errors.append("UnknownValueError")
				finally:
					os.remove(AUDIO_CHUNK)
					pbar.update()
			pbar.end()

		else:
			with sr.AudioFile(self.path+'/'+self.filename) as source:
				audio = self.recognizer.record(source)
				try:
					if self.recognizer_type == "sphinx":
						text = self.recognizer.recognize_sphinx(audio) + " "
						transcript.write(text)
					elif self.recognizer_type == "google":
						text = self.recognizer.recognize_google(audio) + " "
						transcript.write(text)
				except sr.UnknownValueError:
				    errors.append("UnknownValueError")

		os.chdir("..")
		os.rmdir("audio_chunks")
		transcript.close()
		if self.verbose:
			if self.use_chunks and len(errors) == len(self.chunks):
				print("Transcription failed!")
			elif self.use_chunks:
				print(f"Transcription performed successfully! ({len(errors)} errors)")
			elif len(errors) > 0:
				print("Transcription failed!")
			else:
				print("Transcription performed successfully!")
				