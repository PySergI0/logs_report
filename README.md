# **logs_report**

#### **cli-приложение, которое анализирует логи django-приложения и формирует отчет. Отчет выводится в консоль.** 

## Установка
Приложение работает без дополнительных зависимостей.  
Папка с файлами логов должна находиться в корневом каталоге приложения.

 ```git clone https://github.com/Serg0NT/logs_report.git```

## Запуск приложения

```python3 main.py <position arguments> --report <report>```

1. position arguments - пути к файлам логов. Принимает минимум 1 путь. Пример "logs/app1.log".

2. report - название отчета. В данный момент реализован только отчет "handlers". Другие значения не принимает.    
Пример запроса ```python3 main.py logs/app1.log logs/app2.log logs/app3.log --report handlers```

## Пример отчета
    
![alt text](https://github.com/Serg0NT/logs_report/blob/main/example_report.png)

## Добавление нового отчета
1. Добавьте название нового отчета в ```parser.add_argument``` ```"choices=["handlers"]``` , который находится в функции ```args_parser``` в модуле ```src.cli_config.py```
2. Добавьте новый метод класса ```Reports``` в модуле ```reports```
3. В функции ```main``` добавьте вызов нового метода по аналогии с существующим.


