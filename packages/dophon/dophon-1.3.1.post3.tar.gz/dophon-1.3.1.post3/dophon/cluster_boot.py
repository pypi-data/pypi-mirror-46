# coding: utf-8
from multiprocessing import Process, freeze_support
import time, socket, random
from flask import request, make_response
from urllib3 import PoolManager
from dophon import properties
from dophon_logger import *

logger = get_logger(eval(properties.log_types))

logger.inject_logger(globals())

ports = []  # 记录监听端口

proxy_clusters = {}

pool = PoolManager()


def main_freeze():
    freeze_support()


def redirect_request():
    logger.info('touch path: %s [success]' % (request.path))
    res = pool.request(request.method, '127.0.0.1:' + str(random.choice(ports)) + request.path,
                       fields=request.json if request.is_json else request.form)
    return make_response(res.data)


def outer_entity():
    from dophon import boot
    # 重写路由信息(修改为重定向路径)
    boot.get_app().before_request(redirect_request)
    boot.run()


def run_clusters(clusters: int, outer_port: bool = False, start_port: int = 8800, multi_static_fix: bool = False,
                 part_kwargs: dict = {}):
    """
    运行集群式服务器
    :param clusters: 集群个数
    :param outer_port: 是否开启外部端口映射(映射端口为用户配置文件中配置的端口)
    :param start_port: 集群起始监听端口
    :param multi_static_fix: 是否增强静态文件
    :param part_kwargs: 集群节点额外参数(会覆盖默认参数)
    :return:
    """
    part_kwargs['multi_static_fix'] = multi_static_fix
    for i in range(clusters):
        current_port = start_port + i
        create_cluster_cell(port=current_port, part_kwargs=part_kwargs)
        ports.append(current_port)
    while len(ports) != clusters:
        time.sleep(5)

    logger.info('启动检测端口监听')
    for port in ports:
        if check_socket(int(port)):
            continue
    logger.info('集群端口: %s ' % ports)
    if outer_port:
        logger.info('启动外部端口监听[%s]' % (properties.port))
        outer_entity()


def create_cluster_cell(port, part_kwargs):
    kwargs = {
        'host': '127.0.0.1',
        'port': port
    }
    if part_kwargs:
        # 迁移参数
        for k, v in part_kwargs.items():
            kwargs[k] = v
    # http协议
    proc = Process(target=inject_run, kwargs={
        'fix_static': part_kwargs['multi_static_fix'],
        'kwargs': kwargs
    })
    proc.start()


def inject_run(fix_static, kwargs):
    from dophon import boot
    if fix_static:
        boot.fix_static(enhance_power=True)
    boot.run(eval(f'boot.{kwargs["run_type"] if "run_type" in kwargs and kwargs["run_type"] else "FLASK"}'))


def check_socket(port: int):
    s = socket.socket()
    flag = True
    while flag:
        try:
            ex_code = s.connect_ex(('127.0.0.1', port))
            flag = False
            return int(ex_code) == 0
        except Exception as e:
            time.sleep(3)
            continue
