# -*- coding: utf-8 -*-
from application import app,db
from common.models.queue.QueueList import QueueList
import json,requests,datetime
from common.libs.Helper import getCurrentDate
from common.libs.pay.WeChatService import WeChatService
from common.models.pay.PayOrder import PayOrder
from common.models.pay.PayOrderItem import PayOrderItem
from common.models.member.OauthMemberBind import OauthMemberBind
from common.models.food.Food import Food
from common.models.food.FoodSaleChangeLog import FoodSaleChangeLog
from sqlalchemy import func

'''
python manager.py runjob -m queue/index
'''

class JobTask():
    def __init__(self):
        pass
    def run(self,params):
        list = QueueList.query.filter_by(status = -1 )\
            .order_by( QueueList.id.asc() ).limit(1).all()
        for item in list:
            if item.queue_name == "pay":
                self.handlePay( item )

            item.status = 1
            item.updated_time = getCurrentDate()
            db.session.add( item )
            db.session.commit()

    def handlePay(self,item ):
        data = json.loads( item.data )
        if 'member_id' not in data or 'pay_order_id' not in data:
            return False

        oauth_bind_info = OauthMemberBind.query.filter_by(member_id=data['member_id']).first()
        if not oauth_bind_info:
            return False

        pay_order_info = PayOrder.query.filter_by( id = data['pay_order_id']).first()
        if not pay_order_info:
            return False

        #更新销售总量
        pay_order_items = PayOrderItem.query.filter_by( pay_order_id = pay_order_info.id ).all()
        notice_content = []
        if pay_order_items:
            date_from = datetime.datetime.now().strftime( "%Y-%m-01 00:00:00" )
            date_to = datetime.datetime.now().strftime( "%Y-%m-31 23:59:59" )
            for item in pay_order_items:
                tmp_food_info = Food.query.filter_by( id = item.food_id ).first()
                if not tmp_food_info:
                    continue

                notice_content.append( "%s %s份"%( tmp_food_info.name,item.quantity) )

                #当月数量
                tmp_stat_info = db.session.query(FoodSaleChangeLog, func.sum(FoodSaleChangeLog.quantity).label("total")) \
                    .filter( FoodSaleChangeLog.food_id  == item.food_id )\
                    .filter( FoodSaleChangeLog.created_time >= date_from,FoodSaleChangeLog.created_time <= date_to ).first()
                tmp_month_count = tmp_stat_info[ 1 ] if tmp_stat_info[ 1 ] else 0
                tmp_food_info.total_count += 1
                tmp_food_info.month_count = tmp_month_count
                db.session.add( tmp_food_info )
                db.session.commit()

        if pay_order_info.prepay_id != "1":
            #当prepay_id == 1表示用户接受发订阅消息
            app.logger.info("skip notice~~")
            return

        ##发订阅消息
        keyword1_val = pay_order_info.order_number
        keyword2_val = "、".join( notice_content )
        keyword3_val = "总价：" + str( pay_order_info.total_price )
        if pay_order_info.express_info:
            express_info = json.loads( pay_order_info.express_info )
            keyword3_val += "快递信息：" + str( express_info['address'] )
        #发送模板消息
        target_wechat = WeChatService( )
        access_token = target_wechat.getAccessToken()
        headers = {'Content-Type': 'application/json'}
        url = "https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=%s"%access_token
        params = {
            "touser": oauth_bind_info.openid,
            "template_id":"gEWJzj_7_7bBej8grUY7V3ZWLLYU2sIp2jNSO5w2Fos",
            "page": "pages/my/order_list",
            "data": {
                "number1": {
                    "value": keyword1_val
                },
                "thing2": {
                    "value": keyword2_val
                },
                "thing3": {
                    "value": keyword3_val
                }
            }
        }

        r = requests.post(url=url, data= json.dumps( params ).encode('utf-8'), headers=headers)
        r.encoding = "utf-8"
        app.logger.info(r.text)
        return True