import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import Type, List, Optional
from langchain_core.tools import BaseTool
from langchain_core.messages import AIMessage
from openai import APIConnectionError

from dexter.prompts import DEFAULT_SYSTEM_PROMPT
from dexter.config import settings

# Global LLM instance
llm = None

def get_llm():
    """Initializes and returns the LLM client, ensuring it's a singleton."""
    global llm
    if llm is None:
        llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    return llm

def call_llm(
    prompt: str,
    system_prompt: Optional[str] = None,
    output_schema: Optional[Type[BaseModel]] = None,
    tools: Optional[List[BaseTool]] = None,
) -> AIMessage:
    final_system_prompt = system_prompt if system_prompt else DEFAULT_SYSTEM_PROMPT

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", final_system_prompt),
            ("user", "{prompt}"),
        ]
    )

    llm_client = get_llm()
    runnable = llm_client
    if output_schema:
        runnable = llm_client.with_structured_output(
            output_schema, method="function_calling"
        )
    elif tools:
        runnable = llm_client.bind_tools(tools)

    chain = prompt_template | runnable

    return chain.invoke({"prompt": prompt})
