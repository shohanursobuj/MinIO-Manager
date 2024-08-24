from minio import Minio
from minio.error import S3Error
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MinIO configurations
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")

# Initialize the MinIO client
client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=True  # Change to False if not using HTTPS
)

def check_bucket_access(client, bucket_name):
    try:
        # Use `recursive=False` to list objects at the top level, which includes prefixes (folders)
        objects = client.list_objects(bucket_name, recursive=True)

        print(f"MinIO Connection successful. Contents of bucket '{bucket_name}':")
        for obj in objects:
            if obj.is_dir:
                print(f"Folder: {obj.object_name}")
            else:
                print(f"Object: {obj.object_name}")
    except S3Error as e:
        print(f"Failed to access bucket '{bucket_name}': {e}")

if __name__ == "__main__":
    check_bucket_access(client, MINIO_BUCKET_NAME)
