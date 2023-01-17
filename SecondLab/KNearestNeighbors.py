# Method of "k-nearest neighbors"
import math
import sys
import tkinter as tk

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter
from matplotlib.patches import Circle

figure = plt.figure(figsize=(6, 4), dpi=125)
plot = figure.add_subplot(111)
featureSpaceClassNameArray = list()


class Space:
    objectClass = str
    knot = None
    end = None
    distance = float


def IsNaN(string):
    return string != string


def Distance(objIsTrue, objIsFalse):
    return float(math.sqrt(((objIsFalse.end - objIsTrue.end) ** 2) + ((objIsFalse.knot - objIsTrue.knot) ** 2)))


def GetObjectWithoutClass(featureSpaces):
    objectWithoutClass = Space()
    index = 0
    for featureSpaceWithoutClass in featureSpaces.values:
        if IsNaN(featureSpaceWithoutClass[0]):
            objectWithoutClass.end = float(featureSpaceWithoutClass[1])
            objectWithoutClass.knot = float(featureSpaceWithoutClass[2])
            break
        index += 1

    if objectWithoutClass.end is not None and objectWithoutClass.knot is not None:
        return index, objectWithoutClass

    print("Ошибка! Новые точки не найдены!\nПрограмма приостановлена!")
    sys.exit()


def GetListWithExistingObjectClass(featureSpaces, objectWithoutClass=None):
    objectsWithClass = list()
    for featureSpaceWithClass in featureSpaces.values:
        if not IsNaN(featureSpaceWithClass[0]):
            objectWithClass = Space()
            objectWithClass.objectClass = featureSpaceWithClass[0]
            objectWithClass.end = featureSpaceWithClass[1]
            objectWithClass.knot = featureSpaceWithClass[2]
            if objectWithoutClass is not None:
                objectWithClass.distance = Distance(objectWithClass, objectWithoutClass)
            objectsWithClass.append(objectWithClass)
    return objectsWithClass


def GetColorAndSymbolForFeatureSpace(featureSpace):
    color = ''
    symbol = ''
    if featureSpace.objectClass == "first":
        color = 'r'
        symbol = 'x'
    elif featureSpace.objectClass == "second":
        color = 'k'
        symbol = '^'
    elif featureSpace.objectClass == "third":
        color = 'b'
        symbol = '*'

    return color, symbol


def GetFeaturesDrawing(featureSpaceWithClassArray):
    root = tk.Tk()
    root.resizable(False, False)
    root.title('Лабораторная работа № 2')

    plot.set_title('Простейшие методы классификации')
    plot.set_xlabel('Концевые точки')
    plot.set_ylabel('Узловые точки')

    for featureSpace in featureSpaceWithClassArray:
        DrawingFeatureSpace(featureSpace)

    return root


def GetWindow(root):
    plot.grid(True)
    scatter = FigureCanvasTkAgg(figure, root)
    scatter.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    root.mainloop()


def DrawingFeatureSpace(featureSpace):
    featureProperties = GetColorAndSymbolForFeatureSpace(featureSpace)
    color = featureProperties[0]
    symbol = featureProperties[1]
    if featureSpace.objectClass in featureSpaceClassNameArray:
        label = ""
    else:
        featureSpaceClassNameArray.append(featureSpace.objectClass)
        label = featureSpace.objectClass
    plot.scatter(featureSpace.end, featureSpace.knot, None, color, marker=symbol, label=label)
    plot.legend()


def DrawingLineBetweenFeatureSpace(firstSpaceWithoutClass, secondSpaceWithClass):
    color = GetColorAndSymbolForFeatureSpace(firstSpaceWithoutClass)[0]
    plot.plot([firstSpaceWithoutClass.end, secondSpaceWithClass.end],
                                 [firstSpaceWithoutClass.knot, secondSpaceWithClass.knot],
                                 color=color)


def EditExcelFile(index, featureExcelData, className, featureSpaceObjects):
    featureExcelData.loc[index, ['Class']] = className
    featureExcelData['Distance'] = None
    distanceIndex = 0
    for featureSpaceObject in featureSpaceObjects:
        featureExcelData.loc[distanceIndex, ['Distance']] = featureSpaceObject.distance
        distanceIndex += 1
    with pd.ExcelWriter('Класс признаков.xlsx') as writer:
        featureExcelData.to_excel(writer, index=False)


def DrawingCircle(featureSpace, radius):
    drawObject = Circle((featureSpace.end, featureSpace.knot), radius=radius, fill=False, color="green")
    plot.add_patch(drawObject)
    return None


def SearchIncludedRadiusFeatureSpace(radius, featureSpaces):
    includedRadiusFeatureSpace = list()
    while True:
        for featureSpace in featureSpaces:
            if float(featureSpace.distance) <= radius:
                includedRadiusFeatureSpace.append(featureSpace)

        if includedRadiusFeatureSpace.__len__() == 0:
            print("Ни одна из точек не входит в заданный радиус!\nРадиус будет увеличен!")
            radius += 1
            print("Радиус поиска: " + str(radius))
        else:
            return radius, includedRadiusFeatureSpace


def GetClass(featureSpaces, radius):
    className = list()
    for featureSpace in featureSpaces:
        className.append(featureSpace.objectClass)
    value = Counter(className).most_common(3)

    if value.__len__() == 1:
        return value[0][0]
    elif value.__len__() > 1:
        counts = list()
        for index in range(value.__len__()):
            counts.append(value[index][1])
        if Counter(counts).__len__() == value.__len__():
            return value[0][0]
        elif counts[0] > Counter(counts).most_common(1)[0][0]:
            return value[0][0]
        else:
            count = Counter(counts).most_common(1)[0][0]
            indexes = list((i for i, e in enumerate(counts) if e == count))
            classNamesIncludedInRadius = list()
            for index in indexes:
                classNamesIncludedInRadius.append(value[index][0])
            nearestPointDistance = radius
            nearestFeatureSpace = Space()
            for featureSpace in featureSpaces:
                if featureSpace.objectClass in classNamesIncludedInRadius and featureSpace.distance < nearestPointDistance:
                    nearestPointDistance = featureSpace.distance
                    nearestFeatureSpace = featureSpace
            return nearestFeatureSpace


def main():
    if __name__ == "__main__":
        featureSpaceFromExcelData = pd.read_excel('Класс признаков.xlsx')
        index, featureSpaceWithoutClass = GetObjectWithoutClass(featureSpaceFromExcelData)
        featureSpaceWithClassArray = GetListWithExistingObjectClass(featureSpaceFromExcelData, featureSpaceWithoutClass)
        radius = 3.5
        radius, featureSpacesIncludedRadius = SearchIncludedRadiusFeatureSpace(radius, featureSpaceWithClassArray)
        classObject = GetClass(featureSpacesIncludedRadius, radius)
        tkinter = GetFeaturesDrawing(featureSpaceWithClassArray)
        if type(classObject) is Space:
            featureSpaceWithoutClass.objectClass = classObject.objectClass
            DrawingFeatureSpace(featureSpaceWithoutClass)
            DrawingLineBetweenFeatureSpace(featureSpaceWithoutClass, classObject)
        else:
            featureSpaceWithoutClass.objectClass = classObject
            DrawingFeatureSpace(featureSpaceWithoutClass)
            DrawingCircle(featureSpaceWithoutClass, radius)

        EditExcelFile(index, featureSpaceFromExcelData, featureSpaceWithoutClass.objectClass, featureSpaceWithClassArray)
        GetWindow(tkinter)


main()
