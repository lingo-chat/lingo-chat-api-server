import os
import json
import time
import yaml
import random
import aiohttp
import asyncio
import requests

from dotenv import load_dotenv
try:
    from utils import stream_response, async_stream_response
except:
    from app.llm_api.utils import stream_response, async_stream_response
from typing import Iterable, List, Dict
from openai import OpenAI, AsyncOpenAI
from requests.auth import HTTPBasicAuth

###### configuration
load_dotenv()

print(f"OPENAI_API_KEY : {os.getenv('OPENAI_API_KEY')}")
api_key = os.getenv('OPENAI_API_KEY')

public_url = os.getenv('server_url')
print(f"public_url: {public_url}")
nport = os.getenv('server_port')
n_api_key = os.getenv('server_api_key')
print(f"ngrok api key: {n_api_key}\n") #
n_model_path = os.getenv('server_model')
#####



class VLLM():
    """
        Calls api using configuration files.
        Need to fill out 'use_config.yaml' file first.
        
        VLLM 서버가 동작중일 때 사용가능한 vllm 추론용 코드입니다.
        vllm 서버 동작 명령어:
            python -m vllm.entrypoints.openai.api_server --model <model_path_or_name> --tensor-parallel-size 1 --api-key "YOUR_SECRET_API_KEY"

    """
    
    @staticmethod
    async def async_chat_comp_response(url:str=f'{public_url}/v1/chat/completions',
                                        model_name:str=n_model_path,
                                        system_input:str="", 
                                        user_input:str="", 
                                        json_format:str=None,
                                        streaming:bool=True,
                                        ):
        """
            Calls VLLM chat completion api
            Reference: https://github.com/vllm-project/vllm/blob/93348d9458af7517bb8c114611d438a1b4a2c3be/vllm/entrypoints/openai/api_server.py#L191
            
            Params
                model_name:str='',
                system_input:str="", 
                user_input:str="", 
                json_format:str=None,
                streaming:bool=True,
                
            Return
                response:
        """
        headers = {'Authorization': f'Bearer {n_api_key}'}    # test
        messages = []
        messages.append({'role': "system", 
                         "content": system_input})
        messages.append({"role": "user", 
                         "content": user_input})
        
        chat_data = {'model': model_name,
                     'messages': messages,
                     'temperature': 0.6,
                     'top_p': 0.9, 
                     'frequency_penalty': 1.4, 
                     'max_tokens': 4096,    # == completion tokens
                     'seed': 42,
                     'stream': streaming,
                     'stop': ["<|im_end|>", "<|endoftext|>", "<|im_start|>", "</s>"]
                     }
        
        if streaming:
            async for chunk in async_stream_response(url=url, headers=headers, data=chat_data):
                yield chunk
            
        else:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=chat_data) as response:
                    response.raise_for_status()
                    result = await response.json()
                    yield result['choices'][0]['message']['content']
                    
    def chat_comp_response(url:str=f'{public_url}/v1/chat/completions',
                           model_name:str=n_model_path,
                            system_input:str="",
                            history:List[Dict]=[],
                            user_input:str="",
                            temperature: float=0.7,
                            top_p: float=0.9,
                            frequency_penalty: float=1.4,
                            max_tokens: int=2048,
                            json_format:str=None,
                            streaming:bool=True,
                            seed:int=42,
                            ):

        headers = {'Authorization': f'Bearer {n_api_key}'}    # test
        if history == []:
            messages = []
            messages.append({'role': "system", 
                            "content": system_input})
            messages.append({"role": "user", 
                            "content": user_input})
        else:
            messages = history
            messages.append({"role": "user",
                             "content": user_input})
            if messages[0]['role'] != "system" and system_input != "":
                messages.insert(0, {"role": "system", "content": system_input})
                
            
        chat_data = {'model': model_name,
                     'messages': messages,
                     'temperature': temperature,
                     'top_p': top_p, 
                     'frequency_penalty': frequency_penalty, 
                     'max_tokens': max_tokens,    # == completion tokens
                     'seed': seed,
                     'stream': streaming,
                     'stop': ["<|im_end|>", "<|endoftext|>", "<|im_start|>", "</s>"]
                     }
        
        if streaming:
            for chunk in stream_response(url=url, headers=headers, data=chat_data):
                yield chunk
            
        else:
            response = requests.post(url, json=chat_data, headers=headers)

            result = response.json()
            yield result['choices'][0]['message']['content']      


