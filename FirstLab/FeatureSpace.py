# to download pandas use "pip3 install pandas openpyxl"
import pandas as pd
# to download matplotlib use "pip3 install matplotlib"
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# to download tkinter use "pip3 install tk"
import tkinter as tk

# creating tkinter window
root = tk.Tk()
root.resizable(False, False)
root.title('Лабораторная работа № 1')

# reading Excel file
featureSpaceFromExcelData = pd.read_excel('Класс признаков.xlsx')
featureSpace = list()  # list declaration
for spaceName in featureSpaceFromExcelData:
    # adding elements to a list
    featureSpace.append(featureSpaceFromExcelData[spaceName].to_list())

# initialization of features of objects into tuples (x-axis, y-axis values)
firstClassFeatureSpace = (featureSpace[1][0:5], featureSpace[2][0:5])
secondClassFeatureSpace = (featureSpace[1][5:10], featureSpace[2][5:10])
thirdClassFeatureSpace = (featureSpace[1][10:15], featureSpace[2][10:15])

figure = plt.figure(figsize=(6, 4), dpi=125)
plot = figure.add_subplot(111)
plot.scatter(firstClassFeatureSpace[0], firstClassFeatureSpace[1], None, 'r', 'x')
plot.scatter(secondClassFeatureSpace[0], secondClassFeatureSpace[1], None, 'k', '^')
plot.scatter(thirdClassFeatureSpace[0], thirdClassFeatureSpace[1], None, 'b', '*')
plot.legend(['Первый', "Второй", 'Третий'])
plot.set_title('Признаковое пространство')
plot.set_xlabel('Концевые точки')
plot.set_ylabel('Узловые точки')
plot.grid(True)

scatter = FigureCanvasTkAgg(figure, root)
scatter.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

root.mainloop()
