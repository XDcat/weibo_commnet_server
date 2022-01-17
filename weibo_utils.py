import json
import random
import time

import requests
import logging
import re
import log_config
import traceback

log_config.setup_logging()
log = logging.getLogger("simple")


class WeiboHelper():
    def __init__(self):
        self.max_page_count = 200
        self.session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
        self.session.headers.update(headers)
        self.session.trust_env = False  # 不使用系统代理

    def _sleep(self, min_time=1, max_time=3):
        randint = random.randint(min_time, max_time)
        log.debug(f"休眠 {randint} 秒")
        time.sleep(randint)

    def get_page_id(self, url):
        """根据网页直接拿到的url来找出评论需要的页面id
        url 的格式为
            * https://weibo.com/5619014457/LaVCfmfq3
            * https://weibo.com/5619014457/LaVCfmfq3#comment
        """
        # 找到页面原始 id
        url = url.strip()
        log.debug(f"解析页面真实 id: {url}")
        mo = re.match("https://weibo.com/\d+/(\w{9})", url)
        try:
            raw_id = mo.group(1)
        except Exception as e:
            log.error(f"无法解析页面真实id: {url}")
            log.error(traceback.format_exc())
            raise RuntimeError("无法从url中匹配到页面的原始id")
        log.debug(f"页面原始id: {raw_id}")

        # 构造获取页面 id 的链接，并请求获取
        id_url = "https://weibo.com/ajax/statuses/show?id={}"
        id_url = id_url.format(raw_id)
        log.debug(f"访问: {id_url}")
        try:
            response = self.session.get(id_url, )
            response_json = json.loads(response.text)
            true_page_id = response_json["id"]
            log.debug(f"{url} 的真实 id：{true_page_id}")
            self._sleep()
            return true_page_id
        except Exception as e:
            log.error(f"请求页面真实 id 失败，输入：{url}")
            log.error(traceback.format_exc())
            raise RuntimeError(f"请求页面真实 id 失败，输入：{url}")

    def get_comment(self, url, comment_count=200):
        """
        通过微博url获取评论
        url 的格式为
            * https://weibo.com/5619014457/LaVCfmfq3
            * https://weibo.com/5619014457/LaVCfmfq3#comment
        """
        payload = {}
        headers = {}
        page_id = self.get_page_id(url)
        get_comment_url = f"https://weibo.com/ajax/statuses/buildComments?is_reload=1&id={page_id}&is_show_bulletin=3&is_mix=0&count={comment_count}"
        try:
            response = self.session.get(get_comment_url)
            log.debug(f"url: {get_comment_url}")
            log.debug(f"status: {response.status_code}")
            comment_info = json.loads(response.text)
            log.debug("评论总数目 %s" % comment_info["total_number"])
            log.debug("获取到的评论数目 %s" % len(comment_info["data"]))
            log.debug("评论状态 %s" % comment_info["trendsText"])
            user_names = [row["user"]["name"] for row in comment_info["data"]]
            # 去重
            user_names = list(set(user_names))
            log.debug(user_names)
            res = {
                "total_number": comment_info["total_number"],
                "get_comment_number": len(comment_info["data"]),
                "get_no_repeated_comment_number": len(user_names),
                "trendsText": comment_info["trendsText"],
                "user_names": user_names
            }
            return res
        except Exception as e:
            log.error("获取评论出现错误")
            log.error(traceback.format_exc())
            raise RuntimeError("获取评论出现错误")


if __name__ == '__main__':
    url = "https://weibo.com/5619014457/LaVCfmfq3#comment"
    helper = WeiboHelper()
    helper.get_comment(url)
