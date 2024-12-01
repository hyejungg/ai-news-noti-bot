import logging
import time

from langchain_core.language_models import BaseLanguageModel
from typing_extensions import TypeVar, Generic

from config.log import create_logger


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

    def invoke(self, *args, logging_name: str = None, **kwargs) -> T:
        name = logging_name if logging_name else "LLM invocation"
        start = time.time()
        self.logger.info(f"Started {name} ")
        response = self.llm_with_structured_output.invoke(*args, **kwargs)
        end = time.time()
        self.logger.info(f"Finished {name} ({end - start:.2f}s)")
        return response
