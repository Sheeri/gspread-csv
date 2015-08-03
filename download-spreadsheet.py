import csv
import gspread
import urllib
import codecs
from config import config
import json
from oauth2client.client import SignedJwtAssertionCredentials

#config
docs = config['DOCS']

# open the json file with the oath2 credentials
json_key = json.load(open('oauth2_credentials.json'))
scope = ['https://spreadsheets.google.com/feeds']

# login first
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)

client = gspread.authorize(credentials)

#process doc list
for doc in docs:
    spreadsheet = client.open(doc["doc"])
    for i, worksheet in enumerate(spreadsheet.worksheets()):
        filename = path + doc["doc"] + '-worksheet' + str(i) + '.csv'
        with open(filename, 'wb') as f:
            writer = csv.writer(f)
            content = worksheet.get_all_values()
            for row in content:
                new_row=[]
                for record in row:
                    record=record.encode('utf8')
                    new_row.append(record)
                try:
                    writer.writerow(new_row)
                except (UnicodeEncodeError, UnicodeDecodeError):
                    print "Caught unicode error"
    print '== Finished Writing: ' + filename + ' =='
print '====== FINISHED ======'
