# Метод объединения
# Сделать 3-х мерное простр
# Изменить ценры координат
import math

import tkinter as tk

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()
root.resizable(False, False)

figure = plt.figure(figsize=(6, 4), dpi=100)
TwoDimensionalSpacePlot = figure.add_subplot(111)
DataFrameList = list()
ClassData = list()


class Point:
    number = str
    X = float
    Y = float


class NearestPoints:
    firstPoint = Point
    secondPoint = Point
    distance = float


def Distance(firstPoint, secondPoint):
    return float(math.sqrt(((secondPoint.X - firstPoint.X) ** 2) + ((secondPoint.Y - firstPoint.Y) ** 2)))


def PointDrawing(points):
    for point in points:
        if not point.number.isdigit():
            continue
        TwoDimensionalSpacePlot.scatter(point.X, point.Y, None, 'black', 'o')
        TwoDimensionalSpacePlot.annotate(point.number, (point.X, point.Y))
    root.title('Лабораторная работа № 4')
    TwoDimensionalSpacePlot.set_title('Метод объединения')
    TwoDimensionalSpacePlot.set_xlabel('X')
    TwoDimensionalSpacePlot.set_ylabel('Y')


def PoolingPoints(nearPoint):
    TwoDimensionalSpacePlot.plot([nearPoint.firstPoint.X, nearPoint.secondPoint.X],
                                 [nearPoint.firstPoint.Y, nearPoint.secondPoint.Y], color='red')
    CenterPoint(nearPoint.firstPoint, nearPoint.secondPoint)


def CenterPoint(firstPoint, secondPoint):
    newNumber = f'({firstPoint.number}, {secondPoint.number})'
    x, y = GetFromInitialPointsCenter(newNumber)
    TwoDimensionalSpacePlot.scatter(x, y, None, 'blue', 'x')
    print(f'({firstPoint.number}, {secondPoint.number})', (x, y))
    #TwoDimensionalSpacePlot.annotate(f'({firstPoint.number}, {secondPoint.number})', (x, y))
    ChangePointsParameters(firstPoint, secondPoint, x, y, newNumber)


def GetFromInitialPointsCenter(numbers):
    xSum = 0.0
    ySum = 0.0
    count = 0
    for number in numbers:
        for point in InitialPoints:
            if point.number == number:
                xSum += point.X
                ySum += point.Y
                count += 1
    return xSum / count, ySum / count


def ChangePointsParameters(firstPoint, secondPoint, x, y, newNumber):
    newNumber = GetNumbersWithoutBrackets(newNumber)
    GetClassData(firstPoint.number, secondPoint.number, newNumber)
    OperatingPoints.remove(firstPoint)
    OperatingPoints.remove(secondPoint)
    newPoint = Point()
    newPoint.X = x
    newPoint.Y = y
    newPoint.number = newNumber
    OperatingPoints.append(newPoint)
    dataFrame = pd.DataFrame([ClassData], index=[len(OperatingPoints)])
    DataFrameList.append(dataFrame)


def GetClassData(first, second, newNumber):
    ClassData.remove(first)
    ClassData.remove(second)
    ClassData.insert(0, GetNumbersWithoutBrackets(newNumber))


def GetNumbersWithoutBrackets(newNumber):
    newNumber = newNumber.replace("(", "")
    newNumber = newNumber.replace(")", "")
    return f'({newNumber})'


def WindowStart():
    scatter = FigureCanvasTkAgg(figure, root)
    scatter.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    root.mainloop(0)
    plt.show()


def WriteResultTable():
    with pd.ExcelWriter('Result.xlsx') as writer:
        for df in DataFrameList:
            df.to_excel(writer, index=True)
            GetPoolingDataFrame().to_excel(writer, index=True)


def GetPoolingDataFrame():
    return pd.concat(DataFrameList)


def GetPointsFromExcel():
    pointsDataFromExcel = pd.read_excel('Points.xlsx').values
    pointsData = list()
    index = 1
    for pointData in pointsDataFromExcel:
        point = Point()
        point.number = str(index)
        point.X = pointData[0]
        point.Y = pointData[1]
        pointsData.append(point)
        index += 1
    return pointsData


def GetNearestPoint(point, points):
    nearestPoints = list()
    distanceList = list()
    for secondPoint in points:
        if secondPoint != point:
            nearestPoint = NearestPoints()
            nearestPoint.firstPoint = point
            nearestPoint.secondPoint = secondPoint
            distance = Distance(point, secondPoint)
            print(point.number, secondPoint.number, distance)
            nearestPoint.distance = distance
            distanceList.append(distance)
            nearestPoints.append(nearestPoint)
        else:
            continue

    nearestPoint = nearestPoints[distanceList.index(min(distanceList))]
    return nearestPoint.firstPoint, nearestPoint.secondPoint, nearestPoint.distance


def GetNearestPoints():
    nearestPoints = list()
    for point in OperatingPoints:
        nearPoint = NearestPoints()
        nearPoint.firstPoint, nearPoint.secondPoint, nearPoint.distance = GetNearestPoint(point, OperatingPoints)
        nearestPoints.append(nearPoint)
    PoolingPoints(NearPoint(nearestPoints))


def NearPoint(nearPoints):
    distance = list()
    print("_________________________________________")
    for point in nearPoints:
        distance.append(point.distance)
        print(f"X:", point.firstPoint.number, f"Y:", point.secondPoint.number, f"Distance:", point.distance)
    print("_________________________________________" + str(nearPoints[distance.index(min(distance))].firstPoint.number), str(nearPoints[distance.index(min(distance))].secondPoint.number))

    return nearPoints[distance.index(min(distance))]


OperatingPoints = GetPointsFromExcel()
InitialPoints = OperatingPoints.copy()


def ClassInit():
    for classNumber in OperatingPoints:
        ClassData.append(classNumber.number)


def main():
    if __name__ == '__main__':
        classCount = int(input("Enter number: "))
        ClassInit()
        DataFrameList.append(pd.DataFrame([ClassData], index=[len(OperatingPoints)]))
        while True:
            PointDrawing(OperatingPoints)
            GetNearestPoints()
            if len(OperatingPoints) == classCount:
                WriteResultTable()
                break
        WindowStart()


main()
