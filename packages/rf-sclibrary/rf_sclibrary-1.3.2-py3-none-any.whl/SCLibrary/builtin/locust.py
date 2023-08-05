from SCLibrary.base import keyword
from robot.libraries.BuiltIn import BuiltIn
from SCLibrary.builtin.requester import get_doraemon_headers
from argparse import Namespace
from locust import HttpLocust, TaskSet, task, runners, InterruptTaskSet, web
from locust.util.time import parse_timespan
from robot.api import logger
import os, sys, json, time
import gevent
import inspect

Locust_Task_Pool = []
Locust_User_Pool = []
Locust_Statistics = []

current_milli_time = lambda: int(round(time.time() * 1000))

class LocustKeyword(object):

    # ==========================================================
    # ========================== 便捷 ===========================
    # ==========================================================

    '''
    为传入的user添加一个断言的匿名函数
    '''
    def append_assert(self, user, func):
        if user.task.all_assets is None:
            user.task.all_assets = [func]
        else:
            user.task.all_assets.append(func)

    # ==========================================================
    # ========================== 断言 ===========================
    # ==========================================================

    @keyword("Locust HTTP Status Code Should Be")
    def status_code_should_be(self, user, code):
        '''
        断言HTTP完成之后响应状态码
        ``user`` HttpLocust对象
        ``code`` HTTP的响应状态码
        '''
        def core_status_code_should_be(task, response):
            if response.status_code != int(code):
                raise Exception('Locust响应状态码期望为%s, 当前实际得到的状态码为%s' % (code, str(response.status_code)))
        self.append_assert(user, core_status_code_should_be)

    @keyword("Locust JSON Should Be")
    def locust_response_json_equal(self, user, keypath, value):
        '''
        该断言关键字主要用于对返回JSON内容的断言
        ``user`` HttpLocust对象
        ``Keypath`` 键路径，比如data.foo，对应的是data中的foo的内容
        ``value`` 期望的值
        '''
        def core_locust_response_json_equal(task, response):
            try:
                json = response.json()
                for key in keypath.split('.'):
                    json = json[key]
                if json != value:
                    raise Exception('期望从%s中得到%s, 但是实际上却得到了%s' % (keypath, value, json))
            except KeyError:
                raise Exception('%s不存在%s' % (response, keypath))
        self.append_assert(user, core_locust_response_json_equal)

    @keyword("Locust Expect")
    def locust_core_expect(self, user, expection):
        '''
        自定义断言机制
        ``user`` HttpLocust类
        ``expection`` 一个关键字的名字，建议命名规则： 场景-期望
        讨论：
        expection是一个接受一个response参数的关键字，使用者可以拿到这个response进行自定义的断言。\n
        `response.json()`: 本次响应的JSON对象(Returns the json-encoded content of a response, if any)\n
        `response.content`: 本次响应的字节内容(Content of the response, in bytes)
        `response.headers`: 本次响应的响应投(Case-insensitive Dictionary of Response Headers. For example, headers['content-encoding'] will return the value of a 'Content-Encoding' response header)\n
        `response.encoding`: 本次响应的编码方式(Encoding to decode with when accessing r.text)\n
        `response.cookies`: 本次响应的cookies\n
        `response.status_code`: 本次响应的状态码\n
        `response.url`: 本次响应的请求地址
        '''
        self.append_assert(user, expection)

    @keyword("Locust AVE Threshold")
    def locust_ave_response_duration_should_less_than(self, user, time):
        '''
        平均阈值设置，超过阈值测试用例失败
        所有的响应中的平均响应时间不应该大于这个阈值
        ``user`` 模拟用户
        ``time`` 响应时间阈值(毫秒单位)
        '''
        def core_locust_response_duration_should_less_than(task, response):
            globalVaildator.rd_ave_threshold[task.path] = time
        self.append_assert(user, core_locust_response_duration_should_less_than)

    @keyword("Locust MAX Threshold")
    def locust_max_response_duration_should_less_than(self, user, time):
        '''
        最大阈值设置，超过阈值测试用例失败
        所有的响应中的最大响应时间不应该大于这个阈值
        ``user`` 模拟用户
        ``time`` 响应时间阈值(毫秒单位)
        '''
        def core_locust_response_duration_should_less_than(task, response):
            globalVaildator.rd_max_threshold[task.path] = time
        self.append_assert(user, core_locust_response_duration_should_less_than)

    @keyword("Locust MIN Threshold")
    def locust_min_response_duration_should_less_than(self, user, time):
        '''
        最小阈值设置，超过阈值测试用例失败
        所有的响应中的最小响应时间不应该大于这个阈值
        ``user`` 模拟用户
        ``time`` 响应时间阈值(毫秒单位)
        '''
        def core_locust_response_duration_should_less_than(task, response):
            globalVaildator.rd_min_threshold[task.path] = time
        self.append_assert(user, core_locust_response_duration_should_less_than)

    # ==========================================================
    # ========================== 任务 ===========================
    # ==========================================================

    @keyword("Locust GET Task")
    def build_locust_get_task(self, path='/', header=None):
        '''
        创建一个`GET`压测任务
        ``path`` 请求路径
        ``header`` 请求头
        返回一个包含该任务的HttpLocust
        '''
        return LocustWorker.build_locust_core_task('GET', path=path)

    @keyword("Locust POST Task")
    def build_locust_post_task(self, path='/', header=None, body=None):
        '''
        创建一个`POST`任务
        ``path`` 请求路径
        ``header`` 请求头
        ``body`` 请求体
        返回一个包含该任务的HttpLocust
        '''
        return LocustWorker.build_locust_core_task('POST', path=path, header=header, body=body)

    @keyword("Locust PUT Task")
    def build_locust_put_task(self, path='/', header=None, body=None):
        '''
        创建一个`PUT`任务
        ``path`` 请求路径
        ``header`` 请求头
        ``body`` 请求体
        返回一个包含该任务的HttpLocust
        '''
        return LocustWorker.build_locust_core_task('PUT', path=path, header=header, body=body)

    @keyword("Locust DELETE Task")
    def build_locust_delete_task(self, path='/', header=None):
        '''
        创建一个`DELETE`任务
        ``path`` 请求路径
        ``header`` 请求头
        返回一个包含该任务的HttpLocust
        '''
        return LocustWorker.build_locust_core_task("DELETE",path=path, header=header)

    # ==========================================================
    # ========================== 执行 ===========================
    # ==========================================================

    @keyword("Locust Run")
    def run_locust(self, task, host, num_clients=1, hatch_rate=10, timeout='3m'):
        '''
        开始执行所输入的压测任务
        ``task`` 任务类型的数组
        ``host`` 测试接口的域名
        ``num_clients`` 模拟的用户数量， 默认为1
        ``hatch_rate`` 请求发起的速率，默认为10
        ``runtime`` 运行时间，如果超出这个时间执行将被结束
        '''
        num_requests = int(num_clients) * int(hatch_rate)
        return LocustWorker().run(task=task, host=host, num_requests=num_requests, num_clients=num_clients, hatch_rate=hatch_rate, timeout=timeout)

    @keyword("Locust Run Web")
    def run_locust_web(self, task, host):
        LocustWorker().run_with_web(task=task, host=host)

