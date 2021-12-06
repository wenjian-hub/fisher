
# cookie 时效
REMEMBER_COOKIE_DURATION = 1

# 分布式数据库
DATABASE_UERNAME = "root"
DATABASE_PASSWORD = "123456"
DATABASE_HOST = "localhost"
DATABASE_PORT = 3306
PROJECT_NAME = "fisher"

# 用于连接的数据库 URI
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://{}:{}@{}:{}/{}'.format(DATABASE_UERNAME, DATABASE_PASSWORD, DATABASE_HOST,
                                                                  DATABASE_PORT, PROJECT_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = True

# 数据库操作时是否显示原始SQL语句，一般都是打开的，因为我们后台要日志
SQLALCHEMY_ECHO = True

SECRET_KEY = '\089X'

# Email 配置
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
MAIL_USERNAME = "709889894@qq.com"
MAIL_PASSWORD = "rcnglfdhqtmibchi"
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_ASCII_ATTACHMENTS = False
MAIL_SUBJECT_PREFIX = "[鱼书]"
MAIL_SENDER = "鱼书<wenjian@yushu.im>"







