class sellOrderNode:
    def __init__(self, time, order_id, instrument, quantity, client_id, price, buy_or_sell, client_rating, client_position_check):
        #time = int. * 60 and add or *60 * 60 and add
        #order_id = string
        #instrument = string
        #quantity = string
        #client_id = string
        #price = string. "Market" or decimal
        #buy_or_sell = string. "Buy" / "Sell"
        #client_rating = int
        #client_position_check = string "Y" / "N"
        self.time = time
        self.order_id = order_id
        self.instrument = instrument
        self.quantity = quantity
        self.client_id = client_id
        self.price = price
        self.buy_or_sell = buy_or_sell
        self.client_rating = client_rating
        self.client_position_check = client_position_check
    
    def __lt__(self, otherNode):
        #return true if self is smaller than otherNode (self should be popped first)
        #if both of these are market
        if self.price == "Market" and otherNode.price == "Market":
            #check client rating
            #if both ratings are the same
            if self.client_rating == otherNode.client_rating:
                #check order arrival time
                return self.time < otherNode.time
            else:
                #both ratings are different
                #client with higher rating has priority
                return self.client_rating > otherNode.client_rating
        else:
            #maybe one of them is market
            #if self is market
            if self.price == "Market":
                return True
            elif otherNode.price == "Market":
                return False 
            
            
            #both of them arent market
            if self.price == otherNode.price:
                #price is the same
                if self.client_rating == otherNode.client_rating:
                    #rating is the same
                    #check order arrival time
                    return self.time < otherNode.time
                else:
                #both ratings are different
                #client with higher rating has priority
                    return self.client_rating > otherNode.client_rating
            else:
                #prices are different
                #lower price has priority for sell
                return float(self.price) < float(self.price)
