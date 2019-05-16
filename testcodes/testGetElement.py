import testcodes.testFunctions as func
import sample.danawa
import sample.items

comp = sample.items.vga.Vga.instance()
dnw = sample.danawa.Danawa()

func.printCrawlingDataOneComponentOnePage(comp, dnw)