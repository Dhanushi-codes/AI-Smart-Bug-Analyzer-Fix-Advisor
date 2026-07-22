import pandas as pd

# File paths
mozilla_path = r"E:\ai project\Datasets\mozilla_bug_report_data.csv"
eclipse_path = r"E:\ai project\Datasets\eclipse_bug_report_data.csv"
apache_path = r"E:\ai project\Datasets\issues.csv"

# Output file
output_path = r"E:\ai project\Datasets\processed_bug_reports.csv"

# Common columns for our RAG knowledge base
columns = [
    "source",
    "bug_id",
    "title",
    "description",
    "product",
    "component",
    "priority",
    "severity",
    "status",
    "resolution",
    "created",
    "resolved"
]

# Process Mozilla and Eclipse
def process_mozilla_eclipse(file_path, source_name):
    df = pd.read_csv(file_path)

    result = pd.DataFrame()
    result["source"] = source_name
    result["bug_id"] = df["bug_id"]
    result["title"] = df["short_description"]
    result["description"] = df["long_description"]
    result["product"] = df["product_name"]
    result["component"] = df["component_name"]
    result["priority"] = ""
    result["severity"] = df["severity_category"]
    result["status"] = df["status_category"]
    result["resolution"] = df["resolution_category"]
    result["created"] = df["creation_date"]
    result["resolved"] = df["resolution_date"]

    return result


# Process Mozilla
print("Processing Mozilla...")
mozilla = process_mozilla_eclipse(mozilla_path, "Mozilla")

# Process Eclipse
print("Processing Eclipse...")
eclipse = process_mozilla_eclipse(eclipse_path, "Eclipse")

# Save Mozilla and Eclipse first
mozilla.to_csv(output_path, index=False)
eclipse.to_csv(output_path, mode="a", header=False, index=False)

print("Mozilla and Eclipse processed successfully.")

# Process Apache in chunks
print("Processing Apache...")

for chunk in pd.read_csv(apache_path, chunksize=50000):

    result = pd.DataFrame()

    result["source"] = "Apache"
    result["bug_id"] = chunk["key"]
    result["title"] = chunk["summary"]
    result["description"] = chunk["description"]
    result["product"] = chunk["project.name"]
    result["component"] = ""
    result["priority"] = chunk["priority.name"]
    result["severity"] = ""
    result["status"] = chunk["status.name"]
    result["resolution"] = chunk["resolution.name"]
    result["created"] = chunk["created"]
    result["resolved"] = chunk["resolutiondate"]

    result.to_csv(
        output_path,
        mode="a",
        header=False,
        index=False
    )

    print("Processed an Apache chunk...")

print("ALL DATASETS PROCESSED SUCCESSFULLY!")
print("Output:", output_path)