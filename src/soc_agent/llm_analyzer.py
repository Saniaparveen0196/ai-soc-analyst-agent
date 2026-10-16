
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()


def investigate_alert(alert: dict) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    model_name = os.getenv(
        "GROQ_MODEL",
        "llama-3.3-70b-versatile",
    )

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Check your .env file."
        )

    llm = ChatGroq(
        model=model_name,
        temperature=0,
        api_key=api_key,
    )

    messages = [
        SystemMessage(
            content=(
                "You are an assistant supporting a cybersecurity "
                "SOC analyst. Analyze only the supplied alert data. "
                "Separate observed facts from hypotheses. Do not "
                "claim an attack is confirmed without evidence. "
                "Recommend safe investigation steps. Never execute "
                "security actions."
            )
        ),
        HumanMessage(
            content=(
                "Analyze this security alert and produce a concise "
                "investigation summary with these sections:\n"
                "1. Observed evidence\n"
                "2. Potential explanation\n"
                "3. Additional evidence needed\n"
                "4. Recommended investigation steps\n\n"
                f"Alert data: {alert}"
            )
        ),
    ]

    response = llm.invoke(messages)
    return response.content
