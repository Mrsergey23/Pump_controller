import csv
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean
import pandas as pd
angle_open = 80
data_current = []
data_flow = []
dir_name = "C:\\Users\\General\\Documents\\m_UNI\\11semestr\\ResearchWork_NIRS\\course_work\\Pump_controller\\data_from_experiments\\"
for i in range(40, 60, 5):
    file_name = dir_name +"data_from_sensors"+ str(i) + "angle_valve_"+ str(angle_open) + ".csv"
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
            if (data_current_ls[k] > 30) and (counter < 1): # находим индекс начала периода
                # data_current_ls[k] > 30 чтобы точно поймать первое пересечение нуля, как бы порог
                counter += 1
                index_start = k
            if (data_current_ls[k] > 0 and data_current_ls[k+1] < 0 and counter_f < 5): # количество периодов, которое выводим
                counter_f += 1
                index_finish = k
        data_current.append(data_current_ls[index_start:index_finish])
        data_flow.append(data_flow_ls[index_start:index_finish])  

fig, ax = plt.subplots(1, 2, figsize=(8,5), gridspec_kw={'width_ratios': [5, 2]})
plt.figure(1)
legend = []
for j in range(len(data_current)):     
    x = np.arange(0, (len(data_current[j])), 1)
    ax[0].set_xlabel('t, c')
    ax[0].set_ylabel('I, мA')
    legend.append(str(40+5*j)+'Hz, '+ str("{:.2f}".format(mean(data_flow[j])))+ ' L/hour')
    ax[0].plot(x, data_current[j], linewidth=1.5)
    ax[0].annotate(str(max(data_current[j])),color='#293133', xy=(data_current[j].index(max(data_current[j])), max(data_current[j])), 
                   xytext=(data_current[j].index(max(data_current[j]))+10, max(data_current[j])+8),
             arrowprops=dict(arrowstyle="->",color='#293133'),
             )
    x2 = np.arange(0, 4, 1)
    ax[1].bar(j, mean(data_flow[j]))
ax[0].grid()
fig.legend(legend)
fig.suptitle("Данные при открытии крана на " + str(angle_open)+"°") 
#plt.show()

# Данные полученные при разных открытия крана вручную
data = {'Angle': [90, 80, 70, 60, 50, 40], 'Time': [12.63,14.4,16.1,20,31,52]} 
# Create DataFrame 
df = pd.DataFrame(data) 
# Print the output.  
plt.figure(2)
plt.plot(df['Angle'], df['Time'], marker = 'o', color = "orange")
plt.ylabel('Время выливания')
plt.xlabel('Угол открытия крана')
plt.title("Эксперимент с краном")
plt.grid()
#plt.show()

#разгон
file_name = dir_name + "data_from_sensors30__65angle_valve_60_step1Hz.csv"
with open (file_name) as r_file:
    # Создаем объект reader, указываем символ-разделитель ","
    file_reader = csv.reader(r_file, delimiter = ",")
    # массивы для считывания всех данных из csv
    data_current_ls = []
    data_flow_ls = []
    for row in file_reader:
        data_current_ls.append(int(row[0]))
        data_flow_ls.append(int(row[1]))
x = np.arange(0, (len(data_current_ls)), 1)
plt.figure(3)
plt.plot(x, data_current_ls)
plt.annotate(str(max(data_current_ls)),color='#293133', xy=(data_current_ls.index(max(data_current_ls)), max(data_current_ls)), 
                   xytext=(data_current_ls.index(max(data_current_ls))+10, max(data_current_ls)+1),
             arrowprops=dict(arrowstyle="->",color='#293133'))
plt.grid()
plt.show()
        