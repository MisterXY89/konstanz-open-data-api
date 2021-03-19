from API import get_data

test = get_data(["Geo"], tag=True)
kinder = "Kindertagesbetreuung - Einrichtungen csv"
print(test[kinder])
