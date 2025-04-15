from fastapi import FastAPI, Request
from ai import AI

app = FastAPI()
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
