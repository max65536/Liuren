
from LiuRenPan import LiuRenPan

class Printer(object):
    def __init__(self, liurenpan, format="string", space='\u3000') -> None:
        self.space = '\u3000'

    @staticmethod
    def tiandipan(tdp):
        lst = tdp.tianPan.items
        tjp = tdp.tianJiangPan.items
        dun = tdp.dunGanPan.items
        pan = []
        pan.append("%c%c%c%c%c%c%c%c" % ("\u3000", "\u3000", dun[5], dun[6], dun[7], dun[8], "\u3000", "\u3000"))
        pan.append("%c%c%c%c%c%c%c%c" % ("\u3000", "\u3000", tjp[5], tjp[6], tjp[7], tjp[8], "\u3000", "\u3000"))
        pan.append("%c%c%c%c%c%c%c%c" % ("\u3000", "\u3000", lst[5], lst[6], lst[7], lst[8], "\u3000", "\u3000"))
        pan.append("%c%c%c    %c%c%c" % ( dun[4], tjp[4],    lst[4],                 lst[9], tjp[9], dun[9]))
        pan.append("%c%c%c    %c%c%c" % ( dun[3], tjp[3],    lst[3],                 lst[10],tjp[10],dun[10] ))
        pan.append("%c%c%c%c%c%c%c%c" % ("\u3000", "\u3000", lst[2], lst[1], lst[0], lst[11], "\u3000", "\u3000"))
        pan.append("%c%c%c%c%c%c%c%c" % ("\u3000", "\u3000", tjp[2], tjp[1], tjp[0], tjp[11], "\u3000", "\u3000"))
        pan.append("%c%c%c%c%c%c%c%c" % ("\u3000", "\u3000", dun[2], dun[1], dun[0], dun[11], "\u3000", "\u3000"))
        return '\n'.join(pan)       

    def to_string(self):
        pass

    def to_fig(self):
        pass
    
    @staticmethod
    def three_in_one(lrp):
        tdp      = lrp.tianDiPan
        sike     = lrp.siKe
        sanchuan = lrp.sanChuan

        lst = tdp.tianPan.items
        tjp = tdp.tianJiangPan.items
        dun = tdp.dunGanPan.items
        pan = []
        pan.append(''.join(["\u3000", "\u3000", dun[5],  dun[6],  dun[7],   dun[8], "\u3000", "\u3000" , "\u3000", *sike.upper_tianjiang[::-1]] ))
        pan.append(''.join(["\u3000", "\u3000", tjp[5],  tjp[6],  tjp[7],   tjp[8], "\u3000", "\u3000" , "\u3000", *sike.upper[::-1]] ))
        pan.append(''.join(["\u3000", "\u3000", lst[5],  lst[6],  lst[7],   lst[8], "\u3000", "\u3000" , "\u3000", *sike.under[::-1]] ))
        pan.append(''.join([ dun[4], tjp[4],    lst[4], "\u3000", "\u3000", lst[9],   tjp[9], dun[9]   , "\u3000", "\u3000","\u3000","\u3000","\u3000"    ] ))
        pan.append(''.join([ dun[3], tjp[3],    lst[3], "\u3000", "\u3000", lst[10],  tjp[10],dun[10]  , "\u3000", "\u3000","\u3000","\u3000","\u3000"    ] ))
        pan.append(''.join(["\u3000", "\u3000", lst[2],  lst[1],  lst[0],   lst[11], "\u3000", "\u3000", "\u3000", sanchuan.liu_qin[0], sanchuan.xun_dun[0], sanchuan.chuan[0], sanchuan.chuan_tianjiang[0]] ))
        pan.append(''.join(["\u3000", "\u3000", tjp[2],  tjp[1],  tjp[0],   tjp[11], "\u3000", "\u3000", "\u3000", sanchuan.liu_qin[1], sanchuan.xun_dun[1], sanchuan.chuan[1], sanchuan.chuan_tianjiang[1]] ))
        pan.append(''.join(["\u3000", "\u3000", dun[2],  dun[1],  dun[0],   dun[11], "\u3000", "\u3000", "\u3000", sanchuan.liu_qin[2], sanchuan.xun_dun[2], sanchuan.chuan[2], sanchuan.chuan_tianjiang[2]] ))
        return '\n'.join(pan)       

