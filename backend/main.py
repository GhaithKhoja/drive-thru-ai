from fastapi import FastAPI, Request
from ai import AI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add this block to allow CORS from http://localhost:5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

ai_instance = AI()

@app.post("/generate")
async def generate(request: Request):
    
    # Get the prompt from the request
    data = await request.json()
    prompt = data.get("prompt")
    
    # Generate the response
    response = ai_instance.generate_response(prompt)
    
    # Return the response
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
