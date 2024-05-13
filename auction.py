import csv
import heapq
from orderNode import orderNode
from buyOrderNode import buyOrderNode
from sellOrderNode import sellOrderNode
from collections import defaultdict

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


def auction():
    order_data = csv_to_ArrayDict("./filtered_orders_openauction.csv")

    # node = orderNode(time, order_id, instrument, quantity, client_id, price, buy_or_sell, client_rating, client_position_check)

    # loop through order_data and create orderNodes and put it inside a variable called orderBook

    client_holdings = defaultdict(lambda: defaultdict(int))

    instrument_dict= {}

    buyHeap = []
    sellHeap = []
    buyHeapMarket = []
    sellHeapMarket = []

    heapq.heapify(buyHeap)
    heapq.heapify(sellHeap)
    heapq.heapify(buyHeapMarket)
    heapq.heapify(sellHeapMarket)

    for order in order_data: 
        
        if order['Instrument'] not in instrument_dict: 
            instrument_dict[order['Instrument']] = {'buy_heap' :[], 'sell_heap':[], 'sell_market_heap':[], 'buy_market_heap':[]} 
            buy_heap = instrument_dict[order['Instrument']]['buy_heap'] 
            buy_market_heap = instrument_dict[order['Instrument']]['buy_market_heap'] 
            sell_heap = instrument_dict[order['Instrument']]['sell_heap'] 
            sell_market_heap = instrument_dict[order['Instrument']]['sell_market_heap'] 
            if order['Side'] == "Sell": 
                currObj = sellOrderNode(time_string_to_int(order['Time']), order['OrderID'], order['Instrument'], order['Quantity'], order['Client'], order['Price'], order['Side'], order['PositionCheck'], order['Rating']) 
                if order['Price'] == "Market": 
                    heapq.heappush(instrument_dict[order['Instrument']]['sell_market_heap'],currObj) 
                else: 
                    heapq.heappush(instrument_dict[order['Instrument']]['sell_heap'],currObj) 
        
                #sellorder workflow 
                    
        else: 
            currObj = buyOrderNode(time_string_to_int(order['Time']), order['OrderID'], order['Instrument'], order['Quantity'], order['Client'], order['Price'], order['Side'], order['PositionCheck'], order['Rating']) 
            
            if order['Price'] == "Market": 
                heapq.heappush(instrument_dict[order['Instrument']]['buy_market_heap'],currObj) 
            else: 
                heapq.heappush(instrument_dict[order['Instrument']]['buy_heap'],currObj) 
            
            #buyorder workflow

    # for order in order_data: 
        
    #     if order['Instrument'] not in instrument_dict: 
    #         instrument_dict[order['Instrument']] = {'buy_heap' :[], 'sell_heap':[], 'sell_market_heap':[], 'buy_market_heap':[]} 
    #         buy_heap = instrument_dict[order['Instrument']]['buy_heap'] 
    #         buy_market_heap = instrument_dict[order['Instrument']]['buy_market_heap'] 
    #         sell_heap = instrument_dict[order['Instrument']]['sell_heap'] 
    #         sell_market_heap = instrument_dict[order['Instrument']]['sell_market_heap'] 
    #     if order['Side'] == "Sell": 
    #         currObj = sellOrderNode(time_string_to_int(order['Time']), order['OrderID'], order['Instrument'], float(order['Quantity']), order['Client'], order['Price'], order['Side'], client_data[order['Client']]["Rating"], client_data[order['Client']]["PositionCheck"]) 
    #         if order["client_position_check"] == "Y":
    #             with open('./output_exchange_report.csv', 'a', newline="") as csvfile: 
    #                     # creating a csv writer object 
    #                     csvwriter = csv.writer(csvfile) 
    #                     myrows = [[currObj.order_id, 'REJECTED-POSITION CHECK FAILED']] 
    #                     csvwriter.writerows(myrows)
    #             continue
    #         if order['Price'] == "Market": 
    #             heapq.heappush(instrument_dict[order['Instrument']]['sell_market_heap'],currObj) 
    #         else: 
    #             heapq.heappush(instrument_dict[order['Instrument']]['sell_heap'],currObj) 
    
    #         #sellorder workflow 
                
    #     else: 
    #         currObj = buyOrderNode(time_string_to_int(order['Time']), order['OrderID'], order['Instrument'], float(order['Quantity']), order['Client'], order['Price'], order['Side'], client_data[order['Client']]["Rating"], client_data[order['Client']]["PositionCheck"]) 
            
    #         if order['Price'] == "Market": 
    #             heapq.heappush(instrument_dict[order['Instrument']]['buy_market_heap'],currObj) 
    #         else: 
    #             heapq.heappush(instrument_dict[order['Instrument']]['buy_heap'],currObj) 
            

    for key in instrument_dict.keys():

        temp = instrument_dict[key]

        # {'buy_heap' :[], 'sell_heap':[], 'sell_market_heap':[], 'buy_market_heap':[]} 

        buy_market_qty = 0
        sell_market_qty = 0
        
        bestqty = 0
        buyerMore = None
        bestprice = 0

        bestqtysell=0
        bestqtybuy=0

        bestpoppedbuy = None
        bestpoppedsell = None


        curr_sell_price = None

        buy_market_len = len(temp["buy_market_heap"])
        sell_market_len = len(temp["sell_market_heap"])
        buy_market_pointer = 0
        sell_market_pointer = 0

        while buy_market_pointer < buy_market_len:
            order = heapq.heappop(temp["buy_market_heap"])
            buy_market_qty += float(order.quantity)
            heapq.heappush(temp["buy_market_heap"], order)
            buy_market_pointer+=1

        while sell_market_pointer < sell_market_len:
            order = heapq.heappop(temp["sell_market_heap"])
            sell_market_qty += float(order.quantity)
            heapq.heappush(temp["sell_market_heap"], order)
            sell_market_pointer +=1

        # print(buy_market_qty, sell_market_qty, bestqty)

        # print(temp["buy_heap"])

        searching_flag = False
        popped_sells = []
        heapq.heapify(popped_sells)

        popped_buys = []
        heapq.heapify(popped_buys)

        curr_sell_qty = 0
        curr_buy_qty = 0

        while len(temp["sell_heap"]):
            
            curr_sell_qty = 0
            curr_buy_qty = 0

            # find the first sell limit order price
            if curr_sell_price == None:
                curr_sell_obj = heapq.heappop(temp["sell_heap"])
                # popped_sells.heappush(curr_sell_obj)
                heapq.heappush(popped_sells, curr_sell_obj)
                
                curr_sell_price = float(curr_sell_obj.price)
            
            else:
                searching_flag = True
                # find the next lowest price 
                while searching_flag:
                    curr_sell_obj = heapq.heappop(temp["sell_heap"])
                    heapq.heappush(popped_sells, curr_sell_obj)
                    if float(curr_sell_obj.price) > curr_sell_price:
                        curr_sell_price = float(curr_sell_obj.price)
                        searching_flag = False


            # search for all sells at this price
            searching_flag = True
            while searching_flag:
                if len(temp["sell_heap"]) ==0:
                    break
                curr_sell_obj = heapq.heappop(temp["sell_heap"])
                if float(curr_sell_obj.price) <= curr_sell_price:
                    heapq.heappush(popped_sells, curr_sell_obj)
                else:
                    searching_flag = False

            # get max sell qty at price 
            idx = 0
            while idx < len(popped_sells):
                currObj = heapq.heappop(popped_sells)
                curr_sell_qty += float(currObj.quantity)

                heapq.heappush(popped_sells, currObj)
                idx+=1
            
            # print(curr_sell_price)

            # get the buy qty eligible at this price
            searching_flag = True
            while searching_flag:
                if len(temp["buy_heap"]) ==0:
                    break
                curr_buy_obj = heapq.heappop(temp["buy_heap"])
                # print("curr obj", float(curr_buy_obj.price))

                if float(curr_buy_obj.price) >= curr_sell_price:
                    heapq.heappush(popped_buys, curr_buy_obj)
                    curr_buy_qty += float(curr_buy_obj.quantity)
                    # print(curr_buy_qty)

                
                else:
                    searching_flag = False
            
            while len(popped_buys) >0:
                heapq.heappush(temp["buy_heap"], heapq.heappop(popped_buys))

            curr_buy_qty +=buy_market_qty
            curr_sell_qty +=sell_market_qty

            
            if (bestqty < min(curr_buy_qty, curr_sell_qty)):
                bestprice = curr_sell_price
                bestqty = max(bestqty, min(curr_buy_qty, curr_sell_qty))
                bestqtybuy = curr_buy_qty
                bestqtysell = curr_sell_qty

                bestpoppedbuy = popped_buys
                bestpoppedsell = popped_sells

                if bestqtysell > bestqtybuy:
                    buyerMore = False
                else:
                    buyerMore = True


        print(key)
        print("best qty: ", bestqty)
        print("best price: ", bestprice)
        print("best buy qty: ", bestqtybuy)
        print("best sell qty: ", bestqtysell)

        totalqty = float(bestqty)


        while totalqty > 0 and len(temp["buy_market_heap"])>0 :
            node = heapq.heappop(temp["buy_market_heap"])
            float(node.quantity)
            node_qty = float(node.quantity)
            
            qty_traded = min(node_qty, totalqty)
            totalqty -= qty_traded

            node.quantity -= float(qty_traded)
            bestqtybuy -= float(qty_traded)

            if node.client_id not in client_holdings.keys():
                client_holdings[node.client_id] = {}
            
            if node.instrument not in client_holdings[node.client_id].keys():
                client_holdings[node.client_id][node.instrument] = 0
            
            client_holdings[node.client_id][node.instrument] += float(qty_traded)
            
            if node.quantity > 0:
                heapq.heappush(temp["buy_market_heap"], node)
                break
        
        totalqty = float(bestqty)

        while totalqty > 0 and len(temp["sell_market_heap"])>0:
            node = heapq.heappop(temp["sell_market_heap"])
            node_qty = float(node.quantity)
            
            qty_traded = min(float(node.quantity), totalqty)
            totalqty -= qty_traded

            node.quantity -= float(qty_traded)
            bestqtysell -= float(qty_traded)

            if node.client_id not in client_holdings.keys():
                client_holdings[node.client_id] = {}
            
            if node.instrument not in client_holdings[node.client_id].keys():
                client_holdings[node.client_id][node.instrument] = 0
            
            client_holdings[node.client_id][node.instrument] -= float(qty_traded)
            
            if node.quantity > 0:
                heapq.heappush(temp["sell_market_heap"], node)
                break

        if bestqtysell == 0.0 or bestqtybuy== 0.0:
            print ("Done")
        
        else:
            total_remaining = min (bestqtysell, bestqtybuy)

            totalqty = float(total_remaining)

            while totalqty > 0 and len(bestpoppedbuy)>0:
                node = heapq.heappop(bestpoppedbuy)
                float(node.quantity)
                node_qty = float(node.quantity)
                
                qty_traded = min(node_qty, totalqty)
                totalqty -= qty_traded

                node.quantity -= float(qty_traded)
                bestqtybuy -= float(qty_traded)

                if node.client_id not in client_holdings.keys():
                    client_holdings[node.client_id] = {}
                
                if node.instrument not in client_holdings[node.client_id].keys():
                    client_holdings[node.client_id][node.instrument] = 0
                
                client_holdings[node.client_id][node.instrument] += float(qty_traded)
                
                if node.quantity > 0:
                    heapq.heappush(bestpoppedbuy, node)
                    break
            
            totalqty = float(total_remaining)

            # while totalqty > 0 and len(temp["sell_heap"])>0:
            while totalqty > 0 and len(bestpoppedsell)>0:
                node = heapq.heappop(bestpoppedsell)
                node_qty = float(node.quantity)
                
                qty_traded = min(float(node.quantity), totalqty)
                totalqty -= qty_traded

                node.quantity -= float(qty_traded)
                bestqtysell -= float(qty_traded)

                if node.client_id not in client_holdings.keys():
                    client_holdings[node.client_id] = {}
                
                if node.instrument not in client_holdings[node.client_id].keys():
                    client_holdings[node.client_id][node.instrument] = 0
                
                client_holdings[node.client_id][node.instrument] -= float(qty_traded)
                
                if node.quantity > 0:
                    heapq.heappush(bestpoppedsell, node)
                    break
            

            while len(bestpoppedsell)>0:
                curr = heapq.heappop(bestpoppedsell)
                heapq.heappush(temp["sell_heap"], curr)
            while len(bestpoppedbuy)>0:
                curr = heapq.heappop(bestpoppedsell)
                heapq.heappush(temp["buy_heap"],curr)
            

        


            

        
        

        # if buyerMore:

            # while len(temp["buy_market_heap"]) >0:
                # current_market_buy = heapq.heappop(temp["buy_market_heap"])
                # bestqtybuy -= float(current_market_buy.quantity)

                # if current_market_buy.client_id not in client_holdings.keys():
                #     client_holdings[current_market_buy.client_id] = {}
                
                # if current_market_buy.instrument not in client_holdings[current_market_buy.client_id].keys():
                #     client_holdings[current_market_buy.client_id][current_market_buy.instrument] = 0
                
                # client_holdings[current_market_buy.client_id][current_market_buy.instrument] += float(current_market_buy.quantity)

            


            
            # while len(temp["sell_market_heap"]) >0:
            #     current_market_sell = heapq.heappop(temp["sell_market_heap"])
            #     bestqtysell -= float(current_market_sell.quantity)

            #     if current_market_sell.client_id not in client_holdings.keys():
            #         client_holdings[current_market_sell.client_id] = {}
                
            #     if current_market_sell.instrument not in client_holdings[current_market_sell.client_id].keys():
            #         client_holdings[current_market_sell.client_id][current_market_sell.instrument] = 0
                
            #     client_holdings[current_market_sell.client_id][current_market_sell.instrument] += float(current_market_sell.quantity)




        print("remaining buy qty: ", bestqtybuy)
        print("remaining sell qty: ", bestqtysell)

        # print(len(temp["sell_heap"]))
        # print(len(temp["buy_heap"]))

        print(client_holdings)
        print()

        return (client_holdings, instrument_dict)

    





    



