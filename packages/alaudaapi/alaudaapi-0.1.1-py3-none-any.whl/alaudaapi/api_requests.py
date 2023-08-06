# coding=utf-8
import requests

from alaudaapi import settings
from alaudaapi.log import logger


class AlaudaRequest(object):
    def __init__(self):
        self.endpoint = settings.API_URL
        self.headers = settings.headers
        self.params = {"project_name": settings.PROJECT_NAME}
        if settings.CASE_TYPE == "cmb":
            self.account = settings.get_token()[1]
        else:
            self.account = settings.ACCOUNT
        self.sub_account = settings.SUB_ACCOUNT
        self.region_name = settings.REGION_NAME
        self.k8s_namespace = settings.K8S_NAMESPACE
        self.password = settings.PASSWORD
        self.registry_name = settings.REGISTRY_NAME
        self.global_info_path = settings.GLOBAL_INFO_FILE
        self.project_name = settings.PROJECT_NAME
        self.space_name = settings.SPACE_NAME
        self.case_type = settings.CASE_TYPE
        if self.sub_account:
            self.auth = ("{}/{}".format(self.account, self.sub_account), self.password)
        else:
            self.auth = (self.account, self.password)

    def send(self, method, path, auth=None, case_type=settings.CASE_TYPE, **content):
        """
        使用和原生的requests.request一致，只是对url和auth params做了些特殊处理
        :param method:
        :param path:
        :param auth:
        :param content:
        :return:
        """
        url = self._get_url(path)
        if case_type == "cmb":
            pass
        else:
            if auth:
                content["auth"] = auth
            else:
                content["auth"] = self.auth

        if "headers" not in content:
            content["headers"] = self.headers

        # if content.get("data") is not None and content["headers"]["Content-Type"] == "application/json":
        #     content["json"] = content["data"]
        #     content.pop("data")
        if "params" not in content:
            content["params"] = self.params

        logger.info("Requesting url={}, method={}, args={}".format(url, method, content))
        response = requests.request(method, url, **content)
        if response.status_code < 200 or response.status_code > 300:
            logger.error("response code={}, text={}".format(response.status_code, response.text))
        else:
            logger.info("response code={}".format(response.status_code))

        return response

    def _get_url(self, path):
        return "{}/{}".format(self.endpoint, path)
