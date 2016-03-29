# -*- coding: utf-8 -*-

import requests
import json
import unicodedata
import time
import csv
import sys
from datetime import datetime, timedelta

reload(sys)
sys.setdefaultencoding('utf-8')
#date define
dt = datetime.today()
td = timedelta(days = -1)
basedate = dt + td
basedate = basedate.date()
base_date = basedate.strftime("20%y%m%d")

#API parameters
EndpointUrl = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaCode'
ServiceKey = 'DXRmbbl57VC3IgCeGvBCirKXS%2Ba4klA0Qs3XDCRHHbWADxOb3z0y2LxAcagkTUIcpSepdS%2Fo8WstIxtUH8LLBQ%3D%3D'

areaCode = '0'
MobileOS = 'ETC'
MobileApp = 'AppTesting'

#operate

#csv file open
#csv_wfile = open('AreaCode_' + str(base_date) + '.dat', "w")
csv_file = open('SigunguCode.dat', "w")
cw = csv.writer(csv_file , delimiter=',', quotechar='|')

#GET totalCount : URL set => URL Request
REST = '&MobileOS=' + MobileOS + '&MobileApp=' + MobileApp
URL = EndpointUrl + '?ServiceKey=' + ServiceKey + REST +'&_type=json'

r = requests.get(URL)
rawData = json.loads(r.content)

numOfRows = str(rawData['response']['body']['totalCount'])

#GET Real Item : URL set => URL Request
REST = '&numOfRows=' + numOfRows + '&MobileOS=' + MobileOS + '&MobileApp=' + MobileApp
URL = EndpointUrl + '?ServiceKey=' + ServiceKey + REST +'&_type=json'

r = requests.get(URL)
rawData = json.loads(r.content)

#Real Item Variable Set
listOfitem = rawData['response']['body']['items']['item']
areaName = ''

#Json Item Cleansing
for num in range(len(listOfitem)):

	item = listOfitem[num]

	for key in item:

		if key == 'name':

			areaName = str(unicode(rawData['response']['body']['items']['item'][num][key]))
		
		
		if key == 'code':

			areaCode = str(rawData['response']['body']['items']['item'][num][key])
			
			REST = '&areaCode=' + areaCode + '&MobileOS=' + MobileOS + '&MobileApp=' + MobileApp
			URL = EndpointUrl + '?ServiceKey=' + ServiceKey + REST +'&_type=json'

			r = requests.get(URL)
			subrawData = json.loads(r.content)
			subnumOfRows = str(subrawData['response']['body']['totalCount'])

			REST = '&areaCode=' + areaCode + '&numOfRows=' + subnumOfRows + '&MobileOS=' + MobileOS + '&MobileApp=' + MobileApp
			URL = EndpointUrl + '?ServiceKey=' + ServiceKey + REST +'&_type=json'

			r = requests.get(URL)
			subrawData = json.loads(r.content)

			listOfSubItem = subrawData['response']['body']['items']['item']

		if (key == 'rnum' and subnumOfRows > '1'):
			for subnum in range(len(listOfSubItem)):

				subItem = listOfSubItem[subnum]

				for subkey in subItem:
					
					subValue = subItem[subkey]
					
					if subkey == 'name':
						subAreaName = str(unicode(subValue))
					elif subkey == 'code':
						subAreaCode = str(subValue)
					elif subkey == 'rnum':
						#print 'areaName : ' + areaName + ', rawData_1 : ' + areaCode + ', subAreaName : ' + subAreaName + ', subAreaCode : ' + subAreaCode
						cw.writerow([areaName, areaCode, subAreaName, subAreaCode])
						
		elif (key == 'rnum' and subnumOfRows == '1'):

			for subkey in listOfSubItem:

				subValue = listOfSubItem[subkey]

				if subkey == 'name':
					subAreaName = str(unicode(subValue))
				elif subkey == 'code':
					subAreaCode = str(subValue)
				elif subkey == 'rnum':
						#print 'areaName : ' + areaName + ', rawData_1 : ' + areaCode + ', subAreaName : ' + subAreaName + ', subAreaCode : ' + subAreaCode
					cw.writerow([areaName, areaCode, subAreaName, subAreaCode])
