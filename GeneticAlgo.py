import csv
from random import randint

#Adam Apicella
#Chris Sheldon
#Genetic Algo

class Schedule:
    def __init__(self, roomList, timeList):
        self.sched = makeSchedule(roomList, timeList)
        self.fitness = self.getFit()
    def getFit(self):
        temp = 0
        profchecked = []
        roomchecked = []
        for x in self.sched:
            pcheck1 = False
            pcheck2 = False
            rcheck1 = False
            rcheck2 = False
            if x.needMultimedia == True and x.room.multimedia == False:
                temp -= 50
            if x.needMultimedia == True and x.room.multimedia == True:
                temp += 20
            if x.courseSize > x.room.roomSize:
                temp -= 70
            if x.courseSize <= x.room.roomSize:
                temp += 20
            for y in self.sched:
                if (x.time.time == y.time.time and x.time.days == y.time.days) and x.prof == y.prof and x.crn != y.crn:
                    for z in profchecked:
                        if x.crn == z:
                            pcheck1 = True
                    for z in profchecked:
                        if y.crn == z:
                            pcheck2 = True
                    if pcheck1 == True and pcheck2 == True:
                        pass
                    else:
                        temp -= 300
                        profchecked.append(x.crn)
                        profchecked.append(y.crn)
                if x.room.roomNum == y.room.roomNum and x.crn != y.crn:
                    for z in roomchecked:
                        if x.crn == z:
                            rcheck1 = True
                    for z in roomchecked:
                        if y.crn == z:
                            rcheck2 = True
                    if rcheck1 == True and rcheck2 == True:
                        pass
                    else:
                        temp -= 300
                        roomchecked.append(x.crn)
                        roomchecked.append(y.crn)    
        return temp

class Classes:
    def __init__(self, crn, course, prof, courseSize, needMultimedia, room, time): #self is equiv to java "this"
        self.crn = crn
        self.course = course
        self.prof = prof
        self.courseSize = courseSize
        self.needMultimedia = bool(needMultimedia)
        self.room = room
        self.time = time

class Room:
    def __init__(self, roomNum, roomSize, multimedia):
        self.roomNum = roomNum
        self.roomSize = roomSize
        self.multimedia = bool(multimedia)


class Times:
    def __init__(self, periodID, days, time):
        self.periodID = periodID
        self.days = days
        self.time = time

def makeSchedule(roomList, timeList):
    temp = []
    with open("ClassInfo.csv") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        firstline = True
        for row in readCSV:
            if firstline:    #skip first line
                firstline = False
                continue
            temp.append(Classes(row[0], row[1], row[2], row[3], row[4], roomList[randint(0,8)], timeList[randint(0,13)]))
    return temp

def loadTimes():
    temp = []
    with open("TimeSlotInfo.csv") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        firstline = True
        for row in readCSV:
            if firstline:    #skip first line
                firstline = False
                continue
            temp.append(Times(row[0], row[1], row[2]))
    return temp

def loadRooms():
    temp = []
    with open("RoomInfo.csv") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        firstline = True
        for row in readCSV:
            if firstline:
                firstline = False
                continue
            temp.append(Room(row[0], row[1], row[2]))
    return temp

def newGen(currentGen, rooms, times):
    nextGen = []
    i = 0
    while i < 100:
        rand1 = randint(0,49)
        rand2 = randint(0,49)
        if population[rand1].fitness > population[rand2].fitness:
            nextGen.append(population[rand1])
        else:
            nextGen.append(population[rand2])
        i += 1
    i = 0
    while i < 50:
        sched1 = nextGen[randint(0,49)]
        sched2 = nextGen[randint(0,49)]
        crossover = randint(0,26)
        while crossover < 27:
            temp = sched1
            sched1.sched[crossover] = sched2.sched[crossover]
            sched2.sched[crossover] = temp.sched[crossover]
            crossover += 1
        i += 1
    nextGen[randint(0,49)].room = rooms[randint(0,8)]
    nextGen[randint(0,49)].room = rooms[randint(0,8)]
    nextGen[randint(0,49)].room = rooms[randint(0,8)]
    nextGen[randint(0,49)].room = rooms[randint(0,8)]

    return nextGen

if __name__ == "__main__":

    roomList = loadRooms()
    timeList = loadTimes()

    population = []
    
    i = 0
    while i < 50:
        population.append(Schedule(roomList, timeList))        
        i += 1

    bestFit = population[0]
    for x in population:
        if x.fitness > bestFit.fitness:
            bestFit = x
    j = 0
    generation = 1
    while bestFit.fitness < 100:
        population = newGen(population, roomList, timeList)

        for x in population:
            x.fitenss = x.getFit()
            if x.fitness > bestFit.fitness:
                bestFit = x

        if j == 100:
            print('Generation %d' % (generation,))
            print(bestFit.fitness)
            j = 0
        j += 1
        generation += 1
    