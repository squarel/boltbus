import requests
import pymongo
from datetime import date, timedelta
from bs4 import BeautifulSoup

# initial variables
stations = ['Boston South Station - Gate 9 NYC-Gate 10 NWK/PHL',
           'Philadelphia JFK & N. 30th St',
           'New York 34th and 8th by Tick Tock (Phil. or Bos.)',]

max_days = 7

client = MongoClient('localhost','20017')
db = client.boltbus
collection = db.shifts

# helper functions
def next_days(date, days):
    return date + timedelta(days=days)

def get_content(depart, dest, date):
    s = requests.session()
    s.get('https://www.boltbus.com')

    f = open('conf.txt', 'r')
    lines = f.readlines()
    post_data = {}
    for line in lines:
        strs = line.rstrip().rsplit(':')
        post_data[strs[0]] = strs[1]
    post_data['ctl00$cphM$forwardRouteUC$lstDestination$textBox'] = dest
    post_data['ctl00$cphM$forwardRouteUC$lstOrigin$textBox'] = depart
    post_data['ctl00$cphM$forwardRouteUC$txtDepartureDate'] = date
    r = s.post('https://www.boltbus.com', data=post_data)

    return r.content

def create_record(depart, dest, date, content):
    record = {}
    tickets = {}
    record['time']
    record['depart'] = depart
    record['dest'] = dest

    soup = BeautifulSoup(content)
    tickets['fare'] = soup.find_all('td','faresColumn0')
    tickets['start'] = soup.find_all('td','faresColumn1')
    tickets['end'] = soup.find_all('td','faresColumn2')



def create_records(depart, dest):
    # date
    today = date.today()
    flag = True
    next_day = 0
    while True:
        d = next_days(today, next_day)
        date_str = d.strftime('%m/%d/%y')
        content = get_content(depart, dest, date_str)
        next_day += 1


    for d in range(0, max_days + 1):






if __name__ == "__main__":
    for depart in stations:
        for dest in stations:
            if depart == dest:
                continue
            else:
                create_records(depart, dest)


