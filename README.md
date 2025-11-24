# Comic Generator with Nano Banana Pro 🍌
![banner2](https://github.com/user-attachments/assets/8e8ef84d-349f-4c64-8e36-a06c655b994d)


This repository explores how far **Nano Banana Pro** can go in generating manga-style comics from scratch. 
You can provide a one-sentence theme, detailed instructions, and a character reference image to create your own manga. 
With this, you can:
- Generate a complete 1–7 page manga automatically
- Let the AI create a full plot from just a theme
- Use a character reference image to keep designs consistent

# Example
- Check out this [example](https://github.com/Yutarop/comic-generator/blob/main/demo/lena-input.pdf) where I used a picture of [Lena](https://en.wikipedia.org/wiki/Lenna) and set the theme to romantic comedy.
- See another [example](https://github.com/Yutarop/comic-generator/blob/main/demo/interstellar-like-manga.pdf) with a story like the movie Interstellar.

# Setup
### 1. Install Dependencies
The project uses [uv](https://docs.astral.sh/uv/) for project management.
```bash
uv sync
```

### 2. Configure API Key
Create a .env file in the project root. You'll need `gemini-3-pro-image-preview` and `gemini-3-pro-preview` model.
```bash
GOOGLE_API_KEY=your_api_key_here
```
- You can generate an API key from Google AI Studio:  
https://aistudio.google.com/api-keys  
- For more details about Nano Banana Pro and the underlying image generation API, see the official documentation:  
https://ai.google.dev/gemini-api/docs/image-generation?hl=en&batch=file  

### 3. Activate the virtual environment
```bash
# Windows
source .venv/Scripts/activate
# macOS / Linux
source .venv/bin/activate
```

# Runnig the Application
### Run the Streamlit app
```bash
streamlit run app.py --server.address localhost
```
The app will be available at: http://localhost:8501

### Usage
- Select the number of pages (1–7)
- Enter a theme (e.g., High school rom-com, Sci-fi adventure)
- (Optional) Add additional story instructions
- (Optional) Upload a character design reference
- Click Generate Manga (take a while)
- Download the full comic or individual pages

# License
MIT
