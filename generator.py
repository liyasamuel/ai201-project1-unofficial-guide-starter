import os
from dotenv import load_dotenv
from groq import Groq

from retriever import retrieve

load_dotenv()

MODEL = "llama-3.1-8b-instant"


def build_context(chunks):
    context_parts = []

    for i, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"[Source {i}: {chunk['source']}]\n{chunk['text']}"
        )

    return "\n\n".join(context_parts)


def generate_response(query):
    chunks = retrieve(query)
    context = build_context(chunks)

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""
You are the GMU Student Survival Guide, a grounded assistant for George Mason University students.

Answer the user's question using ONLY the provided context.
If the context does not contain enough information, say that the documents do not provide enough information.
Do not make up facts.
Cite the source file names you used.

Context:
{context}

Question:
{query}

Answer:
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    print("GMU Student Survival Guide")
    print("Type 'quit' to exit.\n")

    while True:
        question = input("Ask a question: ")

        if question.lower() == "quit":
            break

        answer = generate_response(question)

        print("\nAnswer:")
        print(answer)
        print("\n" + "=" * 80 + "\n")