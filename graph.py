import matplotlib
from matplotlib.figure import Figure
from matplotlib import style

matplotlib.use("TkAgg")
style.use("ggplot")

figure = Figure(figsize=(4, 2), dpi=100)
a = figure.add_subplot(111)


def animate(i):
    pull_data = open("sampleText.txt", "r").read()
    data_list = pull_data.split('\n')
    x_list = []
    y_list = []
    for eachLine in data_list:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            x_list.append(int(x))
            y_list.append(int(y))

    a.clear()
    a.plot(x_list, y_list, '-o', ms=5, lw=2, alpha=0.9, mfc='#04a6ce', color='#04a6ce')