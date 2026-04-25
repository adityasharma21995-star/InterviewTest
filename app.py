from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from backend import ask_ai

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Procurement AI Assistant</title>
        </head>

        <body style="font-family: Arial; background:#f5f7fa; padding:40px;">
            <div style="background:white; padding:30px; border-radius:10px; max-width:600px; margin:auto;">
                
                <h1>Procurement AI Assistant</h1>
                <p>AI-powered decision support for vendor selection, cost optimization, and risk analysis.</p>

                <form action="/ask" method="post">
                    <input type="text" name="question" placeholder="Ask your question..." 
                           style="width:100%; padding:10px; margin-top:10px;" required>
                    
                    <button type="submit" 
                            style="margin-top:10px; padding:10px; width:100%;">
                        Ask
                    </button>
                </form>

            </div>
        </body>
    </html>
    """


@app.post("/ask", response_class=HTMLResponse)
def ask(question: str = Form(...)):
    response = ask_ai(question)

    return f"""
    <html>
        <head>
            <title>Response</title>
        </head>

        <body style="font-family: Arial; background:#f5f7fa; padding:40px;">
            <div style="background:white; padding:30px; border-radius:10px; max-width:600px; margin:auto;">

                <h2>You asked:</h2>
                <p>{question}</p>

                <h2>AI Response:</h2>
                <pre style="white-space: pre-wrap;">{response}</pre>

                <br><br>
                <a href="/" style="text-decoration:none;">
                    <button style="padding:10px; width:100%;">Ask another question</button>
                </a>

            </div>
        </body>
    </html>
    """
