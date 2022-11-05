import KNearestNeighbors as kn
import pandas as pd

featureSpaceFromExcelData = pd.read_excel('Класс признаков.xlsx')
featureSpacesArray = kn.GetListWithExistingObjectClass(featureSpaceFromExcelData)
tkinter = kn.GetFeaturesDrawing(featureSpacesArray)
kn.GetWindow(tkinter)
