# utils/audio_processing.py
# Functions for audio transcription and text-to-speech

import asyncio
import logging
import os
import tempfile
import subprocess
import json
import wave
from gtts import gTTS
from vosk import Model, KaldiRecognizer
import speech_recognition as sr

logger = logging.getLogger(__name__)

async def text_to_speech(text):
    temp_mp3_path = None
    try:
        fd, temp_mp3_path = tempfile.mkstemp(suffix='.mp3')
        os.close(fd)
        
        def generate_speech(text_to_speak, output_path):
            try:
                tts = gTTS(text=text_to_speak, lang='ru')
                tts.save(output_path)
                return True
            except Exception as e:
                logger.error(f"Error in speech generation: {e}")
                return False
        
        loop = asyncio.get_event_loop()
        success = await loop.run_in_executor(None, generate_speech, text, temp_mp3_path)
        
        if not success or not os.path.exists(temp_mp3_path) or os.path.getsize(temp_mp3_path) == 0:
            logger.error("MP3 file not created or empty")
            return None
        
        return temp_mp3_path
    
    except Exception as e:
        logger.error(f"Error creating voice response: {e}")
        if temp_mp3_path and os.path.exists(temp_mp3_path):
            os.unlink(temp_mp3_path)
        return None

async def transcribe_audio(file_path, model_path):
    wav_file_path = None
    wf = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            wav_file_path = temp_file.name
        
        process = await asyncio.create_subprocess_exec(
            'ffmpeg', '-i', file_path, '-ar', '16000', '-ac', '1', wav_file_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            logger.error(f"FFmpeg error: {stderr.decode()}")
            return "Error: unable to convert audio file"
        
        if not os.path.exists(model_path):
            logger.error(f"Vosk model not found at {model_path}")
            return "Error: speech recognition model not found"
        
        model = await asyncio.to_thread(Model, model_path)
        
        wf = wave.open(wav_file_path, "rb")
        
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            logger.error("Unsupported audio format")
            return "Error: unsupported audio format"
        
        recognizer = await asyncio.to_thread(KaldiRecognizer, model, wf.getframerate())
        await asyncio.to_thread(recognizer.SetWords, True)
        
        result = ""
        while True:
            data = await asyncio.to_thread(wf.readframes, 4000)
            if len(data) == 0:
                break
            if await asyncio.to_thread(recognizer.AcceptWaveform, data):
                part_result = json.loads(await asyncio.to_thread(recognizer.Result))
                result += part_result.get("text", "") + " "
        
        part_result = json.loads(await asyncio.to_thread(recognizer.FinalResult))
        result += part_result.get("text", "")
        
        return result.strip()
    
    except Exception as e:
        logger.error(f"Error during audio transcription: {e}")
        return ""
    
    finally:
        if wf is not None:
            await asyncio.to_thread(wf.close)
        if wav_file_path and os.path.exists(wav_file_path):
            os.unlink(wav_file_path)

async def transcribe_audio_with_sr(file_path):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            wav_file_path = temp_file.name
        
        subprocess.run(['ffmpeg', '-i', file_path, '-ar', '16000', '-ac', '1', wav_file_path])
        
        r = sr.Recognizer()
        
        with sr.AudioFile(wav_file_path) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language="ru-RU")
            
            os.unlink(wav_file_path)
            return text
    except sr.UnknownValueError:
        logger.error("Could not recognize speech")
        return ""
    except sr.RequestError as e:
        logger.error(f"Speech recognition service error: {e}")
        return ""
    except Exception as e:
        logger.error(f"Error during audio transcription: {e}")
        return ""