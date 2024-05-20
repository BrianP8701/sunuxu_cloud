# import requests
# import uuid

# GOOGLE_PLACES_API_KEY = "AIzaSyDGSmpuE4z-zyI72026Dfkdmf5ZOsM8ON8"
# query_1 = "6726"
# query_2 = "6726 Sel"
# query_3 = "6726 Selfridge Street"
# place_id = "Eik2NzI2IFNlbGZyaWRnZSBTdHJlZXQsIEhhbXRyYW1jaywgTUksIFVTQSIxEi8KFAoSCdfKyql00iSIERlyzSnClgh1EMY0KhQKEgmJN5dQC9IkiBGWsZlDVuJTFg"
# session_token = str(uuid.uuid4())
# # url_1 = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input=" + query_1 + "&key=" + GOOGLE_PLACES_API_KEY + "&language=en&sessiontoken=" + session_token
# # url_2 = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input=" + query_2 + "&key=" + GOOGLE_PLACES_API_KEY + "&language=en&sessiontoken=" + session_token
# # url_3 = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input=" + query_3 + "&key=" + GOOGLE_PLACES_API_KEY + "&language=en&sessiontoken=" + session_token

# url_4 = (
#     "https://maps.googleapis.com/maps/api/place/details/json?place_id="
#     + place_id
#     + "&key="
#     + GOOGLE_PLACES_API_KEY
#     + "&language=en&fields=formatted_address,address_components"
# )


# # response_1 = requests.get(url_1)
# # print(response_1.json())
# # print('\n')
# # response_2 = requests.get(url_2)
# # print(response_2.json())
# # print('\n')
# # response_3 = requests.get(url_3)
# # print(response_3.json())
# response_4 = requests.get(url_4)
# print(response_4.json())


# # Example usage:
# def parse_address_components(address_components):
#     parsed_address = {}
#     for component in address_components:
#         if "street_number" in component["types"]:
#             parsed_address["street_number"] = component["long_name"]
#         elif "route" in component["types"]:
#             street_name_parts = component["long_name"].split()
#             parsed_address["street_name"] = " ".join(street_name_parts[:-1])
#             parsed_address["street_suffix"] = street_name_parts[-1]
#         elif "locality" in component["types"]:
#             parsed_address["city"] = component["long_name"]
#         elif "administrative_area_level_1" in component["types"]:
#             parsed_address["state"] = component["short_name"]
#         elif "postal_code" in component["types"]:
#             parsed_address["zip_code"] = component["long_name"]
#         elif "country" in component["types"]:
#             parsed_address["country"] = component["long_name"]
#     return parsed_address


# parsed_address = parse_address_components(
#     response_4.json()["result"]["address_components"]
# )
# print(parsed_address)


def print_bitwise_and_of_i_and_neg_i(number):
    result = number & -number
    print(f"The result of {number} & -{number} is: {result}")


# Example usage
for i in range(1, 128):
    print_bitwise_and_of_i_and_neg_i(i)
