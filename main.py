from minio import Minio
from minio.error import S3Error
from dotenv import load_dotenv
import os
import argparse

load_dotenv()

def upload_file(client, bucket_name, source_file, destination_file):
    try:
        client.fput_object(bucket_name, destination_file, source_file)
        print(f"File '{source_file}' successfully uploaded as object '{destination_file}' to bucket '{bucket_name}'.")
    except S3Error as exc:
        print(f"Error occurred while uploading file: {exc}")

def upload_folder(client, bucket_name, source_folder, destination_folder):
    try:
        for root, _, files in os.walk(source_folder):
            for file in files:
                local_path = os.path.join(root, file)
                # Create a relative path to use as the object key
                relative_path = os.path.relpath(local_path, source_folder)
                # Construct the object key with destination folder
                destination_file = os.path.join(destination_folder, relative_path).replace("\\", "/")
                client.fput_object(bucket_name, destination_file, local_path)
                print(f"File '{local_path}' successfully uploaded as object '{destination_file}' to bucket '{bucket_name}'.")
    except S3Error as exc:
        print(f"Error occurred while uploading folder: {exc}")

def list_objects(client, bucket_name, prefix=""):
    try:
        objects = client.list_objects(bucket_name, prefix=prefix, recursive=True)
        if not list(objects):
            print(f"No objects found with prefix '{prefix}' in bucket '{bucket_name}'.")
        else:
            print(f"Objects in bucket '{bucket_name}' with prefix '{prefix}':")
            for obj in client.list_objects(bucket_name, prefix=prefix, recursive=True):
                print(f"Object: {obj.object_name}")
    except S3Error as exc:
        print(f"Error occurred while listing objects: {exc}")

def download_file(client, bucket_name, object_name, destination_file):
    try:
        client.fget_object(bucket_name, object_name, destination_file)
        print(f"Object '{object_name}' successfully downloaded as file '{destination_file}' from bucket '{bucket_name}'.")
    except S3Error as exc:
        print(f"Error occurred while downloading file: {exc}")

def delete_object(client, bucket_name, object_name):
    try:
        client.remove_object(bucket_name, object_name)
        print(f"Object '{object_name}' successfully deleted from bucket '{bucket_name}'.")
    except S3Error as exc:
        print(f"Error occurred while deleting object: {exc}")

def delete_folder(client, bucket_name, folder_name):
    try:
        objects = client.list_objects(bucket_name, prefix=folder_name, recursive=True)
        for obj in objects:
            client.remove_object(bucket_name, obj.object_name)
            print(f"Object '{obj.object_name}' successfully deleted from bucket '{bucket_name}'.")
    except S3Error as exc:
        print(f"Error occurred while deleting folder: {exc}")

def main():
    # Load environment variables
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
    MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")

    # Create a client with the MinIO server details and credentials
    client = Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=True  # Change to True if using HTTPS
    )

    # Command-line argument parsing
    parser = argparse.ArgumentParser(description='Upload, download, delete, or list files and folders in MinIO.')
    parser.add_argument(
        'action',
        choices=['upload', 'download', 'delete', 'list'],
        help='Action to perform: "upload" for uploading files/folders, "download" for downloading files, "delete" for deleting files/folders, "list" for listing bucket contents.'
    )
    parser.add_argument(
        'source',
        type=str,
        help='Path to the file or folder to upload, object name for downloading or deleting, or prefix for listing objects.'
    )
    parser.add_argument(
        '--destination',
        type=str,
        default=None,
        help='Destination file path for downloading, or destination object name (for files) or folder name (for folders).'
    )

    args = parser.parse_args()
    action = args.action
    source = args.source
    destination = args.destination or ""  # Default to empty string if not specified

    # Make the bucket if it doesn't exist
    found = client.bucket_exists(MINIO_BUCKET_NAME)
    if not found:
        client.make_bucket(MINIO_BUCKET_NAME)
        print("Created bucket", MINIO_BUCKET_NAME)
    else:
        print("Bucket", MINIO_BUCKET_NAME, "already exists")

    if action == 'upload':
        if os.path.isfile(source):
            # Upload a single file
            upload_file(client, MINIO_BUCKET_NAME, source, destination or os.path.basename(source))
        elif os.path.isdir(source):
            # Upload a folder
            upload_folder(client, MINIO_BUCKET_NAME, source, destination)
        else:
            print("The source path is neither a file nor a folder. Please provide a valid file or folder path.")
    elif action == 'list':
        # List objects in the bucket
        list_objects(client, MINIO_BUCKET_NAME, source)
    elif action == 'download':
        # Download a file
        download_file(client, MINIO_BUCKET_NAME, source, destination)
    elif action == 'delete':
        if destination:
            # Delete a specific object
            delete_object(client, MINIO_BUCKET_NAME, source)
        else:
            # Delete all objects with a specific prefix (folder)
            delete_folder(client, MINIO_BUCKET_NAME, source)

if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("Error occurred:", exc)
