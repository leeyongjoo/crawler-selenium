from sample import danawa, crawler
from sample.items import cpu,hdd,mainboard,power,ram,vga
import sample.file
import testcodes.testFunctions as func
from threading import Thread
import time

# 객체 생성
dnw = danawa.Danawa()
file = sample.file.File()
# 각 부품 객체 생성
components = []
components.append(hdd.Hdd.instance())
components.append(mainboard.Mainboard.instance())
components.append(power.Power.instance())

# [멀티스레드]
def checkThreadTime():
    # 1-1 멀티스레드를 이용하지 않고 순차적으로 돌려서 시간 측정
    startTime = time.time()
    func.doCrawlingDataComponents(components, dnw)
    print("순차적으로 돌려서 시간 측정: {} sec".format(time.time()-startTime))

    # 1-2 멀티스레드를 이용하여 시간 측정
    startTime = time.time()
    threads = []
    for comp in components:
        t = Thread(target=func.doCrawlingDataOneComponent, args=(comp, dnw))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print("멀티스레드를 이용하여 시간 측정: {} sec".format(time.time()-startTime))

# [파일]
def checkFileTime():
    # 2-1 한 페이지 마다 매번 파일에 저장
    startTime = time.time()
    func.doCrawlingDataAndSaveFileOften(components, dnw, file)
    print("한 페이지 마다 매번 파일에 저장: {} sec".format(time.time() - startTime))
    # 2-2 모든 페이지를 하나의 리스트에 저장한 후 마지막에 한번 파일에 저장
    startTime = time.time()
    func.doCrawlingDataAndSaveFileOnce(components, dnw, file)
    print("모든 페이지를 하나의 리스트에 저장한 후 마지막에 한번 파일에 저장: {} sec".format(time.time() - startTime))

if __name__ == "__main__":
    # checkThreadTime()
    checkFileTime()