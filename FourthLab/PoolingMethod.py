# Метод объединения
# Сделать 3-х мерное простр
import math

import tkinter as tk

import matplotlib.pyplot as plt
import numpy
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


root = tk.Tk()
root.resizable(False, False)

figure2D = plt.figure(figsize=(6, 4), dpi=100)
figure3D = plt.figure(figsize=(6, 4), dpi=100)
TwoDimensionalSpacePlot = figure2D.add_subplot(111)
ThreeDimensionalSpacePlot = figure3D.add_subplot(projection='3d')
DataFrameList2D = list()
DataFrameList3D = list()
ClassData2D = list()
ClassData3D = list()


class Point:
    space = bytes
    number = str
    X = float
    Y = float
    Z = float


class NearestPoints:
    firstPoint = Point
    secondPoint = Point
    distance = float


def Distance(firstPoint, secondPoint):
    if firstPoint.space == 2 or secondPoint.space == 2:
        firstPoint.Z = 0
        secondPoint.Z = 0

    return float(math.sqrt(((secondPoint.X - firstPoint.X) ** 2) + ((secondPoint.Y - firstPoint.Y) ** 2) ))


def PointDrawing(points):
    for point in points:
        if not point.number.isdigit():
            continue
        if point.space == 3:
            ThreeDimensionalSpacePlot.scatter(point.X, point.Y, point.Z, color='black')
            ThreeDimensionalSpacePlot.text(point.X, point.Y, point.Z, point.number)
        elif point.space == 2:
            TwoDimensionalSpacePlot.scatter(point.X, point.Y, None, 'black', 'o')
            TwoDimensionalSpacePlot.annotate(point.number, (point.X, point.Y))
    root.title('Лабораторная работа № 4')
    TwoDimensionalSpacePlot.set_title('Метод объединения')
    TwoDimensionalSpacePlot.set_xlabel('X')
    TwoDimensionalSpacePlot.set_ylabel('Y')
    ThreeDimensionalSpacePlot.set_title('Метод объединения')
    ThreeDimensionalSpacePlot.set_xlabel('X')
    ThreeDimensionalSpacePlot.set_ylabel('Y')
    ThreeDimensionalSpacePlot.set_zlabel('Z')


def ChangePointsParameters(firstPoint, secondPoint, x, y, z, newNumber):
    newNumber = GetNumbersWithoutBrackets(newNumber)
    if firstPoint.space == 2:
        GetClassData(firstPoint.number, secondPoint.number, newNumber)
        Operating2DPoints.remove(firstPoint)
        Operating2DPoints.remove(secondPoint)
    else:
        Get3DClassData(firstPoint.number, secondPoint.number, newNumber)
        Operating3DPoints.remove(firstPoint)
        Operating3DPoints.remove(secondPoint)
    newPoint = Point()
    newPoint.X = x
    newPoint.Y = y
    newPoint.space = firstPoint.space
    newPoint.number = newNumber
    if firstPoint.space == 2:
        Operating2DPoints.append(newPoint)
        dataFrame = pd.DataFrame([ClassData2D], index=[len(Operating2DPoints)])
        DataFrameList2D.append(dataFrame)
    else:
        newPoint.Z = z
        Operating3DPoints.append(newPoint)
        dataFrame = pd.DataFrame([ClassData3D], index=[len(Operating3DPoints)])
        DataFrameList3D.append(dataFrame)


def GetClassData(first, second, newNumber):
    ClassData2D.remove(first)
    ClassData2D.remove(second)
    ClassData2D.insert(0, GetNumbersWithoutBrackets(newNumber))


def Get3DClassData(first, second, newNumber):
    ClassData3D.remove(first)
    ClassData3D.remove(second)
    ClassData3D.insert(0, GetNumbersWithoutBrackets(newNumber))


def GetNumbersWithoutBrackets(newNumber):
    newNumber = newNumber.replace("(", "")
    newNumber = newNumber.replace(")", "")
    return f'({newNumber})'


def WindowStart():
    scatter2D = FigureCanvasTkAgg(figure2D, root)
    scatter3D = FigureCanvasTkAgg(figure3D, root)
    scatter2D.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    scatter3D.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    root.mainloop(0)
    plt.show()


def GetTextResult(dfs, fileName):
    with open(fileName, "w") as file:
        for df in GetPoolingDataFrame(dfs).values:
            res = str()
            for i in df:
                if i is not numpy.NAN:
                    i = i.replace(')', '')
                    i = i.replace('(', '')
                    res += f"[{i}] "
            file.write(res + "\n")




def WriteResultTable():
    with pd.ExcelWriter('Result_2D.xlsx') as writer:
        for df in DataFrameList2D:
            df.to_excel(writer, index=True)
            GetPoolingDataFrame(DataFrameList2D).to_excel(writer, index=True)
            GetTextResult(DataFrameList2D, "Result_2D.txt")


def WriteResultTable3D():
    with pd.ExcelWriter('Result_3D.xlsx') as writer:
        for df in DataFrameList3D:
            df.to_excel(writer, index=True)
            GetPoolingDataFrame(DataFrameList3D).to_excel(writer, index=True)
            GetTextResult(DataFrameList3D, "Result_3D.txt")


def GetPoolingDataFrame(data):
    return pd.concat(data)


def GetPointsFromExcel():
    pointsDataFromExcel = pd.read_excel('InitialsPoints.xlsx').values
    pointsData = list()
    index = 1
    for pointData in pointsDataFromExcel:
        point = Point()
        point.number = str(index)
        point.space = 2
        point.X = pointData[3]
        point.Y = pointData[4]
        pointsData.append(point)
        index += 1
    return pointsData

