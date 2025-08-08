from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import chainlit as cl
import os
from dotenv import load_dotenv
 
load_dotenv()

model = OpenAIModel(
    'google/gemini-2.5-flash-lite',
    provider=OpenAIProvider(
        base_url='https://openrouter.ai/api/v1',
        api_key=os.getenv("OPENROUTER_API_KEY"),
    ),
)

simple_agent = Agent(
    model=model,
    # 'Be concise, reply with one sentence.' is enough for some models (like openai) to use
    # the below tools appropriately, but others like anthropic and gemini require a bit more direction.
    system_prompt=(
        'You are a UI/UX expert. Please help me with my questions about user interface design. Please do not answer questions that are not related to UI/UX design. ',
        'Please answer in zh-HK.',
    ),
)

@cl.on_chat_start
def on_start():
    cl.user_session.set("agent", simple_agent)

@cl.on_message #decorator 包住下面嘅function
async def on_message(message: cl.Message):
    agent = cl.user_session.get("agent")
    response = agent.run_sync(message.content)
    await cl.Message(content=response.output).send()


#run - chainlit run main.py
    
# response = simple_agent.run_sync("Where is Hong Kong?")
# print(response.output)

