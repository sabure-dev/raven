from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any

InputType = TypeVar('InputType')
OutputType = TypeVar('OutputType')


class BaseUseCase(Generic[InputType, OutputType], ABC):
    @abstractmethod
    async def execute(self, input_data: InputType) -> OutputType:
        pass
