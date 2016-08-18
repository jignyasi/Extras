import networkx as nx

class TicketGenerator:
    
    def __init__(self):
        self.statCodes, self.G = self.data()
        self.newTicket = False
        self.entryString = "Enter Source Station Code: \n"
        self.exitString = "Enter Destination Station Code: \n"
        self.newTickString = "Do you Require another Ticket [y/n]?: \n"
        
    def replace(self, L_in, old_v, new_v):
        while old_v in L_in:
            idx=L_in.index(old_v)
            L_in.pop(idx)
            L_in.insert(idx, new_v)
        return L_in

    def data(self):
        statCodes = {'C3': 'Survey of India', 'B16': 'Falaknuma', 'B14': 'Shamsher Gunj', 'B15': 'Jungametta', 'B12': 'Charminar', 'B13': 'Shalibanda', 'B11': 'Salarjung Museum', 'C13': 'Begumpet', 'A3': 'KPHB Colony', 'C11': 'Rasool Pura', 'C10': 'Paradise', 'C17': 'Road No 5 Jubilee Hills', 'C16': 'Yusuf Guda', 'C15': 'Madhura Nagar', 'A15': 'Lakdikapul', 'A14': 'Khairatabad', 'A17': 'Nampally', 'A16': 'Assembly', 'A10': 'S R Nagar', 'A13': 'Irrum Manzil', 'A12': 'Punjagutta', 'C8': 'Secunderabad', 'A19': 'Osmania Medical College', 'A18': 'Gandhi Bhavan', 'A2': 'JNTU College', 'A5': 'Balanagar', 'A1': 'Miyapur', 'A7': 'Bharat Nagar', 'A6': 'Moosapet', 'X2': 'M G Bus Station', 'A8': 'Erragadda', 'C1': 'Nagole', 'X1': 'Ameerpet', 'C7': 'Mettuguda', 'C6': 'Tarnaka', 'C5': 'Habsiguda', 'A4': 'Kukatpally', 'C22': 'HITEC City', 'C23': 'Shilparamam', 'C20': 'Madhapur', 'C21': 'Durgam Chervu', 'A9': 'ESI Hospital', 'X3': 'Parade Grounds', 'C2': 'Uppal', 'C12': 'Prakash Nagar', 'A21': 'Malakpet', 'A22': 'New Market', 'A23': 'Musarambagh', 'A24': 'Dilsukhnagar', 'A25': 'Chaitanyapuri', 'A26': 'Victoria Memorial', 'A27': 'L B Nagar', 'C18': 'Jubilee Hills Check Post', 'C19': 'Pedamma Temple ', 'B4': 'Gandhi Hospital', 'B5': 'Musheerabad', 'B6': 'RTC Cross Roads', 'B7': 'Chikkadpally', 'B1': 'JBS', 'B3': 'Secunderabad', 'C4': 'NGRI', 'B8': 'Narayanguda', 'B9': 'Sultan Bazar'}

        line1 = map(( lambda x: 'A' + str(x)), range(1,28))
        line2 = map(( lambda x: 'B' + str(x)), range(1,17))
        line3 = map(( lambda x: 'C' + str(x)), range(1,24))

        line1 = self.replace(self.replace(line1,'A11','X1'),'A20','X2')
        line2 = self.replace(self.replace(line2,'B2','X3'),'B10','X2')
        line3 = self.replace(self.replace(line3,'C14','X1'),'C9','X3')

        edge1 = zip(line1[:-1],line1[1:])
        edge2 = zip(line2[:-1],line2[1:])
        edge3 = zip(line3[:-1],line3[1:])

        edge1 = [(x,y,{'weight':2.5}) for x,y in edge1]
        edge2 = [(x,y,{'weight':2.0}) for x,y in edge2]
        edge3 = [(x,y,{'weight':3.0}) for x,y in edge3]

        G=nx.Graph()
        G.add_edges_from(edge1)
        G.add_edges_from(edge2)
        G.add_edges_from(edge3)

        return statCodes, G
               
    def pathNprice(self, source, dest):
        path = nx.shortest_path(self.G,source,dest)
        if len(path) > 4:
            price = sum([self.G[x][y]['weight'] for x,y in zip(path[3:-1],path[4:])]) + 10.0
        else:
            price = 10.0

        return path, price

    def capture_input(self, isSource, source = None):
        if self.newTicket:
            err = "Invalid entry"
            choice = raw_input(self.newTickString)
            if choice in ['y','n']:
                self.newTicket = False
                return choice
            else:
                print err
                return self.capture_input(True)
        else:
            err = "Invalid Station Code"
            src = raw_input(self.entryString) if isSource else source
            if src in self.statCodes.keys():
                dest = raw_input(self.exitString)
                if dest in self.statCodes.keys() and dest != src:
                    return src, dest
                else:
                    err = "Destination and Source can't be same" if dest == src else err
                    print err
                    return self.capture_input(False, src)
            else:
                print err
                return self.capture_input(True)
    
    def UI(self, source, dest, path, price):
        print '*'*61
        print '\t'*3,'Hyderabad Metro Rail'
        print "Source:\t\t{}\t\tDistance ( stations): {}".format(self.statCodes[source],len(path)-1)
        print "Destination:\t{}\t\tCost:\t Rs.{}/-".format(self.statCodes[dest],price)
        print '*'*61

    def interface(self):
        src, dest = self.capture_input(True)
        path, price = tg.pathNprice(src,dest)
        self.UI(src, dest, path, price)
        self.newTicket = True
        choice = self.capture_input(True)
        if choice == 'y':
            self.interface()
        
if __name__ == '__main__':
    tg = TicketGenerator()
    tg.interface()
