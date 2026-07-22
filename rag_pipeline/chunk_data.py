import pandas as pd

input_path = r"E:\ai project\Datasets\processed_bug_reports_sample.csv"
output_path = r"E:\ai project\Datasets\chunked_bug_reports.csv"

df = pd.read_csv(input_path)

chunks = []

chunk_size = 500
overlap = 50

for _, row in df.iterrows():

    bug_id = str(row["bug_id"])
    title = str(row["title"])
    description = str(row["description"])

    # Combine title and description
    text = f"Title: {title}\nDescription: {description}"

    # Remove empty/invalid text
    if not text.strip() or text.strip().lower() in ["nan", "none"]:
        continue

    # Split into chunks
    start = 0
    chunk_number = 0

    while start < len(text):

        end = start + chunk_size
        chunk_text = text[start:end].strip()

        # Ignore very small chunks
        if len(chunk_text) >= 100:

            chunks.append({
                "bug_id": bug_id,
                "chunk_id": f"{bug_id}_chunk_{chunk_number}",
                "chunk_text": chunk_text,
                "source": row["source"],
                "product": row["product"],
                "component": row["component"],
                "priority": row["priority"],
                "severity": row["severity"],
                "status": row["status"],
                "resolution": row["resolution"],
                "created": row["created"],
                "resolved": row["resolved"]
            })

        chunk_number += 1

        start = end - overlap


chunks_df = pd.DataFrame(chunks)

chunks_df.to_csv(output_path, index=False)

print("Chunking completed successfully!")
print("Total valid chunks:", len(chunks_df))
print("Output:", output_path)