# recommendation_engine.py
import json
import numpy as np
from game_data import GameDataProcessor
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import chromadb
from typing import List, Dict

class GameRecommendationEngine:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.setup_vector_db()
        self.load_games()
    
    def setup_vector_db(self):
        """Initialize ChromaDB"""
        self.client = chromadb.Client()
        try:
            self.collection = self.client.get_collection("games")
        except:
            self.collection = self.client.create_collection("games")
    
    def load_games(self):
        """Load games into vector database"""
        try:
            with open('processed_games.json', 'r') as f:
                self.games_data = json.load(f)
        except FileNotFoundError:
            # Create data if doesn't exist
            processor = GameDataProcessor()
            self.games_data = processor.save_processed_data()
        
        # Add to ChromaDB if empty
        if self.collection.count() == 0:
            self.populate_vector_db()
    
    def populate_vector_db(self):
        """Populate ChromaDB with game data"""
        def flatten_metadata(game):
            return {
                "id": game["id"],
                "title": game["title"],
                "genres": ', '.join(game["genres"]) if isinstance(game["genres"], list) else game["genres"],
                "description": game["description"],
                "features": game["features"],
                "difficulty": game["difficulty"],
                "multiplayer": game["multiplayer"],
                "rating": game["rating"],
                "tags": ', '.join(game["tags"]) if isinstance(game["tags"], list) else game["tags"]
            }

        embeddings = [game['embedding'] for game in self.games_data]
        documents = [game['text'] for game in self.games_data]
        metadatas = [flatten_metadata(game['metadata']) for game in self.games_data]
        ids = [game['id'] for game in self.games_data]

        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def get_recommendations_by_preferences(self, preferences: str, num_recommendations: int = 5):
        """Get recommendations based on user preferences"""
        # Create embedding for user preferences
        pref_embedding = self.model.encode(preferences)
        
        # Query vector database
        results = self.collection.query(
            query_embeddings=[pref_embedding.tolist()],
            n_results=num_recommendations
        )
        
        recommendations = []
        for i, metadata in enumerate(results['metadatas'][0]):
            recommendations.append({
                'game': metadata,
                'similarity_score': 1 - results['distances'][0][i]  # Convert distance to similarity
            })
        
        return recommendations
    
    def get_recommendations_by_game(self, game_id: str, num_recommendations: int = 5):
        """Get recommendations based on a specific game"""
        # Find the game in our data
        game_data = None
        for game in self.games_data:
            if game['id'] == game_id:
                game_data = game
                break
        
        if not game_data:
            return []
        
        # Use the game's embedding to find similar games
        results = self.collection.query(
            query_embeddings=[game_data['embedding']],
            n_results=num_recommendations + 1  # +1 to exclude the game itself
        )
        
        recommendations = []
        for i, (metadata, distance) in enumerate(zip(results['metadatas'][0], results['distances'][0])):
            if metadata['id'] != game_id:  # Exclude the input game
                recommendations.append({
                    'game': metadata,
                    'similarity_score': 1 - distance
                })
        
        return recommendations[:num_recommendations]
    
    def get_hybrid_recommendations(self, liked_games: List[str], preferences: str, num_recommendations: int = 5):
        """Hybrid approach: combine game-based and preference-based recommendations"""
        all_recommendations = {}
        
        # Get recommendations based on liked games
        for game_id in liked_games:
            game_recs = self.get_recommendations_by_game(game_id, 10)
            for rec in game_recs:
                game_id = rec['game']['id']
                if game_id not in all_recommendations:
                    all_recommendations[game_id] = []
                all_recommendations[game_id].append(rec['similarity_score'])
        
        # Get recommendations based on preferences
        pref_recs = self.get_recommendations_by_preferences(preferences, 10)
        for rec in pref_recs:
            game_id = rec['game']['id']
            if game_id not in all_recommendations:
                all_recommendations[game_id] = []
            all_recommendations[game_id].append(rec['similarity_score'] * 0.7)  # Weight preference-based lower
        
        # Calculate average scores and sort
        final_recommendations = []
        for game_id, scores in all_recommendations.items():
            if game_id not in liked_games:  # Don't recommend games they already like
                avg_score = np.mean(scores)
                game_metadata = next(g['metadata'] for g in self.games_data if g['id'] == game_id)
                final_recommendations.append({
                    'game': game_metadata,
                    'similarity_score': avg_score
                })
        
        # Sort by score and return top N
        final_recommendations.sort(key=lambda x: x['similarity_score'], reverse=True)
        return final_recommendations[:num_recommendations]
