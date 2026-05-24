# app/llm/verifier.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.config import get_settings
from app.schemas import VerificationResult

settings = get_settings()


def verify_resume(original: str, optimized: str) -> VerificationResult:
    """
    Ensures the optimized resume contains:
    - No hallucinated skills
    - No fabricated experience
    - No invented certifications
    - No false claims
    """

    llm = ChatOpenAI(
        model=settings.OPENAI_MODEL,
        temperature=0.0,
        max_tokens=1200
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a resume verification engine. "
         "Your job is to remove hallucinations from the optimized resume. "
         "If the optimized resume contains information NOT present in the original resume, remove it."),
        ("human",
         "Original Resume:\n{original}\n\n"
         "Optimized Resume:\n{optimized}\n\n"
         "Return a cleaned version of the optimized resume that contains ONLY information "
         "present in the original resume. Remove anything fabricated.")
    ])

    chain = prompt | llm
    response = chain.invoke({
        "original": original,
        "optimized": optimized
    })

    return VerificationResult(
        cleaned_text=response.content
    )