class LocustWorker(object):
    start_time = None
    end_time = None
    '''
    创建`locust`HTTP任务的核心方法
    `method` 请求方法
    `path` 请求路径
    `header` 请求头
    `body` 请求体
    '''
    @staticmethod
    def build_locust_core_task(method, path='/', header={}, body=None):
        task_name = fetch_task_name()
        user_name = fetch_user_name()
        if header is dict:
            header.update({'souche-test': 'pressure'})
        else:
            header = {'souche-test': 'pressure'}
        strong_header = get_doraemon_headers(headers=header)
        if method == 'GET':
            base_task = LocustGetTask
        elif method == 'POST':
            base_task = LocustPostTask
        elif method == 'PUT':
            base_task = LocustPutTask
        elif method == 'DELETE':
            base_task = LocustDeleteTask
        else:
            AssertionError("不支持%s的请求方式" % method)
        task_cls = type(task_name, (base_task,), {'path': path, 'header': strong_header, 'body': body})
        locust_excutor = type(user_name, (HttpLocust,), {'task_set': task_cls, 'max_wait': 2000, 'stop_timeout': 7000})
        locust_excutor.task = task_cls
        Locust_Task_Pool.append(locust_excutor)
        return locust_excutor

    def stats(self):
        '''
        Returns the statistics from the load test in JSON
        '''
        statistics = {
            'requests': [],
            'num_requests_success': runners.locust_runner.stats.num_requests,
            'num_requests_fail': runners.locust_runner.stats.num_failures,
            'locust_host': runners.locust_runner.host,
            'start_time': self.start_time,
            'end_time': self.end_time
        }
        def parser_path_query(name):
            '''
            Extra path and query from url
            '''
            path_and_query = name[0].split('?')
            if len(path_and_query) > 1:
                return (path_and_query[0], path_and_query[1])
            else:
                return (path_and_query[0], None)

        for name, value in runners.locust_runner.stats.entries.items():
            current_requests = statistics['requests']
            (path, query) = parser_path_query(name[0])
            target = {
                'api': path,
                'request_type': name[1],
                'success': {
                    'num_requests': value.num_requests,
                    'min_response_time': value.min_response_time,
                    'median_response_time': value.median_response_time,
                    'avg_response_time': value.avg_response_time,
                    'max_response_time': value.max_response_time,
                    'response_times': value.response_times,
                    'response_time_percentiles': {
                        55: value.get_response_time_percentile(0.55),
                        65: value.get_response_time_percentile(0.65),
                        75: value.get_response_time_percentile(0.75),
                        85: value.get_response_time_percentile(0.85),
                        95: value.get_response_time_percentile(0.95)
                    },
                    'total_rps': value.total_rps,
                    'total_rpm': value.total_rps * 60
                },
                'failure': None
            }
            if query:
                target['query'] = query
            current_requests.append(target)
            statistics['requests'] = current_requests

        for id, error in runners.locust_runner.errors.items():
            current_requests = statistics['requests']
            error_dict = error.to_dict()
            (path, query) = parser_path_query(name[0])
            target = {
                'api': path,
                'query': query,
                'request_type': name[1],
                'success': None,
                'failure': error_dict
            }
            current_requests.append(target)
            statistics['requests'] = current_requests
        Locust_Statistics.append(statistics)
        return statistics

    def run(self, task, host, num_requests=10, num_clients=1, hatch_rate=10, timeout='3m'):
        '''
        开始运行压测任务
        `task`: `Locust`任务对象
        `host`: 域名
        `num_requests`: 总共发起的请求数
        `num_clients`: 模拟用户数
        `hatch_rate`: 请求频率
        '''
        logger.info('num_requests: %d num_clients: %d hatch_rate: %d' % (num_requests, num_clients, hatch_rate))
        all_task = self.build_safe_tasks(task)
        options = self.build_options(host=host, num_clients=num_clients, hatch_rate=hatch_rate, num_requests=num_requests, run_time=timeout)
        def timelimit_stop():
            runners.locust_runner.quit()
        gevent.spawn_later(options.run_time, timelimit_stop)
        runners.locust_runner = runners.LocalLocustRunner(all_task, options)
        runners.locust_runner.start_hatching(wait=True)
        self.start_time = current_milli_time()
        runners.locust_runner.greenlet.join()
        self.end_time = current_milli_time()
        globalVaildator.host = host
        json_result = self.stats()
        append_to_result()
        for name, value in runners.locust_runner.stats.entries.items():
            max_response_time = "N/A"
            min_response_time = "N/A"
            median_response_time = "N/A"
            total_rps = "N/A"
            if value.min_response_time:
                min_response_time = value.min_response_time
            if value.median_response_time:
                median_response_time = value.median_response_time
            if value.max_response_time:
                max_response_time = value.max_response_time
            if value.total_rps:
                total_rps = int(value.total_rps)
            logger.info("[压测报告]==> 接口:%s 请求方式:%s 最快响应时间:%s ms 平均响应时间:%s ms 最慢响应时间:%s ms 每秒请求数:%s" % (name[0], name[1], str(min_response_time), str(median_response_time), str(max_response_time), str(total_rps)))
            globalVaildator.vaildate(name[0], value)
        for error in runners.locust_runner.errors.values():
            raise AssertionError(error.error)
        reset_name_pool()
        return json_result

    def run_with_web(self, task, host):
        '''
        开始运行压测任务，并且打开本地Web监视器
        `task`: `Locust`任务对象
        `host`: 域名
        '''
        all_task = self.build_safe_tasks(task)
        options = self.build_options(host=host)
        logger.info("Web本地监视器已运行: %s:%s" % (options.web_host or "*", str(options.port)))
        main_greenlet = gevent.spawn(web.start, all_task, options)
        runners.locust_runner = runners.LocalLocustRunner(all_task, options)
        main_greenlet.join()

    def build_safe_tasks(self, task):
        if task is None:
            all_task = Locust_Task_Pool
        elif inspect.isclass(task) and issubclass(task, HttpLocust):
            all_task = [task]
        else:
            all_task = task
        return all_task

    def build_options(self, host, web_host='', port=8089, num_clients=0, hatch_rate=0, num_requests=0, run_time=None):
        '''
        The factory for build standard options control
        '''
        options = Namespace()
        options.host = host
        options.web_host = web_host
        options.port = port
        options.reset_stats = False
        options.num_clients = int(num_clients)
        options.hatch_rate = int(hatch_rate)
        options.num_requests = int(num_clients)
        options.run_time = None
        if run_time:
            raw_runtime = parse_timespan(run_time)
            if raw_runtime > 600:
                raw_runtime = 600
            options.run_time = raw_runtime
        return options

