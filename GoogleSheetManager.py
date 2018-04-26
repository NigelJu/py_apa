from __future__ import print_function
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage



SCOPES = "https://www.googleapis.com/auth/spreadsheets"
CLIENT_SECRET_FILE = "client_secret.json"
APPLICATION_NAME = "GoogleSheet"
SPREAD_SHEET_ID = "1PF0sUjwA2JOlsIu-fvnK2lAopGTN9a6weiNuLtAMhIU"
SHEET_NAME = "SheetAPA!"
HOME_DIR = "/Users/Nigel/Desktop/Nigel/VSCode/APA"

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

def get_credentials():
    credential_dir = os.path.join(HOME_DIR, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-apa.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
def get_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    return service

def sheet_range(range_name):
    return SHEET_NAME + range_name

def write_data_with_range(values, range_name):
    rangeName = sheet_range(range_name)
    values = [values]
    body = {
    'values' : values,
    }
    service.spreadsheets().values().update(
    spreadsheetId = SPREAD_SHEET_ID, range = rangeName,
    valueInputOption = 'RAW', body = body).execute()

# test
def write_into_sheet(service):
    rangeName = sheet_range("A9")
    values = [
        [
            500,400,300,200,100,
        ],
    ]

    body = {
    'values' : values,
    }

    

    result = service.spreadsheets().values().update(
    spreadsheetId = SPREAD_SHEET_ID, range = rangeName,
    valueInputOption = 'RAW', body = body).execute()

def fetch_sheet():
    
    rangeName = sheet_range("A2:E")
    result = service.spreadsheets().values().get(
        spreadsheetId = SPREAD_SHEET_ID, range = rangeName).execute()
    values = result.get('values', [])

    print(values)
    """
    if not values:
        print('No data found.')
    else:
        print('Name, Gender, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s, %s' % (row[0], row[1] , row[4]))
    """



def main():
    # service = get_service()
    # write
    ###################
    # write_into_sheet(service)
    ##################
    # read
    # fetch_sheet(service)
    pass
    
    

service = get_service()
if __name__ == '__main__':
    main()
