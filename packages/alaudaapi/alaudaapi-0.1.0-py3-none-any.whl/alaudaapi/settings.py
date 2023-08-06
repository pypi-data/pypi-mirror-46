import os
import json
from time import time

import requests


def get_list_from_str(string, separator=','):
    if string is not None and string != '':
        return string.split(separator)


# necessary
API_URL = os.getenv("API_URL", "http://192.144.193.251:32001")
ACCOUNT = os.getenv("ACCOUNT", "alauda")
SUB_ACCOUNT = os.getenv("SUB_ACCOUNT", "")
PASSWORD = os.getenv("PASSWORD", "Alauda2018!@#")
REGION_NAME = os.getenv("REGION_NAME", "high")
REGISTRY_NAME = os.getenv("REGISTRY_NAME", "high")
GLOBAL_REGISTRY = os.getenv("GLOBAL_REGISTRY", "10.0.128.137:60080")
# not necessary
TESTCASES = os.getenv("TESTCASES", "")
CASE_TYPE = os.getenv("CASE_TYPE", "BAT")
PROJECT_NAME = os.getenv("PROJECT_NAME", "e2e3")
ENV = os.getenv("ENV", "Staging")
RECIPIENTS = get_list_from_str(os.getenv("RECIPIENTS", "testing@alauda.io"))
# 权限测试
PERMISSION_ENABLED = os.getenv("PERMISSION_ENABLED", "true")
PERMISSION_USER = "permissiontestuser"
PERMISSION_PASSWORD = "123456"
PERMISSION_ROLE = "permissiontestrole"
PARENT_ROLE = "parentrole"
# 事件审计测试（测试开始时间）
START_TIME = int(time())
# 测试使用镜像
REPO_NAME = "hello-world"
REPO_PROJECT = "e2etest4"

VM_IPS = os.getenv("VM_IPS",
                   "62.234.83.246;192.144.176.3;62.234.76.94;62.234.104.179;62.234.82.217;62.234.76.202").split(";")
VM_USERNAME = os.getenv("VM_USERNAME", "root")
VM_PASSWORD = os.getenv("VM_PASSWORD", "07Apples")
VM_PEM = "./key.pem"

RERUN_TIMES = int(os.getenv("RERUN_TIMES", 2))

REGISTRY_CREDENTIAL = os.getenv("REGISTRY_CREDENTIAL", "alauda-registry-credential")

JENKINS_ENDPOINT = os.getenv("JENKINS_ENDPOINT",
                             "http://192.144.148.212:8899")
JENKINS_USER = os.getenv("JENKINS_USER", "admin")
JENKINS_TOKEN = os.getenv("JENKINS_TOKEN", "ebc372b57c4ac531f74949a4d71f5325")

SONAR_ENDPOINT = os.getenv("SONAR_ENDPOINT",
                           "http://192.144.148.212:10007")
SONAR_USER = os.getenv("SONAR_USER", "alauda")
SONAR_TOKEN = os.getenv("SONAR_TOKEN", "fe2fce6760ff3170bc99ba84a2a66eada043a9ab")

SVN_REPO = os.getenv("SVN_REPO", "http://192.144.148.212:10009/alauda_test/")
SVN_CREDENTIAL = os.getenv("SVN_CREDENTIAL", "alauda-svn-credential")
SVN_USERNAME = os.getenv("SVN_USERNAME", "User_Name-01")
SVN_PASSWORD = os.getenv("SVN_PASSWORD", "alauda_Test-!@#")

GIT_REPO = os.getenv("GIT_REPO",
                     "http://192.144.148.212:31111/root/test123")
GIT_CREDENTIAL = os.getenv("GIT_CREDENTIAL", "alauda-git-credential")
GIT_USERNAME = os.getenv("GIT_USERNAME", "root")
GIT_PASSWORD = os.getenv("GIT_PASSWORD", "07Apples")

# 应用目录添加git类型用的git参数
GIT_PATH = os.getenv("GIT_PATH", "/catalog")
GIT_BRANCH = os.getenv("GIT_BRANCH", "master")

K8S_NAMESPACE = os.getenv("K8S_NAMESPACE", "{}-{}".format(PROJECT_NAME, REGION_NAME).replace("_", "-"))
SPACE_NAME = os.getenv("SPACE_NAME", "{project_name}-{space_name}".format(
    project_name=PROJECT_NAME,
    space_name="e2espace"
).replace("_", "-"))

