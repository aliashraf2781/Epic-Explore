import pickle
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from helper import get_recommendations
from dotenv import load_dotenv
from pyngrok import ngrok
import os

# Load the environment variables
load_dotenv()

# Load the pre-saved TF-IDF vectorizer, TF-IDF matrix, and DataFrame
with open('tfidf_vectorizer.pkl', 'rb') as f:
    tfidf = pickle.load(f)

with open('tfidf_matrix.pkl', 'rb') as f:
    tfidf_matrix = pickle.load(f)

with open('data.pkl', 'rb') as f:
    df = pickle.load(f)

# Compute cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# FastAPI app
app = FastAPI()

class PlaceRequest(BaseModel):
    place_name: str



@app.get("/ping")
async def ping():
    return "Hello there"

@app.post("/recommendations/")
def recommend_places(request: PlaceRequest):
    place_name = request.place_name
    recommendations = get_recommendations(place_name, df, cosine_sim)
    if recommendations.empty:
        raise HTTPException(status_code=404, detail="Recommendations not found")
    return recommendations.to_dict(orient='records')


if __name__ == "__main__":
    NGROK_AUTH = os.getenv("NGROK_AUTH")
    ngrok.set_auth_token(NGROK_AUTH)
    public_url = ngrok.connect(8000)
    print("Public URL:", public_url)
    uvicorn.run(app, host='localhost', port=8000)