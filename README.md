# Comic Generator with Nano Banana Pro 🍌

<p align="center">
  <img src="https://github.com/Yutarop/comic-generator/blob/main/demo/demo.gif" />
</p>  


This repo shows how far **Nano Banana Pro** can go in making manga-style comics from scratch. 
Just give it a one-sentence theme or idea, and optionally add detailed instructions or a character reference image, to bring your idea to life as a manga.  
With this, you can:
- Generate a complete 1–7 page manga automatically
- Let the LLM create a full plot
- Use a character reference image to keep designs consistent

> This is one-shot attempt, no editing.
> There is a typo and a repeated line, but pretty good!

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


# Model Call Breakdown
This project uses Google’s Gemini API, and **each comic generation requires multiple model calls**.  
Since API usage incurs costs, here is a clear breakdown of how many times each model is called.

### **1. Plot Generation (1 call total)**
- The **`gemini-3-pro-preview`** model is called **once** to generate the entire manga plot.  
- This cost is fixed, regardless of the number of pages.

### **2. Page Image Generation (1 call per page)**
- For each comic page, the **`gemini-3-pro-image-preview`** model is called **once**.
- Example:  
  - **4 pages → 4 image model calls**  
  - **6 pages → 6 image model calls**

### **3. Character Consistency Across Pages**
- To maintain consistent characters, **from page 2 onward, the previous page’s image is included in the prompt**.  
- This does *not* increase the number of API calls, but it does increase prompt size (and therefore may slightly increase cost depending on token usage).

#### **Example Usage**
For a **4-page comic**:

| Action | Model | Calls |
|--------|--------|--------|
| Generate plot | `gemini-3-pro-preview` | **1** |
| Generate page images | `gemini-3-pro-image-preview` | **4** |
| **Total API calls** | — | **5 calls** |

# Troubleshooting
### Known Issues
"Response has no valid parts attribute" Error  
This is a known intermittent issue where the API occasionally fails to return valid image data. The exact same request may succeed on one attempt and fail on the next. Possible causes include content safety filters, temporary server capacity limits, or timeout/network issues. In most cases, simply retrying the generation will succeed.

# License
MIT
