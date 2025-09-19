```bash
# 1. Create a Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the FastAPI application
uvicorn main:app --reload

# 4. Test the API with Swagger UI
# Open http://127.0.0.1:8000/docs in your browser

# 5. Run Ollama locally
ollama serve

# 6. Test a prompt with llama2 via FastAPI
# Send a POST request to your FastAPI endpoint (replace /prompt with your actual endpoint)
curl -X POST "http://127.0.0.1:8000/prompt" -H "Content-Type: application/json" -d '{"model": "llama2", "prompt": "What is FastAPI?"}'
```
