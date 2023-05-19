import asyncio
from typing import TypeAlias

ChatMessages: TypeAlias = list[dict[str, str]]


class MockLanguageModel:
    async def generate(self, prompt: str) -> str:
        await asyncio.sleep(0.5)
        return f"Mock prompt response for {prompt}"


class MockChatModel:
    async def generate(self, messages: ChatMessages) -> str:
        result = "\n".join((f"{m['system']}: {m['content']}" for m in messages))
        await asyncio.sleep(0.5)
        return f"Mock prompt response for {result}"
