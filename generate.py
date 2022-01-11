import os

from consts import GAN, ZHI, YUEJIANG, JIEQI, mapping_JIEQI_to_YUEJIANG 
from SolarLunarDatetime import SolarLunarDatetime
from IPython import embed

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
        dayG = dayGZ[0]
        gan_jigong = self.GAN_to_ZHI[dayG]
        dayZ = dayGZ[1]
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
#        embed()

    def __str__(self):
        # a[start:stop:step] # start through not past stop, by step
        s = "".join(self.upper[::-1]) + '\n' + "".join(self.under[::-1])
        return s

class SanChuan(object):
    
    def __init__(self, tianDiPan, siKe):
        pass

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