def fetch_task_name():
    '''
    从`task`命名池中获取一个`task name`
    '''
    return '__rf_locust_task' + str(len(Locust_Task_Pool))

def fetch_user_name():
    '''
    从`user`命名池获取一个`user name`
    '''
    name = '__rf_locust_user' + str(len(Locust_User_Pool))
    Locust_User_Pool.append(name)
    return name

def reset_name_pool():
    '''
    清空命名池
    '''
    Locust_Task_Pool.clear()
    Locust_User_Pool.clear()

def append_to_result():
    '''
    将一个json对象写入到文本中
    '''
    root = '%s/result' % os.getcwd()
    if not os.path.exists(root):
        os.mkdir(root)
    with open('%s/load-test.json' % root, 'w+') as f:
        result = {
            'executions': Locust_Statistics
        }
        f.write(json.dumps(result))

class LocustVaildator(object):
    # 最快响应阈值，毫秒级别
    rd_min_threshold = {}
    # 平均响应阈值，毫秒级别
    rd_ave_threshold = {}
    # 最慢响应阈值，毫秒级别
    rd_max_threshold = {}

    def __init__(self):
        self._host = None
    
    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self.vaildateHost(value)
        self._host = value

    def vaildateHost(self, host):
        if not host:
            raise AssertionError('不得使用空域名')
        if host.startswith('https'):
            raise AssertionError('不得使用线上环境进行压力测试!')
        if 'prepub' in host:
            raise AssertionError('不得使用预发环境进行压力测试!')
        

    # 核心验证行为
    def vaildate(self, url, result):
        if not result: return
        try:
            if self.rd_min_threshold[url]:
                assert int(self.rd_min_threshold[url]) >= int(result.min_response_time), '接口: %s%s ===> 最快响应不大于%s毫秒' % (self.host, url, str(self.rd_min_threshold[url]))
        except KeyError:
            pass
        try:
            if self.rd_ave_threshold[url]:
                assert int(self.rd_ave_threshold[url]) >= int(result.median_response_time), '接口: %s%s ===> 平均响应时间不能大于%s毫秒' % (self.host, url, str(self.rd_ave_threshold[url]))
        except KeyError:
            pass
        try:
            if self.rd_max_threshold[url]:
                assert int(self.rd_max_threshold[url]) >= int(result.max_response_time), '接口: %s%s ===> 最大响应时间不能大于%s毫秒' % (self.host, url, str(self.rd_max_threshold[url]))
        except KeyError:
            pass

