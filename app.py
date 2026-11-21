from fastapi import FastAPI, Response
from pydantic import BaseModel
import edge_tts

app = FastAPI()

class SpeechRequest(BaseModel):
    text: str
    voice: str = "km-KH-SreymomNeural"

@app.get("/")
def home():
    return {"status": "Khmer Voice API is Running!"}

@app.post("/tts")
async def generate_tts(req: SpeechRequest):
    communicate = edge_tts.Communicate(req.text, req.voice)
    audio_data = bytearray()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data.extend(chunk["data"])
    return Response(content=bytes(audio_data), media_type="audio/mpeg")
