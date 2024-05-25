import requests

access_token = "95643d10e32cc799d8653e9d3bd8e250f30844c1"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept-Encoding": "gzip, deflate"
}

# Ensure proper URL encoding
city = "Horton"

# Correctly format and encode the URL parameters
search_url = (
    "https://api-demo.mlsgrid.com/v2/Lookup"
    "?$filter=OriginatingSystemName eq 'sunflower' and MlgCanView eq true and (LookupName eq '{city}')"
    "&$select=UnparsedAddress,ListPrice,BathroomsTotal,BedroomsTotal,LivingArea,ListingKey"
    "&$expand=Media,Rooms,UnitTypes"
).format(city=city)

# Make the request
response = requests.get(search_url, headers=headers)

# Handle the response
if response.status_code == 200:
    properties = response.json()
    print(properties)
else:
    print(f"Error: {response.status_code} - {response.text}")

# # Search for property given property ID
# property_id = "123456"
# property_url = (
#     "https://api.mlsgrid.com/v2/Property"
#     "?$filter=OriginatingSystemName eq 'actris' and MlgCanView eq true and ListingKey eq '{property_id}'"
#     "&$expand=Media,Rooms,UnitTypes"
# ).format(property_id=property_id)

# # Make the request
# response = requests.get(property_url, headers=headers)

# # Handle the response
# if response.status_code == 200:
#     property_info = response.json()
#     print(property_info)
# else:
#     print(f"Error: {response.status_code} - {response.text}")
