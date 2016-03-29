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

def getTotalNum(url):
	r = requests.get(URL)
	rawData = json.loads(r.content)

	numOfRows = str(rawData['response']['body']['totalCount'])
	return numOfRows

#date define
dt = datetime.today()
td = timedelta(days = -1)
basedate = dt + td
basedate = basedate.date()
base_date = basedate.strftime("20%y%m%d")

#API parameters
EndpointUrl = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/categoryCode'
ServiceKey = 'DXRmbbl57VC3IgCeGvBCirKXS%2Ba4klA0Qs3XDCRHHbWADxOb3z0y2LxAcagkTUIcpSepdS%2Fo8WstIxtUH8LLBQ%3D%3D'

areaCode = '0'
MobileOS = 'ETC'
MobileApp = 'AppTesting'
contentTypeId = {'관광지' : '12', '문화시설' : '14', '축제/공연/행사' : '15', '여행코스' : '25',
				 '레포츠' : '28', '숙박' : '32', '쇼핑' : '38', '음식' : '39'}

csv_file_cat1 = open('Cat1Code.dat', "w")
cwCat1 = csv.writer(csv_file_cat1 , delimiter=',', quotechar='|')

csv_file_cat2 = open('Cat2Code.dat', "w")
cwCat2 = csv.writer(csv_file_cat2 , delimiter=',', quotechar='|')

csv_file_cat3 = open('Cat3Code.dat', "w")
cwCat3 = csv.writer(csv_file_cat3 , delimiter=',', quotechar='|')


#GET totalCount : URL set => URL Request
REST = '&MobileOS=' + MobileOS + '&MobileApp=' + MobileApp
URL = EndpointUrl + '?ServiceKey=' + ServiceKey + REST +'&_type=json'

r = requests.get(URL)
rawData = json.loads(r.content)
numOfRows = getTotalNum(URL)

#GET Real Item : URL set => URL Request
REST = '&numOfRows=' + numOfRows + '&MobileOS=' + MobileOS + '&MobileApp=' + MobileApp
URL = EndpointUrl + '?ServiceKey=' + ServiceKey + REST +'&_type=json'

r = requests.get(URL)
rawData = json.loads(r.content)

#Real Item Variable Set
listOfitem = rawData['response']['body']['items']['item']

cat1code = ''
cat1name = ''
cat2code = ''
cat2name = ''
cat3code = ''
cat3name = ''

