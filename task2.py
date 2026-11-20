import csv
import json
import os
import requests
from dotenv import load_dotenv
from requests.exceptions import ( ConnectionError,Timeout,HTTPError)

# Load environment variables:

load_dotenv()

API_KEY = os.getenv("API_KEY")

print("API key loaded:", API_KEY is not None)

# Employee Data:

with open("data/employees.csv","r")as file:
    reader = csv.DictReader(file)
    employees = list(reader)

# Employees.json:

with open("employees.json","w") as file:
    json.dump(employees, file, indent = 4)

# filter High Earners:

high_earners = [ emp for emp in employees
                if int (emp["salary"]) > 50000 ]

# High Earners.csv:

with open("high_earners.csv","w", newline="") as file:
    writer = csv.DictWriter( file, fieldnames=["id", "name", "department", "salary", "city"])
    writer.writeheader
    writer.writerows(high_earners)
    print("Rows read:", len(employees))
    print("High Earners:", len(high_earners))

    
# 4. API Connection

url = "https://jsonplaceholder.typicode.com/users"


try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()


    users = response.json()


    print("\nAPI connection successful")
    print("Total users:", len(users))


    # Print first 3 users
    print("\nFirst 3 users:")


    for user in users[:3]:
        print(
            user.get("id"),
            "-",
            user.get("name"),
            "-",
            user.get("email")
        )

   
    # 5. Parse Nested JSON


    parsed_users = []


    for user in users:
        address = user.get("address", {})
        geo = address.get("geo", {})


        parsed_users.append({
            "id": user.get("id"),
            "name": user.get("name"),
            "email": user.get("email"),
            "city": address.get("city"),
            "latitude": geo.get("lat"),
            "longitude": geo.get("lng")
        })


    # Save nested JSON
    with open("users.json", "w") as file:
        json.dump(parsed_users, file, indent=4)


    print("\nNested JSON saved to users.json")


except ConnectionError:
    print("Error: No internet connection")


except Timeout:
    print("Error: Request timed out")


except HTTPError as e:
    print("HTTP Error:", e)



# 6. Test 404 Error


print("\nTesting 404 error:")


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