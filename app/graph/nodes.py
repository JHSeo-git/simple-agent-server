from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.llm import get_llm
from app.log import get_logger

from .types import State

logger = get_logger(__name__)

system_prompt = """
You are an assistant that translates the user's message into a string of relevant emojis.
Respond only with emojis.
"""

chat_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{user_input}"),
    ]
)


def emoji_translate_node(state: State):
    logger.info(f"Emoji translate node called with state: {state}")

    chain = chat_template | get_llm() | StrOutputParser()

    answer = chain.invoke({"user_input": state["messages"][-1]})

    return {"messages": [answer]}
