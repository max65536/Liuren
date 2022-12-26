from SolarLunarDatetime import SolarLunarDatetime
from LiuRenPan import LiuRenPan
import datetime
from analyser import check_keti, check_bifa
from IPython import embed

def main():
    #test()
    current_date_time = datetime.datetime.now()
    solartime = SolarLunarDatetime.init_from_solar(current_date_time.year, current_date_time.month, current_date_time.day, current_date_time.hour)
    # lrp = LiuRenPan(dayGZ=solartime.GanZhi['day'], hourZ=solartime.GanZhi['hour'][1], YueJiang=solartime.YueJiang)
    lrp = LiuRenPan.init_from_sizhu(sizhu=solartime.GanZhi, YueJiang=solartime.YueJiang)
    print(lrp)
    embed()

if __name__ == "__main__":
    main()
    # embed()
