import testcodes.testFunctions as func
import sample.danawa
import sample.items

comp = sample.items.hdd.Hdd.instance()
dnw = sample.danawa.Danawa()

func.printCrawlingDataOneComponent(comp, dnw)