GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
WUXING = ["木", "火", "土", "金", "水"]
SHUXIANG = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
NUMBER = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
YUE = ["十一", "十二", "正", "二", "三", "四", "五", "六", "七", "八", "九", "十" ]
RI = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十", 
    "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十", 
    "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十", "卅一"]
CONSTELLATION = ['摩羯', '水瓶', '双鱼', '白羊', '金牛', '双子', '巨蟹', '狮子', '处女', '天秤', '天蝎', '射手']
WEEKDAY = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]

JIEQI                     = ["冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑","白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪"]
mapping_JIEQI_to_YUEJIANG = [   0  ,     0 ,     1 ,     1 ,     2 ,     2 ,     3 ,     3 ,     4 ,     4 ,     5 ,     5 ,     6 ,    6 ,     7 ,     7 ,     8 ,     8 ,     9 ,     9 ,     10,     10,     11,     11]
YUEJIANG = ["丑","子","亥","戌","酉","申","未","午","巳","辰","卯","寅"]
'''
正月，北斗勺柄指向寅，月建为寅；在雨水节气后，太阳落山处于二十八宿室、壁亥宫，故月将为登明亥
二月，北斗勺柄指向卯，月建为卯；在春分节气后，太阳落山处于二十八宿奎、娄戌宫，故月将河魁戌
三月，北斗勺柄指向辰，月建为辰；在谷雨节气后，太阳落山处于二十八宿胃、昴、毕酉宫，故月将从魁酉
四月，北斗勺柄指向巳，月建为巳；在小满节气后，太阳落山处于二十八宿觜、参申宫，故月将传送申
五月，北斗勺柄指向午，月建为午；在夏至节气后，太阳落山处于二十八宿井、鬼未宫，故月将小吉未
六月，北斗勺柄指向未，月建为未；在大暑节气后，太阳落山处于二十八宿柳、星、张午宫，故月将胜光午
七月，北斗勺柄指向申，月建为申；在处暑节气后，太阳落山处于二十八宿翼、轸巳宫，故月将太乙巳
八月，北斗勺柄指向酉，月建为酉；在秋分节气后，太阳落山处于二十八宿角、亢辰宫，故月将天罡辰
九月，北斗勺柄指向戌，月建为戌；在霜降节气后，太阳落山处于二十八宿氐、房、心卯宫，故月将太冲卯
十月，北斗勺柄指向亥，月建为亥；在小雪节气后，太阳落山处于二十八宿尾、箕寅宫，故月将功曹寅
冬月，北斗勺柄指向子，月建为子；在冬至节气后，太阳落山处于二十八宿斗、牛丑宫，故月将大吉丑
腊月，北斗勺柄指向丑，月建为丑；在大寒节气后，太阳落山处于二十八宿女、虚、危子宫，故月将神后子
'''