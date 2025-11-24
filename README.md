# Comic Generator 
This repo is to try how far **Nano Banana Pro** can go in generating manga-style comics from scratch. 🍌 
By simply providing a **theme**, the models create a complete multi-page manga automatically. You can also give a reference image and detailed instructions. 

# Setup
1. Make sure you have **uv** installed.
```bash
uv sync
```

2. Activate the virtual environment
```bash
# Windows
source .venv/Scripts/activate
# macOS / Linux:
source .venv/bin/activate
```

3. Run the Streamlit app
```bash
streamlit run app.py --server.address localhost
```
The app will be available at: http://localhost:8501