SECRET_ID = os.getenv("SECRET_ID", "AKID84kBMHwKUP4VggjwBAKFvxlJcgU3frtg")
SECRET_KEY = os.getenv("SECRET_EKY", "aDlNSjBSZGRPdkxXUjZWZ2JHZnFPaGpXMklJa3d0WjA=")

OAUTH2_CLIENTID = os.getenv("OAUTH2_CLIENTID", "test")
OAUTH2_CLIENTSECRET = os.getenv("OAUTH2_CLIENTSECRET", "test")
DOCKER_ADDRESS = os.getenv("DOCKER_ADDRESS", "harbor.com")
DOCKER_USERNAME = os.getenv("DOCKER_USERNAME", "admin")
DOCKER_PASSWORD = os.getenv("DOCKER_PASSWORD", "password")
DOCKER_EMAIL = os.getenv("DOCKER_EMAIL", "a@b.com")

# 工具链需要的环境变量
JIRA_URL = os.getenv("JIRA_URL", "http://192.144.148.212:10004")
JIRA_USER = os.getenv("JIRA_USER", "admin")
JIRA_PASSWORD = os.getenv("JIRA_PASSWORD", "123456")
TAIGA_URL = os.getenv("TAIGA_URL", "http://192.144.148.212:10003")
TAIGA_USER = os.getenv("TAIGA_USER", "admin")
TAIGA_PASSWORD = os.getenv("TAIGA_PASSWORD", "123123")

# ceph 挂载的磁盘
CEPH_DISK = os.getenv("CEPH_DISK", "vdb")

OPENLDAP_IP = os.getenv("OPENLDAP_IP", "192.144.148.212")
OPENLDAP_PORT = os.getenv("OPENLDAP_PORT", "10001")
OPENLDAP_ADMIN = os.getenv("OPENLDAP_ADMIN", "cn=admin,dc=example,dc=org")
OPENLDAP_ADMIN_PASSWORD = os.getenv("OPENLDAP_ADMIN_PASSWORD", "admin")

SMTP = {
    'host': os.getenv('SMTP_HOST', 'smtpdm.aliyun.com'),
    'port': os.getenv('SMTP_PORT', 465),
    'username': os.getenv('SMTP_USERNAME', 'staging@alauda.cn'),
    'password': os.getenv('SMTP_PASSWORD', 'Ahvooy5ie22H0tel'),
    'sender': os.getenv('EMAIL_FROM', 'staging@alauda.cn'),
    'debug_level': 0,
    'smtp_ssl': True
}

# nfs服务器的地址
NFS_IP = os.getenv('NFS_IP', '10.0.128.198')
NFS_PATH = os.getenv('NFS_PATH', '/exported/path')
LOG_LEVEL = "INFO"
LOG_PATH = "./report"
TARGET_REPO_NAME = "sys-repo"
GLOBAL_INFO_FILE = "./temp_data/global_info.json"

# 招商环境变量
CMB_TP_NAME = os.getenv('TP_NAME', 'oidc')
IMAGE = os.getenv('IMAGE', '')


def get_token():
    url = "{}/v1/tp_sso/{}/login".format(API_URL, CMB_TP_NAME)
    data = {
        "grant_type": "password",
        "user_name": "{}".format(ACCOUNT),
        "password": "{}".format(PASSWORD)
    }
    print("request body: {}".format(data))
    ret = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    print("get token response: {} {}".format(ret.status_code, ret.json()))
    token = ret.json()["alauda_user_info"]["token"]
    namespace = ret.json()["alauda_user_info"]["namespace"]
    return token, namespace


if CASE_TYPE == "cmb":
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Token {}".format(get_token()[0])
    }
else:
    headers = {
        "Content-Type": "application/json"
    }

