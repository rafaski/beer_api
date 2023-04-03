data = [
  {
    "ID": "13",
    "CITY": "Phoenix"
  },
  {
    "ID": "44",
    "CITY": "Denver"
  },
  {
    "ID": "66",
    "CITY": "Caribou"
  }
]

my_dict = {}

for entry in data:
    my_dict[entry["CITY"]] = entry["ID"]

print(my_dict)

data_2 = [
  {
    "CITY": "Phoenix",
    "ANIMAL": "Dog"
  },
  {
    "CITY": "Caribou",
    "ANIMAL": "Cat"
  }
]

for entry in data_2:
    if entry["CITY"] in my_dict.keys():
        entry["ID"] = my_dict[entry["CITY"]]


print(data_2)
