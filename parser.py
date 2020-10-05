
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

def toString(string):
    quote = "\""
    formatted = quote + string.replace(quote, quote+quote) + quote
    return formatted

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        itemFile = open("items.dat", "a")
        userFile = open("users.dat", "a")
        categoryFile = open("categories.dat", "a")
        bidFile = open("bids.dat", "a")
        seperator = str("|")
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """

            buyPrice = "NULL"
            if "Buy_Price" in list(item.keys()):
                buyPrice = transformDollar(item["Buy_Price"])

            #transform start, end, current bid & first bid into right format
            currently = transformDollar(item["Currently"])
            startTime = transformDttm(item["Started"])
            endTime = transformDttm(item["Ends"])
            firstBid = transformDollar(item["First_Bid"])

            seller = item["Seller"]

            # add item information to items.dat
            itemFile.write(item["ItemID"] + seperator + toString(item["Name"]) + seperator
            +  currently + seperator + buyPrice + seperator
            + firstBid + seperator + item["Number_of_Bids"] + seperator 
            + startTime + seperator  + endTime + seperator + toString(str(item["Description"])) 
            + seperator + seller["UserID"] + "\n")
            
            #add categories & userIds to categories.dat
            for category in item["Category"]:
                categoryFile.write(item["ItemID"] + seperator + toString(category) + "\n")

            #add seller info to 'users'
            userFile.write(toString(seller["UserID"]) + seperator + item["ItemID"] + seperator
            + seller["Rating"] + seperator + toString(item["Location"]) + seperator + toString(item["Country"] )
            + "\n")

            #iterate through 'bids'
            if (item["Bids"] is not None):
                for bid in item["Bids"]:
                    bidInfo = bid["Bid"]
                    bidder = bidInfo["Bidder"]
                    amount = transformDollar(bidInfo["Amount"])
                    time = transformDttm(bidInfo["Time"])
                    location = "NULL"
                    country = "NULL"
                    #Check Location & Country for null values
                    if "Location" in bidder.keys() :
                        location = bidder["Location"]
                    if "Country" in bidder.keys():
                        country = bidder["Country"]
                    bidFile.write(toString(bidder["UserID"]) + seperator + item["ItemID"] + seperator 
                    + amount + seperator + time + "\n") 
                    userFile.write(toString(bidder["UserID"]) + seperator + item["ItemID"] + seperator
                    + bidder["Rating"] + seperator + toString(location) + seperator 
                    + toString(country) + "\n") 
            
            pass

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)
