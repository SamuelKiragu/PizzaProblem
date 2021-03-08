class FileReader:
    def __init__(self):
        print("created file reader")

    # reads the data in the file
    def read(self,file):
        import csv
        tp_no = 0 #total number of pizzas
        tm_no = {} # team array [0]
        piz_lst = []
        tm_lst = []
        ingrid_indx = {}

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
                            tp_no = int(row[i])
                        else:
                            tm_no[i+1] = int(row[i])
                    r += 1
                    continue
                # add pizza to the piz_lst
                piz_lst.append(Pizza(row[0], [i for i in row if not(row.index(i) == 0)]))
                # update ingrid_indx
                for ingrid in piz_lst[-1].ingridients:
                    if not(ingrid in ingrid_indx):
                        ingrid_indx[ingrid] = []
                    ingrid_indx[ingrid].append(len(piz_lst) - 1)
        # add team objects
        for n in tm_no.items():
            for i in range(n[1]):
                tm_lst.append(Team(n[0]))
        print("SUCCESS: READ FILE!")
        return piz_lst, tm_lst, ingrid_indx, tp_no, tm_no

    # outputs the resultant data
    def write(self, tm_lst):
        with open('output.txt', 'w+') as output:
            output.write(f"{len(tm_lst)}\n")
            for team in tm_lst[:]:
                output.write(str(f"{len(team.order_list)} ")+"".join([str(el)+" " for el in team.order_list]))
                # output.write(strlen.join([str(el)+" " for el in team.order_list]))
                output.write("\n")

class Pizza:
    counter = 0
    def __init__(self, piz_numb, ingrid_list):
        self.id = Pizza.counter
        self.quantity = piz_numb
        self.ingridients = ingrid_list
        Pizza.counter += 1
    # returns the number of ingridients
    def getIngridNo(self):
        return len(self.ingridients)

    def isEmpty(self):
        return self.quantity == 0

    # restart counter
    def rsetC():
        Pizza.counter = 0

    # reduce the quantity of pizzas
    def rdQntity(self):
        self.quantity -= 1

    # printable form of the object
    def __repr__(self):
        return f"pizza with id {self.id}"

class Pizzeria:
    def __init__(self, file):
        Pizza.rsetC()
        data = FileReader().read(file)
        self.piz_lst = data[0] # list of pizzas available
        self.tm_lst = []
        self.ingrid_indx = data[2] # index system that shows an ingridient the pizzas they are in
        self.tp_no = data[3] # total number of pizzas
        self.tm_no = data[4] # [2]: team of two, [3]: team of three, [4]: team of four

    # calculates heuristics
    def calc_h(self,srted_piz,aw_arr,piz_list):
        import operator

        # if true calculate heuristics,h
        # calculate and use heuristics to select pizza
        # equation x(s_a/b_a) against y(o_p/s_a)
        # slope equation: y = 0.5x

        # array to hold pizzas sorted
        # with heuristics
        h1 = []
        for i in srted_piz:
            s_a = len(next(item for item in self.piz_lst if item.id == i.id).ingridients) #value of initial small array
            b_a = len(aw_arr[1]) #value of initial big array
            o_p = len(i.ingridients) #value of current array

            # in order to be accepted,
            # value, v should be greater than y
            x = s_a/b_a
            y = 0.5 * x
            v = o_p/s_a
            h1.append([i, v, v >= y])
        # print(sorted(h1, reverse=True, key=operator.itemgetter(1)))
        s_h = sorted(h1, reverse=True, key=operator.itemgetter(1))

        for i in s_h[:]:
            if i[2]:
                for ingrid in i[0].ingridients[:]:
                    aw_arr[1].append(ingrid)
                aw_arr[0].append(i[0].id)
                # pop ingridients
                self.popIngrid(i[0].ingridients,piz_list)
                return

    # check for available pizzas and deliver
    # to teams with capacity
    def deliverPiz(self):
        import copy
        cpPizzeria = copy.deepcopy(self)

        # awaiting order
        aw_arr = self.slctPizz(cpPizzeria.piz_lst, [[],[]])
        tm_len = len(aw_arr)

        print(aw_arr)

        if len(aw_arr) == 0 or len(aw_arr) == 1:
            print("PROGRAM COMPLETED EXECUTION !")
            FileReader().write(self.tm_lst)
            return

        # add new team to list
        # update number of teams
        self.tm_lst.append(Team(tm_len,aw_arr))
        self.tm_no[tm_len] -= 1

        # removing used elements
        for piz_id in aw_arr[:]:
            self.piz_lst = [piz for piz in self.piz_lst if not(piz.id == piz_id)]
            cpPizzeria.piz_lst = [piz for piz in self.piz_lst if not(piz.id == piz_id)]


        return self.deliverPiz()

    # returns number of
    # pizzas available
    def getPizNo(self):
        return self.tp_no

    # returns number of Teams
    # with the specified number of members
    def getTmNo(self, no):
        return self.tm_no[no]

    # pop ingridients
    # already in the list
    def popIngrid(self, piz_ingrid, piz_list):
        # pop items from remaining pizzas

        for ingrid in piz_ingrid.copy():
            arr = self.ingrid_indx[ingrid]
            for indx in arr:
                # print(f"removing {ingrid} from {indx}")
                item = next((item for item in piz_list if item.id == indx), None)
                if not(item ==  None):
                    item.ingridients.remove(ingrid)

    # select pizzas
    def slctPizz(self, piz_list, aw_arr=[[],[]], count = 1):
        import operator
        # sort pizzas according to the ingridients
        # descending order
        if len(piz_list) == 0:
            # check if ingridients are over
            # if so, checks if order is full
            # if order is full it is returned
            # otherwise it returns [], since no teams can be filled
            if count == 3 and self.tm_no[3] > 0:
                return aw_arr[0]
            elif count == 2 and self.tm_no[2] > 0:
                return aw_arr[0]
            return []

        srted_piz = sorted(piz_list, reverse=True, key=operator.attrgetter('ingridients'))

        if len(aw_arr[1]) == 0:
            for ingrid in srted_piz[0].ingridients:
                aw_arr[1].append(ingrid)
            aw_arr[0].append(srted_piz[0].id)
        else:
            self.calc_h(srted_piz, aw_arr, piz_list)
        # pop ingridients
        self.popIngrid(srted_piz[0].ingridients,piz_list.copy())
        # print(aw_arr)

        srted_piz = sorted(piz_list, reverse=True, key=operator.attrgetter('ingridients'))

        # check if maximum number of pizzas in a team has been reached
        if count == 4 and self.tm_no[4] > 0:
            return aw_arr[0]

        count += 1
        return self.slctPizz(piz_list,aw_arr, count)

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
    def __init__(self, memb_no, ord_lst = []):
        self.memb_no = memb_no # number of members available team
        self.order_list = ord_lst # list of team orders

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
    import sys
    file = str(sys.argv[1])
    pizzeria = Pizzeria(file)
    pizzeria.deliverPiz()
