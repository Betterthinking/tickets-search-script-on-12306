# coding: utf-8

import re
from prettytable import PrettyTable
from colorama import init, Fore
import requests

class train_parser:
	
	headers = '车次 车站 时间 历时 一等 二等 软卧 硬卧 硬座 无座'.split()

	#to get the back information
	on_sale_match = r'\|Y\|'
	train_header_match = r'\|预订\|([0-9A-Za-z]+)\|([A-Z0-9]+)\|[A-Z]+\|[A-Z]+\|([A-Z]+)\|([A-Z]+)\|([0-9]+:[0-9]+)\|([0-9]+:[0-9]+)\|([0-9]+:[0-9]+)\|'
	tickets_info_match = r'\|([有无0-9]*)\|[有无0-9]*\|[有无0-9]*\|([有无0-9]*)\|[有无0-9]*\|([有无0-9]*)\|([有无0-9]*)\|([有无0-9]*)\|([有无0-9]*)\|[有无0-9]*\|[有无0-9]*\|[0-9A-Za-z]'	
	from_to_match = r'\|[0-9]{8}\|[0-9A-Za-z]*\|[0-9A-Za-z]*\|([0-9]+)\|([0-9]+)\|'
	seat_type_match = r'\|([0-9A-Z]+)$'	
	price_type = ['M','O','A4','A3','A1','WZ']	

	def __init__(self,available_trains,options,maps,date):
		self.available_trains = available_trains
		self.options = options
		self.maps = maps
		self.date = date

	@property
	def trains(self):
		
		for train_info in self.available_trains:
			on_sale = re.search(self.on_sale_match,train_info)
			if on_sale:
				train_headers = re.findall(self.train_header_match,train_info)[0]
				tickets_info = re.findall(self.tickets_info_match,train_info)[0]
				from_to_info = re.findall(self.from_to_match,train_info)[0]
				seat_type_info = re.findall(self.seat_type_match,train_info)
				train_no = train_headers[1]
				
				if train_no[0].lower() in self.options:
					train_code = train_headers[0]
					from_station_no = from_to_info[0]
					to_station_no = from_to_info[1]
					seat_type = seat_type_info[0]

					url = 'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no={}&from_station_no={}&to_station_no={}&seat_types={}&train_date={}'.format(train_code,from_station_no,to_station_no,seat_type,self.date)
					r = requests.get(url,verify=False)
					data = r.json()["data"]
					price = ['票价','','','']
					for key in self.price_type:
						if(key in data.keys()):
							price.append(data[key][1:])#ignore the frist '\xa5' character
						else:
							price.append('')						

					train = [train_no,'\n'.join([self.maps[train_headers[2]],self.maps[train_headers[3]]]),'\n'.join([train_headers[4],train_headers[5]]),train_headers[6],tickets_info[5],tickets_info[4],tickets_info[0],tickets_info[2],tickets_info[3],tickets_info[1]]
					
					yield (train,price)

	def pretty_print(self):
		pt = PrettyTable()
		pt._set_field_names(self.headers)
		
		for (train,price) in self.trains: #use generator as a iteration container to control the print loop
			pt.add_row(train)
			pt.add_row(price)
			#pt.add_row(['','','','','','','','','',''])
		print(pt)
