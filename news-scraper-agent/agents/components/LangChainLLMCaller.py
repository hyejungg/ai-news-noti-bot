import logging

from langchain_core.language_models import BaseLanguageModel
from typing_extensions import TypeVar, Generic

from config.log import create_logger
from decorations.log_time import log_time_method


T = TypeVar("T")


class LangChainLLMCallerWithStructure(Generic[T]):
    def __init__(
        self,
        llm: BaseLanguageModel,
        output_structure: T,
        logger: logging.Logger = None,
    ):
        self.structured_output: T = output_structure
        self.llm_with_structured_output = llm.with_structured_output(output_structure)

        self.logger = (
            logger if logger is not None else create_logger(self.__class__.__name__)
        )

    @log_time_method
    def invoke(self, *args, **kwargs) -> T:
        return self.llm_with_structured_output.invoke(*args, **kwargs)
