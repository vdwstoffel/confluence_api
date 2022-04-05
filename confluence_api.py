import requests
import json
import base64

class ConfluenceApi:
    def __init__(self, base_url: str, email:str, api_key:str):
        self.base_url = base_url
        self.email = email
        self.api_key = api_key

        # Transform the email:api to a base 64 encoded string
        auth = f"{self.email}:{self.api_key}"
        encoded_auth = auth.encode("ascii")
        base64_bytes = base64.b64encode(encoded_auth)
        self.base64_string = base64_bytes.decode("ascii")


    def create_page(self, page_name: str, space_key: str):
        """Creates a new page on confluence"""
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.base64_string}"
        }

        payload = json.dumps( {
            "title": page_name,
            "type": "page",
            "space": {
                "key": space_key
                },
            "status": "current",
            "body": {
                "storage": {
                    "value": "<h1> Test content </h1>",
                    "representation": "storage"
                    }
                }
            } 
        )

        response = requests.post(self.base_url + "/wiki/rest/api/content", data=payload, headers=headers)
        response.raise_for_status()
        feedback = response.json()
        print(f"{page_name} created")


    def get_page_version(self, page_name: str):
        """Gets the page version and return it + 1"""
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.base64_string}"
        }

        params =  {
            "title": page_name,
            "expand": "version"
            } 

        response = requests.get(self.base_url + "/wiki/rest/api/content", params=params, headers=headers)
        response.raise_for_status()
        data= response.json()
        return data["results"][0]["version"]["number"]


    def edit_page(self, id: int, page_name: str, version_number: int, template_file):
        """Edit's a page on confluence. A counter needs to be kept of the version otherwise an error will be thrown. Should implement a try/except"""
        with open(template_file) as f:
            template = f.read()

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.base64_string}"
        }

        payload = json.dumps({
            "version": {
                "number": version_number
                },
            "title": page_name,
            "type": "page",
            "body": {
                "storage": {
                    "value": template,
                    "representation": "storage"
                    }
                }
            }
        )

        response = requests.put(self.base_url + f"/wiki/rest/api/content/{id}", data=payload, headers=headers)
        response.raise_for_status()
        feedback = response.json()
        print(f"{page_name} edited")


    def create_atachment(self, filepath: str, id: int):
        """Add an attachment to the page"""
        headers = {
            'X-Atlassian-Token': 'nocheck',
            "Authorization": f"Basic {self.base64_string}"
        }

        files = {
            'file': (filepath, open(filepath, 'rb')),
        }

        response = requests.put(self.base_url + f"/wiki/rest/api/content/{id}/child/attachment", headers=headers, files=files)
        response.raise_for_status()
        feedback = response.json()
        print("File added to page")
