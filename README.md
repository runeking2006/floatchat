# FloatChat 🌊 – AI-Powered ARGO Data Explorer

FloatChat is an **AI-powered conversational interface** for exploring ARGO float oceanographic data. It allows users to query, explore, and visualize oceanographic information using natural language.

---

## 📝 Features

- **Chatbot-style interface** with **ChatGPT-style bubbles**  
- **Floating input** at the bottom for easy conversation  
- **Interactive visualizations**:  
  - Float locations on a map  
  - Pressure and other parameter time-series  
- **Backend**:  
  - PostgreSQL for structured ARGO data  
  - ChromaDB for vector search and metadata retrieval  
  - Retrieval-Augmented Generation (RAG) for natural language query handling  

---

## 💻 Tech Stack

- **Python 3.x**  
- **Streamlit** – Frontend dashboard and chat interface  
- **Plotly & Leaflet** – Interactive plots and maps  
- **PostgreSQL** – Structured ARGO dataset  
- **ChromaDB** – Vector database for semantic search  
- **Flan-T5 / Local LLM** – Query interpretation  

---

## 🚀 Demo Queries

Try the following queries in the chat interface:

1. Show me the temperature and pressure profiles of ARGO floats near the equator.  
2. Compare salinity levels in the Arabian Sea and Bay of Bengal over the last 6 months.  
3. What are the nearest ARGO floats to latitude 10°N and longitude 75°E?  
4. Show me pressure vs depth for floats in the Indian Ocean.  
5. Plot the pressure trends of ARGO floats in March 2023.  

---

## 🗂 Project Structure

floatchat/
├─ front_end/ # Streamlit app and CSS
├─ utils/ # Visualization utilities
├─ backend.py # LLM query handling and RAG
├─ db_config.py # PostgreSQL & ChromaDB connections
├─ requirements.txt # Python dependencies
├─ .env # Environment variables

yaml
Copy code

---

## ⚡ How to Run

1. Activate your virtual environment:
& D:/my_project/venv/Scripts/Activate.ps1
Run the Streamlit app:

bash
Copy code
cd D:\floatchat
streamlit run front_end/app.py
Open in your browser: http://localhost:8501/

📌 Notes
Demo uses a subset of 500 ARGO floats for speed.

Designed for internal hackathon PoC.

Fully functional chat + inline visualizations for Indian Ocean ARGO dataset.

🔗 Future Work
Full ARGO dataset integration

Additional BGC and satellite data

Enhanced RAG pipeline for advanced queries

Improved UI/UX and multi-modal visualizations

📄 License
This README is **hackathon-ready**, shows all the features, instructions, and tech stack, and looks professional for HR viewing.  
