<div align="center">

# MinIO Manager

![MinIO logo](assets/minio.png)
| Version Info | [![Python](https://img.shields.io/badge/python-v3.10.0-green)](https://www.python.org/downloads/release/python-3913/) [![Platform](https://img.shields.io/badge/Platforms-Ubuntu%2022.04.1%20LTS%2C%20win--64-orange)](https://releases.ubuntu.com/20.04/) |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Release | [![Release](https://img.shields.io/badge/release-v1.0.0--alpha-blue)]() |

---

</div>
MinIO Manager provides functionality for uploading, downloading, listing, and deleting files and folders in a MinIO bucket. This repository supports both file and folder uploads and offers various options for managing objects within a MinIO server.

## Features

- Upload files or folders to a MinIO bucket.
- Download files from a MinIO bucket.
- List objects within a MinIO bucket.
- Delete specific objects or folders from a MinIO bucket.

## Prerequisites

- Python 3.6 or higher
- MinIO server or compatible S3 service
- Environment variables for MinIO access

## 🚀 Installation

1. **Clone the Repository**:

   ```bash
   git clone <repository_url>
   cd Minio-Manager
   ```

2. **Install Dependencies**:
   Ensure you have the required packages. You can install them using `pip`:

   ```bash
   pip install minio python-dotenv
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the root directory of the repository with the following content:
   ```env
   MINIO_ACCESS_KEY=<your_access_key>
   MINIO_SECRET_KEY=<your_secret_key>
   MINIO_ENDPOINT=<your_minio_endpoint>
   MINIO_BUCKET_NAME=<your_bucket_name>
   ```
   Replace `<your_access_key>`, `<your_secret_key>`, `<your_minio_endpoint>`, and `<your_bucket_name>` with your MinIO credentials and bucket details.

## Usage

### Upload Files or Folders

To upload a file or folder to the MinIO bucket:

- **Upload a File**:

  ```bash
  python main.py upload <path_to_file> [--destination <destination_object_name>]
  ```

- **Upload a Folder**:
  ```bash
  python main.py upload <path_to_folder> --destination <destination_folder_name>
  ```

### List Objects

To list objects in the MinIO bucket with an optional prefix:

```bash
python main.py list <prefix>
```

### Download Files

To download a file from the MinIO bucket:

```bash
python main.py download <object_name> --destination <path_to_save_file>
```

### Delete Objects or Folders

To delete a specific object or all objects within a folder:

- **Delete an Object**:

  ```bash
  python main.py delete <object_name>
  ```

- **Delete a Folder**:
  ```bash
  python main.py delete <folder_name>
  ```

## Example

Here are some example commands:

- Upload a single file:

  ```bash
  python main.py upload /path/to/local/file.txt --destination remote-file.txt
  ```

- Upload a folder:

  ```bash
  python main.py upload /path/to/local/folder --destination remote-folder
  ```

- List objects in a bucket:

  ```bash
  python main.py list my-prefix
  ```

- Download a file:

  ```bash
  python main.py download remote-file.txt --destination /path/to/local/file.txt
  ```

- Delete an object:

  ```bash
  python main.py delete remote-file.txt
  ```

- Delete a folder:
  ```bash
  python main.py delete remote-folder/
  ```

## Troubleshooting

- Ensure that the MinIO server is running and accessible.
- Verify that the environment variables in the `.env` file are correct.
- Check for any connectivity issues or permissions problems.

---


For more information about the MinIO Python SDK, visit the [MinIO Python SDK Documentation](https://docs.min.io/docs/python-client-quickstart-guide.html).
---