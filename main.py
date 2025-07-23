from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import base64
import io
import numpy as np
import soundfile as sf
import whisper
from scipy.signal import resample

from property_management import answer_property_question_local

app = FastAPI()
model = whisper.load_model("base")


class Base64Audio(BaseModel):
    audio_base64: str


class Prompt(BaseModel):
    prompt: str


def decode_audio(audio_bytes: bytes) -> np.ndarray:
    # Read audio from bytes
    audio_io = io.BytesIO(audio_bytes)
    audio_np, sample_rate = sf.read(audio_io)

    # Convert stereo to mono if needed
    if len(audio_np.shape) == 2:
        audio_np = np.mean(audio_np, axis=1)

    # Resample to 16000 Hz if needed
    if sample_rate != 16000:
        duration = audio_np.shape[0] / sample_rate
        new_length = int(duration * 16000)
        audio_np = resample(audio_np, new_length)

    return audio_np.astype(np.float32)


def transcribe_audio_from_bytes(audio_bytes: bytes) -> str:
    audio_np = decode_audio(audio_bytes)
    result = model.transcribe(audio_np)
    return result["text"]


@app.post("/prompt")
async def prompt_response(payload: Prompt):
    try:
        return answer_property_question_local(payload.prompt)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/prompt/encodedAudio")
async def transcribe_base64_audio(payload: Base64Audio):
    try:
        audio_bytes = base64.b64decode(payload.audio_base64)
        text = transcribe_audio_from_bytes(audio_bytes)
        return answer_property_question_local(text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/prompt/file")
async def transcribe_audio_file(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        text = transcribe_audio_from_bytes(file_bytes)
        return answer_property_question_local(text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
