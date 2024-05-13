import heapq
import csv
#read in from open auction
buy_heap = []
sell_heap = []
buy_market_heap = []
sell_market_heap = []


#assume heaps have already been updated
with open('samplecsv.csv') as file_obj: 
    #ignore header row
    heading = next(file_obj) 
    reader_obj = csv.reader(file_obj) 
    for row in reader_obj: 
        time = time
        order_id = order_id
        instrument = instrument
        quantity = quantity
        client_id = client_id
        price = price
        buy_or_sell = buy_or_sell
        client_rating = client_rating
        client_position_check = client_position_check