#!/usr/bin/env python3
# -*-coding:utf-8-*-
NOT200_ERROR_MSG = "请求错误与"
NOTOKEN_ERROR_MSG = "未设置TOKEN"
def _code(code):
    if (code[0] in ['0','2','3','6','9']) and len(code)==6:
        if code[0] in ['6','9']:
            code='SH'+code
        elif code[0] in ['0','2','3']:
            code='SZ'+code
    return code
