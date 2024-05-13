import pandas as pd

# Specify the file path
orders_path = "/Users/marcel/Desktop/NUS/MOD MATERIALS/Y2STII/BofA Code to Connect/DataSets/example-set/input_orders.csv"
instruments_path = "/Users/marcel/Desktop/NUS/MOD MATERIALS/Y2STII/BofA Code to Connect/DataSets/example-set/input_instruments.csv"
clients_path = "/Users/marcel/Desktop/NUS/MOD MATERIALS/Y2STII/BofA Code to Connect/DataSets/example-set/input_clients.csv"

# Read the CSV file into a DataFrame
orders_df = pd.read_csv(orders_path)
instruments_df = pd.read_csv(instruments_path)
clients_df = pd.read_csv(clients_path)

# Initialise dictionaries for data query
instrument_currency_dict = {}
instrument_lotsize_dict = {}
client_currencies_dict = {}
client_position_check_dict = {}
client_rating_dict = {}

# Populate data query dictionaries
for index, row in instruments_df.iterrows():
    # Extract ID and value from the current row
    id = row['InstrumentID']
    curr = row['Currency']
    lotsize = row['LotSize']
    
    # Add the data to the dictionary
    instrument_currency_dict[id] = curr
    instrument_lotsize_dict[id] = lotsize

for index, row in clients_df.iterrows():
    # Extract ID and value from the current row
    id = row['ClientID']
    curr = row['Currencies']
    pos_check = row['PositionCheck']
    rating = row['Rating']
    
    # Add the data to the dictionary
    client_currencies_dict[id] = curr.split(",")
    client_position_check_dict[id] = pos_check
    client_rating_dict[id] = rating
    
# Output dataframes
filtered_orders_df = pd.DataFrame(columns=['Time', 'OrderID', 'Instrument', 'Quantity', 'Client', 'Price', 'Side', 'PositionCheck', 'Rating'])
exchange_report_df = pd.DataFrame(columns=['OrderID', 'RejectionReason'])

# Run Policy Checks #1, #2 and #3 on all orders
for index, row in orders_df.iterrows():
    # Extract variables
    time = row['Time']
    orderid = row['OrderID']
    instrument = row['Instrument']
    qty = row['Quantity']
    clientid = row['Client']
    price = row['Price']
    side = row['Side']
    pos_check = client_position_check_dict[clientid]
    rating = client_rating_dict[clientid]
    
    # Flag for valid drop
    drop = False
    
    # Check 1: Instrument Check
    if (instrument not in instrument_currency_dict.keys()):
        drop = True
        reject_reason = "REJECTED - INSTRUMENT NOT FOUND"       
        reject_row = {'OrderID': orderid, 'RejectionReason': reject_reason}
        exchange_report_df = exchange_report_df.append(reject_row, ignore_index=True)
        continue
    # Check 2: Currency Check
    elif (instrument_currency_dict[instrument] not in client_currencies_dict[clientid]):
        drop = True
        reject_reason = "REJECTED - MISMATCH CURRENCY"
        reject_row = {'OrderID': orderid, 'RejectionReason': reject_reason}
        exchange_report_df = exchange_report_df._append(reject_row, ignore_index=True)
        continue
    # Check 3: Lot Size Check
    elif (int(qty) % int(instrument_lotsize_dict[instrument]) != 0):
        drop = True
        reject_reason = "REJECTED - INVALID LOT SIZE"
        reject_row = {'OrderID': orderid, 'RejectionReason': reject_reason}
        exchange_report_df = exchange_report_df._append(reject_row, ignore_index=True)
        continue
    
    # Pass valid orders into new df
    if not drop:
        new_row = {'Time': time, 'OrderID': orderid, 'Instrument': instrument, 'Quantity': qty, 'Client': clientid, 'Price': price, 'Side': side, 'PositionCheck': pos_check, 'Rating': rating}
        filtered_orders_df = filtered_orders_df._append(new_row, ignore_index=True)
    

# Print exchange report
print(exchange_report_df)
# Print valid orders
print(filtered_orders_df)
# End of file
print("End of file")
