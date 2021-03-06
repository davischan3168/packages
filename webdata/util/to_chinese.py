#!/usr/bin/env python3
# -*-coding:utf-8-*-

class NotIntegerError(Exception):
  pass
 
class OutOfRangeError(Exception):
  pass
 
_MAPPING = (u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九', )
_P0 = (u'', u'十', u'百', u'千', )
_S4, _S8, _S16 = 10 ** 4 , 10 ** 8, 10 ** 16
_MIN, _MAX = 0, 9999999999999999
 
def _to_chinese4(num):
  '''转换[0, 10000)之间的阿拉伯数字
  '''
  assert(0 <= num and num < _S4)
  if num < 10:
    return _MAPPING[num]
  else:
    lst = [ ]
    while num >= 10:
      d=num%10
      print(d)
      lst.append(d)
      num = num // 10
    lst.append(num)
    c = len(lst)  # 位数
    result = u''
     
    for idx, val in enumerate(lst):
      print(idx,val)
      if val != 0:
        result += _P0[idx] + _MAPPING[val]
        if idx < c - 1 and lst[idx + 1] == 0:
          result += u'零'
     
    return result[::-1].replace(u'一十', u'十')
     
def _to_chinese8(num):
  assert(num < _S8)
  to4 = _to_chinese4
  if num < _S4:
    return to4(num)
  else:
    mod = _S4
    high, low = num // mod, num % mod
    if low == 0:
      return to4(high) + u'万'
    else:
      if low < _S4 // 10:
        return to4(high) + u'万零' + to4(low)
      else:
        return to4(high) + u'万' + to4(low)
       
def _to_chinese16(num):
  assert(num < _S16)
  to8 = _to_chinese8
  mod = _S8
  high, low = num // mod, num % mod
  if low == 0:
    return to8(high) + u'亿'
  else:
    if low < _S8 // 10:
      return to8(high) + u'亿零' + to8(low)
    else:
      return to8(high) + u'亿' + to8(low)
     
def to_chinese(num):
  """num:输入的类型为int
  """
  if type(num) != int:
    raise NotIntegerError(u'%s is not a integer.' % num)
  if num < _MIN or num > _MAX:
    raise OutOfRangeError(u'%d out of range[%d, %d)' % (num, _MIN, _MAX))
   
  if num < _S4:
    return _to_chinese4(num)
  elif num < _S8:
    return _to_chinese8(num)
  else:
    return _to_chinese16(num)


unitArab=(2,3,4,5,9)
unitStr=u'十百千万亿'
unitStr=u'拾佰仟万亿'
#单位字典unitDic,例如(2,'十')表示给定的字符是两位数,那么返回的结果里面定会包含'十'.3,4,5,9以此类推.
unitDic=dict(zip(unitArab,unitStr))

numArab=u'0123456789'
numStr=u'零一二三四五六七八九'
numStr=u'零壹贰叁肆伍陆柒捌玖'
#数值字典numDic,和阿拉伯数字是简单的一一对应关系
numDic=dict(zip(numArab,numStr))


def ChnNumber(s):
    """
    s:字符串类型的数字,如-->'90'
    """
    def wrapper(v):
        '''针对多位连续0的简写规则设计的函数
        例如"壹佰零零"会变为"壹佰","壹仟零零壹"会变为"壹仟零壹"
        '''
        if u'零零' in v:
            return wrapper(v.replace(u'零零',u'零'))
        return v[:-1] if v[-1]==u'零' else v
    def recur(s,bit):
        '''此函数接收2个参数:
        1.纯数字字符串
        2.此字符串的长度,相当于位数'''
        #如果是一位数,则直接按numDic返回对应汉字
        if bit==1:
            return numDic[s]
        #否则,且第一个字符是0,那么省略"单位"字符,返回"零"和剩余字符的递归字符串
        if s[0]==u'0':
            return wrapper(u'%s%s' % (u'零',recur(s[1:],bit-1)))
        #否则,如果是2,3,4,5,9位数,那么返回最高位数的字符串"数值"+"单位"+"剩余字符的递归字符串"
        if bit<6 or bit==9:
            return wrapper(u'%s%s%s' % (numDic[s[0]],unitDic[bit],recur(s[1:],bit-1)))
        #否则,如果是6,7,8位数,那么用"万"将字符串从万位数划分为2个部分.
        #例如123456就变成:12+"万"+3456,再对两个部分进行递归.
        if bit<9:
            return u'%s%s%s' % (recur(s[:-4],bit-4),u"万",recur(s[-4:],4))
        #否则(即10位数及以上),用"亿"仿照上面的做法进行划分.
        if bit>9:
            return u'%s%s%s' % (recur(s[:-8],bit-8),u"亿",recur(s[-8:],8))
    return recur(s,len(s))
"""
for i in range(18):    
    v1='9'+'0'*(i+1)
    v2='9'+'0'*i+'9'
    v3='1'*(i+2)
    print ('%s->%s\n%s->%s\n%s->%s'% (v1,ChnNumber(v1),v2,ChnNumber(v2),v3,ChnNumber(v3)))"""

common_used_numerals_tmp = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
                            '十': 10, '百': 100, '千': 1000, '万': 10000, '亿': 100000000}
common_used_numerals = {}
for key in common_used_numerals_tmp:
    common_used_numerals[key] = common_used_numerals_tmp[key]


def chinese2digits(uchars_chinese):
    total = 0
    r = 1  # 表示单位：个十百千...
    for i in range(len(uchars_chinese) - 1, -1, -1):
        val = common_used_numerals.get(uchars_chinese[i])
        if val >= 10 and i == 0:  # 应对 十三 十四 十*之类
            if val > r:
                r = val
                total = total + val
            else:
                r = r * val
                # total =total + r * x
        elif val >= 10:
            if val > r:
                r = val
            else:
                r = r * val
        else:
            total = total + r * val
    return total


num_str_start_symbol = ['一', '二', '两', '三', '四', '五', '六', '七', '八', '九',
                        '十']
more_num_str_symbol = ['零', '一', '二', '两', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万', '亿']

def changeChineseNumToArab(oriStr):
    lenStr = len(oriStr);
    aProStr = ''
    if lenStr == 0:
        return aProStr;

    hasNumStart = False;
    numberStr = ''
    for idx in range(lenStr):
        if oriStr[idx] in num_str_start_symbol:
            if not hasNumStart:
                hasNumStart = True;

            numberStr += oriStr[idx]
        else:
            if hasNumStart:
                if oriStr[idx] in more_num_str_symbol:
                    numberStr += oriStr[idx]
                    continue
                else:
                    numResult = str(chinese2digits(numberStr))
                    numberStr = ''
                    hasNumStart = False;
                    aProStr += numResult

            aProStr += oriStr[idx]
            pass

    if len(numberStr) > 0:
        resultNum = chinese2digits(numberStr)
        aProStr += str(resultNum)

    return aProStr




if __name__=="__main__":
    df=to_chinese(1002030040506)
