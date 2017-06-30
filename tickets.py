# coding: utf-8
"""
Usage:
	tickets [-gdtkz] <from> <to> <date> <type>

Options:
	from	出发地点
	to	目的地
	date	日期
	type==A 成人票
	type==S 学生票

	-h,--help	显示帮助
	-g		高铁
	-d		动车
	-t		特快
	-k		快速
	-z		直达

Examples:
	tickets -gdk 成都 上海 2017-09-01 A
"""

from docopt import docopt
from stations import stations
import requests
from pprint import pprint
from train_parser import train_parser

def parse_cmd():
	arguments = docopt(__doc__)
	print(arguments)
	return arguments

def MainProcess():
	print('解析查询指令...')
	try:	
		arguments = parse_cmd()
		type_dict = {'A':"ADULT",'S':"0X00"}
		from_arg = stations.get(arguments['<from>'])
		to_arg = stations.get(arguments['<to>'])
		date = arguments['<date>']
		obj_day = date.split('-')

		for time_data in obj_day:
			if(len(time_data)==1):
				index = obj_day.index(time_data)
				obj_day[index] = '0'+time_data
		date = '-'.join(obj_day)

		guest_type = type_dict.get(arguments['<type>'])

		print('确认查票信息:from %s to %s on %s, purpose_code: %s' %(from_arg,to_arg,date,guest_type))

		url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes={}'.format(date,from_arg,to_arg,guest_type)
			
		r = requests.get(url,verify=False)
		available_trains = r.json()['data']['result']
		maps = r.json()['data']['map']
		options = ''.join([key for key, value in arguments.items() if value is True])
			
		TrainsCollection = train_parser(available_trains,options,maps,date)

		TrainsCollection.pretty_print()
	except :
		print("""查票出错，可能出现的问题:\n  	
			1.查票时间距离当前的时间过远，建议在一个月以内\n  	
			2.网络繁忙或网络链接中断\n  	
			3.参数格式出错，通过tickets --help查看正确参数使用\n  	
			4.12306官网根证书已过期，需要重新下载安装根证书""")
	finally:
		print("完成")
	
if __name__ == '__main__':
	MainProcess()
	
