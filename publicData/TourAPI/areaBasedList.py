# -*- coding: utf-8 -*-

import requests
import json
import unicodedata
import time
import csv
import sys
from datetime import datetime, timedelta

def getRest(var, value):
	if value == '':
		return ''
	return '&' + var + '=' + value

def getTotalNum(url):
	r = requests.get(URL)
	rawData = json.loads(r.content)

	numOfRows = str(rawData['response']['body']['totalCount'])
	return numOfRows

def getPercent(num, total):
	print "{0:.0f}%".format(float(num)/total * 100)

#date define
base_date = datetime.today().date().strftime("20%y%m%d")

#API parameters
EndpointUrl = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList'
ServiceKey = 'DXRmbbl57VC3IgCeGvBCirKXS%2Ba4klA0Qs3XDCRHHbWADxOb3z0y2LxAcagkTUIcpSepdS%2Fo8WstIxtUH8LLBQ%3D%3D'
"""
#contentTypeid set
csv_file_contentid = open('contenttypeid.dat', 'rb')
reader = csv.reader(csv_file_contentid)

for row in reader:
	name = row[0]
	contentTypeid = row[1]
	#print name + ' ' + str(contentTypeid)
"""
#areaName set
csv_file_areacode = open('areaCode.dat', 'rb')
reader = csv.reader(csv_file_areacode)

areaName = {}
sigunguName = {}
cat1Name = {}
cat2Name = {}
cat3Name = {}

for row in reader:
	areaCode = row[0]
	sigunguName[areaCode] = {}
	areaName[areaCode] = row[1]

#sigunguName set
csv_file_sigungucode = open('sigunguCode.dat', 'rb')
reader = csv.reader(csv_file_sigungucode)

for row in reader:
	areaCode = row[1]
	sigunguCode = row[3]
	sigunguName[areaCode][sigunguCode] = row[2]
#cat1Name set
csv_file_cat1 = open('Cat1Code.dat', 'rb')
reader = csv.reader(csv_file_cat1)

for row in reader:
	cat1Code = row[0]
	cat1Name[cat1Code] = row[1]
#cat2Name set
csv_file_cat2 = open('Cat2Code.dat', 'rb')
reader = csv.reader(csv_file_cat2)

for row in reader:
	cat2Code = row[0]
	cat2Name[cat2Code] = row[1]

csv_file_cat3 = open('Cat3Code.dat', 'rb')
reader = csv.reader(csv_file_cat3)

for row in reader:
	cat3Code = row[0]
	cat3Name[cat3Code] = row[1]
print cat3Name
#Var set
areaCode = '0'
MobileOS = 'ETC'
MobileApp = 'AppTesting'
contentTypeIdDefault = {'12' : '관광지', '14' : '문화시설', '15' : '행사/공연/축제', '25' : '여행코스',
				 		'28' : '레포츠', '32' : '숙박', '38' : '쇼핑', '39' : '음식점'}

contentTypeid = ''
areaCode = ''
sigunguCode = ''
cat1 = ''
cat2 = ''
cat3 = ''

#URL set for getTotalNum
REST = getRest('contentTypeid', contentTypeid) + getRest('areaCode', areaCode) + getRest('sigunguCode', sigunguCode) + getRest('cat1', cat1) + getRest('cat2', cat2) + getRest('cat3', cat3) + '&MobileOS=' + MobileOS + '&MobileApp=' + MobileApp
URL = EndpointUrl + '?ServiceKey=' + ServiceKey + REST +'&_type=json'

totalCount = getTotalNum(URL)

#URL set for real request
REST = getRest('contentTypeid', contentTypeid) + getRest('areaCode', areaCode) + getRest('sigunguCode', sigunguCode) + getRest('cat1', cat1) + getRest('cat2', cat2) + getRest('cat3', cat3) + '&MobileOS=' + MobileOS + '&MobileApp=' + MobileApp + '&numOfRows=' + totalCount
URL = EndpointUrl + '?ServiceKey=' + ServiceKey + REST +'&_type=json'

#print URL
r = requests.get(URL)
rawData = json.loads(r.content)

csv_wfile = open('areaBasedList_' + str(base_date) + '.dat', "w")
#print rawData
for row in range(0, int(totalCount)):

	#getPercent(row, int(totalCount))
	diction = rawData['response']['body']['items']['item'][row]

	#var reset
	addr1 = ''
	addr2 = ''
	areacode = ''
	cat1 = ''
	cat2 = ''
	cat3 = ''
	contentid = ''
	contenttypeid = ''
	createdtime = ''
	firstimage = ''
	firstimage2 = ''
	mapx = ''
	mapy = ''
	mlevel = ''
	modifiedtime = ''
	readcount = ''
	sigungucode = ''
	tel = ''
	title = ''
	zipcode = ''
	areaname = ''
	sigunguname = ''


	#print diction.keys()
	for key in diction.keys():
		#dict. key value set

		if type(rawData['response']['body']['items']['item'][row][key]) != unicode:
			value = str(rawData['response']['body']['items']['item'][row][key])
		else:
			value = rawData['response']['body']['items']['item'][row][key].encode('utf8')

		if key == 'addr1':
			addr1 = value
		elif key == 'addr2':
			addr2 = value
		elif key == 'areacode':
			areacode = value
		elif key == 'cat1':
			cat1 = value
		elif key == 'cat2':
			cat2 = value
		elif key == 'cat3':
			cat3 = value
		elif key == 'contentid':
			contentid = value
		elif key == 'contenttypeid':
			contenttypeid = value
		elif key == 'createdtime':
			createdtime = value
		elif key == 'firstimage':
			firstimage = value
		elif key == 'firstimage2':
			firstimage2 = value
		elif key == 'mapx':
			mapx = value
		elif key == 'mapy':
			mapy = value
		elif key == 'mlevel':
			mlevel = value
		elif key == 'modifiedtime':
			modifiedtime = value
		elif key == 'readcount':
			readcount = value
		elif key == 'sigungucode':
			sigungucode = value
		elif key == 'tel':
			tel = value
		elif key == 'title':
			title = value
		elif key == 'zipcode':
			zipcode = value

	try:
		areaname = areaName[areacode]
		sigunguname = sigunguName[areacode][sigungucode]
		contenttypeidname = contentTypeIdDefault[contenttypeid]
		cat1name = cat1Name[cat1]
		cat2name = cat2Name[cat2]
		cat3name = cat3Name[cat3]
	except KeyError, e:
		continue

	cw = csv.writer(csv_wfile, delimiter = '|', quotechar = '%')
	cw.writerow([contentid, areacode, sigungucode, areaname, sigunguname, addr1, addr2, contenttypeid, cat1, cat2, cat3, contenttypeidname, cat1name, cat2name, cat3name, mapx, mapy, mlevel, title, tel, zipcode, firstimage, firstimage2, readcount, createdtime, modifiedtime])