for item in listOfitem:
	cat1code = item['code']
	cat1name = item['name']
	cwCat1.writerow([cat1code, cat1name])

	REST = '&MobileOS=' + MobileOS + '&MobileApp=' + MobileApp + '&cat1=' + cat1code
	URL = EndpointUrl + '?ServiceKey=' + ServiceKey + REST +'&_type=json'
	numOfRows = getTotalNum(URL)

	REST = '&numOfRows=' + numOfRows + '&MobileOS=' + MobileOS + '&MobileApp=' + MobileApp + '&cat1=' + cat1code
	URL = EndpointUrl + '?ServiceKey=' + ServiceKey + REST +'&_type=json'

	r = requests.get(URL)
	rawData = json.loads(r.content)

	#Real Item Variable Set
	listOfCat1item = rawData['response']['body']['items']['item']

	if int(numOfRows) > 1:
		for itemcat1 in listOfCat1item:
			cat2code = itemcat1['code']
			cat2name = itemcat1['name']
			cwCat2.writerow([cat2code, cat2name])

			REST = '&MobileOS=' + MobileOS + '&MobileApp=' + MobileApp + '&cat1=' + cat1code + '&cat2=' + cat2code
			URL = EndpointUrl + '?ServiceKey=' + ServiceKey + REST +'&_type=json'
			numOfcat1Rows = getTotalNum(URL)

			REST = '&numOfRows=' + numOfcat1Rows + '&MobileOS=' + MobileOS + '&MobileApp=' + MobileApp + '&cat1=' + cat1code + '&cat2=' + cat2code
			URL = EndpointUrl + '?ServiceKey=' + ServiceKey + REST +'&_type=json'

			r = requests.get(URL)
			rawDataCat2 = json.loads(r.content)

			try:
				listOfCat2item = rawDataCat2['response']['body']['items']['item']
			except:
				continue

			if int(numOfcat1Rows) > 1:
				for itemcat2 in listOfCat2item:
					cat3code = itemcat2['code']
					cat3name = itemcat2['name']
					cwCat3.writerow([cat3code, cat3name])
			else:
				try:
					cat3code = listOfCat2item['code']
					cat3name = listOfCat2item['name']
					cwCat3.writerow([cat3code, cat3name])
				except:
					continue
	else:
		cat2code = listOfCat1item['code']
		cat2name = listOfCat1item['name']
		cwCat2.writerow([cat2code, cat2name])

		REST = '&MobileOS=' + MobileOS + '&MobileApp=' + MobileApp + '&cat1=' + cat1code + '&cat2=' + cat2code
		URL = EndpointUrl + '?ServiceKey=' + ServiceKey + REST +'&_type=json'
		numOfcat1Rows = getTotalNum(URL)

		REST = '&numOfRows=' + numOfcat1Rows + '&MobileOS=' + MobileOS + '&MobileApp=' + MobileApp + '&cat1=' + cat1code + '&cat2=' + cat2code
		URL = EndpointUrl + '?ServiceKey=' + ServiceKey + REST +'&_type=json'

		r = requests.get(URL)
		rawDataCat2 = json.loads(r.content)

		try:
			listOfCat2item = rawDataCat2['response']['body']['items']['item']
		except:
			continue

		if int(numOfcat1Rows) > 1:
			for itemcat2 in listOfCat2item:
				cat3code = itemcat2['code']
				cat3name = itemcat2['name']
				cwCat3.writerow([cat3code, cat3name])
		else:
			try:
				cat3code = listOfCat2item['code']
				cat3name = listOfCat2item['name']
				cwCat3.writerow([cat3code, cat3name])
			except:
				continue



"""
#Json Item Cleansing
#contentTypeId Cleansing
for key in contentTypeId:

	value = contentTypeId[key]
	print '71: ' + 'key : ' + key + ', value : ' + value

	#GET Total Item Number
	REST = '&contentTypeId=' + value + '&MobileOS=' + MobileOS + '&MobileApp=' + MobileApp
	URL = EndpointUrl + '?ServiceKey=' + ServiceKey + REST +'&_type=json'

	r = requests.get(URL)
	rawData = json.loads(r.content)

	numOfRows = getTotalNum(URL)

	listOfitem = rawData['response']['body']['items']['item']

	if type(listOfitem) is dict:
		for bigkey in listOfitem:
			bigvalue = str(listOfitem[bigkey])
			print '87: ' + 'bigkey : ' + bigkey + ', bigvalue : ' + bigvalue

			#Set bigkey, bigvalue variable
			if bigkey == 'name':
				bigName = bigvalue
			elif bigkey == 'code':
				bigCode = bigvalue

		#middleItem
		REST = '&contentTypeId=' + value + '&cat1=' + bigCode + '&MobileOS=' + MobileOS + '&MobileApp=' + MobileApp
		URL = EndpointUrl + '?ServiceKey=' + ServiceKey + REST +'&_type=json'

		
		bignumOfRows = getTotalNum(URL)
		print '101 : ' + bignumOfRows

		REST = '&contentTypeId=' + value + '&cat1=' + bigCode + '&numOfRows=' + bignumOfRows + '&MobileOS=' + MobileOS + '&MobileApp=' + MobileApp
		URL = EndpointUrl + '?ServiceKey=' + ServiceKey + REST +'&_type=json'
		
		r = requests.get(URL)
		bigrawData = json.loads(r.content)

		biglistOfitem = bigrawData['response']['body']['items']['item']

		if type(biglistOfitem) is dict:
			for middlekey in biglistOfitem:
				middlevalue = str(biglistOfitem[middlekey])
				print '114: ' + 'middlevalue : ' + middlevalue
		else:
			for middlenum in range(len(biglistOfitem)):
				
				middleitem = biglistOfitem[middlenum]
				
				for middlekey in middleitem:
					middlevalue = str(middleitem[middlekey])
					print '122: ' + 'middlevalue : ' + middlevalue

	else:
		for num in range(len(listOfitem)):

			item = listOfitem[num]

			for bigkey in item:
				bigvalue = str(item[bigkey])
				print '131: ' + 'bigkey : ' + bigkey + ', bigvalue : ' + bigvalue
"""
"""
#cat1 Item Cleansing
for num in range(len(listOfitem)):

	item = listOfitem[num]
	print item

	for key in item:

		value = str(item[key])
		print 'key : ' + key + ', value : ' + value
"""

