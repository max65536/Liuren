

def check_keti(lrp):
    '''
    课体
    '''
    keti = []
    siKe = lrp.siKe
    if siKe.upper[0] in "辰戌" or siKe.upper[2] in "辰戌":
        keti.append("斩关")
    if len(siKe.xia_zei_shang)==3 or len(siKe.shang_ke_xia)==3:
        keti.append("度厄")


    return keti

def check_bifa(lrp):
    '''
    毕法赋
    '''
    
    pass
    # if 