import testcodes.testFunctions as func
import sample.danawa
import sample.items.cpu

comp = sample.items.cpu.Cpu.instance()
dnw = sample.danawa.Danawa()


func.printCrawlingDataOneComponent(comp, dnw)