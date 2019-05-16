import testcodes.testFunctions as func
import sample.danawa
import sample.items

comp = sample.items.power.Power.instance()
dnw = sample.danawa.Danawa()

func.printCrawlingDataOneComponentOnePage(comp, dnw)