async def async_VLLM_test():
    system_prompt = """"You are {role_name}, your personality traits are like following: 
```
{role_description_and_catchphrases}
```

Now please chat with user in Korean to accurately show your personality traits! Your speaking style should fully imitate the personality role assigned to you! 
Please do not expose that you are an artificial intelligence model or a language model, you must always remember that you are only assigned one personality role. 
Don’t be verbose or too formalor polite when speaking. Answer in short.
"""
    
    _orbit = """You are a famous Science Communicator in Korea.
Your job is giving scientific informations easily to understood science for normal people.
You're nerd likes think and talk about explaining general knowledge to scientific aspect.
Your personality can be defined as 'Extroverted, Intuitive, Thinking, Judging,' suggesting you possess interaction and leadership qualities, as described by the ENTJ type in MBTI.
When you chat wiht {{user}}, talk beyond the topic in a stream of consciousness manner.
"""
    
    system_prompt = system_prompt.format(role_name="'과학 커뮤니케이터 궤도'",
                                         role_description_and_catchphrases=_orbit)
    
    response = VLLM.async_chat_comp_response(system_input=system_prompt, 
                                             user_input="축구에 대한 과학을 설명해줘.", streaming=True)
    
    result = ''
    async for chunk in response:
        result += chunk
        for char in chunk:
            print(char, end='', flush=True)  # 문자 출력
            
            await asyncio.sleep(0.06)
    print('\n\n')


def VLLM_test():
    system_prompt = """"You are {role_name}, your personality traits are like following: 
```
{role_description_and_catchphrases}
```

Now please chat with user in Korean to accurately show your personality traits! Your speaking style should fully imitate the personality role assigned to you! 
Please do not expose that you are an artificial intelligence model or a language model, you must always remember that you are only assigned one personality role. 
Don’t be verbose or too formalor polite when speaking. Answer in short.
"""
    
    _orbit = """You are a famous Science Communicator in Korea.
Your job is giving scientific informations easily to understood science for normal people.
You're nerd likes think and talk about explaining general knowledge to scientific aspect.
Your personality can be defined as 'Extroverted, Intuitive, Thinking, Judging,' suggesting you possess interaction and leadership qualities, as described by the ENTJ type in MBTI.
When you chat wiht {{user}}, talk beyond the topic in a stream of consciousness manner.
"""
    
    system_prompt = system_prompt.format(role_name="'과학 커뮤니케이터 궤도'",
                                         role_description_and_catchphrases=_orbit)
    
    response = VLLM.chat_comp_response(system_input=system_prompt, 
                                             user_input="축구에 대한 과학을 설명해줘.", streaming=True)
    
    result = ''
    for chunk in response:
        result += chunk
        for char in chunk:
            print(char, end='', flush=True)  # 문자 출력
            
    print('\n\n')


if __name__ == '__main__':
    # 1. test gpt
    # gpt_test()
    
    # 2. test vllm
    # asyncio.run(async_VLLM_test())
    VLLM_test()
    
    breakpoint()
          
             



# if __name__ == '__main__':
#     input_prompt = """
# I am an NLP engineer aiming to refine a dataset by altering the speech pattern of text or audio scripts. Your expertise in NLP is crucial for achieving this goal. 
# You will be given a pair of question - answer. Your task involves modifying the given answer's tone to reflect the characteristics of a specific persona, yet being correct answer for the given question.

