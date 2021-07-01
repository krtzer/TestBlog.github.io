import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

class gs_interface:
    def __init__(self, workbook):
        self.BASEURL = 'https://www.mtgstocks.com/prints/'
        # https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
        # https://github.com/burnash/gspread/issues/513
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open(workbook).sheet1
        self.sheets_df = pd.DataFrame(self.sheet.get_all_records())          

if __name__ == "__main__":
    my_gs = gs_interface("Vintage-Cube-Kurt-Edition")
    print (my_gs.sheets_df)