globalVaildator = LocustVaildator()

class RobotBaseTask(TaskSet):
    path = None
    header = None
    body = None
    all_assets = []
    '''
    统一处理 Response
    '''
    def handle_response(self, response):
        try:
            for asset in self.all_assets:
                if callable(asset):
                    asset(self, response)
                else:
                    BuiltIn().run_keyword(asset, response)
        except Exception as e:
            response.failure(e)
            return
        response.success()
            

class LocustGetTask(RobotBaseTask):
    @task(1)
    def get(self):
        if not self.path:
            raise AssertionError("请求的Path为必传参数!")
        if len(self.all_assets) > 0:
            with self.client.get(self.path, headers=self.header, catch_response=True) as response:
                self.handle_response(response)
        else:
            self.client.get(self.path, headers=self.header)

class LocustPostTask(RobotBaseTask):
    @task(1)
    def post(self):
        if not self.path:
            raise AssertionError("请求的Path为必传参数!")
        if len(self.all_assets) > 0:
            with self.client.post(self.path, self.body, headers=self.header, catch_response=True) as response:
                self.handle_response(response)
        else:
            self.client.post(self.path, self.body, headers=self.header)

class LocustPutTask(RobotBaseTask):
    @task(1)
    def put(self):
        if not self.path:
            raise AssertionError("请求的Path为必传参数!")
        if len(self.all_assets) > 0:
            with self.client.put(self.path, self.body, headers=self.header, catch_response=True) as response:
                self.handle_response(response)
        else:
            self.client.put(self.path, self.body, headers=self.header)

class LocustDeleteTask(RobotBaseTask):
    @task(1)
    def delete(self):
        if not self.path:
            raise AssertionError("请求的Path为必传参数!")
        if len(self.all_assets) > 0:
            with self.client.delete(self.path, headers=self.header, catch_response=True) as response:
                self.handle_response(response)
        else:
            self.client.delete(self.path, headers=self.header)