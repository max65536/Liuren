from SolarLunarDatetime import SolarLunarDatetime
from LiuRenPan import LiuRenPan
import datetime
from analyser import check_keti, check_bifa
from IPython import embed
from pytz import timezone
from printer import Printer
from consts import YUEJIANG_to_NAME
from models import DocumentModel

import tools
import asyncio

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
        texts.append("{0}年\u3000{1}月\u3000{2}日\u3000{3}时\u3000".format(*list(self.sizhu.values())[::-1] ))
        texts.append("旬首：{0}\u3000{1}空\u3000{2}{3}将".format(tools.xunshou(self.sizhu['day']), tools.kongwang(self.sizhu['day']), 
                    YUEJIANG_to_NAME[self.yuejiang], self.yuejiang) )

        texts.append('\n')
        texts.append(Printer.three_in_one(self.lrp))

        texts.append('\n')
        texts.append("占问：" + self.question)
        
        return '\n'.join(texts)
    
    async def save_to_database(self, message_id=None):
        self.document_model = DocumentModel(sizhu=tools.sizhu_to_string(self.sizhu), yuejiang=self.yuejiang, 
                        tianpan=str(self.lrp.tianDiPan.tianPan), tianjiangpan=str(self.lrp.tianDiPan.tianJiangPan), dungan=str(self.lrp.tianDiPan.dunGanPan),
                        sike=self.lrp.siKe.compact_string(), sanchuan=self.lrp.sanChuan.compact_string(),
                        question=self.question,
                        message_id = message_id
                        )
        await self.document_model.save()

    async def update_to_database(self, message_id=None, **kwargs):
        pass
        
async def test(loop):
    import orm
    await orm.create_pool(loop=loop,host='localhost',port=3306,user='root',password='root',db='liuren')

    res = await DocumentModel.findAll(where="message_id=255")
    print(res)
    print(type(res[0]))
    return res





if __name__=="__main__":


    loop = asyncio.get_event_loop()

    res = loop.run_until_complete(test(loop))

    # loop.create_task(init(loop=loop))
    # asyncio.run(DocumentModel.find(2))

    
    # document = Document("test: hello Liuren!") 
    # asyncio.run(document.save_to_database())
    
    embed()
    loop.close()



