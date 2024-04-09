import os
from typing import BinaryIO
from azure.storage.blob import BlobServiceClient, BlobProperties, BlobLeaseClient
from dotenv import load_dotenv

from core.database.abstract_blob_storage import AbstractBlobStorage

load_dotenv()

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

    def upload_blob(self, container_name: str, blob_name: str, data: BinaryIO) -> None:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        if blob_client.exists():
            raise Exception("Blob already exists.")
        blob_client.upload_blob(data)

    def download_blob(self, container_name: str, blob_name: str) -> bytes:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        return blob_client.download_blob().readall()

    def get_etag(self, container_name: str, blob_name: str) -> str:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        blob_properties = blob_client.get_blob_properties()
        return blob_properties.etag

    def update_blob(self, container_name: str, blob_name: str, data: BinaryIO, etag: str = None) -> None:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        if not blob_client.exists():
            raise Exception("Blob does not exist.")
        if etag:
            match_condition = "{}".format(etag)
            blob_client.upload_blob(data, etag=match_condition, overwrite=True)
        else:
            blob_client.upload_blob(data, overwrite=True)

    def delete_blob(self, container_name: str, blob_name: str) -> None:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.delete_blob()

    def blob_exists(self, container_name: str, blob_name: str) -> bool:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        return blob_client.exists()

    def container_exists(self, container_name: str) -> bool:
        container_client = self.blob_service_client.get_container_client(container_name)
        return container_client.exists()

    def copy_blob(self, container_name: str, blob_name: str, new_blob_name: str) -> None:
        container_client = self.blob_service_client.get_container_client(container_name)
        source_blob = container_client.get_blob_client(blob_name)
        target_blob = container_client.get_blob_client(new_blob_name)
        target_blob.start_copy_from_url(source_blob.url)

    def add_custom_blob_property(self, container_name: str, blob_name: str, key: str, value: str) -> None:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        properties = blob_client.get_blob_properties()
        metadata = properties.metadata or {}
        metadata[key] = value
        blob_client.set_blob_metadata(metadata)

    def update_custom_blob_property(self, container_name: str, blob_name: str, key: str, value: str) -> None:
        self.add_custom_blob_property(container_name, blob_name, key, value)

    def delete_custom_blob_property(self, container_name: str, blob_name: str, key: str) -> None:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        properties = blob_client.get_blob_properties()
        metadata = properties.metadata
        if metadata and key in metadata:
            del metadata[key]
            blob_client.set_blob_metadata(metadata)

    def list_blobs(self, container_name: str) -> list:
        container_client = self.blob_service_client.get_container_client(container_name)
        return [blob.name for blob in container_client.list_blobs()]

    def get_blob_properties(self, container_name: str, blob_name: str) -> BlobProperties:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        return blob_client.get_blob_properties()

    def create_container(self, container_name: str) -> None:
        container_client = self.blob_service_client.get_container_client(container_name)
        container_client.create_container()

    def delete_container(self, container_name: str) -> None:
        container_client = self.blob_service_client.get_container_client(container_name)
        container_client.delete_container()

    def acquire_blob_lease(self, container_name: str, blob_name: str, lease_duration: int) -> str:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        lease_client = BlobLeaseClient(blob_client)
        lease = lease_client.acquire(lease_duration)
        return lease.id

    def release_blob_lease(self, container_name: str, blob_name: str, lease_id: str) -> None:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        lease_client = BlobLeaseClient(blob_client, lease_id=lease_id)
        lease_client.release()

    def upload_blob_with_lease(self, container_name: str, blob_name: str, data: BinaryIO, lease_id: str, etag: str = None) -> None:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        if etag:
            match_condition = "{}".format(etag)
            blob_client.upload_blob(data, etag=match_condition, overwrite=True, lease=lease_id)
        else:
            blob_client.upload_blob(data, overwrite=True, lease=lease_id)