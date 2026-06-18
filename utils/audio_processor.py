import yt_dlp
from pydub import AudioSegment
import os

DOWNLOAD_DIR = 'downloades'
os.makedirs(DOWNLOAD_DIR,exist_ok = True)

def download_youtube_audio(url :str) ->str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
    return filename



def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000) #16khz
    audio.export(output_path, format="wav")
    return output_path



def chunk_audio(wav_path : str , chunk_minutes : int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000 

    chunks = []

    for i, start in enumerate(range(0,len(audio),chunk_ms)):
        chunk = audio[start : start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path , format = "wav")

        chunks.append(chunk_path)
    
    return chunks

def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks
""" 
import yt_dlp
# This github repo: yt-dlp is a command-line tool used to download videos, audio, subtitles, and metadata from YouTube and many other websites.
from pydub import AudioSegment
import os 

DOWNLOAD_DIR = 'downloades'
os.makedirs(DOWNLOAD_DIR,exist_ok= True)

# step1 : to download youtube audio through url 
def download_youtube_audio(url:str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR,"%(title)s.%(ext)s") # in the Download_dir we are storing our op & last para - we define how the name off file will be saved.
    ydl_ops = {
        "format": "bestaudio/best",
        #"ffmpeg_location": r"C:\ffmpeg\bin",
    "outtmpl": output_path,
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "wav",
        "preferredquality": "192"
    }],
     "quiet": True ,
    }

    with yt_dlp.YoutubeDL(ydl_ops) as ydl:
        info = ydl.extract_info(url,download=True)
        filename = ydl.prepare_filename(info).replace(".webm",".wav").replace(".m4a",".wav")
    return filename


def convert_to_wav(input_path: str) -> str:
    #Convert any audio/video file to WAV format using pydub.
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000) #16khz
    audio.export(output_path, format="wav")
    return output_path



# Now to Chunk the file 

def chunk_audio(wav_path: str , chunk_mintues : int= 10)-> list:
    # so we will lets say chunk 50 min files into parts- and this chunkedfiles will be saved with names in the downlaoder folder in the list .
    audio = AudioSegment.from_wav(wav_path)
    # chunks works in millisec - 60*1000 
    chunks_ms = chunk_mintues * 60 * 1000

    chunks = []

    for i,start in enumerate(range(0,len(audio),chunks_ms)):
        chunk = audio[start : start + chunks_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format = "wav")

        chunks.append(chunk_path)

        return chunks
    

def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks
    """

    

    






