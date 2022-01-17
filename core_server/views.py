from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from weibo_utils import WeiboHelper
import json
import traceback
import logging
import log_config
log_config.setup_logging()
log = logging.getLogger("simple")

def get_comments(request):
    res = {"status": "success", "msg": ""}
    if request.method == "GET":
        weibo_url = request.GET.get("url", None)
        if weibo_url:
            try:
                helper = WeiboHelper()
                comment_info = helper.get_comment(weibo_url)
                res["data"] = comment_info
            except Exception as e:
                res["status"] = "error"
                res["msg"] = traceback.format_exc()

        else:
            res["status"] = "error"
            res["msg"] = "无有效输入"
    else:
        res = {"status": "error", "msg": "请使用 get 请求"}

    return HttpResponse(json.dumps(res))
