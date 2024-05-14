import pypdf
from typing import List


class PaperworkEditor:
    """
    This class is a wrapper around the paperwork model. It provides a way to fill out the paperwork
    and perform operations on a pdf.
    """

    def __init__(self, id: int):
        pass

    def save(self, id: int):
        """Save pdf bytes to blob storage"""
        pass

    def fill_field(self, field_name: str, value: str):
        """Fill out a field with a value"""
        pass

    def get_field_value(self, field_name: str) -> str:
        """Get the value of a field"""
        pass

    def get_all_field_names(self) -> List[str]:
        """Get all field names"""
        pass

    def change_field_name(self, old_field_name: str, new_field_name: str):
        """Change the name of a field"""
        pass

    def delete_field(self, field_name: str):
        """Delete a field"""
        pass
