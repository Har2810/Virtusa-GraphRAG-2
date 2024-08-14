
import subprocess
import json
from fastapi import FastAPI
from pydantic import BaseModel
import gradio as gr

app = FastAPI()

class Query(BaseModel):
    question: str

def clean_graphrag_output(output):
    lines = output.split('\n')
    # Find the index where the actual answer starts (after "SUCCESS: Global Search Response:")
    start_index = next((i for i, line in enumerate(lines) if line.startswith("SUCCESS: Global Search Response:")), -1)
    if start_index != -1:
        # Join the lines from after the "SUCCESS" line to the end
        cleaned_output = '\n'.join(lines[start_index + 1:]).strip()
        return cleaned_output
    else:
        # If "SUCCESS" line is not found, return the original output
        return output.strip()

def run_graphrag_query(question):
    command = ["python3", "-m", "graphrag.query", "--root", ".", "--method", "global", question]
    try:
        logger.info(f"Running command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True, timeout=300)
        logger.info(f"Command output: {result.stdout}")
        logger.info(f"Command error output: {result.stderr}")
        if result.returncode != 0:
            return f"Error: GraphRAG query failed with return code {result.returncode}\nError output: {result.stderr}"
        cleaned_output = clean_graphrag_output(result.stdout)
        if not cleaned_output:
            return "No relevant response found in the output."
        return cleaned_output
    except subprocess.TimeoutExpired:
        return "The query took too long to process (over 5 minutes). Please try a simpler question or try again later."
    except Exception as e:
        return f"An error occurred: {str(e)}\n{traceback.format_exc()}"

@app.post("/ask")
async def ask_question(query: Query):
    response = run_graphrag_query(query.question)
    return {"answer": response}

import traceback
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def gradio_interface(question):
    try:
        logger.info(f"Processing question: {question}")
        response = run_graphrag_query(question)
        logger.info(f"Got response: {response}")
        if not response:
            return "No response received from GraphRAG. Please check the logs for more information."
        return response
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return error_msg

iface = gr.Interface(
    fn=gradio_interface,
    inputs=gr.Textbox(lines=2, placeholder="Enter your question here..."),
    outputs="text",
    title="GraphRAG Q&A",
    description="Ask questions using GraphRAG (Global method)"
)

app = gr.mount_gradio_app(app, iface, path="/")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)