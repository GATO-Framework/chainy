from typing import Protocol, TypeAlias

ChatMessages: TypeAlias = list[dict[str, str]]


class LanguageModelProtocol(Protocol):
    def generate(self, prompt: str) -> str:
        ...


class ChatModelProtocol(Protocol):
    def generate(self, messages: ChatMessages) -> str:
        ...


class MockChatModel:
    def generate(self, messages: ChatMessages) -> str:
        result = "\n".join((f"{m['system']}: {m['content']}" for m in messages))
        return f"Mock prompt response for {result}"
