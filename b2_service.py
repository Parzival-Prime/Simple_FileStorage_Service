import requests # type: ignore
from dotenv import load_dotenv # type: ignore
import os
import boto3 # type: ignore
from botocore.exceptions import NoCredentialsError # type: ignore
from botocore.config import Config # type: ignore



load_dotenv()

access_key_id = os.getenv("B2_ACCESS_KEY_ID")
application_key = os.getenv("B2_APPLICATION_KEY")
bucket_name = os.getenv("B2_BUCKET_NAME")
endpoint_url = os.getenv("S3_ENDPOINT_URL")

my_config = Config(
    region_name='us-east-005',
    signature_version='s3v4',
    s3={'use_accelerate_endpoint': False, 'addressing_style': 'path'},
    retries={"max_attempts": 3, "mode": "standard"}
)


class B2:
    """Class to use BackBlaze Service"""
    
    def __init__(self):
        self.s3_client = boto3.client('s3', 
                                aws_access_key_id=access_key_id, 
                                aws_secret_access_key=application_key,
                                endpoint_url=endpoint_url,
                                config=my_config)
        
    
    def upload_file(self, object_file, file_name):
        """Upload a file to a specified Backblaze B2 bucket."""
        
        try:
            self.s3_client.put_object(Key=file_name, Bucket=bucket_name, Body=object_file)
        except NoCredentialsError:
            print("Credentials not available.")
        except Exception as e:
            print(f"Error: {e}")

        
    def delete_file(self, key):
        """Delete a file from a Backblaze B2 bucket."""
        
        try:
            self.s3_client.delete_object(
                            Bucket=bucket_name,
                            Key=key
                        )
            print(f"File deleted from {bucket_name}")
        except NoCredentialsError:
            print("Credentials not available.")
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def download_file(self, bucket_name, file_name, key):
        """Download a file from a Backblaze B2 bucket."""
        
        try:
            self.s3_client.download_file(Bucket=bucket_name, Filename=file_name, Key=key)
            # with open(file, 'wb') as f:
            #     f.write('dresume.pdf')
            print(f"File downloaded successfully!")
        except NoCredentialsError:
            print("Credentials not available.")
        except Exception as e:
            print(f"Error: {str(e)}")
        
        
        
# b2_obj = B2()
# # b2_obj.upload_file(file_path='Resume.pdf', file_name='Resume.pdf', bucket_name=bucket_name)
# # b2_obj.download_file(file_name='dresume.pdf', bucket_name=bucket_name, key='Resume.pdf')
# b2_obj.delete_file(bucket_name=bucket_name, key='Resume.pdf')