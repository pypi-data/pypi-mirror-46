from Chiloc import Chiloc
import helper
import numpy as np
import pandas as pd 
import json
from urllib.request import urlopen, quote
import os 

class CityLocator(Chiloc):
	"""
	"""
	
	def __init__(self, place_name = '北京大学国家发展研究院', place_city = '北京市'):
	
		Chiloc.__init__(self, place_name)
		self.name = place_city + ' ' + self.name
		self.city = place_city
		
		
	def distance(self, other):
		
		url = 'http://api.map.baidu.com/directionlite/v1/walking'
		ak = 'H3bQs5XVuBaLnoQ3CvIzZUiEYrr5Bym4'
		
		url = (url + '?' + 'origin=' + str(self.lat) +',' + str(self.lng) 
		+ '&destination=' + str(other.lat) + ',' + str(other.lng) + '&ak=' + ak)
		
		req = urlopen(url)
		# decode as unicode
		res = req.read().decode()
		temp = json.loads(res)
		
		try:
			distance = temp['result']['routes'][0]['distance']
		except:
			pass
		
		return distance
	
	
	def nearest(self, object_ask, radius = 2000):
		
		ak = 'H3bQs5XVuBaLnoQ3CvIzZUiEYrr5Bym4'
		object_quote = quote(object_ask)
		url = ('http://api.map.baidu.com/place/v2/search?query=' + object_quote + '&location=' + str(self.lat) 
		+ ',' + str(self.lng) + '&radius=' + str(radius) + '&output=json&ak=' + ak)
		
		req = urlopen(url)
		res = req.read().decode()
		temp = json.loads(res)
		
		try:
			name = temp['results'][0]['name']
			address = temp['results'][0]['address']
			district = temp['results'][0]['area']
			object_ = object_ask + ' - ' + name
			distance = self.distance(CityLocator(object_ask + name))

			print(f'The nearest {object_ask} is {object_} and it locates at {district}, {address} with the distance {distance} m.')
		
		except:
			print(f'Oops! It is considered that there is no any {object_ask}-like facility within {radius}m. Maybe we can try a greater radius.')
		
			name = ''
			address = ''
			district = ''
			distance = ''
		
		return name, address, district, distance
	
	def subway_initiator(self):
		
		print('Initialization...')
		print(f'Track the citycode for {self.city}')
		city_code = pd.read_csv('City_codes.csv', encoidng = 'gbk')
		code = city_code[city_code['City'] == self.city]['Code']
		
		req = urlopen('http://map.baidu.com/?qt=bsi&c='+ code + '&t=123457788')
		res = req.read().decode()
		temp = json.loads(response)
		
		# Create subway dataframe 
		
		print(f'Generating the subway data in {self.city}.')
		subway = pd.DataFrame()
		subway['Stop'], subway['Line'], subway['lat'], subway['lng'] = np.nan, np.nan, np.nan, np.nan
		
		stops, lines, lats, lngs = [], [], [], []
		
		for i in range(len(temp['content'])):
			line = temp['content'][i]['line_name']
			print(f'Loading for {line}:')
			for j in range(len(temp['content'][i]['stops'])):
				stop = temp['content'][i]['stops'][j]['name']
				stops.append(stop)
				lines.append(line)

				try:
					lats.append(getlnglat(stop + ' - 地铁站')[0])
					lngs.append(getlnglat(stop + ' - 地铁站')[1])
					print(f'	- {stop} is loaded.')
				except: 
					lats.append(np.nan)
					lngs.append(np.nan)
					print(f'	- Fails to load {stop} for some reason.')
				

		subway['Stop'] = stops
		subway['Line'] = lines
		subway['lat'] = lats
		subway['lng'] = lngs
		
		print(f'The subway data of {self.city} is generated!')
		
		try:
			os.mkdir('./subway_data')
		except:
			pass
		
		path = './subway_data/' + self.city + '_subway.csv'
		subway.to_csv(path, index = False)
		
			
