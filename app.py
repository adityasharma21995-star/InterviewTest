from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from backend import ask_ai

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <body>
            <h2>Procurement AI Assistant</h2>
            <form action="/ask" method="post">
                <input type="text" name="question" placeholder="Ask your question..." required>
                <button type="submit">Ask</button>
            </form>
        </body>
    </html>
    """

@app.post("/ask", response_class=HTMLResponse)
def ask(question: str = Form(...)):
    response = ask_ai(question)

    return f"""
    <html>
        <body>
            <h3>Response:</h3>
            <pre>{response}</pre>
            <br>
            <a href="/">Ask another question</a>
        </body>
    </html>
    """