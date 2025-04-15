# Setup

* Python version doesn't really matter, we use 3.11
* Please use [FastAPI](https://fastapi.tiangolo.com/) (sort of setup in main.py) and the [OpenAI library](https://github.com/openai/openai-python)

# Installion

## Installation

1. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

2. Add your OpenAI API key to a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. Run the FastAPI app with Uvicorn:
   ```bash
   uvicorn main:app --reload
   ``` 