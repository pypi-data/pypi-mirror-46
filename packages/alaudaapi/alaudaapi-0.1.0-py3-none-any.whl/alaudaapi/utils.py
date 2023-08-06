# coding=utf-8
import smtplib
import random
import jinja2
import yaml
import json
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep
from bs4 import BeautifulSoup
from common import settings
from common.match_case import casename
from common.settings import SMTP


def retry(times=3, sleep_secs=3):
    def retry_deco(func):
        def retry_deco_wrapper(*args, **kwargs):
            count = 0
            success = False
            data = None
            while not success and count < times:
                count += 1
                try:
                    data = func(*args, **kwargs)
                    success = True
                except Exception:
                    sleep(sleep_secs)
                    if count == times:
                        assert False, "get global info failed"
            return data

        return retry_deco_wrapper

    return retry_deco


def send_email(subject, body, recipients, file_path):
    """class method to send an email"""

    # if settings.EMAIL is None or settings.SMTP is None:
    #    logger.error("No email/smtp config, email not sent.")
    #    return

    if not isinstance(recipients, list):
        raise TypeError(
            "{} should be a list".format(recipients))

    # we only support one sender for now
    from_email = SMTP['sender']

    # build message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ','.join(recipients)
    msg['Subject'] = Header(subject, 'utf8')
    msg.attach(MIMEText(body, 'html', 'utf8'))
    # add report html
    att = MIMEText(open(file_path, 'rb').read(), 'base64', 'gb2312')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename="report.tar"'
    msg.attach(att)

    server = None
    try:
        server = smtplib.SMTP_SSL(host=SMTP['host'], port=SMTP['port'])
        server.set_debuglevel(SMTP['debug_level'])
        server.login(SMTP['username'], SMTP['password'])
        server.sendmail(from_email, recipients, msg.as_string())
        print("send email successfully")
    except Exception as e:
        # don't fatal if email was not send
        print("send email failed，the reason is：{}".format(e))
    finally:
        if server:
            server.quit()


def read_result():
    with open("./report/pytest.html", "r") as fp:
        report = BeautifulSoup(fp, "html.parser")
        tbodys = report.select("tbody")
        not_run_count = 0
        pass_count = 0
        failed_count = 0
        rerun_count = 0
        skip_count = 0
        result_flag = 'Success'
        json_result = {"case_details": []}
        for tbody in tbodys:
            tds = tbody.select("td")
            if tds[1].text.split("::")[-1] != "setup":
                if tds[1].text.split("::")[-1].find("[not_run]") > 0:
                    case_name = "(根账号)-" + casename().get(tds[1].text.split("::")[-1].split("[")[0],
                                                          tds[1].text.split("::")[-1])
                elif tds[1].text.split("::")[-1].find("[run]") > 0:
                    case_name = "(子账号权限)-" + casename().get(tds[1].text.split("::")[-1].split("[")[0],
                                                            tds[1].text.split("::")[-1])
                else:
                    case_name = casename().get(tds[1].text.split("::")[-1], tds[1].text.split("::")[-1])
            else:
                if tds[1].text.split("::")[-2].find("[not_run]") > 0:
                    case_name = "(根账号)-" + casename().get(tds[1].text.split("::")[-2].split("[")[0],
                                                          tds[1].text.split("::")[-2])
                elif tds[1].text.split("::")[-2].find("[run]") > 0:
                    case_name = "(子账号权限)-" + casename().get(tds[1].text.split("::")[-2].split("[")[0],
                                                            tds[1].text.split("::")[-2])
                else:
                    case_name = casename().get(tds[1].text.split("::")[-2], tds[1].text.split("::")[-2])

            if tds[0].text == "Passed" and tds[2].text == "0.00":
                json_result["case_details"].append(
                    {"case_name": case_name, "case_flag": tds[0].text, "case_detail": tds[2].text,
                     "case_time": tds[2].text})
                not_run_count += 1
            elif tds[0].text == "Skipped":
                case_detail = tds[-1].select("div")[0].text.split(":")[-1].split("'")[0]
                json_result["case_details"].append(
                    {"case_name": case_name, "case_flag": tds[0].text, "case_detail": case_detail,
                     "case_time": tds[2].text})
                skip_count += 1
            elif tds[0].text == "Passed" and tds[2].text != "0.00":
                json_result["case_details"].append(
                    {"case_name": case_name, "case_flag": tds[0].text, "case_detail": tds[2].text,
                     "case_time": tds[2].text})
                pass_count += 1
            elif tds[0].text == "Failed" or tds[0].text == "Error":
                error_info = ""
                for content in tbody.select("span"):
                    error_info += content.text
                error_message = "{},失败请单独执行case:{}".format(error_info, tds[1].text)
                json_result["case_details"].append(
                    {"case_name": case_name, "case_flag": tds[0].text, "case_detail": error_message,
                     "case_time": tds[2].text})
                failed_count += 1
                result_flag = 'Failed'
            elif tds[0].text == "Rerun":
                error_info = ""
                for content in tbody.select("span"):
                    error_info += content.text
                json_result["case_details"].append(
                    {"case_name": case_name, "case_flag": tds[0].text, "case_detail": error_info,
                     "case_time": tds[2].text})
                rerun_count += 1
            else:
                pass
        json_result_summary = {
            "summary": report.select("p")[1].text,
            "pass_num": pass_count,
            "notrun_num": not_run_count,
            "failed_num": failed_count,
            "rerun_num": rerun_count,
            "skip_num": skip_count
        }
        json_result.update(json_result_summary)
        with open('./report/pytest.json', 'w') as f:
            f.write(json.dumps(json_result, indent=4, ensure_ascii=False))
        with open('./report/pytest.yaml', 'w') as f:
            f.write(yaml.dump(json_result, indent=4, allow_unicode=True))
    with open("./template/report.j2", "r") as fp:
        content = fp.read()
        template = jinja2.Template(content)
        html = template.render(json_result)
        return result_flag, html


class Global_Map(object):
    @staticmethod
    def _init():
        global _global_dict
        _global_dict = {"timestamp": ""}
        Global_Map().create_timestamp()
        Global_Map.set_value("permissionuser", settings.ACCOUNT)

    @staticmethod
    def set_value(key, value):
        _global_dict[key] = value

    @staticmethod
    def get_value(key, default_value=None):
        try:
            return _global_dict[key]
        except KeyError:
            return default_value

    def create_timestamp(self):
        timestamp = str(random.randint(10000000, 20000000))
        if Global_Map.get_value("timestamp"):
            return
        Global_Map.set_value("timestamp", timestamp)
