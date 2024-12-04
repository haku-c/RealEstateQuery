from query import query


address = input("Enter the Address of the Property: ")
city = input("Enter the City the property is in: ")
state = input("Enter the State the property is in: ")

query(f"{address}, {city}, {state}")
