from langchain_core.language_models import BaseLanguageModel
from typing_extensions import TypeVar, Generic

from config.log import create_logger
from decorations.log_time import log_time_method


T = TypeVar("T")


class LangChainLLMCallerWithStructure(Generic[T]):
    def __init__(
        self,
        caller_instance,
        llm: BaseLanguageModel,
        output_structure: T,
    ):
        self.structured_output: T = output_structure
        self.llm_with_structured_output = llm.with_structured_output(output_structure)

        self.logger = (
            caller_instance.logger
            if hasattr(caller_instance, "logger")
            else create_logger(self.__class__.__name__)
        )

    @log_time_method
    def invoke(self, *args, **kwargs) -> T:
        return self.llm_with_structured_output.invoke(*args, **kwargs)
