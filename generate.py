import os

from consts import GAN, ZHI, YUEJIANG, JIEQI, mapping_JIEQI_to_YUEJIANG, WUXING
from tools import *
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
        
        self.circle_move(move % self.SIZE, inplace=True)

    def circle_move(self, k, inplace=False):
        '''
        在list中是右移，在盘中是顺时针移
        move left: lst << k
        :param int k
        :rtype list
        '''
        lst = self.list
        x = lst[-k:]
        y = lst[:-k]
        new_lst = list(x+y)
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
        return self.list[i % 12]

    def find_pos(self, zhi):
        for i, item in enumerate(self.list):
            if item==zhi:
                return i
        return -1

    def step(self, pos, move=1):
        ''' 
        在盘上往前走或往后走
        '''
        if isinstance(pos, str):
            pos = self.find_pos(pos)
        new_pos = (pos + move) % 12
        return self.get(new_pos)

    def __str__(self):
        return self.pan

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
    GAN_JIGONG_to_ZHI = ["寅", "辰", "巳", "未", "巳", "未", "申", "戌", "亥", "丑"] # 阳干寄禄， 阴干寄冠带
    ZHI_to_GAN_JIGONG = {"丑":"癸", "寅":"甲", "辰":"乙", "巳":["丙","戊"], "未":["丁","己"], "申":"庚", "戌":"辛", "亥":"壬"}
    def __init__(self, hourZ=None, YueJiang=None, move=None):
        self.diPan = Pan(ZHI)
        if move is None:
            num_YueJiang = YueJiang if isinstance(YueJiang, int) else self.ZHI_to_num[YueJiang]
            num_hourZ    = hourZ    if isinstance(hourZ, int)    else self.ZHI_to_num[hourZ]
            move = num_hourZ - num_YueJiang
        self.tianPan = Pan(ZHI, move=move)
        self.FuYin   = True if move==0 else False # 伏吟
        self.FanYin  = True if move==6 else False # 反吟

    def get_upper(self, zhi_or_gan):
        '''
        地盘上神
        '''
        zhi = self.GAN_JIGONG_to_ZHI[GAN.index(zhi_or_gan)] if zhi_or_gan in GAN else zhi_or_gan
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
        self.Ke = []
        under   = [''] * 4
        upper   = [''] * 4
        (under[0], upper[0]) = (dayG, tianDiPan.get_upper(gan_jigong))
        (under[1], upper[1]) = (upper[0], tianDiPan.get_upper(upper[0]))
        (under[2], upper[2]) = (dayZ, tianDiPan.get_upper(dayZ))
        (under[3], upper[3]) = (upper[2], tianDiPan.get_upper(upper[2]))

        self.under = under
        self.upper = upper

        for i in range(4):
            self.Ke.append((under[i], upper[i]))

        self.shangshen_ke_dayG, self.dayG_ke_shangshen = self.count_yaoke()
        self.shang_ke_xia, self.xia_zei_shang = self.count_zeike()

    def count_zeike(self):
        shang_ke_xia  = [shang for (xia, shang) in self.Ke if shengke_WUXING(shang, xia)=="克"] 
        xia_zei_shang = [shang for (xia, shang) in self.Ke if shengke_WUXING(xia, shang)=="克"] 
        return shang_ke_xia, xia_zei_shang

    def count_yaoke(self):
        shangshen_ke_dayG = [shangshen for shangshen in self.upper[1:] if shengke_WUXING(shangshen, self.dayG)=="克"] # 上神克干
        dayG_ke_shangshen = [shangshen for shangshen in self.upper[1:] if shengke_WUXING(self.dayG, shangshen)=="克"] # 干克上神
        return shangshen_ke_dayG, dayG_ke_shangshen



    def __str__(self):
        # a[start:stop:step] # start through not past stop, by step
        s = "".join(self.upper[::-1]) + '\n' + "".join(self.under[::-1])
        return s

