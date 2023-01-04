from SolarLunarDatetime import SolarLunarDatetime
from LiuRenPan import LiuRenPan
import datetime
from analyser import check_keti, check_bifa
from IPython import embed
from pytz import timezone
from printer import Printer
from consts import YUEJIANG_to_NAME

import tools

def datetime_as_timezone(date_time, time_zone):
    tz = timezone(time_zone)
    return date_time.astimezone(tz)

class Document(object):
    def __init__(self, question, time=None, location='Asia/Shanghai'):
        self.lrp = self.generate(location, time=time)
        self.question = question

    def generate(self, time_zone='Asia/Shanghai', time=None):
        date_time = datetime.datetime.now() 
        local_date_time = datetime_as_timezone(date_time=date_time, time_zone=time_zone) if time is None else time
        solartime = SolarLunarDatetime.init_from_solar(local_date_time.year, local_date_time.month, local_date_time.day, local_date_time.hour)

        # lrp = LiuRenPan(dayGZ=solartime.GanZhi['day'], hourZ=solartime.GanZhi['hour'][1], YueJiang=solartime.YueJiang)
        lrp = LiuRenPan.init_from_sizhu(sizhu=solartime.GanZhi, YueJiang=solartime.YueJiang)
        
        self.date_time = local_date_time
        self.sizhu = solartime.GanZhi
        self.yuejiang = solartime.YueJiang
        return lrp

    def get_text(self):
        texts = [self.date_time.strftime('%Y年%m月%d日 %H:%M:%S')]
        texts.append("{0}年\u3000{1}月\u3000{2}日\u3000{3}时\u3000".format(*list(self.sizhu.values()) ))
        texts.append("旬首：{0}\u3000{1}空\u3000{2}{3}将".format(tools.xunshou(self.sizhu['day']), tools.kongwang(self.sizhu['day']), 
                    YUEJIANG_to_NAME[self.yuejiang], self.yuejiang) )

        texts.append('\n')
        texts.append(Printer.three_in_one(self.lrp))

        texts.append('\n')
        texts.append("占问：" + self.question)
        
        return '\n'.join(texts)

if __name__=="__main__":
    document = Document("test: hello Liuren!") 
    embed()
    



