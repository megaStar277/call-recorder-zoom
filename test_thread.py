from concurrent.futures import ThreadPoolExecutor

def record_audio(name):
    print(f"Recording audio {name} ...")

# use ThreadPoolExecutor to create a new thread
with ThreadPoolExecutor() as executor:
    audio_name = "my_audio"
    executor.submit(record_audio, f"{audio_name}.mp3")