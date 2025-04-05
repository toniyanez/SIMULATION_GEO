from fastapi import FastAPI, UploadFile, File
import pandas as pd
import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    df = pd.read_excel(file.file)
    locations = df['Location'].tolist()

    prompt = f"Given recent geopolitical events, analyze potential supply chain impacts for operations in these locations: {locations}. Provide scenarios, impact, probability, and severity."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"analysis": response.choices[0].message.content}
