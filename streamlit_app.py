import streamlit as st
import json
from recommendation_engine import GameRecommendationEngine

from game_data import SAMPLE_GAMES

# Initialize the recommendation engine
@st.cache_resource
def load_recommendation_engine():
    return GameRecommendationEngine()

def main():
    st.set_page_config(
        page_title="Game Recommendation Engine",
        page_icon="🎮",
        layout="wide"
    )
    
    st.title("🎮 AI-Powered Game Recommendation Engine")
    st.markdown("*Built with Vector Databases, Embeddings & LangChain concepts*")
    
    # Load the engine
    engine = load_recommendation_engine()
    
    # Sidebar for user input
    st.sidebar.header("How would you like to discover games?")
    
    method = st.sidebar.radio(
        "Choose recommendation method:",
        ["Describe Your Preferences", "Based on Games You Like", "Hybrid Approach"]
    )
    
    if method == "Describe Your Preferences":
        st.header("Tell us what you're looking for")
        
        preferences = st.text_area(
            "Describe your ideal game:",
            placeholder="I want a story-driven RPG with magic and open world exploration...",
            height=100
        )
        
        num_recs = st.slider("Number of recommendations:", 3, 10, 5)
        
        if st.button("Get Recommendations") and preferences:
            with st.spinner("Finding perfect games for you..."):
                recommendations = engine.get_recommendations_by_preferences(preferences, num_recs)
                display_recommendations(recommendations)
    
    elif method == "Based on Games You Like":
        st.header("Select games you enjoyed")
        
        # Create a searchable multiselect
        game_options = {game['title']: game['id'] for game in SAMPLE_GAMES}
        selected_games = st.multiselect(
            "Choose games you like:",
            options=list(game_options.keys()),
            help="Select multiple games to get better recommendations"
        )
        
        num_recs = st.slider("Number of recommendations:", 3, 10, 5)
        
        if st.button("Get Recommendations") and selected_games:
            selected_ids = [game_options[title] for title in selected_games]
            
            with st.spinner("Analyzing your taste..."):
                recommendations = []
                for game_id in selected_ids:
                    game_recs = engine.get_recommendations_by_game(game_id, 3)
                    recommendations.extend(game_recs)
                
                # Remove duplicates and sort
                unique_recs = {}
                for rec in recommendations:
                    game_id = rec['game']['id']
                    if game_id not in unique_recs or rec['similarity_score'] > unique_recs[game_id]['similarity_score']:
                        unique_recs[game_id] = rec
                
                final_recs = list(unique_recs.values())
                final_recs.sort(key=lambda x: x['similarity_score'], reverse=True)
                
                display_recommendations(final_recs[:num_recs])
    
    else:  # Hybrid Approach
        st.header("Hybrid Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Games you like")
            game_options = {game['title']: game['id'] for game in SAMPLE_GAMES}
            selected_games = st.multiselect(
                "Select games:",
                options=list(game_options.keys())
            )
        
        with col2:
            st.subheader("Additional preferences")
            preferences = st.text_area(
                "Describe what else you're looking for:",
                placeholder="Something with good graphics and multiplayer...",
                height=100
            )
        
        num_recs = st.slider("Number of recommendations:", 3, 10, 5)
        
        if st.button("Get Hybrid Recommendations") and (selected_games or preferences):
            selected_ids = [game_options[title] for title in selected_games]
            
            with st.spinner("Creating personalized recommendations..."):
                recommendations = engine.get_hybrid_recommendations(
                    selected_ids, 
                    preferences or "", 
                    num_recs
                )
                display_recommendations(recommendations)

def display_recommendations(recommendations):
    """Display recommendations in a nice format"""
    if not recommendations:
        st.warning("No recommendations found. Try adjusting your preferences!")
        return
    
    st.header("🎯 Recommended Games")
    
    for i, rec in enumerate(recommendations, 1):
        game = rec['game']
        score = rec['similarity_score']
        
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader(f"{i}. {game['title']}")
               # Safely display genres and tags
                
                st.write(f"**Genres:** {game['genres']}")
                st.write(f"**Description:** {game['description']}")
                st.write(f"**Tags:** {game['tags']}")
                # Display additional info
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Rating", f"{game['rating']}/10")
                with col_b:
                    st.metric("Difficulty", game['difficulty'].title())
                with col_c:
                    st.metric("Multiplayer", game['multiplayer'].title())
            
            with col2:
                st.metric("Match Score", f"{score:.1%}")
                
                # Color-coded score
                if score > 0.8:
                    st.success("Excellent Match!")
                elif score > 0.6:
                    st.info("Good Match")
                else:
                    st.warning("Moderate Match")
            
            st.divider()

if __name__ == "__main__":
    main()