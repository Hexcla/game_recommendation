# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from recommendation_engine import GameRecommendationEngine

app = FastAPI(title="Game Recommendation API", version="1.0.0")

# Initialize recommendation engine
engine = GameRecommendationEngine()

class PreferenceRequest(BaseModel):
    preferences: str
    num_recommendations: int = 5

class GameBasedRequest(BaseModel):
    game_id: str
    num_recommendations: int = 5

class HybridRequest(BaseModel):
    liked_games: List[str]
    preferences: Optional[str] = ""
    num_recommendations: int = 5

@app.get("/")
async def root():
    return {"message": "Game Recommendation Engine API"}

@app.post("/recommendations/preferences")
async def get_preference_recommendations(request: PreferenceRequest):
    try:
        recommendations = engine.get_recommendations_by_preferences(
            request.preferences, 
            request.num_recommendations
        )
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommendations/game")
async def get_game_recommendations(request: GameBasedRequest):
    try:
        recommendations = engine.get_recommendations_by_game(
            request.game_id, 
            request.num_recommendations
        )
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommendations/hybrid")
async def get_hybrid_recommendations(request: HybridRequest):
    try:
        recommendations = engine.get_hybrid_recommendations(
            request.liked_games,
            request.preferences,
            request.num_recommendations
        )
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/games")
async def list_games():
    return {"games": [game['metadata'] for game in engine.games_data]}