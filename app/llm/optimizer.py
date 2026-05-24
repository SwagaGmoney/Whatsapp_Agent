

from typing import List
from langchain_openai import ChatOpenAI
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
    
    Guarantees structural output matching TailoredResume schema.
    """

    # 1. Initialize the model with lower temperature for factual adherence
    base_llm = ChatOpenAI(
        model=settings.OPENAI_MODEL,
        temperature=0.1,  # Kept low to enforce strict truthfulness
        max_tokens=2000   # Slightly bumped to prevent truncation on longer resumes
    )

    # 2. Bind the Pydantic schema to force OpenAI's JSON mode/Structured Output
    llm = base_llm.with_structured_output(TailoredResume)

    constraint_text = "\n".join([f"- {c}" for c in constraints])

    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "You are an expert ATS resume optimizer and technical writer. "
         "Your task is to rewrite the resume to dynamically align with the target job description while strictly conforming to the provided ATS formatting rules.\n\n"
         "CRITICAL GUARDRAILS:\n"
         "- Maintain absolute truthfulness. Do not invent metrics, tools, or experiences.\n"
         "- Eliminate cliché AI fluff (e.g., 'results-driven', 'dynamic', 'strategic'). Keep the tone natural, precise, and human.\n"
         "- Rely entirely on raw text structures; do not embed formatting markdown inside the JSON response fields that violate retrieved constraints."),
        ("human",
         "Resume:\n{resume}\n\n"
         "Job Description:\n{jd}\n\n"
         "ATS Constraints:\n{constraints}\n\n"
         "Optimize the resume for this position while keeping it strictly authentic.")
    ])

    # 3. Chain execution
    chain = prompt | llm
    
    # Because of with_structured_output, the response IS already a TailoredResume instance!
    response: TailoredResume = chain.invoke({
        "resume": resume,
        "jd": job_description,
        "constraints": constraint_text
    })

    return response