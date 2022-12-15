from LiuRenPan import LiuRenPan


Class BiFa(object):

    def __init__(original_text):
        pass


def fa1(lrp):
    '''
    第一法：前后引从升迁吉
    '''
    chuan = lrp.sanChuan.chuan
    tianDiPan = lrp.tianDiPan
    dayGZ = lrp.dayGZ
    guiren_daytime_pos = tianDiPan.tianJiangPan_daytime.find_pos("贵")
    guiren_night_pos   = tianDiPan.tianJiangPan_night.find_pos("贵")
    guiren_pos         = tianDiPan.tianJiangPan.find_pos("贵")
    
    def yincong(pan, yin, cong):
        if pan.step(cong, 2) == yin:
            return pan.step(cong, 1)
        return None
    def jiagong(pan, a, b):
        gong = yincong(a, b)
        if gong is None:
            gong = yincong(b, a)
        return gong

    answers = []
    if yincong(tianDiPan.tianPan, chuan[0], chuan[-1])==tianDiPan.get_upper(dayGZ[0]):
        ans = "引从天支格:初传居于干前(+1)，末传居于干后(-1):主官职升迁"
        if tianDiPan.diPan.find_pos(dayGZ[0])==guiren_pos or lrp.sanChuan.chuan_tianjiang[1]=="贵":
            ans = "拱贵格:初末传引从天干，并夹拱天乙贵人:主官职升迁" 
        answers.append(ans)
    if yincong(tianDiPan.tianPan, chuan[0], chuan[-1])==tianDiPan.get_upper(dayGZ[1]):
        ans = "引从地支格:初传居于支前(+1), 末传居于支后(-1):主家宅修葺"
        answers.append(ans)

    guiren_jiagong = jiagong(tianDiPan.tianPan, guiren_daytime_pos, guiren_night_pos)
    if guiren_jiagong==tianDiPan.get_upper(dayGZ[0]):
        ans = "两贵引从天干格:昼夜两贵引从天干:主受贵人提携，或得两贵引荐而成事"

    # TODO
    # if guiren_jiagong ==   年命，行年，本命，日禄

    if jiagong(tianDiPan.tianJiangPan, tianDiPan.)
        ans = "干支夹拱昼贵或夜贵"

    if jiagong():
        ans = "初传与中传拱地盘贵人"

        





'''
第一法：前后引从升迁吉，
第二法：首尾相见始终宜。
第三法：帘幕贵人高甲第，
第四法：催官使者赴官期。
第五法：六阳数足须公用，
第六法：六阴相继尽昏迷。
第七法：旺禄临身徒妄作，
第八法：权摄不正禄临支。
第九法：避难逃生须弃旧，
第十法：朽木难雕别作为。
第十一法：众鬼虽彰全不畏，
第十二法：虽忧狐假虎威仪。
第十三法：鬼贼当时无畏忌，
第十四法：传财太旺反财亏。
第十五法：脱上逢脱防虚诈，
第十六法：空上乘空事莫追。
第十七法：进茹空亡宜退步，
第十八法：踏脚空亡进用宜。
第十九法：胎财生气妻怀孕，
第二十法：胎财死气损胎推。
第二十一法：交车相合交关利，第二十二法：上下皆合两心齐。第二十三法：彼求我事支传干，第二十四法：我求彼事干传支。第二十五法：金日逢丁凶祸动，第二十六法：水日逢丁财动之。第二十七法：传财化鬼财休觅，第二十八法：传鬼化财钱险危。第二十九法：眷属丰盈居狭宅，第三十法：屋宅宽广致人衰。
第三十一法：三传递生人举荐，第三十二法：三传互克众人欺。第三十三法：有始无终难变易，第三十四法：苦去甘来乐里悲。第三十五法：人宅受脱俱招盗，第三十六法：干支皆败事倾颓。第三十七法：末助初兮三等讼，第三十八法：闭口卦体两般推。第三十九法：太阳照武宜擒贼，第四十法：后合占婚岂用媒。
第四十一法：富贵干支逢禄马，第四十二法：尊崇传内遇三奇。第四十三法：害贵讼直作曲断，第四十四法：课传俱贵转无依。第四十五法：昼夜贵加求两贵，第四十六法：贵人差迭事参差。第四十七法：贵虽在狱宜临干，第四十八法：鬼乘天乙乃神祗。第四十九法：两贵受克难干贵，第五十法：二贵皆空虚喜期。
第五十一法：魁度天门关隔定，第五十三法：罡塞鬼户任谋为。第五十三法：两蛇夹墓凶难免，第五十四法：虎视逢虎力难施。第五十五法：所谋多拙逢网罗，第五十六法：天网自裹己招非。第五十七法：费有余而得不足，第五十八法：用破身心无所归。第五十九法：华盖覆日人昏晦，第六十法：太阳射宅屋光辉。
第六十一法：干乘墓虎无占病，第六十二法：支乘墓虎有伏尸。第六十三法：彼此全伤防两损，第六十四法：夫妇芜淫各有私。第六十五法：干墓并关人宅废，第六十六法：支坟财并旅程稽。第六十七法：受虎克神为病症，第六十八法：制鬼之位乃良医。第六十九法：虎乘遁鬼殃非浅，第七十法：鬼临三四讼灾随。
第七十一法：病符克宅全家患，第七十二法：丧吊全逢挂缟衣。第七十三法：前后逼迫难进退，第七十四法：空空如也事休追。第七十五法：宾主不投刑在上，第七十六法：彼此猜忌害相随。第七十七法：互生俱生凡事益，第七十八法：互旺皆旺坐谋宜。第七十九法：干支值绝凡谋决，第八十法：人宅皆死各衰羸。
第八十一法：传墓入墓分憎爱。
第八十二法：不行传者考初时  第八十三法：万事喜忻三六合，第八十四法：合中犯杀蜜中砒。 第八十五法：初遭夹克不由己，第八十六法：将逢内战所谋危。 第八十七法：人宅坐墓甘招晦，第八十八法：干支乘墓各昏迷。 第八十九法：任信丁马须言动，第九十法：来去俱空岂动宜。
第九十一法：虎临干鬼凶速速，第九十二法：龙加生气吉迟迟。 第九十三法：妄用三传灾福异，第九十四法：喜惧空亡乃妙机。 第九十五法：六爻现卦防其克，第九十六法：旬内空亡逐类推。 第九十七法：所筮不入仍凭类，第九十八法：非占现类勿言之  第九十九法：常问不应逢吉象，第一百法：已灾凶逃返无疑。
'''
