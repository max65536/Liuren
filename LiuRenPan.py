from consts import GAN, ZHI, mapping_GAN_to_GUIREN_pos, TIANJIANG_short
import tools

from IPython import embed

class LiuRenPan(object):
    def __init__(self, dayGZ, hourZ, YueJiang):
        '''
        dayGZ   : 甲子
        hourZ   : 戌
        Yueiang : 亥
        '''
        self.dayGZ     = dayGZ
        self.YueJIang  = YueJiang
        self.tianDiPan = TianDiPan(hourZ=hourZ, YueJiang=YueJiang)
        self.tianDiPan.set_tianjiang(dayG=dayGZ[0])
        self.tianDiPan.set_dungan(dayGZ=dayGZ)
        self.siKe      = SiKe(dayGZ=dayGZ, tianDiPan=self.tianDiPan)
        self.sanChuan  = SanChuan(self.siKe)
        self.generate_12_gong()

    @classmethod
    def init_from_sizhu(cls, sizhu, YueJiang): 
        return cls(dayGZ=sizhu['day'], hourZ=sizhu['hour'][-1], YueJiang=YueJiang)

    def __str__(self):
        return '\n\n'.join((str(self.sanChuan), str(self.siKe), str(self.tianDiPan)))

    @classmethod
    def init_form_PanNum(cls, panNum):
        '''
        panNum(string) : format: "甲子一局"
        '''
        dayGZ = panNum[:2] 
        hourZ = panNum[2:-1]

    def generate_12_gong(self):
        gong_list = []
        tdp = self.tianDiPan
        for i in range(12):
            gong_list.append(Gong(tdp.diPan[i], tdp.tianPan[i], tdp.tianJiangPan[i], tdp.dungan[i]))
        self.gong = Pan(gong_list, move=0)

    def print_prettytable():
        pass


class Pan(object):
    '''
    #class Pan(list):
    report bugs when overwriting methods of innner class, but no bugs if add new methods
    (https://xie.infoq.cn/article/fff6fe5ed00cf50bbc31725e0)
    '''
    SIZE = 12
    def __init__(self, lst, move=0):
        '''
        :param list lst
        :int move
        '''
        self.items = list(lst)
        self.pan  = self.list_to_pan()
        
        self.circle_move(move % self.SIZE, inplace=True)

    def circle_move(self, k, inplace=False):
        '''
        在list中是右移，在盘中是顺时针移
        move left: lst << k
        :param int k
        :rtype list
        '''
        lst = self.items
        x = lst[-k:]
        y = lst[:-k]
        new_lst = list(x+y)
        if inplace:
            self.items = new_lst
            self.pan = self.list_to_pan()
        return new_lst

    def list_to_pan(self):
        '''
        :param list lst
        rtype: str
        '''
        lst = self.items
        if type(lst[0]) is not str:
            return None
        assert len(lst)==12
        pan = []
        pan.append("%c%c%c%c" % (lst[5], lst[6], lst[7], lst[8]))
        pan.append("%c    %c" % (lst[4],                 lst[9]))
        pan.append("%c    %c" % (lst[3],                 lst[10]))
        pan.append("%c%c%c%c" % (lst[2], lst[1], lst[0], lst[11]))
        return '\n'.join(pan)

    def get(self, i):
        return self.items[i % 12]

    def find_pos(self, zhi):
        for i, item in enumerate(self.items):
            if item==zhi:
                return i
        return None

    def step(self, pos, move):
        ''' 
        在盘上往前走或往后走
        '''
        if isinstance(pos, str):
            pos = self.find_pos(pos)
        new_pos = (pos + move) % self.SIZE
        return self.get(new_pos)

    def __str__(self):
        return ''.join(self.items)

    def compact_string(self):
        return ''.join(self.items)        

    def __repr__(self) -> str:
        return '\n'+self.pan

    def __getitem__(self, num):
        return self.items[num % 12]

class Gong(object):
    def __init__(self, di, tian, jiang=None, gan=None):
        self.diPan      = di
        self.tianPan    = tian
        self.tianJiang  = jiang
        self.dunGan     = gan
        self.down_to_up = [di, tian, jiang, gan]
    
    def __str__(self) -> str:
        return '\n'.join(self.down_to_up)

