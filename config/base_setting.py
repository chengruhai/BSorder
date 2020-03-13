SERVER_PORT = 8999
DEBUG = False
SQLALCHEMY_ECHO = False
JSON_AS_ASCII  =  False

AUTH_COOKIE_NAME = "xiaohai_food"

##过滤url
IGNORE_URLS = [
    "^/user/login",
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico"
]

API_IGNORE_URLS = [
    "^/api"
]

PAGE_SIZE = 50
PAGE_DISPLAY = 10

STATUS_MAPPING = {
    "1":"正常",
    "0":"已删除"
}

MINA_APP = {
    'appid':'wx1de93d69c9028d6a',
    'appkey':'3f1f069e7bc5bcded619c1e211ff8a35',
    'paykey':'wxsssssssss',
    'mch_id':'15902900591',
    'callback_url':'/api/order/callback'
}


UPLOAD = {
    'ext':[ 'jpg','gif','bmp','jpeg','png' ],
    'prefix_path':'/web/static/upload/',
    'prefix_url':'/static/upload/'
}

APP = {
    'domain':'http://192.168.137.1:8999'
}


PAY_STATUS_MAPPING = {
    "1":"已支付",
    "-8":"待支付",
    "0":"已关闭"
}

PAY_STATUS_DISPLAY_MAPPING = {
    "0":"订单关闭",
    "1":"支付成功",
    "-8":"待支付",
    "-7":"待发货",
    "-6":"待确认",
    "-5":"待评价"
}
