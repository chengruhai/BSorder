订餐系统
==============

##启动
* set ops_config=local
* python manager.py runserver

* python manager.py runjob -m stat/daily -a site -p 2018-03-12
* python manager.py runjob -m stat/daily -a test

* WeChatService中 改正
* prepay_id = 1
* self.xml_to_dict( r.text ).get('prepay_id')