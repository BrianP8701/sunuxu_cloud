import unittest
from io import BytesIO

from dotenv import load_dotenv

from core.database.azure_blob_storage import AzureBlobStorage

load_dotenv()


class AzureBlobStorageTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.blob_storage = AzureBlobStorage()
        cls.blob_data = b"Test data"

    @classmethod
    def tearDownClass(cls):
        AzureBlobStorage.dispose_instance()

    def tearDown(self):
        try:
            self.blob_storage.delete_blob(self.blob_name)
        except Exception as e:
            print(f"Failed to delete blob in tearDown: {str(e)}")

    def test_upload_and_download_blob(self):
        self.blob_name = "test_upload_and_download_blob"
        self.blob_storage.upload_blob(self.blob_name, BytesIO(self.blob_data))
        downloaded_data = self.blob_storage.download_blob(self.blob_name)
        self.assertEqual(downloaded_data, self.blob_data)

    def test_update_blob(self):
        self.blob_name = "test_update_blob"
        self.blob_storage.upload_blob(self.blob_name, BytesIO(self.blob_data))
        updated_data = b"Updated test data"
        etag = self.blob_storage.get_etag(self.blob_name)
        self.blob_storage.overwrite_blob(self.blob_name, BytesIO(updated_data), etag)
        downloaded_data = self.blob_storage.download_blob(self.blob_name)
        self.assertEqual(downloaded_data, updated_data)

    def test_blob_exists(self):
        self.blob_name = "test_blob_exists"
        self.assertFalse(self.blob_storage.blob_exists(self.blob_name))
        self.blob_storage.upload_blob(self.blob_name, BytesIO(self.blob_data))
        self.assertTrue(self.blob_storage.blob_exists(self.blob_name))

    def test_copy_blob(self):
        self.blob_name = "test_copy_blob"
        self.blob_storage.upload_blob(self.blob_name, BytesIO(self.blob_data))
        new_blob_name = "copied-blob-test_copy_blob"
        self.blob_storage.copy_blob(self.blob_name, new_blob_name)
        self.assertTrue(self.blob_storage.blob_exists(new_blob_name))
        self.blob_storage.delete_blob(new_blob_name)

    def test_add_update_delete_custom_blob_property(self):
        self.blob_name = "test_add_update_delete_custom_blob_property"
        self.blob_storage.upload_blob(self.blob_name, BytesIO(self.blob_data))
        self.blob_storage.add_custom_blob_property(
            self.blob_name, "test_key", "test_value"
        )
        properties = self.blob_storage.get_blob_properties(self.blob_name)
        self.assertEqual(properties.metadata["test_key"], "test_value")
        self.blob_storage.update_custom_blob_property(
            self.blob_name, "test_key", "updated_value"
        )
        properties = self.blob_storage.get_blob_properties(self.blob_name)
        self.assertEqual(properties.metadata["test_key"], "updated_value")
        self.blob_storage.delete_custom_blob_property(self.blob_name, "test_key")
        properties = self.blob_storage.get_blob_properties(self.blob_name)
        self.assertNotIn("test_key", properties.metadata)

    def test_list_blobs(self):
        self.blob_name = "test_list_blobs"
        self.blob_storage.upload_blob(self.blob_name, BytesIO(self.blob_data))
        blob_list = self.blob_storage.list_blobs()
        self.assertIn(self.blob_name, blob_list)

    def test_acquire_and_release_blob_lease(self):
        self.blob_name = "test_acquire_and_release_blob_lease"
        self.blob_storage.upload_blob(self.blob_name, BytesIO(self.blob_data))
        lease_id = self.blob_storage.acquire_blob_lease(
            self.blob_name, lease_duration=15
        )
        self.assertIsNotNone(lease_id)
        self.blob_storage.release_blob_lease(self.blob_name, lease_id)

    def test_upload_blob_with_lease(self):
        self.blob_name = "test_upload_blob_with_lease"
        self.blob_storage.upload_blob(self.blob_name, BytesIO(self.blob_data))
        lease_id = self.blob_storage.acquire_blob_lease(
            self.blob_name, lease_duration=15
        )
        updated_data = b"Updated test data with lease"
        self.blob_storage.upload_blob_with_lease(
            self.blob_name, BytesIO(updated_data), lease_id
        )
        downloaded_data = self.blob_storage.download_blob(self.blob_name)
        self.assertEqual(downloaded_data, updated_data)
        self.blob_storage.release_blob_lease(self.blob_name, lease_id)


if __name__ == "__main__":
    unittest.main()
