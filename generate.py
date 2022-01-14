import os

from consts import GAN, ZHI, YUEJIANG, JIEQI, mapping_JIEQI_to_YUEJIANG, WUXING
from SolarLunarDatetime import SolarLunarDatetime
from IPython import embed

GAN_to_WUXING = []



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
    # ["木", "火", "土", "金", "水"]
    a = GANZHI_to_WUXING(a)
    b = GANZHI_to_WUXING(b)
    dst = relative_pos(a, b, WUXING)
    if dst==(-1, 4):
        shengke = "生"
    elif dst==(-2, 3):
        shengke = "克"
    else:
        shengke = 0
    return shengke

class Pan(object):
#class Pan(list):
    '''
    report bugs when overwriting methods of innner class, but no bugs if add new methods
    (https://xie.infoq.cn/article/fff6fe5ed00cf50bbc31725e0)
    '''
    SIZE = 12
    def __init__(self, lst, move=0):
        '''
        :param list lst
        :int move
        '''
        self.list = lst
        self.pan  = self.list_to_pan()
        if move != 0 and abs(move < self.SIZE):
            self.circle_move(move, inplace=True)

    def circle_move(self, k, inplace=False):
        '''
        在list中是左移，在盘中是逆时针移
        move left: lst << k
        :param int k
        :rtype list
        '''
        lst = self.list
        x = lst[k-1::-1]
        y = lst[:k-1:-1]
        new_lst = list(reversed(x+y))
        if inplace:
            self.list = new_lst
            self.pan = self.list_to_pan()
        return new_lst

    def list_to_pan(self):
        '''
        :param list lst
        rtype: str
        '''
        lst = self.list
        assert len(lst)==12
        pan = []
        pan.append("%c%c%c%c" % (lst[5], lst[6], lst[7], lst[8]))
        pan.append("%c    %c" % (lst[4],                 lst[9]))
        pan.append("%c    %c" % (lst[3],                 lst[10]))
        pan.append("%c%c%c%c" % (lst[2], lst[1], lst[0], lst[11]))
        return '\n'.join(pan)

    def get(self, i):
        return self.list[i]

    def find_pos(self, zhi):
        for i, item in enumerate(self.list):
            if item==zhi:
                return i
        return -1

class TianDiPan(object):
    '''
    DiPan = 
    " 
    巳午未申
    辰    酉
    卯    戌
    寅丑子亥   
    "
    '''
    ZHI_to_num = dict(zip(ZHI, range(12)))
    def __init__(self, hourZ, YueJiang):
        self.diPan = Pan(ZHI)
        num_YueJiang = YueJiang if isinstance(YueJiang, int) else self.ZHI_to_num[YueJiang]
        num_hourZ    = hourZ    if isinstance(hourZ, int)    else self.ZHI_to_num[hourZ]
        self.tianPan = Pan(ZHI, move=num_YueJiang - num_hourZ)

    def get_upper(self, zhi):
        '''
        地盘上神
        '''
        num_zhi = zhi if isinstance(zhi, int) else self.ZHI_to_num[zhi]
        return self.tianPan.get(num_zhi)


    def get_under(self, zhi):
        '''
        天盘下神
        '''
        zhi = ZHI[zhi] if isinstance(zhi, int) else zhi
        pos = self.tianPan.find_pos(zhi)
        return self.diPan.get(pos)

    def __str__(self):
        return self.tianPan.pan
        
