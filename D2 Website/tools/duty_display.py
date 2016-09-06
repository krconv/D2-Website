
from __future__ import print_function
import httplib2
import os
import datetime

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'D2 Website'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
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
    return credentials

def name_on_duty():
    """
    Returns: the name and phone number of the RA that is on duty.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1uTsIJftqI_VyIVY-oFxwOJ9zsTGG4tBdkO1wHwEocp0'
    rangeName = 'Fall!A2:H'
    spreadsheet = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = spreadsheet.get('values', []) # contains all of the data
    today = '{dt.month}/{dt.day}/{dt.year}'.format(dt = datetime.datetime.now() - datetime.timedelta(hours=12))
    for i in range(0, len(values)):
        # go through each of the date rows until today is found
        if (len(values[i]) > 0): # not a padding row
            if ("Date" in values[i][0]):
                for j in range(1, len(values[i])):
                    if today in values[i][j]: # found todays schedule
                        data = values[i + 1][j].replace('(', '').replace(')', '').strip() # the duty data for daniels for today
                        result = { }
                        # parse todays duty for a phone number and name
                        if (len(data) == 0): # no one is on duty
                            result["name"] = "No RA On-Duty"
                            result["phone"] = "508-556-0494"
                        elif (data[-5] == "x"): # a singular person is on with a WPI phone
                            result["name"] = data[:-6]
                            result["phone"] = "508-831-" + data[-4:]
                        elif (len(data) > 12 and '-' in data[-12:]): # a singular person with a cell phone
                            result["name"] = data[:-13]
                            result["phone"] = data[-12:]
                        else: # multiple people 
                            result["name"] = data
                        return result
