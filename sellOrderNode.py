class sellOrderNode:
    def __init__(self, time, order_id, instrument, quantity, client_id, price, buy_or_sell, client_rating, client_position_check):
        #time = int. * 60 and add or *60 * 60 and add
        #order_id = string
        #instrument = string
        #quantity = string
        #client_id = string
        #price = float
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
        
