import requests


class MLSAPI:
    BASE_URL = "https://api.mlsgrid.com/v2"

    def __init__(self, access_token):
        self.access_token = access_token

    def _get_headers(self):
        return {"Authorization": f"Bearer {self.access_token}"}

    def _build_filter_query(self, filters):
        filter_clauses = []
        for key, value in filters.items():
            if isinstance(value, list):
                filter_clauses.append(f"{key} in ({', '.join(map(str, value))})")
            else:
                filter_clauses.append(f"{key} eq {value}")
        return " and ".join(filter_clauses)

    def search_properties(
        self, mls_list, filters=None, sort=None, page_size=100, page_number=1
    ):
        if filters is None:
            filters = {}
        if sort is None:
            sort = []

        filter_query = self._build_filter_query(filters)
        mls_filter = " or ".join(
            [f"OriginatingSystemName eq '{mls}'" for mls in mls_list]
        )
        combined_filter = (
            f"({mls_filter}) and ({filter_query})" if filter_query else mls_filter
        )

        params = {
            "$filter": combined_filter,
            "$top": page_size,
            "$skip": (page_number - 1) * page_size,
            "$orderby": ", ".join(sort),
        }

        response = requests.get(
            f"{self.BASE_URL}/Property", headers=self._get_headers(), params=params
        )
        response.raise_for_status()

        return response.json()

    def get_property(self, property_id, exclude_fields=None):
        if exclude_fields is None:
            exclude_fields = []

        params = {"$select": ",".join([f"'{field}'" for field in exclude_fields])}

        response = requests.get(
            f"{self.BASE_URL}/Property('{property_id}')",
            headers=self._get_headers(),
            params=params,
        )
        response.raise_for_status()

        return response.json()


# Example usage
if __name__ == "__main__":
    access_token = "your_access_token"
    mls_api = MLSAPI(access_token)

    # Example filters
    filters = {
        "ListPrice": "gt 300000 and lt 600000",
        "BedroomsTotal": "ge 2 and le 4",
        "BathroomsTotalInteger": "ge 2 and le 3",
        "City": "'Georgetown'",
    }

    # Example sort
    sort = ["ListPrice desc"]

    # Search properties
    mls_list = ["actris"]
    properties = mls_api.search_properties(mls_list, filters, sort)
    print(properties)

    # Get single property
    property_id = "ACT107472571"
    property_details = mls_api.get_property(
        property_id, exclude_fields=["PhotosCount", "TaxYear"]
    )
    print(property_details)
