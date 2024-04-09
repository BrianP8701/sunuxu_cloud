from abc import ABC, abstractmethod
from typing import Any, BinaryIO

class AbstractBlobStorage(ABC):
    @abstractmethod
    def dispose_instance(self):
        pass

    @abstractmethod
    def upload_blob(self, container_name: str, blob_name: str, data: BinaryIO) -> None:
        """ Uploads a blob to the blob storage. Raises an exception if the blob already exists."""
        pass

    @abstractmethod
    def download_blob(self, container_name: str, blob_name: str) -> bytes:
        """ Returns the data of the blob as bytes. """
        pass

    @abstractmethod
    def get_etag(self, container_name: str, blob_name: str) -> str:
        """ Returns the etag of the blob. """
        pass

    @abstractmethod
    def update_blob(self, container_name: str, blob_name: str, data: BinaryIO, etag: str = None) -> None:
        """ 
        Updates a blob in the blob storage. Optionally include an etag to check for optimistic concurrency.
        Raises an exception if the blob does not exist or the etag does not match.
        """
        pass

    @abstractmethod
    def delete_blob(self, container_name: str, blob_name: str) -> None:
        pass

    @abstractmethod
    def blob_exists(self, container_name: str, blob_name: str) -> bool:
        pass

    @abstractmethod
    def container_exists(self, container_name: str) -> bool:
        pass

    @abstractmethod
    def copy_blob(self, container_name: str, blob_name: str, new_blob_name: str) -> None:
        pass

    @abstractmethod
    def add_custom_blob_property(self, container_name: str, blob_name: str, key: str, value: str) -> None:
        pass

    @abstractmethod
    def update_custom_blob_property(self, container_name: str, blob_name: str, key: str, value: str) -> None:
        pass

    @abstractmethod
    def delete_custom_blob_property(self, container_name: str, blob_name: str, key: str) -> None:
        pass

    @abstractmethod
    def list_blobs(self, container_name: str) -> list:
        pass

    @abstractmethod
    def get_blob_properties(self, container_name: str, blob_name: str) -> Any:
        pass

    @abstractmethod
    def create_container(self, container_name: str) -> None:
        pass

    @abstractmethod
    def delete_container(self, container_name: str) -> None:
        pass

    @abstractmethod
    def acquire_blob_lease(self, container_name: str, blob_name: str, lease_duration: int) -> str:
        pass

    @abstractmethod
    def release_blob_lease(self, container_name: str, blob_name: str, lease_id: str) -> None:
        pass

    @abstractmethod
    def upload_blob_with_lease(self, container_name: str, blob_name: str, data: BinaryIO, lease_id: str, etag: str = None) -> None:
        pass
