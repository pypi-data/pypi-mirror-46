import csv

class Polaris():

    def __init__(self, type, *args):

        if type=='read_csv':

            def order(list, dict_key, reverse=False):
                res = sorted(list, key = lambda i: i[dict_key], reverse=reverse)
                return Polaris('order_csv', {'res':res})

            self.data = args[0]['list']
            self.order_by = lambda a, descending=False : order(args[0]['list'], a, descending)

        if type=='order_csv':

            def order(list, dict_key, reverse=False):
                res = sorted(list, key = lambda i: i[dict_key], reverse=reverse)
                return Polaris('order_csv', {'list':list})

            self.data = args[0]['res']


    def read_csv(path):
        list = []

        with open(path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                list.append(dict(row))

        csvfile.close()
        data = Polaris('read_csv', {'list':list})
        return data