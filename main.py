from recognizer import SpeechRecognizer

if __name__ == "__main__":
	filename = ""
	path = ""
	out = path + "/transcript.txt"

	r = SpeechRecognizer(path, filename, recognizer_type="google")
	r.chunkAudio()
	r.transcribe(out)
