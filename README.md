# traffic_light
machinezone.ru

Сервис для задания от machinezone.ru. Написан на Python3. Тестировался на Ubuntu 14.04 tls

Установка:
	1) создайть каталог /usr/local/traffic_light/
	2) скопирировать файлы в каталог
	3) Скопировать из папки /usr/local/traffic_light/service файл traffic_light в /etc/init.d
	4) регистрация сервиса в системе:
		sudo update-rc.d traffic_light defaults

Как работает:
	1)запуск сервиса:
		service traffic_light start
	2) остановка сервиса:
		service traffic_light stop
	3) Информация о введенных последовательностях храниться в файле:
		/usr/local/traffic_light/data.pickle
	4) Сервис работает на порту 8080. Чтобы запустить на нужном порту измените значение в файле traffic_light.py
	5) Тестовые запросы к сервису приведены в файле test_http.py

Удаление:
	1) удаление севриса из системы:
		sudo update-rc.d -f traffic_light remove
		sudo rm -f /etc/init.d/traffic_light
	2) удаление каталога:
		sudo rm -fr /usr/local/traffic_light

