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

#API parameters
EndpointUrl_ForecastGrib = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService/ForecastGrib'
ServiceKey = 'ssyoBDTCSe4RHaioipEsxKEecLycCh5MI4b5JWZ4swH9e1kAo%2BfLKpg0Rf3V26ISwnwfQQ7qG5T066pQIu%2BK9w%3D%3D'

#operate

#csv file open
csv_wfile = open('ForecastGribData_' + str(base_date) + '.dat', "w")

#base_time define
for h in range(0, 23, 3):
	basetime = "%02d" % h
	base_time = basetime + '00' #base_time is '0000, 0300, 0600, 0900, 1200, 1500, 1800, 2100'
	
	csv_rfile = open('coordinate.dat', 'rb')
	reader = csv.reader(csv_rfile)

	for row in reader:
		nx = row[0]
		ny = row[1]

		REST = '&base_date=' + base_date + '&base_time=' + base_time + '&nx=' + nx + '&ny=' + ny
		URL = EndpointUrl_ForecastGrib + '?ServiceKey=' + ServiceKey + REST +'&_type=json'
		r = requests.get(URL)
		rawData = json.loads(r.content)
		
		totalCount = rawData['response']['body']['totalCount']

		if totalCount == 0:
		    continue	
		else:
			baseData = rawData['response']['body']['items']['item']
		
		for k in range(0, totalCount):
				
			category = unicodedata.normalize('NFKD', baseData[k]['category']).encode('ascii','ignore')
			baseTime = unicodedata.normalize('NFKD', baseData[k]['baseTime']).encode('ascii','ignore')
			nx = str(baseData[k]['nx'])
			ny = str(baseData[k]['ny'])
			obsrValue = str(baseData[k]['obsrValue'])
			baseDate = str(baseData[k]['baseDate'])

			cw = csv.writer(csv_wfile, delimiter = ',', quotechar = '|')
			cw.writerow([category, baseTime, nx, ny, obsrValue, baseDate])