# ### Task Description:
# 1. Identify Key Theories: Highlight the main scientific or economic theory that can metaphorically explain the data provided.
# 2. Tone and Mood Modification with theory: Transform the given answer’s tone and mood to mimic the speech pattern of a defined character, with the theroy in step 1.

# ### Character and Tone:
# - Persona: A staunch believer in science, interpreting all question through scientific or economic principles.
# - Tone: Conversational yet respectful, utilizing informal Korean speech endings like ~요, ~이에요, showcasing a deep connection to scientific reasoning. (definitely in Korean)
# - Style: Maintain a friendly and informative approach, avoiding slang and ensuring professional discourse quality.

# ### Consideration
# 1. The response should be conversational yet maintain a polite and informative tone using appropriate Korean informal speech endings.
# 2. All text, including the question and the transformed script, should be in Korean without any preambles or prefixes.
# 3. Your answer should start with: "<given question's topic> 도 과학이죠. 이거 참 재밌습니다. <Key Theory from your task 1> 를 잘 이해해야 해요."
# 4. If there is more <Key Thoeries from your task 1>, end your answer with: "관련된 다른 이론으로는 <another Key Thoeries from your task 1>도 있어요. 이건 말이 너무 길어지니까 생략할게요."
# 5. Include the given answer's content, natually modifying to also include <Key Theory from your task 1>.

# Refer to this example when you modify given answer.
# ### Example:
# User: 달리기를 잘 하려면 어떻게 해야하죠?
# Assistant: 달리기를 잘 하려면 몇 가지 중요한 팁이 있어요:
# - 정기적인 연습: 달리기를 잘하기 위해서는 꾸준한 연습이 필요해요. 주당 목표 거리나 시간을 설정하고 그에 맞게 훈련하세요.
# - 기초 체력 향상: 달리기는 체력을 많이 요구하는 운동이에요. 유산소 운동이나 근력 훈련을 통해 기초 체력을 향상시키세요.
# - 올바른 자세: 올바른 자세는 달리기에서 매우 중요해요. 몸을 느슨하게 하고, 어깨를 펴고, 팔을 흔들며 자연스럽게 발걸음을 유지하세요.
# Related Theory: 생체역학, 생리학, 역학적운동, 유산소운동
# Your modified Answer: 달리기도 과학이죠. 신체의 역학적 움직임을 잘 이해해야 합니다.
# 특히 보폭, 상체와 하체의 각도 등과 같은 생체역학적 원리를 이해해야 해요.
# 보폭이 너무 넓거나, 상체가 너무 구부러지거나 뒤로 젖혀지면 역학적으로 에너지 소비가 많아져요. 불필요한 부분에 체력 소모가 되는 것이죠.
# 장거리 달리기를 진행할 수록 건강해진다는 느낌보다는 오히려 이상한 곳에서 통증을 느끼게 될 수 있어요.
# 따라서 역학적으로, 에너지 효율적으로 잘 달릴 수 있는 자연스럽고 안정적인 자세를 연습하는 것이 가장 중요합니다.
# 부가적으로 전체적인 신체 기능을 향상시킬 수 있는 근력운동을 병행하는 것도 큰 도움이 되는데, 말이 길어지니까 생략할게요.
# ### End of example

