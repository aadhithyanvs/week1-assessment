def bonus(salary, rate=0.1, *extras, **options):
    result = salary * rate
    for extra in extras:
        result = result + extra
    if "cap" in options: 
        result = min(result, options["cap"])
    return result


#custom Exception:

class InvalidSalaryError(Exception):
    pass

# Employee Class:

class Employee:
    def __init__(self, name, salary):

        if salary < 0:
            raise InvalidSalaryError(f"Invalid salary: {salary}")
        
        self.name = name
        self.salary = salary
    def annual_salary(self):
        return self.salary * 12
    def get_details(self):
        return f"Employee: {self.name}, Salary: {self.salary}"

# Manager Class from Employee:

class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size
    def get_details(self):
        return f"Manager: {self.name}, Salary: {self.salary}, Team Size: {self.team_size}"

# Employee Object:

emp1 = Employee("Rahul",60000)


# Manager Object:

mgr1 = Manager("Priya",45000,5)

print(mgr1.get_details())

# Exception Handling:
 
try:
    emp2 = Employee("Test", -500)

except InvalidSalaryError as e:
    print(f"Error: {e}")

finally:
    print("Transction finished")

 # Employee data:

employees = [ 
               {"name": "Arun",    "salary": 30000, "city":"Chennai"},
               {"name": "Priya",   "salary": 45000, "city":"Chennai"},
               {"name": "Rahul",   "salary": 60000, "city":"Bangalore"},
               {"name": "Divya",   "salary": 75000, "city":"Chennai"},
               {"name": "Karthik", "salary": 90000, "city":"Mumbai"},
               {"name": "Meena",   "salary": 52000, "city":"Bangalore"},
               {"name": "Suresh",  "salary": 68000, "city":"Chennai"},
               {"name": "Anitha",  "salary": 48000, "city":"Mumbai"}
               ]

# List Comprehension:

above_50000 = [emp["name"] for emp in employees if emp["salary"] > 50000]

print("Above 50000:", above_50000)

# Map and Lambda to add a 10% raise:
raised_salaries = list(map(lambda emp: emp["salary"] * 1.10, employees))


# Filter to keep Chennai employees:

chennai_employees =list(filter(lambda emp: emp["city"] == "Chennai", employees))

print("Chennai:", [emp["name"] for emp in chennai_employees])

# For Loop:
for emp in employees:
    salary = emp["salary"]

    if salary == 0:
        continue

    if salary > 85000:
        
        break
