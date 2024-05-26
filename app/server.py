from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect

import requests
import os
import datetime
import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from llm_client import LlmClient
import re
import json
import ast

app = FastAPI() 

personality_prompt_filename = None
llm_client = LlmClient()
filename = None



@app.get("/llm_completion/")
async def llm_completion(last_user_message: str,is_conv_finished: bool):
    if is_conv_finished : # save all the conversation between the LLM and the user in a file
        
        filename = save_conversation(llm_client.context)
        personnality_prompt = llm_client.gen_prompt_from_llm_user_conversation(filename)
        # global personality_prompt_filename
        # personality_prompt_filename = save_prompt_perso(personnality_prompt) # how to save the name fro use in the L

    else : # generate a response to the speech of the user 
        try:
            result = llm_client.LLM_complete(last_user_message)
            return result
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=str(e))



@app.post("/send_convo/")
async def llm_clone_conversation_generator(request: Request):
    body = await request.json()
    conversation = body["conversation"]
    print("convo")
    print(conversation)
    
    corrected_string = re.sub(r'(\b\w+\b):', r'"\1":', conversation)
    corrected_string = re.sub(r'{"role": ([^\}]+), "content":', r'{"role": "\1", "content":', corrected_string)
    corrected_string = re.sub(r'"content": ([^\}]+)}', r'"content": "\1"}', corrected_string)


    # Parse the corrected string as a Python literal
    list_of_dicts = ast.literal_eval(corrected_string)
    print("list of dicts")
    # # Verify the result
    print(list_of_dicts)
    print(type(list_of_dicts))

    # Verify the result
    print(list_of_dicts)
    # personality_prompt  = read_personnality_prompt(conversation)

    prompt = llm_client.gen_prompt_from_llm_user_conversation(list_of_dicts)
    print(prompt)

    conversation = llm_client.gen_LLM_to_LLM_conversation()
    # Save conversation
    global filename
    filename = save_conversation(conversation)


@app.get("/get_chats/")
async def collect_chats():
    filename = "20240526-093613.txt"
    try: 
        conversation = read_conversation(filename)
        return conversation 
    except FileNotFoundError as e: 
        raise HTTPException(status_code=400, detail=str(e))

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


# def gen_prompt_from_llm_user_conversation(filepath : str): 
#     # read the conversation file created in save_conversation and create a prompt based on LLM
#     if not os.path.exists(filepath):
#         raise FileNotFoundError(f'Conversation file {filepath} not found.')
    
#     with open(filepath, "r") as f: 
#         conversation = f.read()

#     prompt = (f"I want you to act like the user and imitate the way they are speaking.", 
#     #           f"You can find a lot of information about the person here: {conversation}")
#     return prompt


def generate_LLM_to_LLM_conversation(prompt: str):
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-large-latest"
    client = MistralClient(api_key=api_key)

    chat_response = client.chat(
        model=model,
        messages=[ChatMessage(role="user", content=prompt)]
    )
    conversation = chat_response.messages
    return conversation


################# Save conversation ####################

def save_conversation(conversation :list):
    """
    TODO: maybe go w/ a JSON later
    """ 
    current_time = datetime.datetime.now()
    filename = current_time.strftime("%Y%m%d-%H%M%S") + ".txt"
    with open(filename, 'w') as file:
        file.write(str(conversation))
    return filename

def read_conversation(filename: str): 
    with open(filename, 'r') as file: 
        conversation = file.read()
    return conversation

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

################# Put LLM psycho in server #################

@app.websocket("/llm-websocket/{call_id}")
async def websocket_handler(websocket: WebSocket, call_id: str): 
    await websocket.accept()
    llm_psycho = LlmClient()
    try: 
         while True: 
             data = await websocket.receive_text()
             context = data["context"]
             initial_discussion = data["initial_discussion"]
             characteristics = data["characteristics"]
             prompt = data["prompt"]

             response = await llm_psycho.init_prompt(
                 conversation= context, 
                 initial_discussion=initial_discussion, 
                 characteristics=characteristics, 
                 prompt=prompt
             )

             await websocket.send_text(response)
    except WebSocketDisconnect: 
        print(f"Client {call_id} disconnected")
    except Exception as e: 
        await websocket.close()
        print(f"Error: {e}")




# @app.get("/llm_clone/")
# async def llm_clone_conversation_generator(request: Request):
#     body = await request.json()
#     conversation = body["conversation"]
#     print(conversation)
    
#     # personality_prompt  = read_personnality_prompt(conversation)

#     prompt = llm_client.gen_prompt_from_llm_user_conversation(conversation)
#     print(prompt)

#     conversation = llm_client.gen_LLM_to_LLM_conversation()
#     print(conversation)
#     # try:
#     #     result = generate_LLM_to_LLM_conversation(context)
#     #     return result
#     # except requests.RequestException as e:
#     #     raise HTTPException(status_code=500, detail=str(e))