class SiKe(object):
    # GAN      = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    GAN_JIGONG = ["寅", "辰", "巳", "未", "巳", "未", "申", "戌", "亥", "丑"] # 阳干寄禄， 阴干寄冠带
    GAN_to_ZHI = dict(zip(GAN, GAN_JIGONG))
    def __init__(self, dayGZ, tianDiPan):
        '''
        :param str(2) dayGZ
        '''
        assert len(dayGZ) == 2
        self.tianDiPan = tianDiPan
        self.dayGZ = dayGZ
 
        dayG = dayGZ[0]
        self.dayG = dayG
        gan_jigong = self.GAN_to_ZHI[dayG]
        dayZ = dayGZ[1]
        self.dayZ = dayZ
        self.ke = []
        under   = [''] * 4
        upper   = [''] * 4
        (under[0], upper[0]) = (dayG, tianDiPan.get_upper(gan_jigong))
        (under[1], upper[1]) = (upper[0], tianDiPan.get_upper(upper[0]))
        (under[2], upper[2]) = (dayZ, tianDiPan.get_upper(dayZ))
        (under[3], upper[3]) = (upper[2], tianDiPan.get_upper(upper[2]))

        self.under = under
        self.upper = upper

        for i in range(4):
            self.ke.append((under[i], upper[i]))

        self.shengke_sike()

    def shengke_sike(self):
        self.shengke = [0] * 4
        for i in range(4):
            shengke_ke  = shengke_WUXING(self.upper[i], self.under[i])
            shengke_zei = shengke_WUXING(self.under[i], self.upper[i])
            if shengke_ke=="克":
                self.shengke[i] = "克"
            if shengke_zei=="克":
                self.shengke[i] = "贼"
        return self.shengke

    def __str__(self):
        # a[start:stop:step] # start through not past stop, by step
        s = "".join(self.upper[::-1]) + '\n' + "".join(self.under[::-1])
        return s

class SanChuan(object):
    '''
    九宗门：
    贼克法：重审：一下贼上 元首：一上克下
    比用法
    涉害法：
    '''
    def __init__(self, siKe, tianDiPan=None):
        self.siKe = siKe
        self.tianDiPan = siKe.tianDiPan if tianDiPan is None else tianDiPan

    def generate_sanchuan(self):
        zei, ke = self.count_zeike()
        num_zei = len(zei)
        num_ke  = len(ke)
        if num_zei==1 or ((num_zei==0) and (num_ke==1):
            self.zeike(zei, ke)
        elif

    def count_zeike(self):
        sike = self.siKe
        ke  = []
        zei = []
        for i in range(4):
            if sike.shengke[i]=="克":
                ke.append(i)
            elif sike.shengke[i]=="贼":
                zei.append(i)
        return zei, ke

    @staticmethod
    def yinyang(ganzhi):
        if ganzhi in GAN:
            return GAN.index(x) % 2
        if ganzhi in ZHI:
            return ZHI_to_WUXING[ZHI.index(x)] % 2


    def zeikefa(self, zei, ke):
        '''
        # 始入课：仅一下贼上
        # 重审课：除一下贼上，还有上克下，仍取下贼上
        # 元首课：无下贼上，仅一上克下
        '''
        chuan1 = 0
        if len(zei)==1:
            # 始入课/重审课
            chuan1 = sike.upper[zei[0]]
        elif len(zei)==0 and len(ke)==1:
            # 元首课
            chuan1 = sike.upper[ke[0]]
        return chuan1

    def biyongfa(self):
        zei, ke = self.count_zeike()
        assert len(zei) > 1 or len(ke) > 1
        sike = self.siKe
        dayG_yinyang = self.yinyang(self.siKe.dayG)
        if len(zei) > 1:
            # 比用课：多下贼上选与日干比用者
            upper_bihe = []
            for z in zei:
                upper = sike.upper[z] 
                if dayG_yinyang==self.yinyang(upper)
                upper_bihe.append(upper)
            if len(upper_bihe)==1:
                chuan1 = upper_bihe[0]
                chuan2, chuan3 = self.chuan23(chuan1)
                self.chuan = (chuan1, chuan2, chuan3)
                return True
        if len(ke) > 1:
            # 知一课：多上克上选与日干比用者
            pass




       


    def chuan23(self, chuan1):
        chuan2 = self.tianDiPan.get_upper(chuan1)
        chuan3 = self.tianDiPan.get_upper(chuan2)
        return (chuan2, chuan3)


class LiuRenPan(object):
    GAN_to_num = dict(zip(GAN, range(10)))
    ZHI_to_num = dict(zip(ZHI, range(12)))

    def __init__(self, dayGZ, hourZ, YueJiang):
        '''
        dayGZ   : 甲子
        hourZ   : 戌
        Yueiang : 亥
        '''
        pass





    @classmethod
    def init_form_PanNum(cls, panNum):
        '''
        panNum(string) : format: "甲子一局"
        '''
        dayGZ = panNum[:2] 
        hourZ = panNum[2:-1]

    def generate_TianDiPan():
        pass

def main():
    pass

if __name__ == "__main__":
    main()
    embed()
