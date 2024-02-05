# uvicon main:app
# uvicorn main:app --reload
# Get-ExecutionPolicy
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# .\venv\Scripts\Activate

from fastapi import FastAPI, File,UploadFile,HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai


# Custome function imports
from functions.openai_request import convert_audio_to_text, get_chat_response
# Custome function imports


app = FastAPI()


# CORS - Origins
Origins =[
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:3000"
]
# CORS - Origins

# CORS - middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=Origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# CORS - middleware


@app.get("/health")
async def root():
    return {"message": "healthy"}

# get audio
@app.get("/post-audio-get/")
async def get_audio():
   # get saved audio
   audio_input = open("audio.mp3","rb")


   #decode audio
   message_decoded = convert_audio_to_text(audio_input)

   print(message_decoded)


   # to ensure message decorderd
   if not message_decoded:
       return HTTPException(status_code=400,detail="failed to decode the audio")

   #get chat gpt response
   chat_response = get_chat_response(message_decoded)

   print(chat_response)

   return "Done"


# post chatbot responses
# ** not playing in browser when post request

#@app.post("/post-audio/")
#async def post_audio( file: UploadFile = File(...)):
 #   print("hello")