# https所需
tls_crt = "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUZWekNDQXorZ0F3SUJBZ0lKQUovdlJwN3dndFdTTUEwR0NTcUdTSWIzRFFFQkN3VUFNRUl" \
          "4Q3pBSkJnTlYKQkFZVEFsaFlNUlV3RXdZRFZRUUhEQXhFWldaaGRXeDBJRU5wZEhreEhEQWFCZ05WQkFvTUUwUmxabUYxYkhRZwpRMjl0Y0dGdW" \
          "VTQk1kR1F3SGhjTk1Ua3dOREF4TURjMU5UVXlXaGNOTWpBd016TXhNRGMxTlRVeVdqQkNNUXN3CkNRWURWUVFHRXdKWVdERVZNQk1HQTFVRUJ3d" \
          "01SR1ZtWVhWc2RDQkRhWFI1TVJ3d0dnWURWUVFLREJORVpXWmgKZFd4MElFTnZiWEJoYm5rZ1RIUmtNSUlDSWpBTkJna3Foa2lHOXcwQkFRRUZB" \
          "QU9DQWc4QU1JSUNDZ0tDQWdFQQpteTFHQlkzYy9qMmFKb2JodVUwRklFUk93WGtJUFk4Q3NVVlFRVnRnV2FmM0k4R3pRQm9PMTFYdk9DZVV0LzB" \
          "ECk1VL1hHbDdiNXo5YXJwN2svTGpCSXVQYnNyRDlsa2p4TDgxNmhaVjZhdERUWHkxeWVNcE1WTVdnaGtIMERiY1cKMThkYTRhUHgrZmZLNk1XS0" \
          "k4NEprQTRZUnhjVEpaTHVwOVREcUVjdEw4VzBNRWhhaWpVKzNvRTNlWFg5SlFvMApOQi9qenZORC8wQ3g0ZjNmSEx4Zkh4bzZFYm8yYUw5QXd2M" \
          "XRhbjkyazRYMkhJVG1lWFlCSXUrVys4V1h6SGViCmJvdytiSGZ1SFp5Q1FLcVJSQWVuQVBBSWZKVEhVcnZSZ1N5cHB5VFFKdG1QMXFHVXFwNUJh" \
          "d2lIUHBoNjAxNzcKbElpeDZRcVZwVzJ3V0djcUkvNWZDMHlQS24yL3NDb2h3ZDZ3MlJKYTY1OVhTb245TEFQZ0hhVFRNamdSU2czRQo2dDkzR0Z" \
          "ZYlBHdFNjcEw0Sm12Qy9Zd3djUlJsS3RhczZSUGs4c1p2Yi8zNkx3czBTbnV3UEFaYUk4djlHQktaCjNXdktIQmZOMEwrWWczSXc3dzhITWZ0bX" \
          "d1dkUrdTZZZ3RwUjhtY1k2Q3o4UDRsREx0M2hJcVZNSlhRSDV4dmcKY3NWL1Vac290aU90Yzd3YVpuVGx5Mmw4blhKN3RVclQyWk5sYmphWGF0V" \
          "VJRb3ZYQ0V3ZkJmeE1EdFhhbjVsYgpzVkZ5U1Y5Y2g4NGtNdWllUlpVTWZrNC84Q3BXR1IzMTg0MDhqMnZ4dmJKVW5hcUkrY1YveFIvSVpxSUgr" \
          "TWZICkNPYXVlWWZHWnNXRXBsbit6SjEyaDFPeXl2L1lwY2pVR1ozYlcrTFRBUjhDQXdFQUFhTlFNRTR3SFFZRFZSME8KQkJZRUZBNnhlbzd6Qk5" \
          "PRWhBbjN5ZjNrVDRGUnJqNy9NQjhHQTFVZEl3UVlNQmFBRkE2eGVvN3pCTk9FaEFuMwp5ZjNrVDRGUnJqNy9NQXdHQTFVZEV3UUZNQU1CQWY4d0" \
          "RRWUpLb1pJaHZjTkFRRUxCUUFEZ2dJQkFJMXlrbzZhClc2ODh3OHpGeTBlUEg0TmhINjJXaXBmVTc0OHlsNkJMRGpLYndDUStIb3h4V2lWbndSN" \
          "lZhSEJZbWEzL0pQNGIKNkoyYnpMZEFKYzg4Q3hKaTIyVDhjeiswWkN0T1g4dWY2TUJGaVEzTTJwQS85bDJGR1R3TlROUWZsT2tabXdpaAp4Y050" \
          "c2Qxdk1wL0wybXAwRWlnSm9QTTlYU2toUElrVXpPd1d0d1NpeC9rM05pNVVuU05FekV1ZlU3ZG01REhKCkN0QlpFRkptckplZk82cnZpSDNKc3J" \
          "6SlFjNEFGbmpiV3FSeUsyMFQyMVhwSDEwVng5bk9wTFlBRW0rN3BRR1kKZk9TL3ppSWNHRW92VC9tazZOL295ZXJSanJ2SVhlMm5EblplM3NTb3" \
          "duZXBPU084SVY4MlNYMThaK2NZb3VzSgpQUEY5TVpvWHNZL2g1QVBicG5pM0o1eExNQ2VEMEluVW1ERnhMOUh4ams1SVRZN3RlSEorRFU0d2VNN" \
          "WVRRkc1CndaR0dLWURwMlFVL1M1VEdIMG1sVTJGazRjOGF6V2hodTE2dE9LYnZFUTVUNlhOQm5GQ21iWXpXd256ZDF4TFoKNDFPTlRPaU9jalNi" \
          "Szg4T3NPekJEWklDdU5vV2xVRGp1bG93akY3d21kQWY4M1JNVzRPc2QrVVppUndqRlZqWQpmS3ZXQXo3NDFtTzBDb0Fhb0dVMHdHMjhLcndyeVp" \
          "kSEZNTkVmUUlESTJDNndzejNIOGFXcGRDVHlkYUc4bjkzCnk0bDhQdU1QeDRqZFVGYlZFYXNtYkQ3MWV3dU13Z1J4VzFOTUF6bFZSOWQ3WFNmVF" \
          "N5TWw0WXpLbUhIK25Rd0YKbXU0YkxBeXNxNXAxWmlKVVFSSmo0djlacSt6TFlWVE8vZHdpCi0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0="

