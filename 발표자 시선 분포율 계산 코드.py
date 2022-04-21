import os
import csv
# 자리별 가중치 파일 로드
weightingFileName = "positionWeighting"
weightingFilePath = "./source/" + weightingFileName + ".csv"
weightingFile = open(weightingFilePath, mode='r', encoding='utf-8-sig')
newWeightingFile = csv.DictReader(weightingFile)
weighting_file = []
for newRow in newWeightingFile:
    weighting_file.append(newRow)
def FloorSwitch(x):
    return {'oneFloor':1, 'twoFloor':2, 'threeFloor':3, 'fourFloor':4}.get(x, 0)
def positionWeightFinding(weighting_file, floor, seatNum):
    for row in weighting_file:
        if row['Floor'] == floor and row['SeatNum'] == seatNum:
            return row['weighting']
    else:
        return '0'
def returnWeightValue(str):
    strArr = str.split(',')
    floorPosition = strArr[1]
    floorNum = FloorSwitch(floorPosition)
    seatNum = strArr[2].replace('\n', '')
    return floorNum, seatNum
# 피험자 Data 파일 로드
fileName = "testGroupR14F"
rfilePath = "./sample/" + fileName + ".txt"
wfilePate = "./sample/" + fileName + ".csv"
detectorInterval = 0.12 #측정 시간 간격
heightScore = 100 #위치 최고 점수
transSec = 1.0/detectorInterval
rf = open(rfilePath, mode='r', encoding='utf-8')
wf = open(wfilePate, mode='a', encoding='utf-8')
detectNum = 0
beforSentence = ''
weightingPointSum = 0
while True:
    sentence = rf.readline()
    detectNum += 1
    if sentence:
        if sentence.find("(") < 1:
            sentence = sentence.replace("\n", "") + " (0)\n"
        newstr = sentence.replace(")", "").replace("-", ",").replace(":", ",").replace(" (", 	",").replace(" ", ",")     
        newPositionTuple = returnWeightValue(newstr)        
        newWeighting=positionWeightFinding(weighting_file,str(newPositionTuple[0] 	), newPositionTuple[1])
        weightingPointSum += float(newWeighting)
        newstr = newstr.replace(',', ','+newWeighting+',',1)
        wf.write(newstr)
        beforSentence = newstr
    else:
        newbeforSentenceArr = beforSentence.split(",")
        observationCount = detectNum-2 # 관측된 횟수
	# 총 발표를 수행한 시간(발표시간(초))
        totalPresentationTime = round(float(newbeforSentenceArr[4]), 1)
	# 발표시간동안 관측 가능한 최대 횟수
        observableMaxNum = totalPresentationTime*transSec 
	# 발표시 청중을 바라본 비율(시선비율)
        totalFocusRatio = (detectNum-2)/(totalPresentationTime*transSec)
	# 발표시간 동안 받을 수 있는 가장 높은 최고점수
        maxiumPoint = totalPresentationTime*transSec*heightScore
	# 발표자의 가중치 비율(가중치비율)
        focusingScore = weightingPointSum/maxiumPoint 

        wf.writelines("observationCount," + str(observationCount)) 
        wf.writelines("\ntotalPresentationTime," + str(totalPresentationTime)) 
        wf.writelines("\nobservableMaxNum," + str(observableMaxNum)) 
        wf.writelines("\ntotalFocusRatio," + str(totalFocusRatio))
        wf.writelines("\nmaxiumPoint," + str(maxiumPoint)) 
        wf.writelines("\nweightingPointSum," + str(weightingPointSum)) 
        wf.writelines("\nfocusingScore," + str(focusingScore))
        break
rf.close()
wf.close()
weightingFile.close()