from query import query


address = input("Enter the Address of the Property: ")
city = input("Enter the City the property is in: ")
state = input("Enter the State the property is in: ")
debug = input("Print record? (Y/N): ")
debug = True if debug.lower() == "y" else False
res = query(f"{address}, {city}, {state}", debug)

if res is not None:
  print(f'Cost {res["Price"]}')
  print(f'{res["Rooms"]} rooms')
  print(f'{res["Baths"]} baths')
  print(f'{res["SqFt"]} square feet')
  for school in res["Schools"]:
            print(
                " ".join(
                    [
                        school["Name"],
                        f'({school["Type"]}, {school["Level"]})',
                        "rated",
                        str(school["Rating"]),
                        "out of 10 at a distance of",
                        str(school["Distance"]),
                        "miles.",
                    ]
                )
            )

