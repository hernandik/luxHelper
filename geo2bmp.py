import csv
from datetime import datetime
from PIL import Image
import argparse
import os.path

def Load_CSV(luxFilename):
    with open(luxFilename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        rows=[r for r in spamreader]
    
    return rows[20:]

def Load_CSV_Headers(luxFilename):
    with open(luxFilename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        rows=[r for r in spamreader]
    
    return rows[:20]

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

def Lux2BMP(luxFilename, outBitmap):
    rows = Load_CSV(luxFilename)
    days_histogram = DetectSamplingsPerDay(rows)
    # this will be used to define the max size of the heigth image
    max_samples_per_day = max(days_histogram)
    total_samples_days = len(days_histogram)

    print("Maximium samples per day found: ", max_samples_per_day)
    print("Total days found: ", total_samples_days)

    img = Image.new( 'RGB', (total_samples_days,max_samples_per_day), "black") # create a new black image
    pixels = img.load()

    col = 0
    lin = 0

    for row in rows:
        lux = int(ParseLuxInfo(row[1]))
        pixels[col,lin] = (lux,lux,lux)

        lin = lin + 1
        #if lin >= max_samples_per_day:
        if lin >= days_histogram[col]:
            lin = 0
            col = col + 1
            if col > total_samples_days:
                raise Exception("max number {} column exceded expected {}".format(col, total_samples_days))
                #col = total_samples_days
    img.save(outBitmap)

def BMP2Lux(bmpFile, refLuxFile, final_lux_filename):
    rows = Load_CSV(refLuxFile)
    days_histogram = DetectSamplingsPerDay(rows)
    # this will be used to define the max size of the heigth image
    max_samples_per_day = max(days_histogram)
    total_samples_days = len(days_histogram)

    print("Maximium samples per day found: ", max_samples_per_day)
    print("Total days found: ", total_samples_days)

    # check that the bmpFile has the sabe width and height that the refLuxFile has
    
    with Image.open(bmpFile) as im:
        if im.width != total_samples_days:
            raise Exception("Bitmap witdh does not correspont to original number of days at the lux file")
        if im.height != max_samples_per_day:
            raise Exception("Bitmap height does not correspont to original number max of samples per day at the lux file")

        rgb_im = im.convert('RGB')
        outLuxDate = []

        col = 0
        lin = 0

        for row in rows:
            # pixels[col,lin] = (lux,lux,lux)
            r, g, b = rgb_im.getpixel((col, lin))
            date = row[0]
            outLuxDate.append([date, (r+g+b)/3])

            lin = lin + 1

            if lin >= days_histogram[col]:
                lin = 0
                col = col + 1
                if col > total_samples_days:
                    raise Exception("max number {} column exceded expected {}".format(col, total_samples_days))

        print("redLux valid rows ", len(rows), " Bitmap rows count ", len(outLuxDate))
        #print(outLuxDate)

        with open(final_lux_filename, mode='w') as csvfile:
            
            headers = Load_CSV_Headers(refLuxFile)
            writer = csv.writer(csvfile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            print (headers)

            for row in headers:
                writer.writerow(row)

            for row in outLuxDate:
                writer.writerow(row)


def ExtractFileName(file_location):
    return os.path.basename(file_location)

def main():

    parser = argparse.ArgumentParser(description="Geo to BMP help adjusting lux files by the use of of bitmap edition tools")

    subparsers = parser.add_subparsers(dest='mode',
                                   help='Enter the mode: "lux2bmp" or "bmp2lux"')

    list_parser = subparsers.add_parser('lux2bmp',
                                    help='Use this parameter to convert a lux file to bitmap to edit in a ourside program')

    list_parser.add_argument('--luxFile', type=str, action='store', required=True,
                        help='name of the lux file to conver to bmp')
    
    list_parser1 = subparsers.add_parser('bmp2lux',
                                    help='Use this parameter to convert a bitmap back to lux')

    list_parser1.add_argument('--bmpFile', type=str, action='store',required=True,
                        help='name of the bmp file to convert back to lux')

    list_parser1.add_argument('--refLuxFile', type=str, action='store',required=True,
                        help='Reference lux file to copy the base data. The same file used during lux2bmp')

    args = parser.parse_args()

    if not args.mode:
        parser.print_help()
        parser.exit(1)

    if args.mode == 'lux2bmp':

        if os.path.isfile(args.luxFile):
            print ("File luxFile exist")
        else:
            print ("File luxFile {} not exist".format(args.luxFile))
            exit(1)

        bmp_filename = "{}.bmp".format(ExtractFileName(args.luxFile))
        Lux2BMP(args.luxFile, bmp_filename)
        print("Successully generated bmp file with name: {}".format(bmp_filename))

    elif args.mode == 'bmp2lux':

        if os.path.isfile(args.bmpFile):
            print ("File bmpFile exist")
        else:
            print ("File bmpFile {} not exist".format(args.bmpFile))
            exit(1)

        if os.path.isfile(args.refLuxFile):
            print ("File refLuxFile exist")
        else:
            print ("File refLuxFile {} not exist".format(args.refLuxFile))
            exit(1)
        
        final_lux_filename = "{}.lux".format(ExtractFileName(args.bmpFile))
        BMP2Lux(args.bmpFile, args.refLuxFile, final_lux_filename)

if __name__ == '__main__':
    main()
