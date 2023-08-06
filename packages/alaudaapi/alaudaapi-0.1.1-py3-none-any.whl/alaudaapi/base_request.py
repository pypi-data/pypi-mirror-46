# coding=utf-8
import json
import sys
import os
from time import sleep, time
from subprocess import getstatusoutput
# import pexpect
import requests
from alaudaapi import settings
from alaudaapi.api_requests import AlaudaRequest
from alaudaapi.exceptions import ResponseError, ParseResponseError
from alaudaapi.loadfile import FileUtils
from alaudaapi.log import logger
from alaudaapi.utils import Global_Map


class Common(AlaudaRequest):
    def __init__(self):
        super(Common, self).__init__()
        self.global_info = {}
        self.final_status = ["S", "F", "Running", "Error", "FAILURE", "failed", "FAIL", "Failed",
                             "CreateError", "StartError"]
        self.region_id = ""
        self.genetate_global_info()

    def genetate_global_info(self):
        self.global_info = FileUtils.load_file(self.global_info_path)
        self.region_id = self.global_info.get("$REGION_ID", "")

    def generate_data(self, file_path, data={}):
        """
        对指定文件替换数据，生成最终测试数据
        :param file_path: 指定测试文件路径
        :param data: 需要替换的数据，传入字典类型，key为文件中被替换的内容，value为替换的字符串
        :return: 最终测试数据 类型是字符串
        """
        self.global_info.update(data)
        content = json.dumps(FileUtils.load_file(file_path))
        for key in self.global_info:
            if isinstance(self.global_info[key], str):
                content = content.replace(key, self.global_info[key])
        return content

    def make_file(self, file, data):
        with open(file, "r") as f:
            content = f.read()
        for key in data:
            content = content.replace(key, data[key])
        filename = file.split("/")[-1]
        if not os.path.exists("temp_data"):
            os.mkdir("temp_data")
        to_file = "temp_data/" + filename
        with open(to_file, "w") as f:
            f.write(content)
        return to_file

    @staticmethod
    def get_value(json_content, query, delimiter='.'):
        """ Do an xpath-like query with json_content.
        @param (json_content) json_content
            json_content = {
                "ids": [1, 2, 3, 4],
                "person": {
                    "name": {
                        "first_name": "Leo",
                        "last_name": "Lee",
                    },
                    "age": 29,
                    "cities": ["Guangzhou", "Shenzhen"]
                }
            }
        @param (str) query
            "person.name.first_name"  =>  "Leo"
            "person.cities.0"         =>  "Guangzhou"
        @return queried result
        """
        if json_content == "" or json_content == []:
            raise ResponseError("response content is {}!".format(json_content))

        try:
            for key in query.split(delimiter):
                if isinstance(json_content, list):
                    json_content = json_content[int(key)]
                elif isinstance(json_content, dict):
                    json_content = json_content[key]
                else:
                    raise ParseResponseError(
                        "response content is in text format! failed to query key {}!".format(key))
        except (KeyError, ValueError, IndexError):
            logger.error("query is {}, json_content is {}".format(query, json_content))
            raise ParseResponseError("failed to query json when extracting response! response: {}".format(json_content))

        return json_content

    @staticmethod
    def get_value_list(data, query, delimiter='.'):
        """
        get value from dict or list
        :param data: 需要被解析的数据
        :param keys: 通过这些keys来解析数据,如果字典传key，如果数据传下标
        :example data = {"key1":{"key2":[{"key3":"key4"},{"key3":"key5"}]}}
        期望获取到key4的值 keys = ["key1","key2", 0, "key3"]
        """
        keys = query.split(delimiter)
        if len(keys) > 1:
            value = Common.get_value(data, delimiter.join(keys[0:-1]))
            list_data = value
        else:
            list_data = data
        ret_list = []
        for data in list_data:
            if keys[-1] in data:
                ret_list.append(data[keys[-1]])
        return ret_list

    @staticmethod
    def generate_time_params():
        current_time = int(time())
        return {"start_time": settings.START_TIME, "end_time": current_time}

    # @staticmethod
    # def generate_time_audit():
    #     current_time = int(time())
    #     return {"start_time": settings.START_TIME, "end_time": current_time}

    # @staticmethod
    # def generate_time_events():
    #     current_time = int(time())
    #     return {"start_time": settings.START_TIME, "end_time": current_time}

    def get_status(self, url, key, expect_value, delimiter='.', params={"project_name": settings.PROJECT_NAME},
                   auth=None):
        """
        :param url: 获取服务或者构建详情的url
        :param key: 获取状态的key 需要是个string，传入层级的key
        :param expect_value:最终判断状态
        :return: true or false
        """
        cnt = 0
        fail_cnt = 0
        flag = False
        while cnt < 120 and not flag:
            cnt += 1
            response = self.send(method="GET", path=url, params=params, auth=auth)
            assert response.status_code == 200, "get status failed"
            value = self.get_value(response.json(), key, delimiter)
            logger.info(value)
            if value == expect_value:
                flag = True
                break
            if value in self.final_status:
                fail_cnt += 1
                if fail_cnt > 2:
                    break
            sleep(5)
        return flag

    def get_logs(self, url, expect_value):
        cnt = 0
        flag = False
        while cnt < 30 and not flag:
            cnt += 1
            params = Common.generate_time_params()
            params.update({"project_name": self.project_name})
            response = self.send(method="GET", path=url, params=params)
            assert response.status_code == 200, "get log failed"
            logger.info("log: {}".format(response.text))
            if expect_value in response.text:
                flag = True
                break
            sleep(5)
        return flag

    def get_uuid_accord_name(self, contents, name, uuid_key):
        """
        方法丑陋 欢迎指正
        :param contents: 通过返回体获取到的列表数组 [{"key":""value"...},{"key":""value"...}...]
        :param name: 资源名称的一个字典:{"name": "resource_name"}
        :param uuid_key: 资源uuid的key
        :return: 资源的uuid
        """
        if type(contents).__name__ == 'list':
            for content in contents:
                for key, value in name.items():
                    if content[key] == value:
                        return content[uuid_key]
        elif type(contents).__name__ == 'dict':
            for key, value in name.items():
                if contents[key] == value:
                    return contents[uuid_key]
        return ""

    def update_result(self, result, flag, case_name):
        """
        如果是非block的验证点，先将结果更新到result内，在最后判断case的执行结果
        :param result: 最终用来判断case执行成功与失败的集合 :{"flag":True/False, case_name: "failed"}
        :param flag: True/False
        :param error_name: case的名称
        :return: result
        """
        if not flag:
            result['flag'] = False
            result.update({case_name: "failed"})
        return result

    # def get_events(self, url, resource_id, operation):
    #     for i in range(0, 40):
    #         params = Common.generate_time_params()
    #         params.update({"project_name": self.project_name, "size": 20, "pageno": 1})
    #         repsponse = self.send(method='get', path=url, params=params)
    #         if repsponse.status_code != 200:
    #             return False
    #         content = repsponse.json().get("results", [])
    #         # logger.error("Requesting the api of events, got content{}".format(content))
    #
    #         for j in range(0, len(content)):
    #             if content[j].get("resource_id") == resource_id and content[j].get("detail", {}).get(
    #                     "operation") == operation:
    #                 return True
    #         sleep(3)
    #     return False

    def get_monitor(self, url, file, data):
        count = 0
        result = ''
        while count < 40:
            times = self.generate_time_params()
            count += 1
            data = self.generate_data(file, data)
            data = json.loads(data)
            data['start'] = times['start_time']
            data['end'] = times['end_time']
            response = self.send(method='post', path=url, data=json.dumps(data), params={})
            code = response.status_code
            content = response.json()
            result = response
            logger.info("get monitor code is {}, content is {}".format(code, content))
            if code == 200 and len(content) > 0:
                break
            sleep(3)
        return result

    def check_search_different_level_key(self, url, payload, count, keys, search_type1, key1, search_type2, key2):
        '''
        用来校验用不同级的搜索条件搜索日志或事件类型的数据，搜索结果是否正确
        count: 接口中对应的返回数据条数key值
        keys: 用来表示返回数据中的results,比如日志就是'logs'
        search_type1: 第一个查询条件
        key1: 第一个查询条件对应接口返回数据中的key值，类型为''
        search_type2: 第二个查询条件
        key2： 第二个查询条件对应接口返回数据中的key值，类型为''
        :return:
        '''
        cnt = 0
        flag = False
        while cnt < 40:
            cnt += 1
            payload.update(self.generate_time_params())
            results = self.send(method='get', path=url, params=payload)
            if results.status_code == 200 and self.get_value(results.json(), count) > 0:
                flag = True
                result = self.get_value(results.json(), keys)
                for i in range(len(result)):
                    if self.get_value(result[i], key1) != search_type1 or self.get_value(result[i],
                                                                                         key2) != search_type2:
                        flag = False
                break
            sleep(3)
        return flag

    # def check_search_same_level_key(self, url, payload, count, keys, search_type1, key1, search_type2):
    #     '''
    #     用来校验用同级的搜索条件搜索日志或事件类型的数据，搜索结果是否正确
    #     count: 接口中对应的返回数据条数key值
    #     keys: 用来表示返回数据中的results,比如日志就是'logs'
    #     search_type1: 第一个查询条件
    #     key1: 第一个查询条件对应接口返回数据中的key值，类型为''
    #     search_type2: 第二个查询条件
    #     :return:
    #     '''
    #     cnt = 0
    #     flag = False
    #     while cnt < 40:
    #         cnt += 1
    #         payload.update(self.generate_time_params())
    #         results = self.send(method='get', path=url, params=payload)
    #         if results.status_code == 200 and self.get_value(results.json(), count) > 0:
    #             flag = True
    #             result = self.get_value(results, keys)
    #             for i in range(len(result)):
    #                 if self.get_value(result[i], key1) != search_type1 and self.get_value(result[i],
    #                                                                                       key1) != search_type2:
    #                     flag = False
    #             break
    #         sleep(3)
    #     return flag

    def check_search_single_key(self, url, payload, count, keys, search_type, key):
        '''
        用来校验用一个搜索条件搜索日志或事件类型的数据，搜索结果是否正确
        count: 接口中对应的返回数据条数key值
        keys: 用来表示返回数据中的results,比如日志就是'logs'
        search_type: 查询条件
        key: 查询条件对应接口返回数据中的key值，类型为''
        :return:
        '''
        cnt = 0
        flag = False
        while cnt < 40:
            cnt += 1
            payload.update(self.generate_time_params())
            results = self.send(method='get', path=url, params=payload)
            if results.status_code == 200 and self.get_value(results.json(), count) > 0:
                flag = True
                result = self.get_value(results.json(), keys)
                for i in range(len(result)):
                    if self.get_value(result[i], key) != search_type:
                        flag = False
                break
            sleep(3)
        return flag

    def get_events_url(self, account=None):
        event_account = self.account
        if account:
            event_account = account
        return "v1/events/{}".format(event_account)

    def check_operation_events(self, operation, resource_name, resource_type, operator=None, auth=None):
        '''
        检验操作资源是否有事件
        :param auth: 认证
        :param operation:操作类型，比如创建删除等
        :param resource_name:操作对象，即操作资源的名称
        :param resource_type:对象类型，即操作资源的对象，例如告警、通知等等。
        :return:
        '''

        rel_operator = Global_Map.get_value("audit_event_operator")

        if rel_operator is None:
            rel_operator = self.account

        account = None
        if auth:
            account = auth[0]
        if operator is not None:
            rel_operator = operator
        logger.info("event verify data: operator: {}, operation: {}, resource_name: {}, resource_type: {}".format(
            rel_operator, operation, resource_name, resource_type
        ))
        url = self.get_events_url(account=account)
        cnt = 0
        flag = False
        while cnt < 40:
            cnt += 1
            params = self.generate_time_params()
            params.update({"pageno": 1, "size": 20, "query_string": resource_type})
            results = self.send(method='get', path=url, params=params, auth=auth)
            if results.status_code == 200 and self.get_value(results.json(), 'total_items') > 0:
                result = self.get_value(results.json(), 'results')
                for i in range(len(result)):
                    if self.get_value(result[i], 'detail.operator') == rel_operator and \
                                    self.get_value(result[i], 'detail.operation') == operation and \
                                    self.get_value(result[i], 'resource_name') == resource_name and \
                                    self.get_value(result[i], 'resource_type') == resource_type:
                        flag = True
                        return flag
            sleep(3)
        return flag

    def get_audit_url(self, account=None):
        audit_account = self.account
        if account:
            audit_account = account
        return "v1/audits/{}".format(audit_account)

    def check_operation_audits(self, operation, resource_name, resource_type, auth=None, operator=None):
        '''
        检验操作资源是否有审计
        :param operation:操作类型，比如创建删除等
        :param resource_name:操作对象，即操作资源的名称
        :param resource_type:对象类型，即操作资源的对象，例如告警、通知等等。
        :return:
        '''
        rel_operator = Global_Map.get_value("audit_event_operator")
        if rel_operator is None:
            rel_operator = self.account
        account = None
        if auth:
            account = auth[0]
        if operator is not None:
            rel_operator = operator
        logger.info("event verify data: operator: {}, operation: {}, resource_name: {}, resource_type: {}".format(
            rel_operator, operation, resource_name, resource_type
        ))
        url = self.get_audit_url(account=account)
        cnt = 0
        flag = False
        while cnt < 40:
            cnt += 1
            params = self.generate_time_params()
            params.update({"user_name": rel_operator, "operation_type": operation, "resource_name": resource_name,
                           "resource_type": resource_type})
            results = self.send(method='get', path=url, params=params, auth=auth)
            if results.status_code == 200 and self.get_value(results.json(), 'total_items') > 0:
                result = self.get_value(results.json(), 'results')
                for i in range(len(result)):
                    if self.get_value(result[i], 'detail.operator') == rel_operator and \
                                    self.get_value(result[i], 'detail.operation') == operation and \
                                    self.get_value(result[i], 'resource_name') == resource_name and \
                                    self.get_value(result[i], 'resource_type') == resource_type:
                        flag = True
                        return flag
            sleep(3)
        return flag

    # def commands(self, ip, service_uuid, pod_instance, app_name):
    #     if self.sub_account:
    #         cmd = 'ssh -p 4022 -t {}/{}@{} {}/{}/{}/{} /bin/sh'.format(self.account, self.sub_account, ip,
    #                                                                    self.account, service_uuid, pod_instance,
    #                                                                    app_name)
    #     else:
    #         cmd = 'ssh -p 4022 -t {}@{} {}/{}/{}/{} /bin/sh'.format(self.account, ip, self.account, service_uuid,
    #                                                                 pod_instance, app_name)
    #     return cmd

    # def login_container(self, ip, service_uuid, pod_instance, app_name):
    #     cmd = self.commands(ip, service_uuid, pod_instance, app_name)
    #     logger.info("exec command: {}".format(cmd))
    #     child = pexpect.spawn(cmd)
    #     ret = child.expect([pexpect.EOF, pexpect.TIMEOUT, 'yes/no', 'password:'])
    #     if ret == 0:
    #         logger.error('ssh connect terminated: {}'.format(pexpect.EOF))
    #         return
    #     elif ret == 1:
    #         logger.error('ssh connect timeout: {}'.format(pexpect.TIMEOUT))
    #         return
    #     elif ret == 2:
    #         child.sendline('yes')
    #         rev = child.expect([pexpect.EOF, pexpect.TIMEOUT, 'password:'])
    #         if rev == 0:
    #             logger.error('ssh connect terminated: {}'.format(pexpect.EOF))
    #             return
    #         elif rev == 1:
    #             logger.error('ssh connect timeout: {}'.format(pexpect.TIMEOUT))
    #             return
    #         elif rev == 2:
    #             child.sendline(self.password)
    #             r = child.expect([pexpect.EOF, pexpect.TIMEOUT, '#'])
    #             if r == 0:
    #                 logger.error('ssh connect terminated: {}'.format(pexpect.EOF))
    #                 return
    #             elif r == 1:
    #                 logger.error('ssh connect timeout: {}'.format(pexpect.TIMEOUT))
    #                 return
    #             elif r == 2:
    #                 return child
    #     elif ret == 3:
    #         child.sendline(self.password)
    #         r = child.expect([pexpect.EOF, pexpect.TIMEOUT, '#'])
    #         if r == 0:
    #             logger.error('ssh connect terminated: {}'.format(pexpect.EOF))
    #             return
    #         elif r == 1:
    #             logger.error('ssh connect timeout: {}'.format(pexpect.TIMEOUT))
    #             return
    #         elif r == 2:
    #             return child

    # def send_command(self, service_uuid, pod_instance, app_name, command):
    #     ip = self.global_info['$HAPROXY_IP']
    #     child = self.login_container(ip, service_uuid, pod_instance, app_name)
    #     if child:
    #         child.sendline(command)
    #         ret = child.expect('#')
    #         logger.info(child.before)
    #         return ret

    def check_exists(self, url, expect_status, params={"project_name": settings.PROJECT_NAME}, expect_cnt=60):
        '''
        主要用于判断资源是否存在
        :param url: 获取资源的url
        :param expect_status: 期望返回的code
        :return:
        '''
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        cnt = 0
        flag = False
        while cnt < expect_cnt and not flag:
            cnt += 1
            response = self.send(method="GET", path=url, params=params)
            if response.status_code == expect_status:
                flag = True
            sleep(5)
        return flag

    def check_value_in_response(self, url, value, params={"project_name": settings.PROJECT_NAME}, expect_cnt=60):
        '''
        主要用于判断创建后的资源是否在资源列表中，
            个别资源创建后会延时出现在列表中，需要循环获取
        :param url: 获取资源列表的url
        :param value: 资源名称
        :return:
        '''
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        cnt = 0
        flag = False
        while cnt < expect_cnt and not flag:
            cnt += 1
            response = self.send(method="GET", path=url, params=params)
            assert response.status_code in (200, 404), "get list failed"
            if value in response.text:
                flag = True
                break
            sleep(5)
        return flag

    @staticmethod
    def access_service(url, query=None, auth=None):
        logger.info("************************** access service ********************************")
        try:
            ret = requests.request(method='get', url=url, auth=auth)
            if query:
                if ret.status_code == 200 and query in ret.text:
                    return True
            else:
                if ret.status_code == 200:
                    return True
        except Exception as e:
            logger.error("access service failed: {}".format(e))
        return False

    @staticmethod
    def log_info(func):
        def wrapper(*args, **kwargs):
            logger.info(func.__name__.center(50, '*'))
            return func(*args, **kwargs)

        return wrapper

    def excute_script(self, cmd, ip):
        '''
        主要用于远程在虚拟机执行脚本
        :param cmd: 远程需要执行的命令
        :param ip：虚拟机IP
        :return:
        '''
        if os.path.exists(settings.VM_PEM):
            remote_cmd = "ssh -i {} -o StrictHostKeyChecking=no {}@{} '{}'".format(settings.VM_PEM,
                                                                                   settings.VM_USERNAME,
                                                                                   ip, cmd)
        else:
            remote_cmd = "sshpass -p {} ssh -o StrictHostKeyChecking=no {}@{} '{}'".format(settings.VM_PASSWORD,
                                                                                           settings.VM_USERNAME,
                                                                                           ip, cmd)
        logger.info("excute cmd is :{}".format(remote_cmd))
        result = getstatusoutput(remote_cmd)
        logger.info("excute cmd result is {}".format(result))
        return result

    def copy_file_to_vm(self, files, ip):
        for file in files:
            if os.path.exists(settings.VM_PEM):
                copy_cmd = "scp -o StrictHostKeyChecking=no -i {} {} {user}@{ip}:/{user}/".format(settings.VM_PEM, file,
                                                                                                  user=settings.VM_USERNAME,
                                                                                                  ip=ip)
            else:
                copy_cmd = "sshpass -p {} scp -o StrictHostKeyChecking=no {} {user}@{ip}:/{user}/".format(
                    settings.VM_PASSWORD, file,
                    user=settings.VM_USERNAME,
                    ip=ip)
            logger.info("excute cmd is :{}".format(copy_cmd))
            result = getstatusoutput(copy_cmd)
            logger.info("excute cmd result is {}".format(result))

    def access_app_shell(self, alb_address, domain, http_port, path="", params={}, header={}, cookie=""):
        """
        :param alb_address: the alb address (string)
        :param domain: domain (string)
        :param http_port: http port (number)
        :param path: request path (string)
        :param params: query params (dict)
        :param header: request header (dict)
        :param cookie: cookie (string)
        :return:
        """
        query_params = ''
        for key, value in params.items():
            query_params = query_params + '{}={}&'.format(key, value)

        query_params = query_params.strip('&')

        headers = ''
        for key, value in header.items():
            headers = headers + '-H "{}:{}" '.format(key, value)

        headers = headers.strip()

        cookies = ''
        if cookie:
            cookies = '-b "{}"'.format(cookie)

        return 'echo "{}  {}" >> /etc/hosts;sleep 3;curl -v http://{}:{}/{}?{} {} {} --connect-timeout 10;sleep 3;' \
               'sed -i "/{}/d" /etc/hosts'.format(alb_address, domain, domain, http_port, path, query_params,
                                                  headers,
                                                  cookies, domain)

    @staticmethod
    def is_weblab_open(weblab_name):
        global_info = FileUtils.load_file(settings.GLOBAL_INFO_FILE)
        if weblab_name in global_info.keys() and global_info[weblab_name]:
            return True
        else:
            return False

    def resource_pagination(self, url, query="results.0.name", params={"project_name": settings.PROJECT_NAME}):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        params.update({"page_size": 1, "page": 1})
        page1 = self.send(method="GET", path=url, params=params)
        if page1.status_code != 200:
            return False
        logger.info("列表1的结果:{}".format(page1.json()))
        name1 = self.get_value(page1.json(), query)
        params.update({"page_size": 1, "page": 2})
        page2 = self.send(method="GET", path=url, params=params)
        if page2.status_code != 200:
            return False
        logger.info("列表2的结果:{}".format(page2.json()))
        name2 = self.get_value(page2.json(), query)
        # 将params更新回20个一页
        if name1 == name2:
            return False
        return True

    def search_resource(self, url, name, total_count='count', search_key="name", query="kubernetes.metadata.name",
                        params={"project_name": settings.PROJECT_NAME}):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        params.update({"page_size": 20, "page": 1, search_key: name})
        result = self.send(method="GET", path=url, params=params)
        logger.info("search的结果:{}".format(result.json()))
        params.pop(search_key)
        if result.status_code != 200:
            return False
        # elif self.get_value(result.json(), total_count) != 1:
        #     return False
        # elif self.get_value(result.json(), query) != name:
        #     return False
        # else:
        #     return True
        contents = self.get_value(result.json(), "results")
        for content in contents:
            if self.get_value(content, query=query).find(name) < 0:
                return False
        return True
