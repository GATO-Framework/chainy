from typing import Protocol, TypeAlias

ChatMessages: TypeAlias = list[dict[str, str]]


class LanguageModelProtocol(Protocol):
    async def generate(self, prompt: str) -> str:
        ...


class ChatModelProtocol(Protocol):
    async def generate(self, messages: ChatMessages) -> str:
        ...


LargeLanguageModel: TypeAlias = LanguageModelProtocol | ChatModelProtocol
