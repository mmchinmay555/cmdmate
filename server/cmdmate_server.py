from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from server.core import CmdMate

# -----------------------------
# FastAPI Setup
# -----------------------------
app = FastAPI()
cmdMate_ai = CmdMate()  # Make sure OPENAI_API env variable is set

# -----------------------------
# Request Models
# -----------------------------
class InputText(BaseModel):
    text: str  # The user's query
    os: str    # The operating system (linux/mac/windows)

class ExplainInput(BaseModel):
    text: str  # The user's query for explanation

class RespondBasedOnInput(BaseModel):
    input: str  # Additional input data
    query: str  # The user's input for general response

# -----------------------------
# Routes
# -----------------------------
@app.get("/")
def root():
    return {"message": "Server is running! Use POST /getCmd to get commands."}

@app.post("/echo")
def echo(data: InputText):
    return {"response": f"#{data.text}"}

@app.post("/getCmd")
def getCmd(data: InputText):
    try:
        # Pass both query and OS from client
        command = cmdMate_ai.query_command(data.text, data.os)
        return {"command": command}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/getExplaination")
def getExplaination(data: ExplainInput):
    try:
        explanation = cmdMate_ai.query_explain(data.text)
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/getCommitMsg")
def getCommitMsg(data: ExplainInput):
    try:
        # Future feature placeholder
        commit_message = cmdMate_ai.query_getCommit(data.text)
        return {"commit_message": commit_message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/getResponseFromInput")
def getResponseFromInput(data: RespondBasedOnInput):
    try:
        response = cmdMate_ai.query_response_from_input(data.input, data.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))