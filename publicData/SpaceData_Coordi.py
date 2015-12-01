import requests
import json
import unicodedata
import time
import csv
import sys
from datetime import datetime, timedelta

#date define
dt = datetime.today()
td = timedelta(days = -1)
basedate = dt + td
basedate = basedate.date()
base_date = basedate.strftime("20%y%m%d")

x_range = 149
y_range = 253

#API parameters
EndpointUrl_ForecastSpaceData = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService/ForecastSpaceData'
ServiceKey = 'ssyoBDTCSe4RHaioipEsxKEecLycCh5MI4b5JWZ4swH9e1kAo%2BfLKpg0Rf3V26ISwnwfQQ7qG5T066pQIu%2BK9w%3D%3D'

#sample Variables
base_time = '0500'

csv_file = open('SpaceData_Coordi.dat', "w")
cw = csv.writer(csv_file, delimiter = ',', quotechar = '|')

for i in range(1, x_range):
	for j in range(1, y_range):
		nx = str(i)
		ny = str(j)
		REST = '&base_date=' + base_date + '&base_time=' + base_time + '&nx=' + nx + '&ny=' + ny
		URL = EndpointUrl_ForecastSpaceData + '?ServiceKey=' + ServiceKey + REST +'&_type=json'
		r = requests.get(URL)

		rawData = json.loads(r.content)		
		totalCount = rawData['response']['body']['totalCount']
		baseData = rawData['response']['body']['items']['item']
		category = unicodedata.normalize('NFKD', baseData[1]['category']).encode('ascii','ignore')
		
		if category == 'PTY':
			if fcstValue != '-1':
				cw.writerow([nx, ny])

