# import pickle
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from sklearn.metrics.pairwise import cosine_similarity
# from helper import get_recommendations
# import uvicorn
# import os
# from pyngrok import ngrok  # Import ngrok from pyngrok

import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from helper import get_recommendations
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from pyngrok import ngrok
import os

# Load your data into df (example with pickle)
with open('tfidf_vectorizer.pkl', 'rb') as f:
    tfidf = pickle.load(f)

with open('tfidf_matrix.pkl', 'rb') as f:
    tfidf_matrix = pickle.load(f)

with open('data.pkl', 'rb') as f:
    df = pickle.load(f)

# Compute cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Assuming other necessary imports and setup for FastAPI

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
    port = 80  # Replace with your actual port number if different

    # Use pyngrok to open a tunnel to your local FastAPI application
    ngrok_tunnel = ngrok.connect(addr=port, proto="http")
    public_url = ngrok_tunnel.public_url
    print(f"Ngrok Tunnel URL: {public_url}")

    try:
        # Run FastAPI application using uvicorn
        uvicorn.run(app, host='localhost', port=port)
    finally:
        # Disconnect ngrok
        ngrok.kill()

# Load necessary data and setup as before
# Load the necessary pickle files and setup your FastAPI application as before

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
    port = 80

    # Use pyngrok to open a tunnel to your local FastAPI application
    ngrok_tunnel = ngrok.connect(addr=port, proto="http")
    public_url = ngrok_tunnel.public_url
    print(f"Ngrok Tunnel URL: {public_url}")

    try:
        # Run FastAPI application using uvicorn
        uvicorn.run(app, host='localhost', port=port)
    finally:
        # Disconnect ngrok
        ngrok.kill()
