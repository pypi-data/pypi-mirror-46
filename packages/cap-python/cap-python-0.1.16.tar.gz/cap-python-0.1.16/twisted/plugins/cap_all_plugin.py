# coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2015/7/20.
# ---------------------------------
from zope.interface import implements
from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker, MultiService, Application
from twisted.application.internet import TCPServer
import sys
from twisted.web import server
import os
import netifaces
import re
from twisted.internet import reactor
from twisted.web.wsgi import WSGIResource

reload(sys)
sys.setdefaultencoding("utf-8")


def get_local_ipaddr():
    results = []
    for i in netifaces.interfaces():
        info = netifaces.ifaddresses(i)
        if netifaces.AF_INET not in info:
            continue
        _ = info[netifaces.AF_INET][0]['addr']
        if _ != "127.0.0.1":
            results.append(_)
    return results


def option_mysql_url_valid(val):
    if re.match(r".+?:\d+/.+", val):
        return val
    else:
        raise Exception("%s 不是一个可用的数据库地址。 例子：192.168.8.94:3306/cap_db" % (val))


option_mysql_url_valid.coerceDoc = "数据库地址， 例如：192.168.8.94:3306/cap_db"


def option_mysql_user_valid(val):
    return val


option_mysql_user_valid.coerceDoc = "数据库用户， 例如：admin"


def option_mysql_password_valid(val):
    return val


option_mysql_password_valid.coerceDoc = "数据库密码， 例如：123456"


def option_host_valid(val):
    if val in get_local_ipaddr():
        return val
    else:
        raise Exception("%s 不是一个可用的地址, 本机所有可绑定的地址如下 %s" % (val, ",".join(get_local_ipaddr())))


option_host_valid.coerceDoc = "服务绑定的IP地址，本机所有可绑定的IP地址如下 %s" % (
    ",".join(get_local_ipaddr()))


def option_work_dir_valid(val):
    if val[0] != '/':
        raise Exception("%s 必须是一个绝对路径,比如 /data/crondeamon_work ")
    try:
        assert os.path.exists(val)
    except:
        raise Exception("%s 不是一个可用的目录,请检查目录是否存在及权限是否正确！" % val)
    return val


option_work_dir_valid.coerceDoc = "服务的工作目录"


class Options(usage.Options):
    optParameters = [
        ["mysql_url", "l", None, None, option_mysql_url_valid],
        ["mysql_user", "r", None, None, option_mysql_user_valid],
        ["mysql_password", 'd', None, None, option_mysql_password_valid],
        ["host", "h", None, None, option_host_valid],
        ["work_dir", "w", None, None, option_work_dir_valid]
    ]


class AServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "cap-all"
    description = "cap-all服务"
    options = Options

    def makeService(self, options):
        config = options
        import cap
        from cap_twisted import service as mainrpc
        import sys
        s = MultiService()
        sys.path.insert(1, cap.__path__[0])
        del sys.modules["cap"]
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cap.settings")
        mysql_url = options["mysql_url"].strip()
        try:
            a, b = mysql_url.split(":")
            mysql_host = a
            mysql_port, mysql_db = b.split("/")
            mysql_port = int(mysql_port)
        except:
            print "mysql相关配置错误"
            raise Exception("mysql相关配置错误")
        else:
            mysql_user = options["mysql_user"]
            mysql_password = options["mysql_password"]
        os.config = [mysql_host, mysql_port, mysql_db, mysql_user, mysql_password]
        os.work_dir = options["work_dir"]
        os.host = options["host"]
        from django.core.handlers.wsgi import WSGIHandler
        application = WSGIHandler()
        resource = WSGIResource(reactor, reactor.getThreadPool(), application)
        ui_service = TCPServer(9912, server.Site(resource), interface=config["host"])
        serverfactory = server.Site(mainrpc.MainRpc(config["host"], config["work_dir"]))
        slave_service = TCPServer(9913, serverfactory, interface=config["host"])
        slave_service.setServiceParent(s)
        ui_service.setServiceParent(s)
        return s


serviceMaker = AServiceMaker()
