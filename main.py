from fastapi import FastAPI
import uvicorn

# Application Configuration
PORT = 8000
HOST = "0.0.0.0"

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello DevOps! 🚀"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
