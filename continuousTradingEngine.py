import heapq
import csv
#read in from open auction
buy_heap = []
sell_heap = []
buy_market_heap = []
sell_market_heap = []


#assume heaps have already been updated

def csv_to_ArrayDict(filename):
    with open(filename, mode='r') as infile:
        reader = csv.DictReader(infile)
        data = [row for row in reader]
    return data

def csv_to_dict(filename):
    with open(filename, mode='r') as infile:
        reader = csv.DictReader(infile)
        data = {row[next(iter(reader.fieldnames))]: {key: value for key, value in row.items() if key != next(iter(reader.fieldnames))} for row in reader}
    return data
order_data = csv_to_ArrayDict('./test-set/input_orders.csv')
print(order_data)

def time_string_to_int(time_string):
    #input "9:02:43" output: time
    split_arr = time_string.split(":")
    final_time = 0
    final_time += int(split_arr[0]) * 60 * 60
    final_time += int(split_arr[1]) * 60
    final_time += int(split_arr[2])
    return final_time

for order in order_data:
    if order['Side'] == "Sell":
        currObj = orderNode(order['Time'], order['OrderID'], order['Instrument'], order['Quantity'], order['Client'], order['Price'], order['Side'], client_data[order['Client']]["Rating"], client_data[order['Client']]["PositionCheck"])
        if order['Price'] == "Market":
            sell_market_heap.append(currObj)
        else:
            sell_heap.append(currObj)
    else:
        currObj = orderNode(order['Time'], order['OrderID'], order['Instrument'], order['Quantity'], order['Client'], order['Price'], order['Side'], client_data[order['Client']]["Rating"], client_data[order['Client']]["PositionCheck"])
        
        if order['Price'] == "Market":
            buy_market_heap.append(currObj)
        else:
            buy_heap.append(currObj)


    for row in reader_obj: 
        time = row[0]
        order_id = order_id
        instrument = instrument
        quantity = quantity
        client_id = client_id
        price = price
        buy_or_sell = buy_or_sell
        client_rating = client_rating
        client_position_check = client_position_check