import os

from datalab_sdk import DatalabClient
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

DATALAB_KEY=os.getenv("DATALAB_API_KEY")  # Get the Datalab API key from environment variables
    
client = DatalabClient(api_key=DATALAB_KEY)  # Initialize the Datalab client with your API key

# Convert a document to markdown
result = client.convert("CCMR_Q1 2025.pdf")
print(result.markdown) # type: ignore

# Save output with images
result.save_output("output/") # type: ignore