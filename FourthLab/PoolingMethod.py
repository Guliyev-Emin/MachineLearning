# Метод объединения
import math

import tkinter as tk

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


root = tk.Tk()
root.resizable(False, False)

figure = plt.figure(figsize=(6, 4), dpi=100)
plot = figure.add_subplot(111)
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
        plot.scatter(point.X, point.Y, None, 'black', 'o')
        plot.annotate(point.number, (point.X, point.Y))
    root.title('Лабораторная работа № 4')
    plot.set_title('Метод объединения')
    plot.set_xlabel('X')
    plot.set_ylabel('Y')


def PoolingPoints(nearPoint):
    plot.plot([nearPoint.firstPoint.X, nearPoint.secondPoint.X],
              [nearPoint.firstPoint.Y, nearPoint.secondPoint.Y],
              color='red')
    CenterPoint(nearPoint.firstPoint, nearPoint.secondPoint)


def CenterPoint(firstPoint, secondPoint):
    x = (firstPoint.X + secondPoint.X) / 2
    y = (firstPoint.Y + secondPoint.Y) / 2
    plot.scatter(x, y, None, 'blue', 'x')
    plot.annotate(f'({firstPoint.number}, {secondPoint.number})', (x, y))
    newNumber = f'({firstPoint.number}, {secondPoint.number})'
    newNumber = GetNumbersWithoutBrackets(newNumber)
    GetClassData(firstPoint.number, secondPoint.number, newNumber)

    print(str(firstPoint.number) + "_" + str(secondPoint.number))
    Points.remove(firstPoint)
    Points.remove(secondPoint)

    newPoint = Point()
    newPoint.X = x
    newPoint.Y = y
    newPoint.number = newNumber
    Points.append(newPoint)
    dataFrame = pd.DataFrame([ClassData], index=[len(Points)])
    DataFrameList.append(dataFrame)


def GetClassData(first, second, newNumber):
    ClassData.remove(first)
    ClassData.remove(second)
    #ClassData.append(GetNumbersWithoutBrackets(newNumber))
    ClassData.insert(0, GetNumbersWithoutBrackets(newNumber))


def GetNumbersWithoutBrackets(newNumber):
    newNumber = newNumber.replace("(", "")
    newNumber = newNumber.replace(")", "")
    return f'({newNumber})'


def WindowStart():
    scatter = FigureCanvasTkAgg(figure, root)
    scatter.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    root.mainloop(0)


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
            nearestPoint.distance = distance
            distanceList.append(distance)
            nearestPoints.append(nearestPoint)
        else:
            continue

    nearestPoint = nearestPoints[distanceList.index(min(distanceList))]
    return nearestPoint.firstPoint, nearestPoint.secondPoint, nearestPoint.distance


def GetNearestPoints():
    nearestPoints = list()
    for point in Points:
        nearPoint = NearestPoints()
        nearPoint.firstPoint, nearPoint.secondPoint, nearPoint.distance = GetNearestPoint(point, Points)
        nearestPoints.append(nearPoint)
    PoolingPoints(NearPoint(nearestPoints))


def NearPoint(nearPoints):
    distance = list()
    for point in nearPoints:
        distance.append(point.distance)

    return nearPoints[distance.index(min(distance))]


Points = GetPointsFromExcel()


def PointsStringData():
    for point in Points:
        print(f'(X = {point.X}, Y = {point.Y}) - Number: {point.number}')
    print(ClassData)
    print('---------------------------------------------------------------')


def ClassInit():
    for classNumber in Points:
        ClassData.append(classNumber.number)


def main():
    if __name__ == '__main__':
        classCount = int(input("Enter number: "))
        ClassInit()
        DataFrameList.append(pd.DataFrame([ClassData], index=[len(Points)]))
        print(ClassData)
        while True:
            PointDrawing(Points)
            GetNearestPoints()
            PointsStringData()
            if len(Points) == classCount:
                break
        WriteResultTable()
        for dataFrame in DataFrameList:
            print(dataFrame)
        WindowStart()



main()