"""
		if key == 'name':

			areaName = str(unicode(rawData['response']['body']['items']['item'][num][key]))
		
		
		if key == 'code':

			areaCode = str(rawData['response']['body']['items']['item'][num][key])
			
			REST = '&areaCode=' + areaCode + '&MobileOS=' + MobileOS + '&MobileApp=' + MobileApp
			URL = EndpointUrl + '?ServiceKey=' + ServiceKey + REST +'&_type=json'

			r = requests.get(URL)
			bigrawData = json.loads(r.content)
			bignumOfRows = str(bigrawData['response']['body']['totalCount'])

			REST = '&areaCode=' + areaCode + '&numOfRows=' + bignumOfRows + '&MobileOS=' + MobileOS + '&MobileApp=' + MobileApp
			URL = EndpointUrl + '?ServiceKey=' + ServiceKey + REST +'&_type=json'

			r = requests.get(URL)
			bigrawData = json.loads(r.content)

			listOfbigItem = bigrawData['response']['body']['items']['item']

		if (key == 'rnum' and bignumOfRows > '1'):
			for bignum in range(len(listOfbigItem)):

				bigItem = listOfbigItem[bignum]

				for bigkey in bigItem:
					
					bigValue = bigItem[bigkey]
					
					if bigkey == 'name':
						bigAreaName = str(unicode(bigValue))
					elif bigkey == 'code':
						bigAreaCode = str(bigValue)
					elif bigkey == 'rnum':
						#print 'areaName : ' + areaName + ', rawData_1 : ' + areaCode + ', bigAreaName : ' + bigAreaName + ', bigAreaCode : ' + bigAreaCode
						cw.writerow([areaName, areaCode, bigAreaName, bigAreaCode])

					
					if type(bigValue) is int:
						#cw.writerow([areaName, areaCode, comp_yesterday, bigkey, high_price, low_price, total_amount, search_keyword])
						print 'areaName : ' + areaName + ', rawData_1 : ' + areaCode + ', bigkey : ' + bigkey + ', rawData_2 : ' + str(bigValue)
					else:
						print 'areaName : ' + areaName + ', rawData_1 : ' + areaCode + ', bigkey : ' + bigkey + ', rawData_2 : ' + str(unicode(bigValue))
					
						
		elif (key == 'rnum' and bignumOfRows == '1'):
			for bignum in range(len(listOfbigItem)):
				for bigkey in listOfbigItem:

					bigValue = listOfbigItem[bigkey]

					if bigkey == 'name':
						bigAreaName = str(unicode(bigValue))
					elif bigkey == 'code':
						bigAreaCode = str(bigValue)
					elif bigkey == 'rnum':
						#print 'areaName : ' + areaName + ', rawData_1 : ' + areaCode + ', bigAreaName : ' + bigAreaName + ', bigAreaCode : ' + bigAreaCode
						cw.writerow([areaName, areaCode, bigAreaName, bigAreaCode])

					
					if type(bigValue) is int:
						print 'areaName : ' + areaName + ', rawData_1 : ' + areaCode + ', bigkey : ' + bigkey + ', rawData_2 : ' + str(bigValue)
					else:
						print 'areaName : ' + areaName + ', rawData_1 : ' + areaCode + ', bigkey : ' + bigkey + ', rawData_2 : ' + str(unicode(bigValue))
					
"""