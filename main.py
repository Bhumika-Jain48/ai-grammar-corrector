from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from dotenv import load_dotenv
from google import genai

import os
import json

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


class TextInput(BaseModel):
    text: str


@app.get("/")
async def home():

    with open(
        "templates/index.html",
        "r",
        encoding="utf-8"
    ) as file:

        return HTMLResponse(file.read())


@app.post("/correct")
async def correct(data: TextInput):

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=f"""
You are a grammar correction assistant.

Return ONLY valid JSON.

Example:

{{
  "corrected_text":"I went to the market yesterday.",
  "explanation":"Changed 'has went' to 'went' because simple past tense is required."
}}

Text:
{data.text}
"""
        )

        text = response.text.strip()

        if text.startswith("```json"):
            text = text.replace("```json", "")
            text = text.replace("```", "").strip()

        result = json.loads(text)

        return result

    except Exception as e:

        return {
            "corrected_text": "",
            "explanation": "",
            "error": str(e)
        }