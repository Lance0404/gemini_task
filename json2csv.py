import json
import csv


# format
# {'timestamp': '2019-04-01T14:51:39.690-0700', 'user': 'USER085', 'action': 'failed', 'app': 'app_1', 'server': 'SERVER03.gemini.datalab'}


infile = 'data/firewall.json'
# infile = open('data/firewall.json', 'r')
outfile = open('data/firewall.csv', 'w')
writer = csv.writer(outfile)

header = ['timestamp', 'user', 'action', 'app', 'server']
writer.writerow(header)

with open(infile) as fp:
    for i, line in enumerate(fp):
        # print(i, line)
        data = json.loads(line)
        row = []
        for i in header:
            row.append(data[i])
        writer.writerow(row)