class TianDiPan(object):
    '''
    始终以地盘"子"的位置作为0点,其他依次后排,包括天盘与天将
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

    def __init__(self, hourZ=None, YueJiang=None, move=None, day_or_night=None):
        '''
        :param str hourZ: must be included in ZHI
        :param str YueJiang: must be included in ZHI
        :param int move: offset of "子"
        '''
        self.diPan = Pan(ZHI)
        self.hourZ = hourZ
        self.YueJiang = YueJiang
        if move is None:
            num_YueJiang = YueJiang if isinstance(YueJiang, int) else self.ZHI_to_num[YueJiang]
            num_hourZ    = hourZ    if isinstance(hourZ, int)    else self.ZHI_to_num[hourZ]
            move = (num_hourZ - num_YueJiang) % 12
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

    def get_tianjiang(self, zhi):
        if hasattr(self, "tianJiangPan"):
            return self.tianJiangPan.get(self.tianPan.find_pos(zhi))
        else:
            return None
        
    def set_tianjiang(self, dayG, day_or_night=None):
        '''
        :param str dayG
        :param str day_or_night: "昼" or "夜"        
        若得时贵人的下神为“亥子丑寅卯辰”（冬春地支），则其余天将皆顺布。
        若得时贵人的下神为“巳午未申酉戌”（夏秋地支），则其余天将皆逆布。
        这里注意所言的是地盘，而非天盘。
        '''
        guiren_ZHI = mapping_GAN_to_GUIREN_pos[dayG]
        if self.get_under(guiren_ZHI[0]) in "亥子丑寅卯辰":
            tianJiangPan_daytime = Pan(TIANJIANG_short, move=self.tianPan.find_pos(guiren_ZHI[0]))        # 昼贵 顺布
        else:
            tianJiangPan_daytime = Pan(reversed(TIANJIANG_short), move=self.tianPan.find_pos(guiren_ZHI[0])+1)        # 昼贵 逆布

        if self.get_under(guiren_ZHI[1]) in "亥子丑寅卯辰":
            tianJiangPan_night = Pan(TIANJIANG_short, move=self.tianPan.find_pos(guiren_ZHI[1]))          # 夜贵 顺布
        else:
            tianJiangPan_night = Pan(reversed(TIANJIANG_short), move=self.tianPan.find_pos(guiren_ZHI[1])+1)          # 夜贵 逆布

        self.tianJiangPan_daytime = tianJiangPan_daytime
        self.tianJiangPan_night   = tianJiangPan_night

        if day_or_night is None:
            self.day_or_night = "昼" if self.hourZ in "卯辰巳午未申" else "夜"
        self.tianJiangPan = tianJiangPan_daytime if self.day_or_night=="昼" else tianJiangPan_night

    def get_dungan(self, zhi):
        if hasattr(self, "dunGanPan"):
            return self.dunGanPan.get(self.tianPan.find_pos(zhi))
        else:
            return None

    def set_dungan(self, dayGZ):
        '''
        :param str[2] dayGZ: 日干支
        return 遁干盘
        '''
        # dungan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", "〇", "〇"]
        self.dungan = [tools.xundun(dayGZ, zhi) for zhi in self.tianPan.items]
        self.dunGanPan = Pan(self.dungan)  

    def __str__(self, dungan=True):
        '''
        :param bool dungan: 遁干
        '''
        if dungan:
            assert hasattr(self, "dunGanPan")
            lst = self.tianPan.items
            tjp = self.tianJiangPan.items
            dun = self.dunGanPan.items
            pan = []
            pan.append("%c%c%c%c%c%c%c%c" % ("\u3000", "\u3000", dun[5],   dun[6],  dun[7], dun[8], "\u3000", "\u3000"))
            pan.append("%c%c%c%c%c%c%c%c" % ("\u3000", "\u3000", tjp[5],   tjp[6],  tjp[7], tjp[8], "\u3000", "\u3000"))
            pan.append("%c%c%c%c%c%c%c%c" % ("\u3000", "\u3000", lst[5],   lst[6],  lst[7], lst[8], "\u3000", "\u3000"))
            pan.append("%c%c%c%c%c%c%c%c" % ( dun[4], tjp[4],    lst[4], "\u3000","\u3000", lst[9], tjp[9], dun[9]))
            pan.append("%c%c%c%c%c%c%c%c" % ( dun[3], tjp[3],    lst[3], "\u3000","\u3000", lst[10],tjp[10],dun[10] ))
            pan.append("%c%c%c%c%c%c%c%c" % ("\u3000", "\u3000", lst[2],   lst[1],  lst[0], lst[11], "\u3000", "\u3000"))
            pan.append("%c%c%c%c%c%c%c%c" % ("\u3000", "\u3000", tjp[2],   tjp[1],  tjp[0], tjp[11], "\u3000", "\u3000"))
            pan.append("%c%c%c%c%c%c%c%c" % ("\u3000", "\u3000", dun[2],   dun[1],  dun[0], dun[11], "\u3000", "\u3000"))
            return '\n'.join(pan)            
        else:
            if hasattr(self, "tianJiangPan"):
                lst = self.tianPan.items
                tjp = self.tianJiangPan.items
                pan = []
                pan.append("%c%c%c%c%c%c" % ("\u3000", tjp[5],   tjp[6],  tjp[7], tjp[8], "\u3000"))
                pan.append("%c%c%c%c%c%c" % ("\u3000", lst[5],   lst[6],  lst[7], lst[8], "\u3000"))
                pan.append("%c%c%c%c%c%c" % (  tjp[4], lst[4], "\u3000","\u3000", lst[9], tjp[9]))
                pan.append("%c%c%c%c%c%c" % (  tjp[3], lst[3], "\u3000","\u3000", lst[10],tjp[10]))
                pan.append("%c%c%c%c%c%c" % ("\u3000", lst[2],   lst[1],  lst[0], lst[11],"\u3000"))
                pan.append("%c%c%c%c%c%c" % ("\u3000", tjp[2],   tjp[1],  tjp[0], tjp[11],"\u3000"))
                return '\n'.join(pan)
            else:
                return self.tianPan.pan

        
class SiKe(object):
    # GAN      = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    GAN_JIGONG = ["寅", "辰", "巳", "未", "巳", "未", "申", "戌", "亥", "丑"] # 阳干寄禄， 阴干寄冠带
    GAN_to_ZHI = dict(zip(GAN, GAN_JIGONG))
    def __init__(self, dayGZ, tianDiPan):
        '''
        :param str(2) dayGZ
        :param TianDiPan tianDiPan
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

        if hasattr(self.tianDiPan, "tianJiangPan"):
            self.upper_tianjiang = [self.tianDiPan.get_tianjiang(zhi) for zhi in self.upper]

        for i in range(4):
            self.Ke.append((under[i], upper[i]))

        self.shangshen_ke_dayG, self.dayG_ke_shangshen = self.count_yaoke()
        self.shang_ke_xia, self.xia_zei_shang = self.count_zeike()

    def count_zeike(self):
        shang_ke_xia  = [shang for (xia, shang) in self.Ke if tools.shengke_WUXING(shang, xia)=="克"] 
        xia_zei_shang = [shang for (xia, shang) in self.Ke if tools.shengke_WUXING(xia, shang)=="克"] 
        return shang_ke_xia, xia_zei_shang

    def count_yaoke(self):
        shangshen_ke_dayG = [shangshen for shangshen in self.upper[1:] if tools.shengke_WUXING(shangshen, self.dayG)=="克"] # 上神克干
        dayG_ke_shangshen = [shangshen for shangshen in self.upper[1:] if tools.shengke_WUXING(self.dayG, shangshen)=="克"] # 干克上神
        return shangshen_ke_dayG, dayG_ke_shangshen

    def __str__(self):
        if hasattr(self, "upper_tianjiang"):
            ke = []
            ke.append("\u3000\u3000%s\u3000\u3000" % "".join(self.upper_tianjiang[::-1]))
            ke.append("\u3000\u3000%s\u3000\u3000" % "".join(self.upper[::-1]))
            ke.append("\u3000\u3000%s\u3000\u3000" % "".join(self.under[::-1]))
            s = "\n".join(ke)
        else:
            # a[start:stop:step] # start through not past stop, by step
            s = "".join(self.upper[::-1]) + '\n' + "".join(self.under[::-1])
        return s

    def compact_string(self):
        res = []
        for i in range(4):
            res += [*self.Ke[i], self.upper_tianjiang[i]]
        return ''.join(res)

