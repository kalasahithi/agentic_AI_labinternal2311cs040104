import os
from dotenv import load_dotenv
from google import genai
import numpy as np


# --------------------------------
# Gemini Client
# --------------------------------
load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "No Gemini API key found. Create a .env file next to this script "
        "with a line like:\nGEMINI_API_KEY=your_key_here"
    )

client = genai.Client(api_key=API_KEY)

GENERATION_MODEL = "gemini-3.1-flash-lite"
EMBEDDING_MODEL = "gemini-embedding-2"


# --------------------------------
# Knowledge Base
# --------------------------------
documents = [
    """
    Artificial Intelligence is a field of computer science
    that focuses on creating systems capable of performing
    tasks that normally require human intelligence.
    """,

    """
    Machine Learning is a subset of Artificial Intelligence.
    It allows computers to learn patterns from data without
    being explicitly programmed for every task.
    """,

    """
    Deep Learning is a subset of Machine Learning.
    It uses neural networks with multiple layers to learn
    complex patterns from large amounts of data.
    """,

    """
    Natural Language Processing, or NLP, enables computers
    to understand, process and generate human language.
    """,

    """
    Retrieval Augmented Generation, commonly called RAG,
    combines information retrieval with language generation.
    The system first retrieves relevant documents and then
    provides those documents as context to an LLM.
    """,

    """
    Large Language Models are AI models trained on large
    collections of text. They can generate, summarize,
    translate and answer questions using natural language.
    """
]


# --------------------------------
# Generate Embeddings
# --------------------------------
def create_embeddings(texts):

    embeddings = []

    for text in texts:

        result = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text
        )

        embeddings.append(
            np.array(result.embeddings[0].values)
        )

    return embeddings


# --------------------------------
# Create document embeddings
# --------------------------------
print("Creating document embeddings...")

document_embeddings = create_embeddings(
    documents
)


# --------------------------------
# Cosine Similarity
# --------------------------------
def cosine_similarity(a, b):

    return np.dot(a, b) / (
        np.linalg.norm(a) *
        np.linalg.norm(b)
    )


# --------------------------------
# Retrieve relevant documents
# --------------------------------
def retrieve_documents(question, top_k=3):

    question_embedding = create_embeddings(
        [question]
    )[0]

    scores = []

    for index, document_embedding in enumerate(
        document_embeddings
    ):

        score = cosine_similarity(
            question_embedding,
            document_embedding
        )

        scores.append(
            (score, index)
        )

    # Sort highest similarity first
    scores.sort(
        reverse=True
    )

    retrieved_documents = []

    for score, index in scores[:top_k]:

        retrieved_documents.append(
            documents[index]
        )

    return retrieved_documents


# --------------------------------
# Generate Answer
# --------------------------------
def generate_answer(
    question,
    retrieved_documents
):

    context = "\n\n".join(
        retrieved_documents
    )

    prompt = f"""
You are a helpful question-answering assistant.

Use the CONTEXT below if it is relevant to the question.

If the context is not relevant or does not contain the
answer, ignore it and answer the question yourself using
your own general knowledge, just like a normal chatbot.

CONTEXT:
{context}

QUESTION:
{question}

Give a clear and simple answer.
"""

    response = client.models.generate_content(
        model=GENERATION_MODEL,
        contents=prompt
    )

    return response.text


# --------------------------------
# Main RAG Pipeline
# --------------------------------
def main():

    print("=" * 60)
    print("RAG-BASED QUESTION ANSWERING SYSTEM")
    print("=" * 60)

    question = input(
        "\nAsk a question: "
    )

    print(
        "\nSearching for relevant information..."
    )

    retrieved_documents = retrieve_documents(
        question
    )

    print(
        "\nGenerating final answer..."
    )

    answer = generate_answer(
        question,
        retrieved_documents
    )

    print("\n" + "=" * 60)
    print("FINAL ANSWER")
    print("=" * 60)

    print(answer)


if __name__ == "__main__":
    main()