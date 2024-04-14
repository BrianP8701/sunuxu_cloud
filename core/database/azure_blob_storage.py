import os
from typing import BinaryIO
from azure.storage.blob import BlobServiceClient, BlobProperties, BlobLeaseClient
from dotenv import load_dotenv

from core.database.abstract_blob_storage import AbstractBlobStorage

load_dotenv()
container_name = os.getenv('AZURE_BLOB_CONTAINER_NAME')

class AzureBlobStorage(AbstractBlobStorage):
    _instance = None

    def __init__(self):
        connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AzureBlobStorage, cls).__new__(cls)
        return cls._instance

    @classmethod
    def dispose_instance(cls):
        if cls._instance:
            cls._instance.blob_service_client.close()
            cls._instance = None

    def upload_blob(self, blob_name: str, data: BinaryIO) -> None:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        if blob_client.exists():
            raise Exception("Blob already exists.")
        blob_client.upload_blob(data)

    def download_blob(self, blob_name: str) -> bytes:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        return blob_client.download_blob().readall()

    def get_etag(self, blob_name: str) -> str:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        blob_properties = blob_client.get_blob_properties()
        return blob_properties.etag

    def overwrite_blob(self, blob_name: str, data: BinaryIO, etag: str = None) -> None:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        if not blob_client.exists():
            raise Exception("Blob does not exist.")
        access_conditions = None
        if etag:
            current_etag = self.get_etag(blob_name)
            if current_etag != etag:
                raise Exception("Etag does not match. Retry the operation.")
        try:
            blob_client.upload_blob(data, overwrite=True)
        except Exception as e:
            print(f"Failed to update blob: {str(e)}")
            raise

    def delete_blob(self, blob_name: str) -> None:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        if not blob_client.exists():
            print(f"Blob {blob_name} does not exist, cannot delete.")
            return
        try:
            blob_client.delete_blob(delete_snapshots="include")
        except Exception as e:
            print(f"Failed to delete blob: {str(e)}")

    def blob_exists(self, blob_name: str) -> bool:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        return blob_client.exists()

    def copy_blob(self, blob_name: str, new_blob_name: str) -> None:
        container_client = self.blob_service_client.get_container_client(container_name)
        source_blob = container_client.get_blob_client(blob_name)
        target_blob = container_client.get_blob_client(new_blob_name)
        target_blob.start_copy_from_url(source_blob.url)

    def add_custom_blob_property(self, blob_name: str, key: str, value: str) -> None:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        properties = blob_client.get_blob_properties()
        metadata = properties.metadata or {}
        metadata[key] = value
        blob_client.set_blob_metadata(metadata)

    def update_custom_blob_property(self, blob_name: str, key: str, value: str) -> None:
        self.add_custom_blob_property(blob_name, key, value)

    def delete_custom_blob_property(self, blob_name: str, key: str) -> None:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        properties = blob_client.get_blob_properties()
        metadata = properties.metadata
        if metadata and key in metadata:
            del metadata[key]
            blob_client.set_blob_metadata(metadata)

    def list_blobs(self) -> list:
        container_client = self.blob_service_client.get_container_client(container_name)
        return [blob.name for blob in container_client.list_blobs()]

    def get_blob_properties(self, blob_name: str) -> BlobProperties:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        return blob_client.get_blob_properties()

    def acquire_blob_lease(self, blob_name: str, lease_duration: int) -> str:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        if not blob_client.exists():
            raise Exception(f"Blob {blob_name} does not exist, cannot acquire lease.")
        lease_client = BlobLeaseClient(blob_client)
        lease_client.acquire(lease_duration=lease_duration)  # This updates lease_client.id
        return lease_client.id  # Access the updated id attribute for the lease ID

    def release_blob_lease(self, blob_name: str, lease_id: str) -> None:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        lease_client = BlobLeaseClient(blob_client, lease_id)
        lease_client.release()

    def upload_blob_with_lease(self, blob_name: str, data: BinaryIO, lease_id: str, etag: str = None) -> None:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        if etag:
            match_condition = "{}".format(etag)
            blob_client.upload_blob(data, etag=match_condition, overwrite=True, lease=lease_id)
        else:
            blob_client.upload_blob(data, overwrite=True, lease=lease_id)

    def clear_container(self, safety: str) -> None:
        if safety != "I understand this will clear the container.":
            raise Exception("Safety string does not match.")
        if os.getenv('MODE') == 'production':
            raise Exception("Cannot clear container in production.")
        container_client = self.blob_service_client.get_container_client(container_name)
        # Delete the entire container
        container_client.delete_container()
        # Recreate the container
        self.blob_service_client.create_container(container_name)
