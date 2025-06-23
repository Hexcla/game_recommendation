import json
import pandas as pd
from sentence_transformers import SentenceTransformer
# Sample games with rich descriptions

  # Sample games with rich descriptions
SAMPLE_GAMES = [
    {
        "id": "witcher3",
        "title": "The Witcher 3: Wild Hunt",
        "genres": ["RPG", "Action", "Adventure"],
        "description": "Open-world fantasy RPG with deep narrative, monster hunting, and moral choices",
        "features": "story-driven, open-world, character-progression, mature-themes",
        "difficulty": "moderate",
        "multiplayer": "single-player",
        "rating": 9.3,
        "tags": ["fantasy", "medieval", "magic", "exploration", "narrative"]
    },
    {
        "id": "minecraft",
        "title": "Minecraft",
        "genres": ["Sandbox", "Survival", "Creative"],
        "description": "Block-building sandbox game with infinite possibilities and creative freedom",
        "features": "creative, building, survival, multiplayer, mod-support",
        "difficulty": "easy",
        "multiplayer": "both",
        "rating": 8.7,
        "tags": ["building", "creative", "survival", "family-friendly", "endless"]
    },
    {
        "id": "cyberpunk2077",
        "title": "Cyberpunk 2077",
        "genres": ["RPG", "Action", "Shooter"],
        "description": "Futuristic cyberpunk RPG in Night City with branching storylines and cybernetic enhancements",
        "features": "story-driven, open-world, character-customization, mature-themes",
        "difficulty": "moderate",
        "multiplayer": "single-player",
        "rating": 7.8,
        "tags": ["cyberpunk", "futuristic", "technology", "crime", "narrative"]
    },
    {
        "id": "valorant",
        "title": "Valorant",
        "genres": ["Shooter", "Tactical", "Competitive"],
        "description": "5v5 character-based tactical shooter with unique agent abilities and precise gunplay",
        "features": "competitive, team-based, skill-based, esports",
        "difficulty": "hard",
        "multiplayer": "multiplayer",
        "rating": 8.2,
        "tags": ["tactical", "competitive", "team-play", "esports", "precision"]
    },
    {
        "id": "animalcrossing",
        "title": "Animal Crossing: New Horizons",
        "genres": ["Simulation", "Social", "Casual"],
        "description": "Peaceful life simulation where you build and customize your island paradise",
        "features": "relaxing, customization, social, daily-activities",
        "difficulty": "easy",
        "multiplayer": "both",
        "rating": 8.5,
        "tags": ["peaceful", "customization", "social", "family-friendly", "relaxing"]
    },
    {
        "id": "darksouls3",
        "title": "Dark Souls III",
        "genres": ["RPG", "Action", "Souls-like"],
        "description": "Challenging action RPG with intricate combat, dark atmosphere, and brutal difficulty",
        "features": "challenging, atmospheric, combat-focused, exploration",
        "difficulty": "very-hard",
        "multiplayer": "both",
        "rating": 9.0,
        "tags": ["challenging", "dark", "medieval", "combat", "atmospheric"]
    },
    {
        "id": "stardewvalley",
        "title": "Stardew Valley",
        "genres": ["Simulation", "RPG", "Farming"],
        "description": "Charming farming simulation with relationships, crafting, and rural life",
        "features": "relaxing, farming, relationships, crafting, pixel-art",
        "difficulty": "easy",
        "multiplayer": "both",
        "rating": 9.1,
        "tags": ["farming", "peaceful", "relationships", "crafting", "pixel-art"]
    },
    {
        "id": "gtav",
        "title": "Grand Theft Auto V",
        "genres": ["Action", "Adventure", "Open-world"],
        "description": "Open-world crime saga with three protagonists in modern Los Santos",
        "features": "open-world, crime, vehicles, mature-themes, sandbox",
        "difficulty": "moderate",
        "multiplayer": "both",
        "rating": 8.9,
        "tags": ["crime", "vehicles", "modern", "sandbox", "mature"]
    },
    {
        "id": "amongus",
        "title": "Among Us",
        "genres": ["Social", "Party", "Deduction"],
        "description": "Social deduction game where crewmates identify impostors through discussion and voting",
        "features": "social, deduction, party-game, quick-sessions",
        "difficulty": "easy",
        "multiplayer": "multiplayer",
        "rating": 7.5,
        "tags": ["social", "deduction", "party", "communication", "simple"]
    },
    {
        "id": "rocketleague",
        "title": "Rocket League",
        "genres": ["Sports", "Racing", "Competitive"],
        "description": "Fast-paced vehicular soccer with rocket-powered cars and aerial gameplay",
        "features": "competitive, physics-based, team-sports, skill-based",
        "difficulty": "moderate",
        "multiplayer": "both",
        "rating": 8.6,
        "tags": ["sports", "cars", "competitive", "physics", "team-play"]
    },
    {
        "id": "zelda_botw",
        "title": "The Legend of Zelda: Breath of the Wild",
        "genres": ["Adventure", "Action", "Open-world"],
        "description": "Open-world adventure with puzzle-solving, exploration, and innovative physics",
        "features": "exploration, puzzle-solving, open-world, adventure",
        "difficulty": "moderate",
        "multiplayer": "single-player",
        "rating": 9.7,
        "tags": ["adventure", "exploration", "puzzles", "fantasy", "nintendo"]
    },
    {
        "id": "fortnite",
        "title": "Fortnite",
        "genres": ["Battle Royale", "Shooter", "Building"],
        "description": "Battle royale with building mechanics and colorful, ever-changing world",
        "features": "battle-royale, building, competitive, seasonal-content",
        "difficulty": "moderate",
        "multiplayer": "multiplayer",
        "rating": 7.8,
        "tags": ["battle-royale", "building", "colorful", "competitive", "seasonal"]
    },
    {
        "id": "overwatch2",
        "title": "Overwatch 2",
        "genres": ["Shooter", "Team-based", "Hero"],
        "description": "Team-based hero shooter with diverse characters and objective-based gameplay",
        "features": "team-based, hero-abilities, competitive, role-based",
        "difficulty": "moderate",
        "multiplayer": "multiplayer",
        "rating": 7.6,
        "tags": ["heroes", "team-play", "competitive", "abilities", "colorful"]
    },
    {
        "id": "civilization6",
        "title": "Civilization VI",
        "genres": ["Strategy", "Turn-based", "4X"],
        "description": "Turn-based strategy game where you build and lead civilizations through history",
        "features": "strategic, turn-based, empire-building, historical",
        "difficulty": "hard",
        "multiplayer": "both",
        "rating": 8.8,
        "tags": ["strategy", "historical", "empire-building", "turn-based", "complex"]
    },
    {
        "id": "fallout4",
        "title": "Fallout 4",
        "genres": ["RPG", "Post-apocalyptic", "Shooter"],
        "description": "Post-apocalyptic RPG with base building, crafting, and moral choices in wasteland Boston",
        "features": "post-apocalyptic, crafting, base-building, story-driven",
        "difficulty": "moderate",
        "multiplayer": "single-player",
        "rating": 8.4,
        "tags": ["post-apocalyptic", "crafting", "building", "wasteland", "narrative"]
    },
    {
        "id": "apex_legends",
        "title": "Apex Legends",
        "genres": ["Battle Royale", "Shooter", "Team-based"],
        "description": "Fast-paced battle royale with unique character abilities and squad-based gameplay",
        "features": "battle-royale, team-based, character-abilities, fast-paced",
        "difficulty": "moderate",
        "multiplayer": "multiplayer",
        "rating": 8.1,
        "tags": ["battle-royale", "fast-paced", "team-play", "abilities", "competitive"]
    },
    {
        "id": "skyrim",
        "title": "The Elder Scrolls V: Skyrim",
        "genres": ["RPG", "Fantasy", "Open-world"],
        "description": "Epic fantasy RPG with dragons, magic, and endless exploration in Nordic-inspired world",
        "features": "open-world, fantasy, character-progression, modding",
        "difficulty": "moderate",
        "multiplayer": "single-player",
        "rating": 9.2,
        "tags": ["fantasy", "dragons", "magic", "exploration", "modding"]
    },
    {
        "id": "terraria",
        "title": "Terraria",
        "genres": ["Sandbox", "Adventure", "2D"],
        "description": "2D sandbox adventure with crafting, building, and boss battles in procedural world",
        "features": "sandbox, crafting, building, boss-battles, 2d",
        "difficulty": "moderate",
        "multiplayer": "both",
        "rating": 8.9,
        "tags": ["2d", "crafting", "adventure", "building", "bosses"]
    },
    {
        "id": "cod_warzone",
        "title": "Call of Duty: Warzone",
        "genres": ["Battle Royale", "Shooter", "Military"],
        "description": "Large-scale military battle royale with realistic weapons and tactical gameplay",
        "features": "battle-royale, military, realistic, tactical",
        "difficulty": "moderate",
        "multiplayer": "multiplayer",
        "rating": 7.9,
        "tags": ["military", "realistic", "battle-royale", "tactical", "weapons"]
    },
    {
        "id": "hades",
        "title": "Hades",
        "genres": ["Roguelike", "Action", "Indie"],
        "description": "Stylish roguelike with Greek mythology, tight combat, and compelling narrative",
        "features": "roguelike, mythology, narrative, fast-paced, indie",
        "difficulty": "moderate",
        "multiplayer": "single-player",
        "rating": 9.0,
        "tags": ["roguelike", "mythology", "stylish", "narrative", "indie"]
    },
    {
        "id": "pokemon_legends",
        "title": "Pokémon Legends: Arceus",
        "genres": ["RPG", "Adventure", "Monster-collecting"],
        "description": "Open-world Pokémon adventure with catching, battling, and exploration in ancient Sinnoh",
        "features": "pokemon, exploration, collecting, adventure, family-friendly",
        "difficulty": "easy",
        "multiplayer": "single-player",
        "rating": 8.3,
        "tags": ["pokemon", "collecting", "adventure", "family-friendly", "exploration"]
    },
    {
        "id": "elden_ring",
        "title": "Elden Ring",
        "genres": ["RPG", "Souls-like", "Open-world"],
        "description": "Challenging open-world souls-like with intricate world design and tough boss battles",
        "features": "challenging, open-world, boss-battles, exploration",
        "difficulty": "very-hard",
        "multiplayer": "both",
        "rating": 9.5,
        "tags": ["challenging", "bosses", "open-world", "fantasy", "exploration"]
    },
    {
        "id": "csgo",
        "title": "Counter-Strike: Global Offensive",
        "genres": ["Shooter", "Tactical", "Competitive"],
        "description": "Tactical team-based shooter with precise gunplay and strategic round-based gameplay",
        "features": "tactical, competitive, team-based, skill-based, esports",
        "difficulty": "hard",
        "multiplayer": "multiplayer",
        "rating": 8.7,
        "tags": ["tactical", "competitive", "esports", "precision", "team-play"]
    },
    {
        "id": "sims4",
        "title": "The Sims 4",
        "genres": ["Simulation", "Life", "Casual"],
        "description": "Life simulation where you create and control virtual people in their daily lives",
        "features": "life-simulation, character-creation, building, relationships",
        "difficulty": "easy",
        "multiplayer": "single-player",
        "rating": 7.9,
        "tags": ["life-sim", "creation", "relationships", "casual", "building"]
    },
    {
        "id": "hollow_knight",
        "title": "Hollow Knight",
        "genres": ["Metroidvania", "Platformer", "Indie"],
        "description": "Beautiful hand-drawn metroidvania with challenging combat and atmospheric exploration",
        "features": "metroidvania, hand-drawn, atmospheric, challenging, indie",
        "difficulty": "hard",
        "multiplayer": "single-player",
        "rating": 9.2,
        "tags": ["metroidvania", "hand-drawn", "atmospheric", "challenging", "exploration"]
    },
    {
        "id": "red_dead_2",
        "title": "Red Dead Redemption 2",
        "genres": ["Action", "Adventure", "Western"],
        "description": "Epic western adventure with stunning visuals, deep narrative, and immersive open world",
        "features": "western, story-driven, open-world, cinematic, immersive",
        "difficulty": "moderate",
        "multiplayer": "both",
        "rating": 9.4,
        "tags": ["western", "cinematic", "story", "immersive", "beautiful"]
    },
    {
        "id": "league_legends",
        "title": "League of Legends",
        "genres": ["MOBA", "Strategy", "Competitive"],
        "description": "Strategic team-based MOBA with diverse champions and competitive ranked gameplay",
        "features": "moba, strategic, team-based, competitive, esports",
        "difficulty": "hard",
        "multiplayer": "multiplayer",
        "rating": 8.4,
        "tags": ["moba", "strategic", "competitive", "champions", "esports"]
    },
    {
        "id": "portal2",
        "title": "Portal 2",
        "genres": ["Puzzle", "First-person", "Sci-fi"],
        "description": "Mind-bending puzzle game with portal mechanics, humor, and cooperative gameplay",
        "features": "puzzle, innovative-mechanics, humor, cooperative, sci-fi",
        "difficulty": "moderate",
        "multiplayer": "both",
        "rating": 9.6,
        "tags": ["puzzle", "innovative", "humor", "cooperative", "sci-fi"]
    },
    {
        "id": "subnautica",
        "title": "Subnautica",
        "genres": ["Survival", "Adventure", "Underwater"],
        "description": "Underwater survival adventure with base building, exploration, and alien ocean mysteries",
        "features": "survival, underwater, exploration, base-building, mystery",
        "difficulty": "moderate",
        "multiplayer": "single-player",
        "rating": 8.8,
        "tags": ["underwater", "survival", "exploration", "mystery", "beautiful"]
    },
    {
        "id": "destiny2",
        "title": "Destiny 2",
        "genres": ["Shooter", "MMO", "Sci-fi"],
        "description": "Sci-fi MMO shooter with raids, PvP, and cooperative gameplay in space opera setting",
        "features": "mmo, cooperative, raids, pvp, sci-fi",
        "difficulty": "moderate",
        "multiplayer": "multiplayer",
        "rating": 8.0,
        "tags": ["sci-fi", "mmo", "cooperative", "raids", "space"]
    },
    {
        "id": "fall_guys",
        "title": "Fall Guys",
        "genres": ["Party", "Platformer", "Casual"],
        "description": "Colorful battle royale party game with obstacle courses and silly physics",
        "features": "party-game, casual, colorful, physics-based, fun",
        "difficulty": "easy",
        "multiplayer": "multiplayer",
        "rating": 7.4,
        "tags": ["party", "colorful", "casual", "fun", "physics"]
    },
    {
        "id": "disco_elysium",
        "title": "Disco Elysium",
        "genres": ["RPG", "Detective", "Narrative"],
        "description": "Narrative-heavy detective RPG with deep dialogue, choices, and psychological themes",
        "features": "narrative-heavy, detective, choices, psychological, mature",
        "difficulty": "moderate",
        "multiplayer": "single-player",
        "rating": 9.3,
        "tags": ["narrative", "detective", "psychological", "choices", "mature"]
    },
    {
        "id": "genshin_impact",
        "title": "Genshin Impact",
        "genres": ["RPG", "Gacha", "Open-world"],
        "description": "Anime-style open-world RPG with elemental combat and character collection",
        "features": "anime-style, elemental-combat, gacha, open-world, free-to-play",
        "difficulty": "easy",
        "multiplayer": "both",
        "rating": 8.1,
        "tags": ["anime", "elemental", "gacha", "open-world", "free-to-play"]
    },
    {
        "id": "minecraft_dungeons",
        "title": "Minecraft Dungeons",
        "genres": ["Action", "Dungeon-crawler", "Family"],
        "description": "Simplified dungeon crawler in Minecraft universe with cooperative gameplay",
        "features": "dungeon-crawler, cooperative, family-friendly, minecraft-style",
        "difficulty": "easy",
        "multiplayer": "both",
        "rating": 7.6,
        "tags": ["dungeon-crawler", "cooperative", "family-friendly", "minecraft", "simple"]
    },
    {
        "id": "sea_thieves",
        "title": "Sea of Thieves",
        "genres": ["Adventure", "Pirate", "Multiplayer"],
        "description": "Pirate adventure with ship sailing, treasure hunting, and cooperative crew gameplay",
        "features": "pirate, cooperative, sailing, treasure-hunting, social",
        "difficulty": "moderate",
        "multiplayer": "multiplayer",
        "rating": 7.8,
        "tags": ["pirate", "sailing", "cooperative", "adventure", "treasure"]
    },
    {
        "id": "ori_will_wisps",
        "title": "Ori and the Will of the Wisps",
        "genres": ["Metroidvania", "Platformer", "Beautiful"],
        "description": "Gorgeous hand-painted metroidvania with emotional story and fluid movement",
        "features": "beautiful, emotional, fluid-movement, hand-painted, atmospheric",
        "difficulty": "moderate",
        "multiplayer": "single-player",
        "rating": 9.0,
        "tags": ["beautiful", "emotional", "platformer", "atmospheric", "hand-painted"]
    },
    {
        "id": "factorio",
        "title": "Factorio",
        "genres": ["Strategy", "Automation", "Building"],
        "description": "Complex automation and factory building game with resource management and optimization",
        "features": "automation, complex, optimization, resource-management, addictive",
        "difficulty": "hard",
        "multiplayer": "both",
        "rating": 9.1,
        "tags": ["automation", "complex", "optimization", "addictive", "engineering"]
    },
    {
        "id": "it_takes_two",
        "title": "It Takes Two",
        "genres": ["Cooperative", "Adventure", "Platformer"],
        "description": "Innovative cooperative adventure designed specifically for two players with creative mechanics",
        "features": "cooperative, innovative, creative-mechanics, story-driven, two-player",
        "difficulty": "moderate",
        "multiplayer": "cooperative",
        "rating": 8.9,
        "tags": ["cooperative", "innovative", "two-player", "creative", "story"]
    },
    {
        "id": "cities_skylines",
        "title": "Cities: Skylines",
        "genres": ["Simulation", "City-builder", "Strategy"],
        "description": "Comprehensive city building simulation with traffic management and urban planning",
        "features": "city-building, simulation, planning, management, modding",
        "difficulty": "moderate",
        "multiplayer": "single-player",
        "rating": 8.6,
        "tags": ["city-building", "simulation", "planning", "management", "complex"]
    },
    {
        "id": "cuphead",
        "title": "Cuphead",
        "genres": ["Platformer", "Boss-rush", "Indie"],
        "description": "Hand-drawn 1930s cartoon-style platformer with challenging boss battles",
        "features": "hand-drawn, cartoon-style, boss-battles, challenging, artistic",
        "difficulty": "very-hard",
        "multiplayer": "both",
        "rating": 8.7,
        "tags": ["hand-drawn", "cartoon", "challenging", "bosses", "artistic"]
    },
    {
        "id": "pubg",
        "title": "PlayerUnknown's Battlegrounds",
        "genres": ["Battle Royale", "Shooter", "Realistic"],
        "description": "Realistic battle royale with tactical gameplay and military-style combat",
        "features": "battle-royale, realistic, tactical, military, competitive",
        "difficulty": "hard",
        "multiplayer": "multiplayer",
        "rating": 7.7,
        "tags": ["battle-royale", "realistic", "tactical", "military", "competitive"]
    },
    {
        "id": "dota2",
        "title": "Dota 2",
        "genres": ["MOBA", "Strategy", "Competitive"],
        "description": "Complex MOBA with deep strategic gameplay, diverse heroes, and professional esports scene",
        "features": "moba, complex, strategic, esports, competitive",
        "difficulty": "very-hard",
        "multiplayer": "multiplayer",
        "rating": 8.5,
        "tags": ["moba", "complex", "strategic", "esports", "competitive"]
    },
    {
        "id": "spiritfarer",
        "title": "Spiritfarer",
        "genres": ["Adventure", "Management", "Emotional"],
        "description": "Cozy management game about caring for spirits on their journey to the afterlife",
        "features": "cozy, emotional, management, hand-drawn, peaceful",
        "difficulty": "easy",
        "multiplayer": "both",
        "rating": 8.4,
        "tags": ["cozy", "emotional", "peaceful", "hand-drawn", "management"]
    },
    {
        "id": "chess_com",
        "title": "Chess.com",
        "genres": ["Strategy", "Board", "Competitive"],
        "description": "Classic chess with online multiplayer, tutorials, and competitive rating system",
        "features": "chess, strategic, competitive, educational, timeless",
        "difficulty": "hard",
        "multiplayer": "multiplayer",
        "rating": 8.8,
        "tags": ["chess", "strategic", "competitive", "educational", "classic"]
    },
    {
        "id": "no_mans_sky",
        "title": "No Man's Sky",
        "genres": ["Exploration", "Survival", "Sci-fi"],
        "description": "Infinite space exploration with planet discovery, base building, and multiplayer adventures",
        "features": "exploration, infinite, space, base-building, multiplayer",
        "difficulty": "moderate",
        "multiplayer": "both",
        "rating": 8.2,
        "tags": ["space", "exploration", "infinite", "sci-fi", "discovery"]
    },
    {
        "id": "satisfactory",
        "title": "Satisfactory",
        "genres": ["Building", "Automation", "First-person"],
        "description": "First-person factory building game with automation, exploration, and resource optimization",
        "features": "automation, building, first-person, optimization, exploration",
        "difficulty": "moderate",
        "multiplayer": "both",
        "rating": 8.9,
        "tags": ["automation", "building", "optimization", "first-person", "factory"]
    },
    {
        "id": "the_forest",
        "title": "The Forest",
        "genres": ["Survival", "Horror", "Building"],
        "description": "Survival horror with base building, crafting, and cannibal enemies in dense forest",
        "features": "survival, horror, building, crafting, atmospheric",
        "difficulty": "hard",
        "multiplayer": "both",
        "rating": 8.3,
        "tags": ["survival", "horror", "building", "atmospheric", "scary"]
    },
    {
        "id": "roblox",
        "title": "Roblox",
        "genres": ["Platform", "Social", "Creative"],
        "description": "Social platform with user-generated games, creation tools, and virtual worlds",
        "features": "user-generated, social, creative, platform, family-friendly",
        "difficulty": "easy",
        "multiplayer": "multiplayer",
        "rating": 7.2,
        "tags": ["social", "creative", "user-generated", "platform", "family-friendly"]
    },
    {
        "id": "rust",
        "title": "Rust",
        "genres": ["Survival", "PvP", "Multiplayer"],
        "description": "Hardcore survival game with base building, PvP combat, and resource competition",
        "features": "hardcore, pvp, survival, base-building, competitive",
        "difficulty": "very-hard",
        "multiplayer": "multiplayer",
        "rating": 8.0,
        "tags": ["hardcore", "pvp", "survival", "competitive", "brutal"]
    }
    # ... add 48 more games covering different genres
]

    # ... add 48 more games covering different genres

class GameDataProcessor:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def create_game_embeddings(self, games):
        """Create embeddings for all games"""
        embeddings_data = []
        
        for game in games:
            # Create rich description for embedding
            text = f"{game['title']} {' '.join(game['genres'])} {game['description']} {game['features']} {' '.join(game['tags'])}"
            
            embedding = self.model.encode(text)
            
            embeddings_data.append({
                'id': game['id'],
                'text': text,
                'embedding': embedding.tolist(),
                'metadata': game
            })
        
        return embeddings_data
    
    def save_processed_data(self):
        """Save processed game data"""
        embeddings = self.create_game_embeddings(SAMPLE_GAMES)
        
        with open('processed_games.json', 'w') as f:
            json.dump(embeddings, f)
        
        return embeddings