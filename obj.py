class Pizza:
    def __init__(self, piz_numb, ingrid_list):
        self.quantity = piz_numb
        self.ingridients = ingrid_list

    # returns the number of ingridients
    def getIngridNo(self):
        return len(self.ingridients)

    def isEmpty(self):
        return self.quantity == 0

    # reduce the quantity of pizzas
    def rdQntity(self):
        self.quantity -= 1

    # printable form of the object
    def __repr__(self):
        return f"pizza with {len(self.ingridients)}"


class Pizzeria:
    def __init__(self, file):
        import csv

        self.piz_lst = [] # list of pizzas available
        self.tm_lst = [] # list of teams
        self.ingrid_indx = {} # index system that shows an ingridient the pizzas they are in
        self.tp_no = 0 # total number of pizzas
        self.tm_no = {} # [0]: team of two, [1]: team of three, [2]: team of three

        # read file as csv
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=" ")
            r = 1
            for row in csv_reader:
                # r is added in the if
                # there is no need to increment it
                # after its usage there
                if r == 1:
                    for i in range(4):
                        if i == 0:
                            self.tp_no = int(row[i])
                        else:
                            self.tm_no[i+1] = int(row[i])
                    r += 1
                    continue
                # add pizza to the piz_lst
                self.piz_lst.append(Pizza(row[0], [i for i in row if not(row.index(i) == 0)]))
                # update ingrid_indx
                for ingrid in self.piz_lst[-1].ingridients:
                    if not(ingrid in self.ingrid_indx):
                        self.ingrid_indx[ingrid] = []
                    self.ingrid_indx[ingrid].append(len(self.piz_lst) - 1)
        # add team objects
        for n in self.tm_no.items():
            for i in range(n[1]):
                self.tm_lst.append(Team(n[0]))

    # returns number of
    # pizzas available
    def getPizNo(self):
        return self.tp_no

    # returns number of Teams
    # with the specified number of members
    def getTmNo(self, no):
        return self.tm_no[no]

    # select pizzas
    def slctPizz(self, pz_list, tm_list):
        # TODO WRITE RECURSIVE CODE HERE
        return

    # printable form of the object
    # created
    def __repr__(self):
        return f"""
        {self.getPizNo()} Pizzas,
        {self.tm_no[2]} team of 2,
        {self.tm_no[3]} team of 3,
        {self.tm_no[4]} team of 4
        """

class Team:
    def __init__(self, memb_no):
        self.memb_no = memb_no # number of members available team
        self.order_list = [] # list of team orders

    # gets the list of orders made by team
    def getOrders(self):
        return self.order_list

    # check if team order is empty
    def isOrdrEmpy(self):
        return bool(not(self.order_list))

    # check if the order list is full
    def isOrdrFull(self):
        return len(self.order_list) == self.memb_no

    # add a new order to the order list
    def setOrder(self, order):
        self.order_list.append(order)

    # printable form of the object
    def __repr__(self):
        return f"""Team of {self.memb_no} members created"""

if __name__ == "__main__":
    pizzeria = Pizzeria('a_example')
    print(pizzeria.ingrid_indx)
