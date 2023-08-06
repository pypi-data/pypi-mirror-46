# Used for micro service developed by nameko
# Have to install nameko
"""
    Example::

        from wisdoms.auth import permit

        host = {'AMQP_URI': "amqp://guest:guest@localhost"}

        auth = permit(host)

        class A:
            @auth
            def func():
                pass
"""

from nameko.standalone.rpc import ClusterRpcProxy
from nameko.rpc import rpc
from wisdoms.utils import xpt_func
from functools import wraps


def ms_base(ms_host, **extra):
    """
    返回父类，闭包，传参数ms host
    :param ms_host:
    :param extra: 额外信息
    :return:
    """

    class MsBase:
        name = 'ms-base'

        @rpc
        # @exception()
        def export_info2db(self):
            """
            export information of this service to database
            :return:
            """
            clazz = type(self)
            service = clazz.name
            functions = list(clazz.__dict__.keys())

            origin = dict()
            origin['service'] = service
            origin['functions'] = functions
            origin['roles'] = extra.get('roles')
            origin['name'] = extra.get('name')
            origin['types'] = extra.get('types', 'free')
            origin['entrance'] = extra.get('entrance')
            with ClusterRpcProxy(ms_host) as r:
                r.baseUserApp.app2db(origin)

    return MsBase


def permit(host):
    """ 调用微服务功能之前，进入基础微服务进行权限验证

    :param: host: micro service host
    """

    def wrapper(f):
        @wraps(f)
        def inner(*args, **kwargs):
            service = args[0].name
            func = f.__name__
            token = args[1].get('token')

            with ClusterRpcProxy(host) as r:
                res = r.baseUserApp.verify({'service': service, 'func': func, 'token': token})
            if res:
                args[1]['user'] = res
                return f(*args, **kwargs)

            raise Exception('verified failed')

        return inner

    return wrapper


def add_uid(host):
    """
    用户token 返回用户id
    :param host:
    :return:
    """

    def wrapper(f):
        @wraps(f)
        def inner(*args, **kwargs):
            token = args[1].get('token')

            with ClusterRpcProxy(host) as r:
                res = r.baseUserApp.get_uid({'token': token})
            if res:
                args[1]['uid'] = res
                return f(*args, **kwargs)

            raise Exception('verified failed')

        return inner

    return wrapper


def add_user(host):
    """
    用户token 返回用户信息
    :param host:
    :return:
    """

    def wrapper(f):
        @wraps(f)
        def inner(*args, **kwargs):
            token = args[1].get('token')

            with ClusterRpcProxy(host) as r:
                res = r.baseUserApp.get_user({'token': token})
            if res:
                args[1]['user'] = res
                return f(*args, **kwargs)

            raise Exception('verified failed')

        return inner

    return wrapper


def assemble(rpc, service, function1, param1='', *params):
    str1 = rpc + '.' + service + '.' + function1
    str2 = '(' + param1
    for param in params:
        str2 += ',' + param
    str2 += ')'
    return str1 + str2


def crf_closure(ms_host):
    def crf(service, function1, data):
        with ClusterRpcProxy(ms_host) as rpc:
            result = eval(assemble('rpc', service, function1, 'data'))
        return result

    return crf
