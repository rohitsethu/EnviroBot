import requests
import json

API_KEY = "df7ead2b880e18ef32c2e0d12d4c50fcbb505dc4"

def test_api(city_name, api_key):
    base_url = "https://api.waqi.info/feed/"
    url = f"{base_url}{city_name}/?token={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data["status"] == "ok":
            print(f"API is working for {city_name}. Response:")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"API returned an error for {city_name}: {data['message']}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to API for {city_name}: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for {city_name}: {e}")
        return False

if __name__ == "__main__":
    city_to_test = "Dubai"
    if test_api(city_to_test, API_KEY):
        print("The WAQI API appears to be working.")
    else:
        print("There might be an issue with the WAQI API or your request.")
