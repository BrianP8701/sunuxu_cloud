import webbrowser

client_id = "random"
redirect_uri = "https://www.google.com"
response_type = "code"
scope = "profile_access"

auth_url = f"https://api.books.skyslope.com/oauth/authorize?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"

# Open the URL in a web browser
webbrowser.open(auth_url)
