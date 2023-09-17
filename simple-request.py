import requests

url = "https://stackoverflow.com"

payload = ""
headers = {
  'Cookie': 'prov=7ce1f615-22c5-0371-3c05-3a35bae9678a'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)