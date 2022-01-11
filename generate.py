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
        num_YueJiang = YueJiang if isInstance(YueJiang, int) else ZHI_to_num[YueJiang]
        num_hourZ    = hourZ    if isInstance(hourZ, int)    else ZHI_to_num[hourZ]
        self.tianPan = Pan(ZHI, move=num_YueJiang - num_hourZ)

    def get_upper(self, zhi):
        '''
        地盘上神
        '''
        num_zhi = zhi if isInstance(zhi, int) else ZHI_to_num[zhi]

    def get_under(self, zhi):
        '''
        天盘下神
        '''
        
class SiKe(object):
    # GAN      = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    GAN_JIGONG = ["寅", "辰", "巳", "未", "巳", "未", "申", "戌", "亥", "丑"] # 阳干寄禄， 阴干寄冠带
    def __init__(self, dayGZ, tianDiPan):
        '''
        :param str(2) dayGZ
        '''
        assert len(dayGZ) == 2
        dayG = dayGZ[0]
        dayZ = dayGZ[1]
        

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
