from fastapi import FastAPI, HTTPException
import requests
import os
import datetime


app = FastAPI() 

personality_prompt_filename = None

@app.post("/llm_completion/")
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

@app.post("/llm_clone/")
async def llm_clone_conversation_generator(prompt: str):
    personality_prompt  = read_personnality_prompt()
    
    for _ in range(10):
        #ping pong
        
    try:
        result = call_mistral_llm_clone(personality_prompt)
        return result
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    


def call_mistral_llm_clone(prompt: str):
    response = requests.post(f"{MISTRAL_API_URL}/llm_clone", json={"prompt": prompt})
    response.raise_for_status()
    return response.json()


def call_mistral_llm_completion(prompt: str):
    response = requests.post(f"{MISTRAL_API_URL}/llm_completion", json={"prompt": prompt})
    response.raise_for_status()
    return response.json()

def save_conversation(conversation: str):
    """
    TODO: maybe go w/ a JSON later
    """ 
    current_time = datetime.datetime.now()
    filename = current_time.strftime("%Y%m%d-%H%M%S") + ".txt"

    with open(filename, 'w') as file:
        file.write(conversation)

    return filename
    
def prompt_generator(filepath : str): 
    # read the conversation file created in save_conversation and create a prompt based on LLM
    if not os.path.exists(filepath):
        raise FileNotFoundError(f'Conversation file {filepath} not found.')
    
    with open(filepath, "r") as f: 
        conversation = f.read()

    prompt = (f"I want you to act like the user and imitate the way they are speaking.", 
              f"You can find a lot of information about the person here: {conversation}")
    return prompt

def save_prompt_perso(prompt: str):
    """
        Save the generated prompt (prompt_generator) and save it into a text file too. 
    """
    current_time = datetime.datetime.now()
    filename = current_time.strftime("%Y%m%d-%H%M%S_prompt.txt")

    with open(filename, 'w') as f: 
        f.write(prompt)
    return filename

