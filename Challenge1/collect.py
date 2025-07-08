import requests
import csv
import os

def collect_contacts(access_token: str, output_path: str = "../Challenge2/contact_collection.csv"):
    url = "https://api.hubapi.com/crm/v3/objects/contacts/search"
    all_contacts = []
    has_more = True
    after = None

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    properties = [
        "firstname", "lastname", "country", "phone", "training___create_date",
        "industry", "address", "checkbox", "raw_email_id", "hs_object_id"
    ]

    data = {
        "filterGroups": [
            {
                "filters": [
                    {
                        "propertyName": "allowed_to_collect",
                        "operator": "EQ",
                        "value": "true"
                    }
                ]
            }
        ],
        "properties": properties,
        "limit": 100,
        "after": 0
    }

    while has_more:
        if after:
            data["after"] = after
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        for contact in result.get("results", []):
            row = {prop: contact["properties"].get(prop, "") for prop in properties}
            all_contacts.append(row)
        after = result.get("paging", {}).get("next", {}).get("after")
        has_more = after is not None

    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_path, mode="w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=properties)
        writer.writeheader()
        writer.writerows(all_contacts)
    print(f"Collected {len(all_contacts)} contacts and saved to {output_path}")

if __name__ == "__main__":
    access_token = ""
    output_path = "../Challenge2/contact_collection.csv"
    collect_contacts(access_token, output_path)
