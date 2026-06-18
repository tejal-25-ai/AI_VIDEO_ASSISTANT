import rich 
from utils.audio_processor import process_input
from core.transcriber import transcribe_all

source = "https://youtu.be/eGoszzMkGfU"

chunks = process_input(source)
print(transcribe_all(chunks=chunks))