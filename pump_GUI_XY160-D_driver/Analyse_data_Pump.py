import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from statistics import mean
import pandas as pd
from mpl_toolkits.axisartist.axislines import SubplotZero
angle_open = 80
data_current = []
data_flow = []

def read_data(_file_name_):
    with open (_file_name_) as r_file:
        file_reader = csv.reader(r_file, delimiter = ",")
        # массивы для считывания всех данных из csv
        data_current_ls = []
        data_flow_ls = [] 
        for row in file_reader:
            data_current_ls.append(int(row[0]))
            data_flow_ls.append(int(row[1]))
    return data_current_ls, data_flow_ls

def equal_begin_and_period(_data_current_, _data_flow_):
    counter = 0
    counter_f = 0
    for k in range(len(_data_current_)-1):
        if (_data_current_[k] > 100) and (counter < 1): # находим индекс начала периода
            # data_current_ls[k] > 30 чтобы точно поймать первое пересечение нуля, как бы порог
            counter += 1
            index_start = k
        if (_data_current_[k] > 0 and _data_current_[k+1] < 0 and counter_f < 5): # количество периодов, которое выводим
            counter_f += 1
            index_finish = k
    data_current.append(_data_current_[index_start:index_finish])
    data_flow.append(_data_flow_[index_start:index_finish])  

def plot_builder(_data_current_): 
    # построение обычного линейного графика
    pass
    

# dir_name = "C:/Users/General/Documents/m_UNI/11semestr/ResearchWork_NIRS/course_work/Pump_controller/data_from_experiments/"
# for i in range(40, 60, 5):
#     file_name = dir_name +"data_from_sensors"+ str(i) + "angle_valve_"+ str(angle_open) + ".csv"
#     data_full_curr, data_full_flow = read_data(file_name)
#     equal_begin_and_period(data_full_curr, data_full_flow)
# fig, ax = plt.subplots(1, 2, figsize=(8,5), gridspec_kw={'width_ratios': [5, 2]})
# plt.figure(1)
# legend = []
# for j in range(len(data_current)):     
#     x = np.arange(0, (len(data_current[j])), 1)
#     ax[0].set_xlabel('t, c')
#     ax[0].set_ylabel('I, мA')
#     legend.append(str(40+5*j)+'Hz, '+ str("{:.2f}".format(mean(data_flow[j])))+ ' L/hour')
#     ax[0].plot(x, data_current[j], linewidth=1.5)
#     ax[0].annotate(str(max(data_current[j])),color='#293133', xy=(data_current[j].index(max(data_current[j])), max(data_current[j])), 
#                    xytext=(data_current[j].index(max(data_current[j]))+10, max(data_current[j])+8),
#              arrowprops=dict(arrowstyle="->",color='#293133'),
#              )
#     x2 = np.arange(0, 4, 1)
#     ax[1].bar(j, mean(data_flow[j]))
# ax[0].grid()
# fig.legend(legend)
# fig.suptitle("Данные при открытии крана на " + str(angle_open)+"°") 
# #plt.show()

# # Данные полученные при разных открытия крана вручную
data = {'Angle': [90, 80, 70, 60, 50, 40], 'Time': [12.63,14.4,16.1,20,31,52]} 
# Create DataFrame 
df = pd.DataFrame(data)
# Print the output.  
# plt.plot(df['Angle'], df['Time'], marker = 'o', color = "orange")

# plt.ylabel('Время выливания')
# plt.xlabel('Угол открытия крана')
# plt.title("Эксперимент с краном")
# plt.grid()
# #plt.show()

# Эксперимент при одной частоте, разных углах открытия
plt.figure()
dir_name = "C:/Users/General/Documents/m_UNI/11semestr/ResearchWork_NIRS/course_work/Pump_controller/data_from_experiments/"
for i in range(90, 30, -10):
    file_name = dir_name +"data_from_sensors"+ str(45) + "angle_valve_"+ str(i) + ".csv"
    data_full_curr, data_full_flow = read_data(file_name)
    equal_begin_and_period(data_full_curr, data_full_flow)
fig2, ax2 = plt.subplots(1, 2, figsize=(8,5), gridspec_kw={'width_ratios': [5, 2]})
legend = []
for j in range(len(data_current)):     
    x = np.arange(0, (len(data_current[j])), 1)
    ax2[0].set_xlabel('t, c')
    ax2[0].set_ylabel('I, мA')
    legend.append(str(90 - j*10) + "гр. " +"{:.2f}".format(mean(data_flow[j]))+ ' L/hour')
    ax2[0].plot(x, data_current[j], linewidth=1.5, marker = 'o', linestyle = '--')

    #x2 = np.arange(0, 4, 1)
    ax2[1].set_xlabel('Открытие крана')
    ax2[1].set_ylabel('Q, L/hour')
    ax2[1].scatter(j, mean(data_flow[j]))
       
ax2[1].scatter(np.arange(0,6,1), 1.2/(df['Time']/3600))
legend.append("Вручную проведенные эксперименты")
# добавление стрелок в график
# removing the default axis on all sides:
for side in ['bottom','right','top','left']:
    ax2[0].spines[side].set_visible(False)
dps = fig2.dpi_scale_trans.inverted()
bbox = ax2[0].get_window_extent().transformed(dps)
width, height = bbox.width, bbox.height

# manual arrowhead width and length
hw = 1./30.*(max(max(data_current))-min(min(data_current))) 
hl = 1./30.*(x.max()-x.min())
lw = 1 # axis line width
ohg = 0.3 # arrow overhang

# compute matching arrowhead length and width  
yhw = hw/(max(max(data_current))-min(min(data_current))) *(x.max()-x.min())* height/width 
yhl = hl/(x.max()-x.min())*(max(max(data_current))-min(min(data_current))) * width/height
ax2[0].arrow(0, min(min(data_current))-50, 0., (max(max(data_current))-min(min(data_current)))+100 , fc='k', ec='k', lw = lw, 
            head_width=yhw, head_length=yhl, overhang = ohg, 
            length_includes_head= True, clip_on = False)
ax2[0].arrow(0, min(min(data_current))-50, x.max()-x.min()+50, 0., fc='k', ec='k', lw = lw, 
             head_width=hw, head_length=hl, overhang = ohg, 
             length_includes_head= True, clip_on = False) 
    
x_ticks = [k1 for k1 in range(6)]
plt.xticks(ticks = x_ticks, labels = [k for k in range(90, 30, -10)])
ax2[0].grid()
ax2[1].grid()
fig2.legend(legend)
fig2.suptitle("Данные при работе крана при частоте "+str(45)+" Гц") 

plt.figure()
#График разгона
file_name = "C:/Users/General/Documents/m_UNI/11semestr/ResearchWork_NIRS/course_work/Pump_controller/" + "data_from_sensors35__75angle_valve_90.csv"
data_full_curr, data_full_flow = read_data(file_name)
x = np.arange(0, (len(data_full_curr)), 1)
plt.plot(x, data_full_curr)
plt.annotate(str(max(data_full_curr)),color='#293133', xy=(data_full_curr.index(max(data_full_curr)), max(data_full_curr)), 
                   xytext=(data_full_curr.index(max(data_full_curr))+10, max(data_full_curr)+1),
             arrowprops=dict(arrowstyle="->",color='#293133'))
plt.grid()

plt.show()       