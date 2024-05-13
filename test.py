import csv

with open('input_clients.csv') as file_obj: 
    #ignore header row
    heading = next(file_obj) 
    reader_obj = csv.reader(file_obj) 
    count = 0
    for row in reader_obj: 
        count += 1
        print(row[3])
        #print(row[2])
    print(count)