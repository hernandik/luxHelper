from struct import pack
import csv
from datetime import datetime
from PIL import Image

def Load_CSV():
    with open('/home/hernandi/Downloads/Chestnut_BV753.lux', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        rows=[r for r in spamreader]
    
    return rows[20:]

def ParseCSVDate(date_str):
    # current datetime format at lux file
    # ['DD/MM/YYYY HH:MM:SS', 'light(lux)'
    # ['11/01/2020 00:09:04', '98.793']

    formater = "%d/%m/%Y %H:%M:%S"
    parsedDateTime = datetime.strptime(date_str, formater).timestamp()
    # print(parsedDateTime)
    return parsedDateTime

def ParseLuxInfo(lux):
    return float(lux)

def DetectSamplingsPerDay(rows):
    # count the number of samples per day
    # generate a histogram
    days_histogram = []
    days_histogram.append(0)
    day_index = 0
    last_day = datetime.fromtimestamp(ParseCSVDate(rows[0][0])).day
    for row in rows:

        date_timestamp = ParseCSVDate(row[0])
        # print(datetime.fromtimestamp(date_timestamp).day)
        day = datetime.fromtimestamp(date_timestamp).day

        if day != last_day:
            # start count on the next day
            day_index = day_index + 1
            last_day = day
            days_histogram.append(0)
        
        days_histogram[day_index] = days_histogram[day_index] + 1

    # list results
    # for day in days_histogram:
    #     print(day)

    return days_histogram

def main():
    rows = Load_CSV()
    # print(rows[0])
    # dt = ParseCSVDate(rows[0][0])
    # lux = ParseLuxInfo(rows[0][1])
    days_histogram = DetectSamplingsPerDay(rows)
    # this will be used to define the max size of the heigth image
    max_samples_per_day = max(days_histogram)
    total_samples_days = len(days_histogram)

    print(max_samples_per_day, total_samples_days)

    img = Image.new( 'RGB', (total_samples_days,max_samples_per_day), "black") # create a new black image
    pixels = img.load()

    col = 0
    lin = 0
    i = 0
    for row in rows:
        lux = int(ParseLuxInfo(row[1]))
        # print (i, j)
        pixels[col,lin] = (lux,lux,lux)
        
        i = i + 1
        lin = lin + 1
        #if lin >= max_samples_per_day:
        if lin >= days_histogram[col]:
            lin = 0
            col = col + 1
            if col > total_samples_days:
                raise Exception("max number {} column exceded expected {}".format(col, total_samples_days))
                #col = total_samples_days
    img.save("test2.bmp")


if __name__ == '__main__':
    main()