def GetPointsFromExcelFor3D():
    pointsDataFromExcel = pd.read_excel('InitialsPoints.xlsx').values
    pointsData = list()
    index = 1
    for pointData in pointsDataFromExcel:
        point = Point()
        point.number = str(index)
        point.space = 3
        point.X = pointData[0]
        point.Y = pointData[1]
        point.Z = pointData[2]
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


def GetNearest2DPoints():
    nearestPoints = list()
    for point in Operating2DPoints:
        nearPoint = NearestPoints()
        nearPoint.firstPoint, nearPoint.secondPoint, nearPoint.distance = GetNearestPoint(point, Operating2DPoints)
        nearestPoints.append(nearPoint)
    PoolingPoints(NearPoint(nearestPoints))


def GetNearest3DPoints():
    nearestPoints = list()
    for point in Operating3DPoints:
        nearPoint = NearestPoints()
        nearPoint.firstPoint, nearPoint.secondPoint, nearPoint.distance = GetNearestPoint(point, Operating3DPoints)
        nearestPoints.append(nearPoint)
    PoolingPoints(NearPoint(nearestPoints))


def PoolingPoints(nearPoint):
    if nearPoint.firstPoint.space == 2 and nearPoint.secondPoint.space == 2:
        TwoDimensionalSpacePlot.plot([nearPoint.firstPoint.X, nearPoint.secondPoint.X],
                                    [nearPoint.firstPoint.Y, nearPoint.secondPoint.Y], color='red')
        CenterPoint(nearPoint.firstPoint, nearPoint.secondPoint)
    elif nearPoint.firstPoint.space == 3 and nearPoint.secondPoint.space == 3:
        ThreeDimensionalSpacePlot.plot3D([nearPoint.firstPoint.X, nearPoint.secondPoint.X], [nearPoint.firstPoint.Y, nearPoint.secondPoint.Y], [nearPoint.firstPoint.Z, nearPoint.secondPoint.Z], color='red')
        Center3DPoint(nearPoint.firstPoint, nearPoint.secondPoint)


def CenterPoint(firstPoint, secondPoint):
    newNumber = f'({firstPoint.number}, {secondPoint.number})'
    x, y = GetFromInitialPointsCenter(newNumber)
    TwoDimensionalSpacePlot.scatter(x, y, None, 'blue', 'x')
    TwoDimensionalSpacePlot.annotate(f'({firstPoint.number}, {secondPoint.number})', (x, y))
    ChangePointsParameters(firstPoint, secondPoint, x, y, float, newNumber)


def Center3DPoint(firstPoint, secondPoint):
    newNumber = f'({firstPoint.number}, {secondPoint.number})'
    x, y, z = GetFromInitial3DPointsCenter(newNumber)
    ThreeDimensionalSpacePlot.scatter(x, y, z, color='blue', marker='x')
    ChangePointsParameters(firstPoint, secondPoint, x, y, z, newNumber)


def GetFromInitialPointsCenter(numbersStr):
    numbersStr = numbersStr.replace('(', '')
    numbersStr = numbersStr.replace(')', '')
    numbers = numbersStr.split(', ')
    xSum = 0.0
    ySum = 0.0
    count = 0
    for number in numbers:
        for point in Initial2DPoints:
            if point.number == number:
                xSum += point.X
                ySum += point.Y
                count += 1
                break
    return xSum / count, ySum / count


def GetFromInitial3DPointsCenter(numbersStr):
    numbersStr = numbersStr.replace('(', '')
    numbersStr = numbersStr.replace(')', '')
    numbers = numbersStr.split(', ')
    xSum = 0.0
    ySum = 0.0
    zSum = 0.0
    count = 0
    for number in numbers:
        for point in Initial3DPoints:
            if point.number == number:
                xSum += point.X
                ySum += point.Y
                zSum += point.Z
                count += 1
                break
    return xSum / count, ySum / count, zSum / count


def NearPoint(nearPoints):
    distance = list()
    for point in nearPoints:
        distance.append(point.distance)
    return nearPoints[distance.index(min(distance))]


def Distinct(points):
    distinct_points_str = list()
    distinct_points = list()
    for point in points:
        disc = f"{point.X}_{point.Y}_{point.Z}_{point.space}"
        if disc not in distinct_points_str:
            distinct_points_str.append(disc)
            distinct_points.append(point)
    return distinct_points


# Operating2DPoints = Distinct(GetPointsFromExcel())
# Operating3DPoints = Distinct(GetPointsFromExcelFor3D())
Operating2DPoints = GetPointsFromExcel()
Operating3DPoints = GetPointsFromExcelFor3D()
Initial2DPoints = Operating2DPoints.copy()
Initial3DPoints = Operating3DPoints.copy()


def ClassInit():
    for class2DNumber in Operating2DPoints:
        ClassData2D.append(class2DNumber.number)
    for class3DNumber in Operating3DPoints:
        ClassData3D.append(class3DNumber.number)


def main():
    if __name__ == '__main__':
        Distinct(Initial3DPoints)
        classCount = int(input("Enter number: "))
        ClassInit()
        DataFrameList2D.append(pd.DataFrame([ClassData2D], index=[len(Operating2DPoints)]))
        DataFrameList3D.append(pd.DataFrame([ClassData3D], index=[len(Operating3DPoints)]))
        PointDrawing(Operating2DPoints)
        PointDrawing(Operating3DPoints)
        while True:
            if len(Operating2DPoints) > classCount:
                GetNearest2DPoints()
            if len(Operating3DPoints) > classCount:
                GetNearest3DPoints()
            if (len(Operating2DPoints) == classCount) and (len(Operating3DPoints) == classCount):
                WriteResultTable()
                WriteResultTable3D()
                break
        WindowStart()


main()
