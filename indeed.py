from apify_client import ApifyClient
import csv

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_dKaFEZg2stUGTgXJ16wOPbxDa4Gbib1lFT2s")

# Prepare the Actor input
run_input = {
    "position": "web developer",
    "country": "US",
    "location": "San Francisco",
    "maxItems": 50,
    "parseCompanyDetails": False,
    "saveOnlyUniqueItems": True,
    "followApplyRedirects": False,
}

# Run the Actor and wait for it to finish
run = client.actor("hMvNSpz3JnHgl5jkh").call(run_input=run_input)

# Define the CSV file name
csv_file = "output.csv"

# Fetch the dataset
dataset_items = client.dataset(run["defaultDatasetId"]).iterate_items()

# Open CSV file to write
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Job Title", "Company", "Job Type", "Rating", "Apply Link"])
    
    # Write the header to the CSV
    writer.writeheader()
    
    # Iterate over each item in the dataset and write to CSV
    for item in dataset_items:
        writer.writerow({
            "Job Title": item.get("positionName", "N/A"),           # Job title
            "Company": item.get("company", "N/A"),                 # Extract Company directly from the top-level field
            "Job Type": item.get("jobType", "N/A"),                # Job type
            "Rating": item.get("rating", "N/A"),                   # Rating
            "Apply Link": item.get("url", "N/A")                   # Apply link
        })

print(f"Data has been successfully saved to {csv_file}")
