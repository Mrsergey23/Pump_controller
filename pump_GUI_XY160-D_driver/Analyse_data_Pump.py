import csv
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean

data_current = []
data_flow = []
for i in range(40, 60, 5):
    file_name = "data_from_experiments/data_from_sensors"+ str(i) + "_angle_valve_90.csv"
    with open (file_name) as r_file:
        # Создаем объект reader, указываем символ-разделитель ","
        file_reader = csv.reader(r_file, delimiter = ",")
        # массивы для считывания всех данных из csv
        data_current_ls = []
        data_flow_ls = []
        for row in file_reader:
            data_current_ls.append(int(row[0]))
            data_flow_ls.append(int(row[1]))
        counter = 0
        counter_f = 0
        for k in range(len(data_current_ls)-1):
            if (data_current_ls[k] > 0) and (counter < 1): # находим индекс начала периода
                counter += 1
                index_start = k
            if (data_current_ls[k] > 0 and data_current_ls[k+1] < 0 and counter_f < 4):
                counter_f += 1
                index_finish = k
        data_current.append(data_current_ls[index_start:index_finish])
        data_flow.append(data_flow_ls[index_start:index_finish])  
fig, ax = plt.subplots()
legend = []
for j in range(len(data_current)):     
    x = np.arange(0, (len(data_current[j])), 1)
    ax.set_xlabel('t, c')
    ax.set_ylabel('I, мA')
    legend.append(str(40+5*j)+'Hz '+ str("{:.2f}".format(mean(data_flow[j])))+ ' L/hour')
    ax.plot(x, data_current[j], linewidth=1.5)
    ax.grid()
ax.legend(legend)
plt.show()


