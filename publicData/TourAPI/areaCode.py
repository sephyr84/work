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
csv_file = open('AreaCode.dat', "w")
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
	print item

	for key in item:

		if key == 'name':
			areaName = str(unicode(rawData['response']['body']['items']['item'][num][key]))
		elif key == 'code':
			areaCode = str(rawData['response']['body']['items']['item'][num][key])
		elif key == 'rnum':
			cw.writerow([areaCode, areaName])
