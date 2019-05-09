import sample.file
import etc.time

file = sample.file.File()

dir = ["csv", "cpu"]
data = [str(a) for a in range(10)]

dirPath = file.generateDirPath(dir)
fileName = file.generateFile(dirPath, "cpu", etc.time.getYMD_HM(), 'csv')

file.saveListToCsv(data, dirPath, fileName)