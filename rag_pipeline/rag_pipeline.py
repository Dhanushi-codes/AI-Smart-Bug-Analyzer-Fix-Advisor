import os
import chromadb
from sentence_transformers import SentenceTransformer
from google import genai

# ---------------------------------------
# CONFIGURATION
# ---------------------------------------

DB_PATH = r"E:\ai project\vector_db"
COLLECTION_NAME = "historical_bug_reports"

# ---------------------------------------
# INITIALIZE GEMINI
# ---------------------------------------

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY environment variable is not set."
    )

gemini_client = genai.Client(
    api_key=api_key
)

# ---------------------------------------
# LOAD EMBEDDING MODEL
# ---------------------------------------

print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# ---------------------------------------
# CONNECT TO CHROMADB
# ---------------------------------------

client = chromadb.PersistentClient(
    path=DB_PATH
)

collection = client.get_collection(
    name=COLLECTION_NAME
)

print("Connected to vector database.")
print(
    "Total historical chunks:",
    collection.count()
)

# ---------------------------------------
# GET NEW BUG REPORT
# ---------------------------------------

bug_report = input(
    "\nEnter your new bug report:\n"
)

# ---------------------------------------
# CREATE QUERY EMBEDDING
# ---------------------------------------

query_embedding = model.encode(
    bug_report
).tolist()

# ---------------------------------------
# RETRIEVE SIMILAR BUGS
# ---------------------------------------

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)

# ---------------------------------------
# BUILD RAG CONTEXT
# ---------------------------------------

context_parts = []

for i in range(
    len(results["documents"][0])
):

    metadata = results["metadatas"][0][i]

    document = results["documents"][0][i]

    context = f"""
Historical Bug {i + 1}

Product:
{metadata.get("product", "Unknown")}

Component:
{metadata.get("component", "Unknown")}

Severity:
{metadata.get("severity", "Unknown")}

Status:
{metadata.get("status", "Unknown")}

Resolution:
{metadata.get("resolution", "Unknown")}

Bug Information:
{document}
"""

    context_parts.append(context)

rag_context = "\n".join(
    context_parts
)

# ---------------------------------------
# CREATE AI PROMPT
# ---------------------------------------

prompt = f"""
You are an AI Smart Bug Analyzer.

Analyze the new bug report using the historical bug reports
retrieved from the organization's defect knowledge base.

NEW BUG REPORT:
{bug_report}

HISTORICAL BUG KNOWLEDGE:
{rag_context}

Provide a structured analysis with the following sections:

1. Probable Root Cause
2. Duplicate Likelihood
3. Severity Assessment
4. Recommended Fix
5. Supporting Historical Evidence
6. Confidence Score

Important:
- Base your reasoning on the provided historical bug knowledge.
- Do not claim that the new bug is an exact duplicate unless the evidence supports it.
- Clearly distinguish between facts from historical bugs and your own hypothesis.
- If the historical evidence is insufficient, say so.
"""

# ---------------------------------------
# SEND TO GEMINI
# ---------------------------------------

print("\nAnalyzing bug with Gemini...")

response = gemini_client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt
)

# ---------------------------------------
# DISPLAY RESULT
# ---------------------------------------

print("\n" + "=" * 70)
print("           AI SMART BUG ANALYSIS")
print("=" * 70)

print(response.text)

print("\n" + "=" * 70)
print("           ANALYSIS COMPLETED")
print("=" * 70)