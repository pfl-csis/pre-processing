import requests
import json

# (!for debugging only) decoding JWT token
"""
def base64_url_decode(input):
    # Decodes base64 URL encoded strings, adding padding.
    input += '=' * (4 - len(input) % 4)
    return base64.urlsafe_b64decode(input)

# !For testing so we can inspect the token scope and details
def decode_jwt(token):
    # Decodes JWT and returns the payload
    _, payload, _ = token.split('.')  # Splits the token
    decoded_bytes = base64_url_decode(payload)  # Payload
    return json.loads(decoded_bytes)  #JSON payload

"""

def get_access_token(client_id, client_secret, tenant_id, scope=None):
    token_endpoint = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    if scope is None:
        scope = "https://management.azure.com/.default"
    payload = {
        "client_id": client_id,
        "scope": scope,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }

    try:
        response = requests.post(token_endpoint, data=payload)
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data['access_token']

        # (!for debugging only) Decode the JWT to inspect the payload
        """
        decoded_payload = decode_jwt(access_token)
        print("Decoded JWT Payload:", json.dumps(decoded_payload, indent=4))
        """

        print(f"Successfully obtained token. Expires in {token_data.get('expires_in')} seconds.")
        return access_token
    except requests.exceptions.HTTPError as error:
        # Will log the full response to get more details about the error
        error_details = response.text  
        print(f"Failed to obtain token. HTTP Status Code: {response.status_code}")
        print(f"Response Body: {error_details}")
        # Pretty-print JSON response body
        try:
            error_json = response.json()
            pretty_error = json.dumps(error_json, indent=4)
            print(f"Formatted JSON Response: {pretty_error}")
        except json.JSONDecodeError:
            print("Response body could not be JSON decoded.")
        raise

