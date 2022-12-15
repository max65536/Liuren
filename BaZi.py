import tools
from prettytable import PrettyTable
from IPython import embed

class BaZi(object):

    def __init__(self, yearGZ, monthGZ, dayGZ, hourGZ):
        self.yearGZ  = yearGZ
        self.monthGZ = monthGZ
        self.dayGZ   = dayGZ
        self.hourGZ  = hourGZ
        self.gan     = [yearGZ[0], monthGZ[0], dayGZ[0], hourGZ[0]]
        self.zhi     = [yearGZ[1], monthGZ[1], dayGZ[1], hourGZ[1]]

        self.dayG = dayGZ[0]


    def __str__(self):
        return ''.join(self.gan) + '\n' + ''.join(self.zhi)


    def pretty_table(self, has_color=True):
        sizhu_table = PrettyTable()
        columns = ["年柱", "月柱", "日柱", "时柱"]
        if has_color:
            sizhu_table.add_column(columns[0], [tools.wrap_color(x) for x in self.yearGZ])
            sizhu_table.add_column(columns[1], [tools.wrap_color(x) for x in self.monthGZ])
            sizhu_table.add_column(columns[2], [tools.wrap_color(x) for x in self.dayGZ])
            sizhu_table.add_column(columns[3], [tools.wrap_color(x) for x in self.hourGZ])
        else:
            sizhu_table.add_column(columns[0], self.yearGZ)
            sizhu_table.add_column(columns[1], self.monthGZ)
            sizhu_table.add_column(columns[2], self.dayGZ)
            sizhu_table.add_column(columns[3], self.hourGZ)
        return sizhu_table

if __name__=='__main__':
    bz = BaZi(yearGZ="辛丑", monthGZ="壬寅", dayGZ="丙戌", hourGZ="癸丑")
    print(bz.pretty_table())
    embed()    
