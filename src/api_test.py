import csv
import json
import os
import requests
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, Timeout, HTTPError


# Load environment variables
load_dotenv()


API_KEY = os.getenv("API_KEY")
print("API key loaded:", API_KEY is not None)


# Read employees.csv

with open("data/employees.csv", "r", newline="") as file:
    reader = csv.DictReader(file)
    employees = list(reader)


# Save employees to JSON
with open("employees.json", "w") as file:
    json.dump(employees, file, indent=4)


# Filter high earners


high_earners = [
    emp for emp in employees
    if float(emp["salary"]) > 50000
]


with open("high_earners.csv", "w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=employees[0].keys()
    )
    writer.writeheader()
    writer.writerows(high_earners)


print("Rows read:", len(employees))
print("High earners:", len(high_earners))


# 3. Connect to API


url = "https://jsonplaceholder.typicode.com/users"


try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()


    users = response.json()


    print("\nAPI connection successful")


    # Print first 3 users
    for user in users[:3]:
        print(
            user["id"],
            "-",
            user["name"],
            "-",
            user["email"]
        )


    # Parse nested JSON using get()
    parsed_users = []


    for user in users:
        company = user.get("company", {})
        address = user.get("address", {})


        parsed_users.append({
            "id": user.get("id"),
            "name": user.get("name"),
            "email": user.get("email"),
            "city": address.get("city"),
            "company": company.get("name")
        })


    # Save parsed users
    with open("users.json", "w") as file:
        json.dump(parsed_users, file, indent=4)


except ConnectionError:
    print("Error: No internet connection")


except Timeout:
    print("Error: Request timed out")


except HTTPError as e:
    print("HTTP Error:", e)



# Test 404 error



try:
    error_url = "https://jsonplaceholder.typicode.com/users/9999"


    error_response = requests.get(error_url, timeout=5)


    if error_response.status_code == 404:
        print("/users/9999 -> 404 Not Found")
    else:
        print("Status code:", error_response.status_code)


except ConnectionError:
    print("Error: No internet connection")


except Timeout:
    print("Error: Request timed out")


except HTTPError as e:
    print("HTTP Error:", e)