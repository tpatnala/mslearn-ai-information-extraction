from dotenv import load_dotenv
import os
import sys
import requests
import json
from azure.ai.projects.models import ConnectionType
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient


def main():

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    # Get the buisness card
    image_file = 'biz-card-1.png'
    if len(sys.argv) > 1:
        image_file = sys.argv[1]

    try:

        # Get config settings
        load_dotenv()
        project_connection = os.getenv('PROJECT_CONNECTION')
        analyzer = os.getenv('ANALYZER')

        # Get AI Services endpoint and key from the project
        project_client = AIProjectClient.from_connection_string(
            conn_str=project_connection,
            credential=DefaultAzureCredential())

        ai_svc_connection = project_client.connections.get_default(
            connection_type=ConnectionType.AZURE_AI_SERVICES,
            include_credentials=True, 
            )

        ai_svc_endpoint = ai_svc_connection.endpoint_url
        ai_svc_key = ai_svc_connection.key

        # Analyze the business card
        analyze_card (image_file, analyzer, ai_svc_endpoint, ai_svc_key)

        print("\n")

    except Exception as ex:
        print(ex)



def analyze_card (image_file, analyzer, endpoint, key):
    
    # Use Content Understanding to analyze the image





if __name__ == "__main__":
    main()        
