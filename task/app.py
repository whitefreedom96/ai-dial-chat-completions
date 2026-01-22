import asyncio

from task.clients.client import DialClient
from task.clients.custom_client import DialClient as CustomDialClient
from task.constants import DEFAULT_SYSTEM_PROMPT
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role


def get_user_input(prompt: str) -> str:
    try:
        return input(prompt)
    except EOFError:
        return 'exit'


async def start(stream: bool = True, use_custom: bool = False) -> None:
    # 1.1/1.2: Choose client
    deployment_name = 'gpt-4o'  # Or let user choose
    ClientClass = CustomDialClient if use_custom else DialClient
    client = ClientClass(deployment_name)
    # 2. Conversation object
    conversation = Conversation()
    # 3. System prompt
    system_prompt = get_user_input("Provide System prompt or press 'enter' to continue.\n> ")
    if not system_prompt.strip():
        system_prompt = DEFAULT_SYSTEM_PROMPT
    conversation.add_message(Message(role=Role.SYSTEM, content=system_prompt))
    print("\nType your question or 'exit' to quit.")
    while True:
        user_input = get_user_input('> ')
        if user_input.strip().lower() == 'exit':
            print('Exiting the chat. Goodbye!')
            break
        if not user_input.strip():
            continue
        conversation.add_message(Message(role=Role.USER, content=user_input))
        if stream:
            ai_message = await client.stream_completion(conversation.get_messages())
        else:
            ai_message = client.get_completion(conversation.get_messages())
        conversation.add_message(ai_message)

if __name__ == "__main__":
    # You can toggle stream/custom here
    asyncio.run(start(stream=True, use_custom=False))