class SanChuan(object):
    '''
    九宗门：
    贼克法：重审：一下贼上 元首：一上克下
    比用法：
    涉害法：
    '''
    def __init__(self, siKe, tianDiPan=None):
        self.siKe = siKe
        self.dayGZ = siKe.dayGZ
        self.tianDiPan = siKe.tianDiPan if tianDiPan is None else tianDiPan
        self.generate_sanchuan()
        print(self.type)

    def generate_sanchuan(self):
        if self.tianDiPan.FuYin:
            self.type = "伏吟"
        elif self.tianDiPan.FanYin:
            self.type = "反吟"

        else:
            num_zei = len(self.siKe.xia_zei_shang)
            num_she = len(self.siKe.shang_ke_xia)
            if num_zei==0 and num_she==0:
                if len(self.siKe.shangshen_ke_dayG)>0 or len(self.siKe.dayG_ke_shangshen)>0:
                    self.type = "遥克"
                    chuan1 = self.yaokefa()
                else:
                    num_sike = len(set(self.siKe.upper))
                    if num_sike==4:
                        # 四课全备
                        self.type = "昴星"
                        chuan1 = self.maoxingfa()
                    elif num_sike==3:
                        # 四课三备
                        self.type = "别责"
                        self.biezefa()
                    else:
                        assert num_sike==2
                        self.type = "八专"

            elif num_zei==1 or (num_zei==0 and num_she==1):
                self.type = "贼克"
                chuan1 = self.zeikefa(zei=self.siKe.xia_zei_shang, ke=self.siKe.shang_ke_xia)
                chuan2, chuan3 = self.chuan23(chuan1)
            else:
                bihe = self.biyongfa()
                # print("比合=", bihe)
                if isinstance(bihe, list) and len(bihe)==1:
                    self.type = "比用"
                    chuan1 = bihe[0]
                else:
                    self.type = "涉害"
                    if bihe==0:
                        chuan1 = self.shehaifa(self.siKe.upper)
                    else:
                        chuan1 = self.shehaifa(bihe)
                    
                chuan2, chuan3 = self.chuan23(chuan1)
        #self.chuan = [chuan1, chuan2, chuan3]
        self.chuan1 = chuan1
        print(self.type, chuan1)
        

    def yaokefa(self):
        '''
        遥克法：
        蒿矢格：上神(shangshen)克日干
        弹射格：四课不克日干，取日干克二三四课发用

        '''
        shangshen_ke_dayG = self.siKe.shangshen_ke_dayG
        dayG_ke_shangshen = self.siKe.dayG_ke_shangshen

        def bihe_then_shehai(shangshen_ke_dayG):
            bihe = self.get_bihe(ref=self.siKe.dayG ,lst=shangshen_ke_dayG)
            if len(bihe)==1:
                return bihe[0]
            check_list = shangshen_ke_dayG if len(bihe)==0 else bihe
            count_shehai = [self.get_shehai(x) for x in check_list]
            max_shehai = max(count_shehai)
            assert count_shehai.count(max_shehai)==1
            return check_list[count_shehai.index(max_shehai)]

        if len(shangshen_ke_dayG)>=1:
            # 蒿矢格
            if len(shangshen_ke_dayG)==1:
                return shangshen_ke_dayG[0]
            chuan1 = bihe_then_shehai(shangshen_ke_dayG)
        else:
            # 弹射格 
            if len(shangshen_ke_dayG)==1 :
                return shangshen_ke_dayG[0]
            chuan1 = bihe_then_shehai(dayG_ke_shangshen)
        return chuan1
       
    def maoxingfa(self):
        '''
        昴星法:
        虎视格：   阳日取地盘酉上神发用, 支上神为中传, 干上神为末传
        冬蛇掩目格：阴日取天盘酉下神发用, 干上神为中传, 支上神为末传
        '''
        if self.get_yinyang(self.dayGZ[0])=="阳":
            chuan1 = self.tianDiPan.get_upper("酉")
            chuan2 = self.tianDiPan.get_upper(self.dayGZ[1])
            chuan3 = self.tianDiPan.get_upper(self.dayGZ[0])
        else:
            assert self.get_yinyang(self.dayGZ[0])=="阴"
            chuan1 = self.tianDiPan.get_under("酉")
            chuan2 = self.tianDiPan.get_upper(self.dayGZ[0])
            chuan3 = self.tianDiPan.get_upper(self.dayGZ[1])

        self.chuan = [chuan1, chuan2, chuan3]
        return chuan1

    def biezefa(self):
        '''
        别责法
        '''
        pass

    @staticmethod
    def get_yinyang(ganzhi):
        yangyin = "阳阴"
        if ganzhi in GAN:
            return yangyin[GAN.index(ganzhi) % 2]
        if ganzhi in ZHI:
            return yangyin[ZHI.index(ganzhi) % 2]
        raise Exception("ganzhi must be included in GAN or ZHI!")

    @staticmethod
    def get_bihe(ref, lst):
        bihe = []
        ref_yinyang = SanChuan.get_yinyang(ref)
        for item in lst:
            if SanChuan.get_yinyang(item) == ref_yinyang:
                bihe.append(item)
        return bihe
 
    def zeikefa(self, zei, ke):
        '''
        # 始入课：仅一下贼上
        # 重审课：除一下贼上，还有上克下，仍取下贼上
        # 元首课：无下贼上，仅一上克下
        '''
        chuan1 = 0
        sike = self.siKe
        if len(zei)==1:
            # 始入课/重审课
            chuan1 = zei[0]
        elif len(zei)==0 and len(ke)==1:
            # 元首课
            chuan1 = ke[0]
        return chuan1

    def biyongfa(self):
        shang_ke_xia = self.siKe.shang_ke_xia
        xia_zei_shang = self.siKe.xia_zei_shang
        chuan1 = 0
        assert len(shang_ke_xia) > 1 or len(xia_zei_shang) > 1
        if len(xia_zei_shang) > 1:
            # 比用课：多下贼上选与日干比用者
            chuan1 = self.get_bihe(self.siKe.dayG, xia_zei_shang)
        elif len(shang_ke_xia) > 1:
            # 知一课：多上克下选与日干比用者
            chuan1 = self.get_bihe(self.siKe.dayG, shang_ke_xia)

        if chuan1==0:
            return 0
        else:
            assert isinstance(chuan1, list)
            return chuan1

    def shehaifa(self, check_list, dayGZ=None):
        '''
        涉害课：涉害不等
        见机格：涉害相等，取四孟
        察微格：无当四孟，取四仲
        缀瑕格：无当四仲，阳日取干上神，阴日取支上神
        '''
        dayGZ = self.siKe.dayGZ if dayGZ is None else dayGZ
        check_bihe = self.get_bihe(dayGZ[0], check_list)
        assert len(check_bihe)==0 or len(check_bihe)==len(check_list), "必须是俱比或俱不比"
        count_shehai = [self.get_shehai(x) for x in check_list]
        max_shehai = max(count_shehai)
        if count_shehai.count(max_shehai)==1:
            # 涉害课
            return check_list[count_shehai.index(max_shehai)]
        else:
            xiashen = [self.tianDiPan.get_under(x) for x in check_list]
            # 见机格
            meng = [x for x in xiashen if x in "寅巳申亥"] # 孟位
            if len(meng)==1:
                return self.tianDiPan.get_upper(meng[0])
            # 察微格
            zhong = [x for x in xiashen if x in "子卯午酉"] # 仲位
            if len(zhong)==1:
                return self.tianDiPan.get_upper(zhong[0])
            # 缀瑕格
            if self.get_yinyang(dayGZ[0])=="阳":
                return self.tianDiPan.get_upper(dayGZ[0])
            elif self.get_yinyang(dayGZ[0])=="阴":
                return self.tianDiPan.get_upper(dayGZ[1])
            else:
                raise Exception("Value Error, must be one of '阴阳'")

    def get_shehai(self, zhi):
        tdp = self.tianDiPan
        pos = tdp.tianPan.find_pos(zhi)
        count=0
        while True:
            current_di = tdp.diPan.get(pos)
            count +=1 if shengke_WUXING(current_di, zhi)=="克" else 0
            # count +=1 if shengke_WUXING(tdp.tianPan.get(pos), zhi)=="克" else 0
            GAN_jigong = tdp.ZHI_to_GAN_JIGONG[current_di] if current_di in tdp.ZHI_to_GAN_JIGONG.keys() else ""
            for gan in GAN_jigong:
                count +=1 if shengke_WUXING(gan, zhi)=="克" else 0
            if current_di==zhi:
                break
            # print(pos, current_di, count)
            pos += 1
            if pos>30:
                return -1
        return count

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
