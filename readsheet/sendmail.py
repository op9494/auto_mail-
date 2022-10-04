from cgi import print_arguments
import yagmail
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pandas as pd



sheet_id = "1uN98kvGDlZ0ALUirHPmFZh7sme0eV-DLiKLvITShtKg"# <Your spreadsheet ID>
sheet_name = "maildata"# <Your Sheet name>

#Get the sheet data using th google API
def get_google_sheet(spreadsheet_id, sheet_name):
    """ Retrieve sheet data using OAuth credentials and Google Python API. """
    scopes = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    # Setup the Sheets API
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', scopes)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    # Call the Sheets API
    gsheet = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=sheet_name).execute()
    print(gsheet)
    return gsheet

# converting the sheet data to data frame
def gsheet2df(gsheet):
    """ Converts Google sheet data to a Pandas DataFrame.
    Note: This script assumes that your data contains a header file on the first row!

    Also note that the Google API returns 'none' from empty cells - in order for the code
    below to work, you'll need to make sure your sheet doesn't contain empty cells,
    or update the code to account for such instances.

    """
    header = gsheet.get('values', [])[0]   # Assumes first line is header!
    values = gsheet.get('values', [])[1:]  # Everything else is data.
    if not values:
        return 'No data found.'
    else:
        all_data = []
        for col_id, col_name in enumerate(header):
            column_data = []
            for row in values:
                column_data.append(row[col_id])
            ds = pd.Series(data=column_data, name=col_name)
            all_data.append(ds)
        df = pd.concat(all_data, axis=1)
        return df

def get_csv_data():
    gsheet = get_google_sheet(sheet_id, sheet_name)
    dataframe = gsheet2df(gsheet)
    return dataframe




'''
Send email
'''
gmail_user = 'o.pradeep64@gmail.com'
gmail_password = '999469958Op*'
receiver_address = 'op@mail7.io'
#Setup the MIME

data= get_csv_data()
print(data.columns)
app_password = 'fekegdztqcmnchod' # a token for gmail
print(data.loc[0][0])



for sendemailcount in range(data.shape[0]):
    subject="test mail"
    content = 'HI Dude I am #Name# ,#Total#,#Count#'
    for field in range(data.shape[1]):
        if data.columns[field]=="To":
            to=data.loc[sendemailcount][field]    
        content = content.replace('#'+data.columns[field]+'#',data.loc[sendemailcount][field])
    with yagmail.SMTP(gmail_user, app_password) as yag:
        yag.send(to, subject, content)
        print('Sent email successfully')
        