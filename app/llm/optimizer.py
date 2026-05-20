# app/llm/optimizer.py

from typing import List
from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.config import get_settings
from app.schemas import TailoredResume

settings = get_settings()


def optimize_resume(resume: str, job_description: str, constraints: List[str]) -> TailoredResume:
    """
    Uses an LLM to rewrite the resume based on:
    - Sanitized resume
    - Sanitized job description
    - ATS constraints retrieved from Qdrant
    """

    llm = ChatOpenAI(
        model=settings.OPENAI_MODEL,
        temperature=0.2,
        max_tokens=1500
    )

    constraint_text = "\n".join([f"- {c}" for c in constraints])

    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "You are an expert ATS resume optimizer. "
         "Rewrite the resume to match the job description while strictly following ATS rules. "
         "Do NOT hallucinate. Only use information present in the resume."),
        ("human",
         "Resume:\n{resume}\n\n"
         "Job Description:\n{jd}\n\n"
         "ATS Constraints:\n{constraints}\n\n"
         "Rewrite the resume to maximize ATS score while keeping it truthful.")
    ])

    chain = prompt | llm
    response = chain.invoke({
        "resume": resume,
        "jd": job_description,
        "constraints": constraint_text
    })

    return TailoredResume(
        optimized_text=response.content
    )
