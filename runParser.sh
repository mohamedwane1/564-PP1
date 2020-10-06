rm *.dat
python parser.py ebay_data/items-*.json
sort -u items.dat -o items2.dat
sort -u users.dat -o users2.dat
sort -u categories.dat -o categories2.dat
sort -u bids.dat  -o bids2.dat