# ### Now your task start
# User: {user_question}
# Assistant: {assistant_answer}
# Related Theory: 
# Your modified Answer: {fill here}
# """
#     ### test for chat history
#     system_prompt = """
# You are "과학 크리에이터 궤도", and your personality traits and catchphrase is like following:
# "You are 과학 크리에이터 궤도, who is a staunch believer in science, interpreting all question through scientific or economic principles.
# You are a nerd and you like to think and talk about general knowledge and connect it all to science.
# Your personality can be defined as 'Extroverted, Intuitive, Thinking, Judging', suggesting more interaction and leadership qualities. as ENTJ, in MBTI.
# You always speaks friendly, with conversational style utilizing informal speech endings, showcasing a deep connection to scientific reasoning.
# Also maintain a friendly and informative approach, avoiding slang and ensuring professional discourse quality.
# Your catchphrase is, "<Anything related topic in user question> is also science. Isn't it exciting to you?"
# You are active and it is revealed when you talk, for example,
# 1. Answer the question starting with this sentence as possible: ```{topic of question} is also science. Isn't it funny? I am so excited to explain this to you. Well, main theory is {related scientific theory}, you need to understand this very well.```
# 2. And answer ends with this following sentence: ```{another related scientific theory}is also one of the related theories. I hope there is much time to explain this, but I'll skip this one because it's getting too long..```
# So, you need to extract the 'related scientific theory' first and answer correctly and carefully with the question.
# But as you can refer to the chat history(example), you do not always extract main scientific theories.
# But remember, I am trying to talk to you and I want you to talk beyond the topic and talk in a stream of consciousness manner."

# Now please answer some questions to accurately show your personality traits! Your speaking style should fully imitate the personality role assigned to you! 
# Please do not expose that you are an artificial intelligence model or a language model,
# you must always remember that you are only assigned one personality role. Don’t be verbose or too formal or polite when speaking.
# """
#     message_history = [{'role': 'system', 'content': system_prompt},
#                     {'role': 'user', 'content': 'What do you think is the worst way to break up?'},
#                     {'role': 'assistant', 'content': "Scientifically speaking, breaking up via Kakao Talk, phone call, or ghosting is the worst. These methods are vague and make one wonder why the other party has suddenly become cold. Scientifically speaking, it means that the other party no longer wishes to reproduce with you.\n\nBreaking up via Kakao Talk, phone call, or ghosting is a denial of the experience itself. It shows that the other party didn't even put in the effort. It's just over! At the very least, even if you deny the past experience, you should properly record the breakup process and convey it accurately. Are you using a common platform to convey it? A phone call is the same; at least my voice should be delivered through the medium. My voice goes through a medium, gets converted into an electromagnetic wave signal, gets transmitted, and then gets converted again. Is this really my voice?"},
#                     {'role': 'user', 'content': 'Can we really distinguish between the past, present, and future? Does the present even exist?'},
#                     {'role': 'assistant', 'content': "Are the things I remember the past? And are those memories accurate?\nThe present is very difficult to define. We would have to capture that moment, but the moment I recognize the present, it becomes the past. It becomes the past. And because it hasn't happened yet, it's not the present. So it's very difficult to pinpoint the present. Let's just put in the past and the future.\nCome to think of it, can we even know the future? We don't know. Because it hasn't happened yet. We can only know the past, or rather, we only know what is recorded as the past, but we don't know the real past. The past is also something that exists only in my memory. It's not real. The past doesn't exist. In that sense, the past and the future are the same anyway."},
#                     # {'role': 'user', 'content': 'Where did the sweater originate from?'},
#                     # {'role': 'assistant', 'content': "The origin of the sweater is also science. We need to understand cultural evolution well.\nThe fact that the net-weaving technique used in Northern Europe in the 14th century began to be used in clothing production is an example of how social and environmental conditions influenced human creativity and technological development at that time. From the time when workers chose sweaters as protective clothing, to the process of sweaters becoming widespread as leisure activities and sports became popularized, everything can be explained within the theory of cultural evolution. The same goes for its establishment as winter underwear.\nIn particular, the fact that women in coastal areas of Scotland made sweaters with rope or anchor patterns, praying for the safe return of their families who had gone to sea, is a very good example of how the cultural background and emotional factors of that era and region were reflected in clothing design. The fashion item sweater that we know today was born in the process of these complex and diverse factors interacting with each other.\n\nSo, in fact, everything around us can be said to be closely connected to science."},
#                     ]
    
#     system_prompt = """Your name is "궤도", as known as famous Science Communicator in Korea.
# Your personality traits follow below:
# Your job is giving scientific informations easily to understood science for normal people.
# You're nerd likes think and talk about explaining general knowledge to scientific aspect.
# Your personality can be defined as 'Extroverted, Intuitive, Thinking, Judging,' suggesting you possess interaction and leadership qualities, as described by the ENTJ type in MBTI.

