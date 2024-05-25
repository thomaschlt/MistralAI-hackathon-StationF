from fastapi import FastAPI, HTTPException, Request

import requests
import os
import datetime
import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

app = FastAPI() 

personality_prompt_filename = None

@app.get("/llm_completion/")
async def llm_completion(context: str,is_conv_finished: bool):
    if is_conv_finished : # save all the conversation between the LLM and the user in a file
        filename = save_conversation(context)
        personnality_prompt = prompt_generator(filename)
        global personality_prompt_filename
        personality_prompt_filename = save_prompt_perso(personnality_prompt) # how to save the name fro use in the L


    else : # generate a response to the speech of the user 
        try:
            result = call_mistral_llm_completion(context)
            return result
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=str(e))



@app.get("/llm_clone/")
async def llm_clone_conversation_generator(request: Request):
    # personality_prompt  = read_personnality_prompt(personality_prompt_filename)
    data = await request.json()
    
    context = data['context']

    for _ in range(10):
        #ping pong
        print("ping")
        print("pong")
        
    try:
        result = call_mistral_llm_clone_generate_conversation(context)
        return result
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))



################# UTILS ####################


def call_mistral_llm_completion(prompt: str):
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-large-latest"
    client = MistralClient(api_key=api_key)

    chat_response = client.chat(
        model=model,
        messages=[ChatMessage(role="user", content=prompt)]
    )
    return chat_response


def call_mistral_llm_clone_generate_conversation(prompt: str):
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-large-latest"
    client = MistralClient(api_key=api_key)

    chat_response = client.chat(
        model=model,
        messages=[ChatMessage(role="user", content=prompt)]
    )
    conversation = chat_response.messages
    return conversation


def prompt_generator(filepath : str): 
    # read the conversation file created in save_conversation and create a prompt based on LLM
    if not os.path.exists(filepath):
        raise FileNotFoundError(f'Conversation file {filepath} not found.')
    
    with open(filepath, "r") as f: 
        conversation = f.read()

    prompt = (f"I want you to act like the user and imitate the way they are speaking.", 
              f"You can find a lot of information about the person here: {conversation}")
    return prompt

################# Save conversation ####################

def save_conversation(conversation: str):
    """
    TODO: maybe go w/ a JSON later
    """ 
    current_time = datetime.datetime.now()
    filename = current_time.strftime("%Y%m%d-%H%M%S") + ".txt"
    with open(filename, 'w') as file:
        file.write(conversation)
    return filename

def save_prompt_perso(prompt: str):
    """
        Save the generated prompt (prompt_generator) and save it into a text file too. 
    """
    current_time = datetime.datetime.now()
    filename = current_time.strftime("%Y%m%d-%H%M%S_prompt.txt")

    with open(filename, 'w') as f: 
        f.write(prompt)
    return filename

def read_personnality_prompt(filename: str):
    with open(filename, 'r') as f:
        return f.read()