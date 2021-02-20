import csv
import operator

# object Pizza
class Pizza:
    # attributes for pizza
    # number available
    # toppings
    def __init__(self, numb, toppings):
        self.numb = numb
        self.toppings = toppings

    def __repr__(self):
        return f'{self.numb},{self.toppings}'

# array containing important info
# [0] contains pizza_number
# [1:3] contains team values for teams
info =[0,0,0,0]

# array containing info
# about available pizzas
pizza_arr = []

with open('a_example') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = " ")
    count = 0
    for row in csv_reader:
        if count == 0:
            i = count
            while i < 4 in row:
                info[i] = col
                i += 1
        else:
            # create a pizza object and add it to the list of pizzas
            pizza_arr.append(Pizza(row[0], [i for i in row if not(row.index(i) == 0)]))
        count += 1
