from SolarLunarDatetime import SolarLunarDatetime
from LiuRenPan import LiuRenPan
import datetime
from analyser import check_keti, check_bifa
from IPython import embed
from pytz import timezone

def main():
    #test()
    current_date_time = datetime.datetime.now()
    solartime = SolarLunarDatetime.init_from_solar(current_date_time.year, current_date_time.month, current_date_time.day, current_date_time.hour)
    # lrp = LiuRenPan(dayGZ=solartime.GanZhi['day'], hourZ=solartime.GanZhi['hour'][1], YueJiang=solartime.YueJiang)
    lrp = LiuRenPan.init_from_sizhu(sizhu=solartime.GanZhi, YueJiang=solartime.YueJiang)
    print(lrp)
    embed()

def datetime_as_timezone(date_time, time_zone):
    tz = timezone(time_zone)
    utc = timezone('UTC')
    return date_time.replace(tzinfo=utc).astimezone(tz)

def generate(time_zone='Asia/Shanghai'):
    date_time = datetime.datetime.now()
    local_date_time = datetime_as_timezone(date_time=date_time, time_zone=time_zone)
    solartime = SolarLunarDatetime.init_from_solar(local_date_time.year, local_date_time.month, local_date_time.day, local_date_time.hour)
    # lrp = LiuRenPan(dayGZ=solartime.GanZhi['day'], hourZ=solartime.GanZhi['hour'][1], YueJiang=solartime.YueJiang)
    lrp = LiuRenPan.init_from_sizhu(sizhu=solartime.GanZhi, YueJiang=solartime.YueJiang)
    # embed()      
    return lrp


if __name__ == "__main__":
    generate()
    # embed()
