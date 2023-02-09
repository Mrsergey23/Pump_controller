import csv
import matplotlib.pyplot as plt
import numpy as np

file_name = 'data_from_sensors49.csv'
with open (file_name) as r_file:
    # Создаем объект reader, указываем символ-разделитель ","
    file_reader = csv.reader(r_file, delimiter = ",")
    # Счетчик для подсчета количества строк и вывода заголовков столбцов
    data_current = []
    
    for row in file_reader:
        data_current.append(int(row[0])+600)
x = np.arange(0, (len(data_current)), 1)

fig, ax = plt.subplots()
ax.set_xlabel('t, c')
ax.set_ylabel('I, мA')
ax.plot(x, data_current, linewidth=2.0)
ax.grid()
plt.show()