class SanChuan(object):
    '''
    九宗门:
    贼克法:重审:一下贼上 元首:一上克下
    比用法:
    涉害法:
    '''
    def __init__(self, siKe, tianDiPan=None):
        self.siKe = siKe
        self.dayGZ = siKe.dayGZ
        self.tianDiPan = siKe.tianDiPan if tianDiPan is None else tianDiPan
        self.generate_sanchuan()

        if hasattr(self.siKe, "upper_tianjiang"):
            self.chuan_tianjiang = [self.tianDiPan.get_tianjiang(zhi) for zhi in self.chuan]
            self.xun_dun = [tools.xundun(self.dayGZ, zhi) for zhi in self.chuan]
            self.liu_qin = [tools.liuqin(other=zhi, base=self.dayGZ[0]) for zhi in self.chuan]

    def __str__(self):
        if hasattr(self, "chuan_tianjiang"):
            sc = []
            sc.append("\u3000\u3000%c%c%c%c\u3000\u3000" % (self.liu_qin[0], self.xun_dun[0], self.chuan[0], self.chuan_tianjiang[0]))
            sc.append("\u3000\u3000%c%c%c%c\u3000\u3000" % (self.liu_qin[1], self.xun_dun[1], self.chuan[1], self.chuan_tianjiang[1]))
            sc.append("\u3000\u3000%c%c%c%c\u3000\u3000" % (self.liu_qin[2], self.xun_dun[2], self.chuan[2], self.chuan_tianjiang[2]))
            return "\n".join(sc)
        else:
            return "\n".join(self.chuan)

    def compact_string(self):
        sc = []
        sc.append("%c%c%c%c" % (self.liu_qin[0], self.xun_dun[0], self.chuan[0], self.chuan_tianjiang[0]))
        sc.append("%c%c%c%c" % (self.liu_qin[1], self.xun_dun[1], self.chuan[1], self.chuan_tianjiang[1]))
        sc.append("%c%c%c%c" % (self.liu_qin[2], self.xun_dun[2], self.chuan[2], self.chuan_tianjiang[2]))        
        return ''.join(sc)

    def generate_sanchuan(self):
        num_zei = len(self.siKe.xia_zei_shang)
        num_she = len(self.siKe.shang_ke_xia)
        sum_ke = len(self.siKe.shangshen_ke_dayG) + len(self.siKe.dayG_ke_shangshen) + num_zei + num_she
        if self.tianDiPan.FuYin and sum_ke==0:
            self.type = "伏吟"
            chuan1 = self.fuyinfa()
        elif self.tianDiPan.FanYin and sum_ke==0:
            self.type = "反吟"
            chuan1 = self.fanyinfa()
        else:
            num_sike = len(set(self.siKe.upper))
            if num_zei==0 and num_she==0:
                if num_sike==2:
                    # 四课两备 不取遥克 
                    self.type = "八专"
                    chuan1 = self.bazhuanfa()
                elif len(self.siKe.shangshen_ke_dayG)>0 or len(self.siKe.dayG_ke_shangshen)>0:
                    self.type = "遥克"
                    chuan1 = self.yaokefa()
                    chuan2, chuan3 = self.chuan23(chuan1)
                    self.chuan = (chuan1, chuan2, chuan3)
                else:                    
                    if num_sike==4:
                        # 四课全备 有遥克取遥克
                        self.type = "昴星"
                        chuan1 = self.maoxingfa()
                    else:
                        assert num_sike==3
                        # 四课三备 有遥克取遥克
                        self.type = "别责"
                        chuan1 = self.biezefa()
            else:
                chuan1 = self.zeike_then_biyong_then_shehai()
                chuan2, chuan3 = self.chuan23(chuan1)
                self.chuan = (chuan1, chuan2, chuan3)
        return self.chuan


    def fuyinfa(self):
        '''
        伏吟法
        '''
        def get_chuan2(chuan1, ganzhi):
            xing = self.get_ZHI_xiangxing(chuan1)
            chuan2 = self.tianDiPan.get_upper(ganzhi) if chuan1==xing else xing
            return chuan2

        if len(self.siKe.xia_zei_shang)==1:
            # 不虞格
            chuan1 = self.siKe.xia_zei_shang[0]
            chuan2 = get_chuan2(chuan1=chuan1, ganzhi=self.dayGZ[1])
        elif len(self.siKe.shang_ke_xia)==1:
            # 不虞格
            chuan1 = self.siKe.shang_ke_xia[0]
            chuan2 = get_chuan2(chuan1=chuan1, ganzhi=self.dayGZ[1])
        else:
            assert len(self.siKe.xia_zei_shang)==0 and len(self.siKe.shang_ke_xia)==0
            if self.get_yinyang(self.dayGZ[0])=="阳":
                # 自任格
                chuan1 = self.tianDiPan.get_upper(self.dayGZ[0])
                chuan2 = get_chuan2(chuan1=chuan1, ganzhi=self.dayGZ[1])
            elif self.get_yinyang(self.dayGZ[0])=="阴":
                # 自信格
                chuan1 = self.tianDiPan.get_under(self.dayGZ[1])
                chuan2 = get_chuan2(chuan1=chuan1, ganzhi=self.dayGZ[0])
            else:
                raise ValueError("must be one of '阴阳'")
        xing = self.get_ZHI_xiangxing(chuan2)
        chuan3 = self.get_ZHI_liuchong(chuan2) if chuan2==xing else xing
        self.chuan = (chuan1, chuan2, chuan3)
        return chuan1

    def fanyinfa(self):
        '''
        返吟法
        无依格:有贼克以贼克发用
        无奈格:无贼克以驿马发用

        '''
        chuan1 = self.zeike_then_biyong_then_shehai(type_overwrite="返吟", sike_may_substitute_bihe=False)
        if chuan1==-1:
            # 无奈格
            chuan1 = self.get_yima(self.dayGZ[1])
            chuan2 = self.tianDiPan.get_upper(self.dayGZ[1])
            chuan3 = self.tianDiPan.get_upper(self.dayGZ[0])
        else:
            # 无依格
            chuan2 = self.get_ZHI_liuchong(chuan1)
            chuan3 = self.get_ZHI_liuchong(chuan2)
        self.chuan = (chuan1, chuan2, chuan3)
        return chuan1


    def yaokefa(self):
        '''
        遥克法:
        蒿矢格:上神(shangshen)克日干
        弹射格:四课不克日干，取日干克二三四课发用

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
        虎视格:   阳日取地盘酉上神发用, 支上神为中传, 干上神为末传
        冬蛇掩目格:阴日取天盘酉下神发用, 干上神为中传, 支上神为末传
        '''
        if self.get_yinyang(self.dayGZ[0])=="阳":
            chuan1 = self.tianDiPan.get_upper("酉")
            chuan2 = self.tianDiPan.get_upper(self.dayGZ[1])
            chuan3 = self.tianDiPan.get_upper(self.dayGZ[0])
        elif self.get_yinyang(self.dayGZ[0])=="阴":
            chuan1 = self.tianDiPan.get_under("酉")
            chuan2 = self.tianDiPan.get_upper(self.dayGZ[0])
            chuan3 = self.tianDiPan.get_upper(self.dayGZ[1])
        else:
            raise ValueError("must be one of '阴阳'")
        self.chuan = (chuan1, chuan2, chuan3)
        return chuan1

    def biezefa(self):
        '''
        别责法
        '''
        if self.get_yinyang(self.dayGZ[0])=="阳":
            Gan_he = self.get_GAN_wuhe(self.dayGZ[0]) # 天干五合，取干之五合
            chuan1 = self.tianDiPan.get_upper(Gan_he)
            chuan2 = self.tianDiPan.get_upper(self.dayGZ[0])
            chuan3 = self.tianDiPan.get_upper(self.dayGZ[0])
        elif self.get_yinyang(self.dayGZ[0])=="阴":
            Zhi_he1, Zhi_he2 = self.get_ZHI_sanhe(self.dayGZ[1])
            chuan1 = Zhi_he1
            chuan2 = self.tianDiPan.get_upper(self.dayGZ[0])
            chuan3 = self.tianDiPan.get_upper(self.dayGZ[0]) 
        else:
            raise ValueError("must be one of '阴阳'")                   
        self.chuan = (chuan1, chuan2, chuan3)
        return chuan1

    def bazhuanfa(self):
        '''
        八专法
        '''
        if self.get_yinyang(self.dayGZ[0])=="阳":
            chuan1 = self.tianDiPan.tianPan.step(self.siKe.upper[0], move=2)
            chuan2 = self.tianDiPan.get_upper(self.dayGZ[0])
            chuan3 = self.tianDiPan.get_upper(self.dayGZ[0])
        elif self.get_yinyang(self.dayGZ[0])=="阴":
            chuan1 = self.tianDiPan.tianPan.step(self.siKe.upper[-1], move=-2)
            chuan2 = self.tianDiPan.get_upper(self.dayGZ[0])
            chuan3 = self.tianDiPan.get_upper(self.dayGZ[0])   
        else:
            raise ValueError("must be one of '阴阳'")     
        self.chuan = (chuan1, chuan2, chuan3)
        return chuan1

    
    def zeike_then_biyong_then_shehai(self, type_overwrite=None, sike_may_substitute_bihe=True):
        chuan1 = self.zeikefa(zei=self.siKe.xia_zei_shang, ke=self.siKe.shang_ke_xia)
        self.type = "贼克"
        if chuan1==-1:
            chuan1 = self.biyongfa()
            self.type = "比用"
            # print("比合=", bihe)
        if chuan1==-1:
            assert hasattr(self, "_bihe")
            if len(self._bihe)==0:
                if sike_may_substitute_bihe:
                    chuan1 = self.shehaifa(self.siKe.upper)
                else:
                    chuan1 = -1
            else:
                chuan1 = self.shehaifa(self._bihe)
            self.type = "涉害"
        if type_overwrite is not None:
            self.type = type_overwrite
        return chuan1
 
    def zeikefa(self, zei, ke):
        '''
        # 始入课:仅一下贼上
        # 重审课:除一下贼上，还有上克下，仍取下贼上
        # 元首课:无下贼上，仅一上克下
        '''
        if len(zei)==1:
            # 始入课/重审课
            return zei[0]
        elif len(zei)==0 and len(ke)==1:
            # 元首课
            return ke[0]
        else:
            return -1

    def biyongfa(self):
        shang_ke_xia = self.siKe.shang_ke_xia
        xia_zei_shang = self.siKe.xia_zei_shang
        if len(shang_ke_xia)==0 and len(xia_zei_shang)==0:
            self._bihe = []
            return -1
        if len(xia_zei_shang) > 1:
            # 比用课：多下贼上选与日干比用者
            bihe = self.get_bihe(self.siKe.dayG, xia_zei_shang)
        elif len(shang_ke_xia) > 1:
            # 知一课：多上克下选与日干比用者
            bihe = self.get_bihe(self.siKe.dayG, shang_ke_xia)

        if len(set(bihe))==1:
            return bihe[0]
        else:
            self._bihe = bihe
            return -1

    def shehaifa(self, check_list, dayGZ=None):
        '''
        涉害课:涉害不等
        见机格:涉害相等，取四孟
        察微格:无当四孟，取四仲
        缀瑕格:无当四仲，阳日取干上神，阴日取支上神
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
            count +=1 if tools.shengke_WUXING(current_di, zhi)=="克" else 0
            GAN_jigong = tdp.ZHI_to_GAN_JIGONG[current_di] if current_di in tdp.ZHI_to_GAN_JIGONG.keys() else ""
            for gan in GAN_jigong:
                count +=1 if tools.shengke_WUXING(gan, zhi)=="克" else 0
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

    @staticmethod
    def get_GAN_wuhe(gan):
        G_he = GAN[(GAN.index(gan) + 5) % 10] # 天干五合，取干之五合
        return G_he

    @staticmethod
    def get_ZHI_sanhe(zhi):
        zhi1 = ZHI[(ZHI.index(zhi) + 4) % 12]
        zhi2 = ZHI[(ZHI.index(zhi1) + 4) % 12]
        return zhi1, zhi2

    @staticmethod
    def get_ZHI_xiangxing(zhi):
        '''
        地支相刑
        '''
        #ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        xing = ["卯", "戌", "巳", "子", "辰", "申", "午", "丑", "寅", "酉", "未", "亥"]
        map_xing = dict(zip(ZHI, xing))
        return map_xing[zhi]

    @staticmethod
    def get_ZHI_liuchong(zhi):
        '''
        地支相冲
        '''
        chong = ZHI[(ZHI.index(zhi) + 6) % 12]
        return chong

    @staticmethod
    def get_yima(zhi):
        '''
        驿马: 申子辰在寅, 寅午戌在申, 巳酉丑在亥, 亥卯未在巳
        '''
        #ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        yima = ["寅", "亥", "申", "巳", "寅", "亥", "申", "巳", "寅", "亥", "申", "巳"]
        map_yima = dict(zip(ZHI, yima))
        return map_yima[zhi]        



def test():
    checking_list = [{"day":"丙戌","hour":"巳","yuejiang":"申","type":"贼克","chuan1":"申"},
                     {"day":"丁丑","hour":"子","yuejiang":"申","type":"贼克","chuan1":"巳"},
                     {"day":"戊寅","hour":"子","yuejiang":"巳","type":"比用","chuan1":"子"},
                     {"day":"壬辰","hour":"巳","yuejiang":"辰","type":"比用","chuan1":"戌"},
                     {"day":"甲辰","hour":"卯","yuejiang":"亥","type":"涉害","chuan1":"子"},
                     {"day":"丙子","hour":"辰","yuejiang":"亥","type":"涉害","chuan1":"子"},
                     {"day":"庚午","hour":"辰","yuejiang":"申","type":"涉害","chuan1":"辰"},
                     {"day":"戊辰","hour":"辰","yuejiang":"亥","type":"涉害","chuan1":"子"},
                     {"day":"壬辰","hour":"寅","yuejiang":"巳","type":"遥克","chuan1":"戌"},
                     {"day":"壬申","hour":"申","yuejiang":"亥","type":"遥克","chuan1":"巳"},
                     {"day":"戊寅","hour":"申","yuejiang":"子","type":"昴星","chuan1":"丑"},
                     {"day":"丁亥","hour":"寅","yuejiang":"巳","type":"昴星","chuan1":"午"},
                     {"day":"丙辰","hour":"巳","yuejiang":"午","type":"别责","chuan1":"亥"},
                     {"day":"辛酉","hour":"子","yuejiang":"亥","type":"别责","chuan1":"丑"},
                     {"day":"甲寅","hour":"申","yuejiang":"巳","type":"八专","chuan1":"丑"},
                     {"day":"丁未","hour":"酉","yuejiang":"子","type":"八专","chuan1":"亥"},
                     {"day":"己未","hour":"辰","yuejiang":"午","type":"八专","chuan1":"酉"},
                     {"day":"癸丑","hour":"子","yuejiang":"子","type":"伏吟","chuan1":"丑"},
                     {"day":"丙辰","hour":"寅","yuejiang":"寅","type":"伏吟","chuan1":"巳"},
                     {"day":"丁丑","hour":"申","yuejiang":"申","type":"伏吟","chuan1":"丑"},
                     {"day":"壬辰","hour":"亥","yuejiang":"亥","type":"伏吟","chuan1":"亥"},
                     {"day":"庚戌","hour":"巳","yuejiang":"亥","type":"返吟","chuan1":"寅"},
                     {"day":"辛丑","hour":"寅","yuejiang":"申","type":"返吟","chuan1":"亥"}
    ]
    for item in checking_list:
        print(item)
        sc = SanChuan(SiKe(item["day"],TianDiPan(hourZ=item["hour"], YueJiang=item["yuejiang"])))
        if sc.chuan[0]==item["chuan1"] and sc.type==item["type"]:
            print("checked")
            print(sc)
        else:
            print("error")
            print(sc)

if __name__ == "__main__":
    test()
    lrp = LiuRenPan(dayGZ='辛丑', hourZ='寅', YueJiang='申')
    print(lrp)

