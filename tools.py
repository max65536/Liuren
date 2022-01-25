from consts import GAN, ZHI, YUEJIANG, JIEQI, mapping_JIEQI_to_YUEJIANG, WUXING
from IPython import embed


def circle_substract(a, b, n):
    '''
    rtype tuple (count_left(-), count_right(+))
    '''
    res = a - b
    if res<0:
        return (res, res+n)
    elif res>0:
        return (res-n, res)
    elif res==0:
        return (0, 0)

def relative_pos(a, b, lst):
    '''
    计算list中两个元素相对位置
    '''
    assert a in lst
    assert b in lst
    return circle_substract(lst.index(a), lst.index(b), len(lst))

def GANZHI_to_WUXING(x):
    # GAN         = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    # ZHI         = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    GAN_to_WUXING = ["木", "木", "火", "火", "土", "土", "金", "金", "水", "水" ]
    ZHI_to_WUXING = ["水", "土", "木", "木", "土", "火", "火", "土", "金", "金", "土", "水"]
    if x in GAN:
        return GAN_to_WUXING[GAN.index(x)]
    if x in ZHI:
        return ZHI_to_WUXING[ZHI.index(x)]
    return x

def shengke_WUXING(a, b):
    '''
    计算干支或五行的生克
    '''
    # ["木", "火", "土", "金", "水"]
    a = GANZHI_to_WUXING(a)
    b = GANZHI_to_WUXING(b)
    try:
        dst = relative_pos(a, b, WUXING)
    except AssertionError:
        return 0
    if dst==(-1, 4):
        shengke = "生"
    elif dst==(-2, 3):
        shengke = "克"
    else:
        shengke = 0
    return shengke

