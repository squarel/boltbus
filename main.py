import requests
from pymongo import MongoClient
from datetime import date, timedelta
from bs4 import BeautifulSoup

# initial variables
stations = ['Boston South Station - Gate 9 NYC-Gate 10 NWK/PHL',
           'New York 34th and 8th by Tick Tock (Phil. or Bos.)',
           'Philadelphia JFK & N. 30th St']

max_days = 7

client = MongoClient('localhost', 27017)
db = client.boltbus
collection = db.shifts

# helper functions
def next_days(date, days):
    return date + timedelta(days=days)

def get_content(depart, dest, date):
    s = requests.session()
    r = s.get('https://www.boltbus.com')

    f = open('conf2.txt', 'r')
    lines = f.readlines()
    post_data = {}
    for line in lines:
        strs = line.rstrip().rsplit(':')
        post_data[strs[0]] = strs[1]


    soup = BeautifulSoup(r.content)
    event_validation = soup.find('input',id='__EVENTVALIDATION')
    post_data['__EVENTVALIDATION'] = event_validation.attrs['value']
    viewstate = soup.find('input',id='__VIEWSTATE')
    post_data['__VIEWSTATE'] = viewstate.attrs['value']
    #toolkit = soup.find('input',id='ctl00_toolkitScriptManager_HiddenField')
    post_data['ctl00_toolkitScriptManager_HiddenField'] = ';;AjaxControlToolkit, Version=1.0.20229.20821, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en-US:c5c982cc-4942-4683-9b48-c2c58277700f:e2e86ef9:1df13a87;;AjaxControlToolkit, Version=1.0.20229.20821, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en-US:c5c982cc-4942-4683-9b48-c2c58277700f:c4c00916:9ea3f0e2:9e8e87e9:4c9865be:ba594826:c76f1358:182913ba:bae32fb7:8ccd9c1b:3858419b:96741c43:c7c04611:cd120801:38ec41c0:a6a5a927;'

    post_data['ctl00$cphM$forwardRouteUC$lstDestination$textBox'] = dest
    post_data['ctl00$cphM$forwardRouteUC$lstOrigin$textBox'] = depart
    post_data['ctl00$cphM$forwardRouteUC$txtDepartureDate'] = date
    r = s.post('https://www.boltbus.com/Default.aspx', data=post_data, allow_redirects=True)
    #print post_data['__EVENTVALIDATION']
    #print s.cookies

    #f2 = open('page.html','w')
    #f2.write(r.content)

    return r.content

def create_record(depart, dest, date, content):
    record = {}
    tickets = []
    record['date'] = date.strftime('%m/%d/%y')
    record['depart'] = depart
    record['dest'] = dest

    soup = BeautifulSoup(content)
    fares = soup.find_all('td','faresColumn0')
    starts =  soup.find_all('td','faresColumn1')
    ends = soup.find_all('td','faresColumn2')
    for i in range(len(fares)):
        ticket = {}
        ticket['fare'] = fares[i].getText().strip()
        ticket['start'] = starts[i].getText().strip()
        ticket['ends'] = ends[i].getText().strip()
        tickets.append(ticket)
    record['tickets'] = tickets

    print record

def have_content(content):
    soup = BeautifulSoup(content)
    fare = soup.find_all('td','faresColumn0')
    if fare == []:
        return False
    else:
        return True


def create_records(depart, dest):
    # date
    today = date.today()
    crawl_flag = True
    next_day = 0
    no_days = 0
    while crawl_flag:
        d = next_days(today, next_day)
        date_str = d.strftime('%m/%d/%y')
        content = get_content(depart, dest, date_str)
        if have_content(content):
            create_record(depart, dest, d, content)
            no_days = 0
        else:
            no_days += 1
            print "no_days:" + str(no_days)
        next_day += 1
        if no_days >= max_days:
            break


if __name__ == "__main__":
    for depart in stations:
        for dest in stations:
            if depart == dest:
                continue
            else:
                create_records(depart, dest)