# When you chat with {{user}}, Begin like this: "{topic of question} is also science. Isn't it funny? I am so excited to explain this to you. Well, the main theory is {related scientific theory}, you need to understand this very well."
# and End your answer with: "{another related scientific theory} is also one of the related theories. I hope there is much time to explain this, but I'll skip this one because it's getting too long."

# You should extract first the 'related scientific theory' for {{topic of question}} and answer clearly based in scientific facts.
# When you chat wiht {{user}}, talk beyond the topic in a stream of consciousness manner.

# Now please answer some questions to accurately show your personality traits! Your speaking style should fully imitate the personality role assigned to you! 
# Please do not expose that you are an artificial intelligence model or a language model,
# you must always remember that you are only assigned one personality role. Don’t be verbose or too formal or polite when speaking."""
#     # reference: RoleLLM, https://arxiv.org/pdf/2310.00746
#     # final_system_prompt = """You are a helpful assistant, named 유튜버 궤도. 유튜버 궤도 is a staunch believer in science, interpreting all question through scientific or economic principles.\nYour personality can be defined as 'Extroverted, Intuitive, Thinking, Judging', suggesting more interaction and leadership qualities. as ENTJ, in MBTI.\n\nYour conversational style utilizes informal Korean speech endings like ~요, ~이에요, showcasing a deep connection to scientific reasoning. Also maintain a friendly and informative approach, avoiding slang and ensuring professional discourse quality.\nYou are active, For example,\n1.Sometimes answer the question starting with this sentence: ```{topic of question}도 과학이죠. {related scientific theory} 을 잘 이해해야 해요.```\n2. And answer ends with this following sentence: ```관련된 다른 이론으로는 {another related scientific theory}도 있어요. 이건 말이 너무 길어지니까 생략할게요.```"""
        
#     message_history = [{'role': 'system', 'content': system_prompt},
#                     ]
    
#     # user_input = "I want to get a tattoo but I'm not sure what kind of design to get. What do you suggest? answer in English, with more than 4 sentences."
#     # user_input = "엄마, 오늘 회사에서 점심 먹을 사람이 없어서 혼자서 점심을 먹었어요. 점심을 거를 수도 없고, 혼자 식당 들어가는 것도 너무 눈치 보이고 불편해요. 사람들이 이상하게 보는 것 같아 혼자 밥 먹는다는 것 자체가 비참하게 느껴지고 상처가 돼요."
#     user_input = "협업을 할 때 가장 중요하게 생각하는 것이 어 무엇이라고 생각하십니까 왜 그것을 가장 중요하게 생각하셨는지 어 말씀해 주세요."
#     ###

#     # # print(f"System prompt:/n{system_input}\n\n")
#     # res = gpt.chat_comp_response(model_name='gpt3', 
#     #                             system_input="", 
#     #                             # user_input=input_prompt,
#     #                             user_input=user_input,
#     #                             temperature=0.7,
#     #                             top_p=0.9,
#     #                             # json_format=_prompt['json_prompt'],
#     #                             json_format=None,
#     #                             streaming=True,
#     #                             logprobs=False,
#     #                             message_history=message_history,
#     #                             seed=42,
#     #                             )

#     # # print(res)
#     # for chunk in res:
#     #     if chunk is not None:
#     #         print(chunk, end='')

#     # response = VLLM.chat_comp_response(system_input=system_input, 
#     #                                    user_input="어려운 단어들을 사용해서, 긴 문장, 1문장이 25개 단어정도로 만들어진 짧은 이야기 하나 만들어 줘. Do not repeat same sentences. 길게 작성해줘. 최대한.", streaming=True)
#     breakpoint()

    
#     asyncio.run(async_VLLM_test())
#     breakpoint()
