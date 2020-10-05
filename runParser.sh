rm *.dat
python parser.py ebay_data/items-*.json
sort items.dat | uniq 
sort users.dat | uniq 
sort categories.dat | uniq 
sort bids.dat | uniq 