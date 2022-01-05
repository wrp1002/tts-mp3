from pygame import mixer
import requests
import time
import socketio
import os

def play_audio(audio_file):
	print(f"playing audio from {audio_file}")
	mixer.init()
	mixer.music.load(audio_file)
	mixer.music.play()
	while mixer.music.get_busy():  # wait for music to finish playing
		time.sleep(1)
	mixer.quit()
	print("Done!")


def ttsmp3(text):
	make_new_url = "https://ttsmp3.com/makemp3_new.php"

	params = {
		"msg": text,
		"lang": "Salli",
		"source": "ttsmp3",
	}

	res = requests.post(make_new_url, data=params).json()

	print(res)

	download_url = res.get("URL")
	file_name = res.get("MP3")

	r = requests.get(download_url, stream=True)
	with open(file_name,'wb') as file:
		for chunk in r.iter_content(chunk_size=1024):
			file.write(chunk)

	play_audio(file_name)
	print("Deleting file")
	time.sleep(1)
	os.remove(file_name)


def bablepod():
	sio = socketio.Client(logger=True, engineio_logger=True)
	#sio = socketio.Client()

	@sio.event
	def connect():
		print('connection established')

	@sio.event
	def disconnect():
		print('disconnected from server')

	@sio.event
	def available_inputs(data):
		print("YO GOT AN EVENT")
		print("available inputs", data)



	sio.connect('http://nextcloud.local:3000/socket.io/')
	print('my sid is', sio.sid)

	sio.emit("switch_input", "plughw:2,1")
	# sleep to avoid weird click sound
	sio.sleep(3)
	sio.emit("switch_output", "airplay_192.168.4.30_7000")


	# do audio output
	sio.sleep(3)


	# reset input and output
	sio.emit("switch_output", "void")
	sio.emit("switch_input", "void")

	sio.sleep(1)

	sio.disconnect()