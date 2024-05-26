from openai import AsyncOpenAI
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY') 
openai_organization_key = os.getenv('OPENAI_ORGANIZATION_ID')
init_chat_prompt = "What's your favorite way to spend a weekend?\nWhat kind of music do you enjoy the most, and why?\nDo you prefer staying in or going out on a typical night?\nWhat's the best vacation you've ever been on?\nWhat are your top three favorite movies?\nDo you enjoy cooking, and if so, what's your signature dish?\nWhat are some of your hobbies or interests outside of work?\nAre you more of an introvert or an extrovert?\nWhat's one book that has significantly influenced your life?\nDo you have any pets? If so, tell me about them.\nWhat is your dream job or career goal?\nHow do you usually handle stress or difficult situations?\nWhat's your family like? Are you close to them?\nWhat qualities do you value most in a friend or partner?\nWhat's your favorite childhood memory?\nHow do you like to celebrate your birthday?\nDo you enjoy any sports or physical activities?\nWhat are some things on your bucket list?\nHow do you define success and what does it look like for you?\nWhat's the most spontaneous thing you've ever done?"

class LlmPsycho: 
    def __init__(self):
        self.client = AsyncOpenAI(
            organization=openai_api_key,
            api_key=openai_organization_key,
        )
        self.model = "gpt-3.5-turbo"
        self.context = [
            {"role": "system", "content": init_chat_prompt + "GIVE ONLY THE INFORMATION."}, 
            {"role": "user", "content": "How you doing little cutey?"}
        ]
    
    def LLM_complete(self, user_message:str): 
        last_user = "user2"

        chat_response = self.client.chat_completions.create(
                    model=self.model,
                    messages=self.context
                )
        message = chat_response.choices[0].message.content
        self.context.append(message)

        return message
    

    def gen_prompt_from_llm_user_conversation(conversation):
        #TODO phrases too short need to feed the conversation, not cut it 
        prompt = "You're roleplaying a dating person. In the following you'll find details about the person. Match as best as you can the following writing style of the person's messages. GIVE RELATIVELY SHORT ANSWERS." #basic prompt

        user_messages = ""
        for message in conversation:
            if message["role"] == "user":
                user_messages += "\n" + message["content"]

        context = conversation
        context += [{"role": "system", "content": "You're a psychologist. From a past interaction with the user, summarise the important informations about him. GIVE ONLY THE INFORMATION." }]
        chat_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=context,
                )
        
    
        prompt += "\nDetails :\n" + chat_response.choices[0].message.content
        prompt += "\nPerson's messages :" + user_messages

        #return the general charastics of the user + extracts from the conversation
        return prompt


    async def gen_promp_from_llm_uuser_conversation(self, conversation: str):
        context1 = [
        {"role": "system", "content": "You are a geek that loves redbull but likes to go outside for a chill drink from time to time. Looking for nothing too serious as you're not confortable with sentiments" + " GIVE ONLY SHORT ANSWERS."},
        {"role": "user", "content": "How you doing little cutey?"}]
        context2 = [
        #{"role": "system", "content": "You are really angry, and sad. And you talk like a Pirate with \"Hoy\", and \"Hey\" and \"matey\" all the time in your sentence. GIVE ONLY SHORT ANSWERS."},
        {"role": "system", "content": "You are a really lovely and happy person that loves to know more about the people's lives. Your task is to ask whatever question you find is the most adapted to know someone in a few steps. You can get inspired by the ones provided below. GIVE ONLY SHORT ANSWERS.\nQuestions :\n"},
        {"role": "assistant", "content": "How you doing little cutey?"}]
        last_user = "user2"
        #model = "text-davinci-002"  # Replace with your desired model

        for _ in range(10):
            if last_user == "user2":
                chat_response = client.chat.completions.create(
                    model=model,
                    messages=context1,
                    #safe_mode=False
                )
                new_content = chat_response.choices[0].message.content
                context1.append({"role": "assistant", "content": new_content})
                context2.append({"role": "user", "content": new_content})
                last_user = "user1"
            else:
                chat_response = client.chat.completions.create(
                    model=model,
                    messages=context2,
                    #safe_mode=False
                )
                new_content = chat_response.choices[0].message.content
                context1.append({"role": "user", "content": new_content})
                context2.append({"role": "assistant", "content": new_content})
                last_user = "user2"

        return context2



        # prompt = "You're roleplaying a dating person. In the following you'll find details about the person. Match as best as you can the following writing style of the person's messages. GIVE RELATIVELY SHORT ANSWERS." #basic prompt
        # user_messages = ""
        # for message in conversation: 
        #     if message["role"] == "user": 
        #         user_messages += "\n" + message["content"]
            
        # context = conversation
        # context += [{"role": "system", "content": "You're a psychologist. From a past interaction with the user, summarise the important informations about him. GIVE ONLY THE INFORMATION." }]
        # chat_response = await self.client.chat.completions.create(
        #     model=self.model,
        #     messages=context,
        # )
            
            

        # prompt += "\nDetails :\n" + chat_response.choices[0].message.content
        # prompt += "\nPerson's messages :" + user_messages

        # #return the general charastics of the user + extracts from the conversation
        # return prompt



