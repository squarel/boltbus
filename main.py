import requests
from bs4 import BeautifulSoup

s = requests.session()
s.get('https://www.boltbus.com')


def time_converter(time):
    pass

stations = ['Boston South Station - Gate 9 NYC-Gate 10 NWK/PHL',
           'Philadelphia JFK & N. 30th St',
           'New York 34th and 8th by Tick Tock (Phil. or Bos.)',]

f = open('conf.txt', 'r')
lines = f.readlines()
post_data = {}
for line in lines:
    strs = line.rstrip().rsplit(':')
    post_data[strs[0]] = strs[1]

post_data['ctl00$cphM$forwardRouteUC$lstDestination$textBox'] = stations[0]
post_data['ctl00$cphM$forwardRouteUC$lstOrigin$textBox'] = stations[1]
post_data['ctl00$cphM$forwardRouteUC$txtDepartureDate'] = '05/13/2013'


r = s.post('https://www.boltbus.com', data=post_data)
#print r.content
soup = BeautifulSoup(r.content)
price = soup.find_all('td','faresColumn0')
print price

