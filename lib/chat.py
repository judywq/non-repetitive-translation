from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

official_model_gpt_4o = 'gpt-4o-2024-05-13'
official_model_sonnet = 'claude-3-5-sonnet-20240620'

models = {
    "gpt4o": {
        "vendor": "openai",
        "model_id": official_model_gpt_4o,
    },
    "sonnet": {
        "vendor": "anthropic",
        "model_id": official_model_sonnet,
    },
}

def run_model(model_name, system_message, user_message, temperature=0):
    if model_name not in models:
        raise ValueError(f"Invalid model name: {model_name}")

    model = models[model_name]
    model_id = model["model_id"]
    if model["vendor"] == "openai":
        llm = ChatOpenAI(
            model=model_id,
            temperature=temperature,
            max_tokens=4096,
            timeout=None,
            max_retries=2,
        )
    elif model["vendor"] == "anthropic":
        llm = ChatAnthropic(
            model=model_id,
            temperature=temperature,
            max_tokens=4096,
            timeout=None,
            max_retries=2,
        )
    else:
        raise ValueError("Invalid vender")

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_message,
            ),
            ("human", "{input}"),
        ]
    )

    chain = prompt | llm
    ai_msg = chain.invoke({"input": user_message})
    return ai_msg.content


def run_model_finetuned(model_id, system_message, user_message, temperature=0):
    llm = ChatOpenAI(
        model=model_id,
        temperature=temperature,
        # max_tokens=1024,
        timeout=None,
        max_retries=2,
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_message,
            ),
            ("human", "{input}"),
        ]
    )

    chain = prompt | llm
    ai_msg = chain.invoke({"input": user_message})
    return ai_msg.content
