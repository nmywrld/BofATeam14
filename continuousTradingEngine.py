import heapq
import csv
from collections import defaultdict
from buyOrderNode import buyOrderNode
from sellOrderNode import sellOrderNode
from auction import auction, auction2
#read in from open auction
#instrument dict maps instruments to the 4 heaps


#assume heaps have already been updated
#TODO

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


def time_string_to_int(time_string):
    #input "9:02:43" output: time
    split_arr = time_string.split(":")
    final_time = 0
    final_time += int(split_arr[0]) * 60 * 60
    final_time += int(split_arr[1]) * 60
    final_time += int(split_arr[2])
    return final_time

def engine(client_dict, instrument_dict):
    order_data = csv_to_ArrayDict('./hong_testing/filtered_orders_continuoustrading.csv')
    #client dict is a default dict. read in from open auction? but prolly dn
    for order in order_data:
        if order['Time'] == "16:00:00":
            break
        # print(order)
        # break
        # print("Pritning order number")
        # print(count)
        # count+= 1
        if order['Instrument'] not in instrument_dict:
            instrument_dict[order['Instrument']] = {'buy_heap' :[], 'sell_heap':[], 'sell_market_heap':[], 'buy_market_heap':[]}
        buy_heap = instrument_dict[order['Instrument']]['buy_heap']
        buy_market_heap = instrument_dict[order['Instrument']]['buy_market_heap']
        sell_heap = instrument_dict[order['Instrument']]['sell_heap']
        sell_market_heap = instrument_dict[order['Instrument']]['sell_market_heap']
        if order['Side'] == "Sell":
            #HAVE TO CHECK BALANCE!! TODO
            currObj = sellOrderNode(time_string_to_int(order['Time']), order['OrderID'], order['Instrument'], float(order['Quantity']), order['Client'], order['Price'], order['Side'], order['PositionCheck'], int(order['Rating']))
            #if currObj.client_position_check == 'Y':
                #print(1)
            #checking balance
            if client_dict[currObj.client_id][currObj.instrument] < currObj.quantity and currObj.client_position_check == 'Y':
                #order is invalid
                #OUTPUT!! TODO
                #print(7237287827737321)
                with open('./hong_testing/output_exchange_report.csv', 'a', newline="") as csvfile:
                    # creating a csv writer object
                    csvwriter = csv.writer(csvfile)
                    myrows = [[currObj.order_id, 'REJECTED-POSITION CHECK FAILED']]
                    csvwriter.writerows(myrows)
                continue

            #sellorder workflow

            #split into 2 branches
            if currObj.price == "Market":
                #this is a market sell order
                while currObj.quantity >0:
                    #there are no limit buyorders
                    if len(buy_heap) == 0:
                        break

                    #there is a valid buy order                        
                    #no need to check if there is market
                    
                    
                    #Pop highest limit order and satisfy it
                    if True:
                        buy_node = heapq.heappop(buy_heap)
                        quantity_executed = min(float(currObj.quantity), float(buy_node.quantity))
                        currObj.quantity -= quantity_executed
                        buy_node.quantity -= quantity_executed
                        client_dict[currObj.client_id][currObj.instrument] -= quantity_executed
                        client_dict[buy_node.client_id][currObj.instrument] += quantity_executed
                        if buy_node.quantity != 0:
                            #buy node got leftover
                            heapq.heappush(buy_heap, buy_node)
                        else:       
                            #buy  node no more leftover
                            pass
                        with open('./hong_testing/transactions.csv', 'a', newline="") as csvfile:
                            # creating a csv writer object
                            csvwriter = csv.writer(csvfile)
                            myrows = [[currObj.instrument, quantity_executed, buy_node.price]]
                            csvwriter.writerows(myrows)

                        #ORDER HAS EXECUTED
                        continue
            else:
                #this is a limit sell order
                while currObj.quantity >0:
                    #there are no buyorders
                    if len(buy_heap) == 0 and len(buy_market_heap) == 0:
                        break
                    
                    #there are no market, and the limit buy is less than sell
                    if len(buy_market_heap) == 0 and float(buy_heap[0].price) < float(currObj.price):
                        break

                    #there is a valid buy order                        
                    #check if there is market
                    if len(buy_market_heap) != 0:
                        #there is a market order. this takes priority
                        buy_market_node = heapq.heappop(buy_market_heap)
                        quantity_executed = min(currObj.quantity, buy_market_node.quantity)
                        currObj.quantity -= quantity_executed
                        buy_market_node.quantity -= quantity_executed
                        client_dict[currObj.client_id][currObj.instrument] -= quantity_executed
                        client_dict[buy_market_node.client_id][currObj.instrument] += quantity_executed
                        with open('./hong_testing/transactions.csv', 'a', newline="") as csvfile:
                            # creating a csv writer object
                            csvwriter = csv.writer(csvfile)
                            myrows = [[currObj.instrument, quantity_executed, currObj.price]]
                            csvwriter.writerows(myrows)
                        if buy_market_node.quantity != 0:
                            #buymarket node got leftover
                            heapq.heappush(buy_market_heap, buy_market_node)
                        else:       
                            #buy market node no more leftover
                            pass

                        #ORDER HAS EXECUTED
                        continue
                    
                    #no market orders to execute with. look at limit
                    if float(buy_heap[0].price) >= float(currObj.price):
                        buy_node = heapq.heappop(buy_heap)
                        quantity_executed = min(currObj.quantity, buy_node.quantity)
                        currObj.quantity -= quantity_executed
                        buy_node.quantity -= quantity_executed
                        client_dict[currObj.client_id][currObj.instrument] -= quantity_executed
                        client_dict[buy_node.client_id][currObj.instrument] += quantity_executed
                        with open('./hong_testing/transactions.csv', 'a', newline="") as csvfile:
                            # creating a csv writer object
                            csvwriter = csv.writer(csvfile)
                            myrows = [[currObj.instrument, quantity_executed, buy_node.price]]
                            csvwriter.writerows(myrows)
                        if buy_node.quantity != 0:
                            #buy node got leftover
                            heapq.heappush(buy_heap, buy_node)
                        else:       
                            #buy  node no more leftover
                            pass

                        #ORDER HAS EXECUTED
                        continue
            #broke out of while loop. nothing can satisfy this. add to heap
            if currObj.quantity != 0:
                if order['Price'] == "Market":
                    heapq.heappush(instrument_dict[order['Instrument']]['sell_market_heap'],currObj)
                    
                else:
                    heapq.heappush(instrument_dict[order['Instrument']]['sell_heap'],currObj)
                    
                    

        else:
            #this is a buy
            currObj = buyOrderNode(time_string_to_int(order['Time']), order['OrderID'], order['Instrument'], float(order['Quantity']), order['Client'], order['Price'], order['Side'], order['PositionCheck'], int(order['Rating']))
            #no need to check balance 

            #buyorder workflow
            #split into 2 branches
            if currObj.price == "Market":
                #this is a market buy order
                while currObj.quantity >0:
                    #there are no limit selllorders
                    if len(sell_heap) == 0:
                        break
                    #there is a valid sell order                        
                    #no need to check if there is market
                    #Pop highest limit order and satisfy it
                    if True:
                        sell_node = heapq.heappop(sell_heap)
                        quantity_executed = min(currObj.quantity, sell_node.quantity)
                        currObj.quantity -= quantity_executed
                        sell_node.quantity -= quantity_executed
                        client_dict[currObj.client_id][currObj.instrument] += quantity_executed
                        client_dict[sell_node.client_id][currObj.instrument] -= quantity_executed
                        with open('./hong_testing/transactions.csv', 'a', newline="") as csvfile:
                            # creating a csv writer object
                            csvwriter = csv.writer(csvfile)
                            myrows = [[currObj.instrument, quantity_executed, sell_node.price]]
                            csvwriter.writerows(myrows)
                        if sell_node.quantity != 0:
                            #sell node got leftover
                            heapq.heappush(sell_heap, sell_node)
                        else:       
                            #sell  node no more leftover
                            pass

                        #ORDER HAS EXECUTED
                        continue
            else:
                #this is a limit buy order
                while currObj.quantity >0:
                    #there are no sell orders
                    if len(sell_heap) == 0 and len(sell_market_heap) == 0:
                        break
                    
                    #there are no market, and the limit sell is greater than this buy order
                    if len(sell_market_heap) == 0 and float(sell_heap[0].price) > float(currObj.price):
                        break

                    #there is a valid sell order                        
                    #check if there is market
                    if len(sell_market_heap) != 0:
                        #there is a market order. this takes priority
                        sell_market_node = heapq.heappop(sell_market_heap)
                        quantity_executed = min(currObj.quantity, sell_market_node.quantity)
                        currObj.quantity -= quantity_executed
                        sell_market_node.quantity -= quantity_executed
                        client_dict[currObj.client_id][currObj.instrument] += quantity_executed
                        client_dict[sell_market_node.client_id][currObj.instrument] -= quantity_executed
                        with open('./hong_testing/transactions.csv', 'a', newline="") as csvfile:
                            # creating a csv writer object
                            csvwriter = csv.writer(csvfile)
                            myrows = [[currObj.instrument, quantity_executed, currObj.price]]
                            csvwriter.writerows(myrows)
                        if sell_market_node.quantity != 0:
                            #buymarket node got leftover
                            heapq.heappush(sell_market_heap, sell_market_node)
                        else:       
                            #buy market node no more leftover
                            pass

                        #ORDER HAS EXECUTED
                        continue
                    
                    #no market orders to execute with. look at limit
                    if float(sell_heap[0].price) <= float(currObj.price):
                        sell_node = heapq.heappop(sell_heap)
                        quantity_executed = min(currObj.quantity, sell_node.quantity)
                        currObj.quantity -= quantity_executed
                        sell_node.quantity -= quantity_executed
                        client_dict[currObj.client_id][currObj.instrument] += quantity_executed
                        client_dict[sell_node.client_id][currObj.instrument] -= quantity_executed
                        with open('./hong_testing/transactions.csv', 'a', newline="") as csvfile:
                            # creating a csv writer object
                            csvwriter = csv.writer(csvfile)
                            myrows = [[currObj.instrument, quantity_executed, sell_node.price]]
                            csvwriter.writerows(myrows)
                        if sell_node.quantity != 0:
                            #sell node got leftover
                            heapq.heappush(sell_heap, sell_node)
                        else:       
                            #sell  node no more leftover
                            pass

                        #ORDER HAS EXECUTED
                        continue
            #broke out of while loop. nothing can satisfy this. add to heap
            if currObj.quantity != 0:
                if order['Price'] == "Market":
                    heapq.heappush(instrument_dict[order['Instrument']]['buy_market_heap'],currObj)
                    
                else:
                    heapq.heappush(instrument_dict[order['Instrument']]['buy_heap'],currObj)

    return (client_dict, instrument_dict)

a = auction()
client_dict, instrument_dict = a[0], a[1]
a =engine(client_dict, instrument_dict)
client_dict, instrument_dict = a[0], a[1]
auction2(client_dict, instrument_dict)