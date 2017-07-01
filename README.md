这是基于实验楼网站项目：https://www.shiyanlou/courses/623
（Linux下火车票查询小工具）在Windows平台下的移植版本，并且做了如下修改：

1.	解决了Windows下命令行GBK编码导致的部分特殊字符无法显示的问题
2.	扩充了车票查询选项，允许成人票与学生票之间切换查询
3.	扩充了查询结果，增加了销售车票的价位信息

使用要求：
1.	Windows操作系统
2.	安装Python环境，版本最好为3.4以上
3.	安装了需求的包：requests, docopt, prettytable, colorama, setuptools(均基于pip3安装)

项目安装说明：

	在Windows环境下进入命令行输入环境，进入项目文件中:
		cd master-dir\\"tickets search"

	调用python解释器执行安装脚本：
		python setup.py install

	安装完成后，可通过tickets --help查看使用说明

若对于项目有任何改进意见或发现项目存在的bug，欢迎联系lyxok1@sjtu.edu.cn进行反馈
