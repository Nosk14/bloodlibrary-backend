import csv
import os

EXPANSIONS_CSV = 'D:/Projectes/bloodlibrary-backend/vtescards/data/vtessets_parsed.csv'

print("Working...")
expansions = set()
with open(EXPANSIONS_CSV, 'r') as csv_file:
    next(csv_file)
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        abbrv = row[0].split(':')[0].lower()
        expansions.add(abbrv)

print(expansions)

for expansion in expansions:
    os.mkdir("C:/Users/Carlos/Pictures/vtes/vtes cards organized/"+expansion)


print("Done!")