tls_key = "LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JSUpRZ0lCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQ1N3d2dna29BZ0VBQW9JQ0FRQ2JMVVl" \
          "GamR6K1Bab20KaHVHNVRRVWdSRTdCZVFnOWp3S3hSVkJCVzJCWnAvY2p3Yk5BR2c3WFZlODRKNVMzL1FNeFQ5Y2FYdHZuUDFxdQpudVQ4dU1FaT" \
          "Q5dXlzUDJXU1BFdnpYcUZsWHBxME5OZkxYSjR5a3hVeGFDR1FmUU50eGJYeDFyaG8vSDU5OHJvCnhZb2p6Z21RRGhoSEZ4TWxrdTZuMU1Pb1J5M" \
          "HZ4YlF3U0ZxS05UN2VnVGQ1ZGYwbENqUTBIK1BPODBQL1FMSGgKL2Q4Y3ZGOGZHam9SdWpab3YwREMvVzFxZjNhVGhmWWNoT1o1ZGdFaTc1Yjd4" \
          "WmZNZDV0dWpENXNkKzRkbklKQQpxcEZFQjZjQThBaDhsTWRTdTlHQkxLbW5KTkFtMlkvV29aU3Fua0ZyQ0ljK21IclRYdnVVaUxIcENwV2xiYkJ" \
          "ZClp5b2ovbDhMVEk4cWZiK3dLaUhCM3JEWkVscnJuMWRLaWYwc0ErQWRwTk15T0JGS0RjVHEzM2NZVmhzOGExSnkKa3ZnbWE4TDlqREJ4RkdVcT" \
          "FxenBFK1R5eG05di9mb3ZDelJLZTdBOEJsb2p5LzBZRXBuZGE4b2NGODNRdjVpRApjakR2RHdjeCsyYkM2OFQ2N3BpQzJsSHlaeGpvTFB3L2lVT" \
          "XUzZUVpcFV3bGRBZm5HK0J5eFg5Um15aTJJNjF6CnZCcG1kT1hMYVh5ZGNudTFTdFBaazJWdU5wZHExUkZDaTljSVRCOEYvRXdPMWRxZm1WdXhV" \
          "WEpKWDF5SHppUXkKNko1RmxReCtUai93S2xZWkhmWHpqVHlQYS9HOXNsU2Rxb2o1eFgvRkg4aG1vZ2Y0eDhjSTVxNTVoOFpteFlTbQpXZjdNblh" \
          "hSFU3TEsvOWlseU5RWm5kdGI0dE1CSHdJREFRQUJBb0lDQVFDTHpPN3ZwQTQ4RXYya3hoSG9Ja2FDCittZEZrS2ZtNWNlVU01RUpRS3grT1gvQy" \
          "9BaGtzTlU4RlJTT3I4SWhQRlc3QUdZWFFPeTIybkgxTGZ1NDN5NUoKSTZWVHlIYStCWHNkQ083Z0dIb1FiNUJ1aUFCQWFHajZXbzJ6UnduN3JUN" \
          "XNLaE5yZzR0R0c0TDMwTGdTWjlaZgpyUU1jVU9LVUVGcm9ZeHZlcURsQ2Q4aE5VM0lXWDhBREw4RHRzV25lQytKYUwzektmb2w5Rmlqc0pBNzAw" \
          "WlNVCjdjanhIYVZWR3pEYU92MXZXK1JWSmZSRFgweFFrd3FWRWVzaGFyUEdwdDhtYWp6MjlkbFZYaUpPNWh3M2dQbHAKTTlkQmZieFJnaHBPV1J" \
          "HREh2eFVjOTlOaTRibmErb2Q1cklKcDgvSVRDTTFmeTFoZVlLMlppcmdpaGtDRW5KRwowWVhsZkNRektYVmQ0elF5SXJhdUo5ZXJMd2wvWkYwYX" \
          "AxQWk3K2hQd1NjejlxbXVsTWEwSHNMcUlyVitGcXllCmZ1TUxtQURmckRSSjYxMHU4cEdFQ0UvZit5UzNGQVJ3OG8zb0tYQlNHU2cwVWd5ZktjS" \
          "klXTXkvQzIwcEpHdC8KRGNERURjdzVtM3ZQaU5hNDllUTdQZzUvdFRROGYrbkovdXEzeUdvUldJNG9CbFVob2dGaXdwdEJlU0swSGRHbApqazFu" \
          "NW91WXdjSWEvckJMQlNSZTN2Ly8vRTlndWw1TjJIRStkYjhCb05hTTdLeWRaN1R2SHRZbjhRS1JUSVM1CmVYU0NFbUp5WHV2L241MU9GUDdoVzZ" \
          "KOWdwc05zUXUxTFhuNkNWa0ZIaUtqdm9ydWZWbWs1TFRwYzlnOWp1cDIKcHdVZXdlYkFpNUQ4WWJJUEJXaXdTUUtDQVFFQXlwcEFsU0o2ZXVLWl" \
          "N4WXd1bEpXT2R3TmFma3RKenNVV09hbApkNXQ1NHVVS0poQkJZMzIyS1EvUDQ2Tk5paDRDbW9qSXNxQzhFUG5RQVZ2SG56VGVXRitxT2l3RWdvW" \
          "StkRGpuCmFiY1ovbE5zZlUxUjFPWSs2ZTZHQ2ROQjNTUnhNQ2I2THhtRm9BbkI1QXZXcjBZaXhaUGJGTC9JV2p4M2NKWkIKd0VpZEU0S1ZoZkxC" \
          "T252am9MWkdZN0E2cG5PdEJGay9NRW9XTXpWYlJpM29YekNkMjdDVUVhNU0rRGJLT0dOTwp5K2hPV0Juc25sMlNKckJiV1pRT0t5dktpazQ1aDN" \
          "zTW5BSGZ4T3dOMytkS0RaSkU1RmZVTjdqVXhzSHl6UXVWCkp5bkYza2JIMGNzZTU2SldUd1REbCtaV3M3MWtZUldoTHdiRkErRytvZG5HQlJwL1" \
          "hRS0NBUUVBeEJNc1lxU1QKTUNUai9YUkhuY3czYTJWdkRhZWZrZHpTS1JMV29CZWJHVzFuSmZqbVFvWDM1eStwa1VYVlJ4TFphYkNZbTZQTgpmZ" \
          "2h2WU9OVndoT01Xb1ZDVGcrNXhGYWtGbzg3aTZwWTNXdmRxeWs2cTVVWTl1dGNtODBIOE8yU3dVMjJMVjZkCjlOczNSbTcyRmJUQTdaa3Bxc0FW" \
          "L2pZY0tmNWNGZS9aK0h0NzdKcW10ZnQ1bytlYldpZ3U0ZkhyZWJMa1NJMWwKZ2JSTW5rcUxteTM3NTBvRzVYS05wWW1kdjA3NDBRWWF2dURBUWp" \
          "pd2oyYUtoSVdqaHdhc1l6bHFMQkVuV3c5YQoyRU5iZzIrMEZrQkMxOVNXdjlHMVhWTmpuOThHbEZHcUJuR1Q5dUszYklmdlFmUmQ4YjVFOXhjbT" \
          "YrdWUrNGkrClpkci9vVWIxdGpiR3F3S0NBUUJVRTlGclVtU2JySC9MSGtsWWVTVFpYQTJoQmN3TU5NTkw1V09Ua0V6enNQTVcKT3JhNEVBcFJYZ" \
          "042eDJFOVNSanhnb1F2Uk83bTZKUytpNVQ2NTlqQnVlbU52SWllbGhGQzcvNXc2NUI0NzZ2ZApFQUkrcE5KRkNEeE54WUxXdi9ITTlzL3FUZUFi" \
          "T3hGZ2p0MG4zYVkrY2c1L3ZOcnJQNTZkZFcyUjIxQjhNVHZWCjI1aitxVDBjaTZnSVpMRGlOS3ovV2Y0VUR4ckpZNEllVEp6YksvVEduNi9DNnA" \
          "5OGZsaExNRU1aOGF6WmVPQ3UKRTh5OEM0SE5XZGpMWjUvazUzT09XcTB2N01NdEdIemxoemsvQ28xV2FYQmpNMnZ4azdrc0NIdDhSaVNjQ3FtUA" \
          "owWWhndmdpdFFCL2ZZTEpvWXRkT1JzaWVHR1FZS1UyUUl5eS9IM0R0QW9JQkFCdTZhbWg0eGFmbFQ2aWtMUXlQCnVMYWpYWlVjdzJBcFRqOG92d" \
          "GxjL1Q0WFRxTDhFL1FNWmdaM293ODhSUEVNSlZyZzhuUHdNanRFamh1eGlvc3IKb0ltY2xzZmJTWFlPbXAzbUc1R2d3WGh1cktacjZqUWhuYW90" \
          "bHFjaDA2R3F0enBHOXlCclpRTWZqUzJVdTVCTwpRNHBXUXFJM0QrVW5XY3hHZ0ZkSjJCVmZ3U0t3ckNySUtXZVlkVXZHcXZxZzc2QUNRRzVTTUt" \
          "5ckJyckw1L3BHCkFuMnU1bExFWkd1b2pucGpmS1J5ckkyWjB4YUtWYzJ4dnAwSEdSMGJRSDIzdk9BR2ZQNVBxWlV6MFZsQkRzS20KeTgwaDd6K3" \
          "BOSERDUGpCNXBjQ0wyL09WVkV0eHZHYkl3bmtkU2J2S0lJNmc0NHd4Z2dZb1RHU3pGN3VEQVhTSApRb2tDZ2dFQVAzSG5sdW9qWXVpNVVMYzhqR" \
          "G9zcHJnaEtLSlBMNWlJQUlxSEpuNW9VdGViL2xpSm5RTVdLVVVkCllFYWN1SWZyU2hDQVdkeFV1akIrdXpVTGZ1bm1rMUtoczlBODJ2bVVvVjlZ" \
          "aFF6UkZYZ0dJaW9kREoxT3VhVFkKLzZueWJLSEFqZC9oa0FqNHdLbW9lRG51KzVGaGxpQ3doUnNWdmJUTjF0TkpvN0QzVStPTy9STlkzUjVEOGt" \
          "NTQpsUERTMEZQVStyWTRmZ3kwL3JFNC81cUZzR3JMU20yZVNLUjVCcnZDUDdlR28yWDlrQzdTRHJPNE9hWFI3OEJnCkFuT0JOb01mUVdVdFJoeG" \
          "hXUnlNcERLM2JUSG1RdnBiWVdBOHNoOE4zQ2QyS1dtQmtTSGxka284N1pmaUwyaG4KODRKY1N4MDcrSzJ4aFdQWEE2TTFLczBmbW1YT05RPT0KL" \
          "S0tLS1FTkQgUFJJVkFURSBLRVktLS0tLQ=="
