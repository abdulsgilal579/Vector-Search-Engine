import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ["GROQ_API_KEY"])
MODEL = "llama-3.3-70b-versatile"


def ask_llm(question, context):
    prompt = (
        "You are a helpful assistant. Answer the question using ONLY the context below.\n"
        "If the context doesn't contain the answer, say you don't know.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}"
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content
