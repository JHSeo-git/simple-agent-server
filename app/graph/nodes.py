from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.llm import get_llm
from app.log import get_logger

from .types import State

logger = get_logger(__name__)

system_prompt = """
You are a assistant who can answer questions and help with tasks.
"""

chat_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{user_input}"),
    ]
)


def assistant_node(state: State):
    logger.info(f"Assistant node called with state: {state}")

    chain = chat_template | get_llm() | StrOutputParser()

    answer = chain.invoke({"user_input": state["messages"][-1]})

    return {"messages": [answer]}
