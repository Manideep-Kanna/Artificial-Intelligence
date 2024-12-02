import gradio as gr
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage,AIMessage
import random
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

model = ChatOpenAI(model="gpt-4o-mini")

def generate_response(message,history):
    
    langchain_history_format = []
    for msg in history:
        if msg["role"] == "user":
            langchain_history_format.append(HumanMessage(msg["content"]))
        else:
            langchain_history_format.append(AIMessage(msg["content"]))
    langchain_history_format.append(HumanMessage(message))
    
    gpt_response = model.invoke(langchain_history_format)
    return gpt_response.content
        

gr.close_all()
gr.ChatInterface(
    fn=generate_response ,
    type="messages",
    title="Simple ChatBot with LLM",
    description="Ask any question to the powerfull LLM"
).launch()