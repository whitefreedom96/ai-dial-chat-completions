from aidial_client import Dial, AsyncDial

from task.clients.base import BaseClient
from task.constants import DIAL_ENDPOINT
from task.models.message import Message
from task.models.role import Role


class DialClient(BaseClient):
    def __init__(self, deployment_name: str):
        super().__init__(deployment_name)
        # Create Dial and AsyncDial clients
        self._client = Dial(base_url=DIAL_ENDPOINT, api_key=self._api_key)
        self._async_client = AsyncDial(base_url=DIAL_ENDPOINT, api_key=self._api_key)

    def get_completion(self, messages: list[Message]) -> Message:
        # Synchronous chat completion
        response = self._client.chat.completions.create(
            deployment_name=self._deployment_name,
            messages=[msg.to_dict() for msg in messages]
        )
        if hasattr(response, 'choices') and response.choices and hasattr(response.choices[0], 'message'):
            content = response.choices[0].message.content
            print(content)
            return Message(role=Role.AI, content=content)
        raise Exception("No choices in response found")

    async def stream_completion(self, messages: list[Message]) -> Message:
        # Asynchronous streaming chat completion
        contents = []
        chunks = await self._async_client.chat.completions.create(
            deployment_name=self._deployment_name,
            messages=[msg.to_dict() for msg in messages],
            stream=True
        )
        async for chunk in chunks:
            if hasattr(chunk, 'choices') and chunk.choices:
                delta = chunk.choices[0].delta
                if delta and getattr(delta, 'content', None):
                    print(delta.content, end='')
                    contents.append(delta.content)
        print()
        return Message(role=Role.AI, content=''.join(contents))
