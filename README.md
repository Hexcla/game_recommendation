# 🎮 AI-Powered Game Recommendation Engine

An intelligent web app that recommends video games based on your preferences or games you’ve already liked. Built with **sentence embeddings**, **ChromaDB vector search**, and an interactive **Streamlit** UI.

---

## 🚀 Features

- 🔍 **Search by Preferences**: Enter a text description of your ideal game and get recommendations.
- 🎮 **Game-to-Game Recommendations**: Select games you’ve liked and get similar ones.
- 🤝 **Hybrid Recommendations**: Combines liked games + preferences for best match.
- 📊 **Semantic Matching**: Uses sentence-transformers + cosine similarity.
- ⚡ **Fast Retrieval**: Powered by ChromaDB vector store.
- 🎨 **Streamlit Interface**: Simple and interactive frontend.

---

## 🧠 How It Works

1. Game descriptions are converted into embeddings using `all-MiniLM-L6-v2`.
2. Embeddings + metadata are stored in ChromaDB.
3. User input is also embedded and compared for similarity.
4. The top matches are shown with confidence scores and game details.

---

## 📁 Project Structure

```

gameZop/
├── game\_data.py                 # Embedding & metadata processor
├── recommendation\_engine.py     # Core recommendation engine
├── streamlit\_app.py             # Streamlit frontend
├── processed\_games.json         # Embedded game data
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation

````

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/game-recommendation-app.git
cd game-recommendation-app
````

### 2. Create and activate a virtual environment

```bash
conda create -n gameZop python=3.9
conda activate gameZop
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run streamlit_app.py
```

---

## 📝 Example Inputs

* `"Open world RPG with magic and character progression."`
* `"Multiplayer shooting games with strategy and fun."`
* `"Games like Witcher 3 and Skyrim"`

---

## 📦 Dependencies

Make sure the following are included in your `requirements.txt`:

```
streamlit
sentence-transformers
chromadb
scikit-learn
pandas
numpy
```
---

## 🔮 Future Improvements

* 🎯 Integrate live game reviews and price APIs
* 🧬 Genre-specific fine-tuning
* 🔐 User authentication and history
* ☁️ Deployment to Streamlit Cloud or Hugging Face

---

## 🧑‍💻 Author

Built with ❤️ by **\[YOGENDRA LAKSHMAN]**

* GitHub: [https://github.com/your-username](https://github.com/Hexcla)
* LinkedIn: [https://linkedin.com/in/your-profile](https://www.linkedin.com/in/yogendra-lakshman/)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

```

---


```
