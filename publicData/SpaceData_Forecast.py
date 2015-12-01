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
nx = '59'
ny = '125'

REST = '&base_date=' + base_date + '&base_time=' + base_time + '&nx=' + nx + '&ny=' + ny
URL = EndpointUrl_ForecastSpaceData + '?ServiceKey=' + ServiceKey + REST +'&_type=json'
r = requests.get(URL)

rawData = json.loads(r.content)		
totalCount = rawData['response']['body']['totalCount']

baseData = rawData['response']['body']['items']['item']
print baseData[1]

category = unicodedata.normalize('NFKD', baseData[1]['category']).encode('ascii','ignore')
baseTime = unicodedata.normalize('NFKD', baseData[1]['baseTime']).encode('ascii','ignore')
nx = str(baseData[1]['nx'])
ny = str(baseData[1]['ny'])
fcstValue = str(baseData[1]['fcstValue'])
baseDate = str(baseData[1]['baseDate'])

print 'category = ' + category
print 'baseTime = ' + baseTime
print 'nx = ' + nx
print 'ny = ' + ny
print 'fcstValue = ' + fcstValue
print 'baseData = ' + baseDate

csv_file = open('SpaceData_Coordi.dat', "w")
cw = csv.writer(csv_file, delimiter = ',', quotechar = '|')

for i in range(1, x_range):
	for j in range(1, y_range):
		REST = '&base_date=' + base_date + '&base_time=' + base_time + '&nx=' + nx + '&ny=' + ny
		URL = EndpointUrl_ForecastSpaceData + '?ServiceKey=' + ServiceKey + REST +'&_type=json'
		r = requests.get(URL)

		rawData = json.loads(r.content)		
		totalCount = rawData['response']['body']['totalCount']
		baseData = rawData['response']['body']['items']['item']
		category = unicodedata.normalize('NFKD', baseData[1]['category']).encode('ascii','ignore')
		
		if category == 'PTY':
			if fcstValue != '-1':
				nx = str(i)
				ny = str(j)
				cw.writerow([nx, ny])

