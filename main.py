from crawler import Crawler
from items.danawa import mainboard, power, ram, hdd, vga, cpu
from threading import Thread
import file

# url: danawa.com / tab: ad / limit: number of products / query: something to search
url_search = "http://search.danawa.com/dsearch.php?tab=goods&limit=90&query="

if __name__ == "__main__":
    cpu = cpu.Cpu.instance()
    vga = vga.Vga.instance()
    ram = ram.Ram.instance()
    mainboard = mainboard.Mainboard.instance()
    hdd = hdd.Hdd.instance()
    power = power.Power.instance()

    assorters = [cpu, ram, vga, mainboard, hdd, power]

    crawlers = []
    threads = []

    for com in assorters:
        c = Crawler()
        f = file.File()
        f.create_csv(com._name)

        url = url_search + com.get_name()
        if com.get_name() == 'cpu':
            pages = 3
        else:
            pages = 9

        t = Thread(target=c.crawling_to_csv, args=(url, pages, com, f))
        threads.append(t)
        crawlers.append(c)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    for c in crawlers:
        c.quit()