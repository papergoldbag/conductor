<h2>Conductor</h2>

<h4>Реализованная функциональность</h4>
<ul>
    <li>Авторизация(Cookie Token, Header Token)</li>
    <li>Страница roadmap</li>
    <li>Возможность просмотра тестов</li>
    <li>Сеть (блок контактов )</li>
    <li>Возможность сохранять прогресс адаптации</li>
    <li>Возможность получения информации о своих целях в адаптации</li>
</ul>


<h4>Особенность проекта в следующем:</h4>
<ul>
    <li>Полная асинхронность</li>
    <li>Полная адаптивность сайта/приложения</li>
    <li>Плавная смена темы в ночную/дневную</li>  
</ul>


<h4>Основной стек технологий:</h4>
<ul>
    <li>Python3.10, FastAPI, SqlAlchemy, async databases</li>
	<li>PostgreSQL</li>
	<li>HTML/CSS/JS</li>
	<li>Kotlin, okHttp, Epoxy</li>
 </ul>


<h4>Демо</h4>
<p>Демо сервиса доступно по адресу: http://31.172.66.226:8080/</p>
<p>Реквизиты тестового пользователя: login: <b>Ivan</b>, пароль: <b>Ivan</b></p>


СРЕДА ЗАПУСКА
------------
1) развертывание сервиса производится на Ubuntu 20
2) требуется для запуска ASGI(uvicorn)
3) требуется установленная СУБД PostgreSQL


УСТАНОВКА
------------
###
Настройка системы
~~~
sudo apt update
sudo apt upgrade
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.10
sudo apt install python3.10-venv
sudo apt install postgresql postgresql-contrib
~~~
Настройка python приложения
~~~
adduser psb
su - psb
python3.10 -m venv venv
git clone git@github.com:papergoldbag/psb.git
cd psb
source ./venv/bin/activate
pip install -r requirements
~~~


### База данных
Необходимо создать пустую базу данных, а подключение к базе прописать в app/core/settings.py
~~~
sudo systemctl start postgresql
sudo -i -u postgres
psql
CREATE DATABASE psb encoding 'UTF-8';
CREATE USER psb with password '123...';
\q
~~~


### Приложение как сервис
Нужно создать файл psb.service с текстом ниже и поместить его в /etc/systemd/system/
~~~
[Unit]
Description=psb
After=network.target

[Service]
User=psb
WorkingDirectory=/home/psb/psb
ExecStart=/home/psb/psb/venv/bin/python3.10 /home/psb/psb/start.py
Environment="PYTHONPATH=/home/psb/psb/venv/"
RestartSec=10
Restart=always

[Install]
WantedBy=multi-user.target
~~~
И после этого выполните в терминале команду ниже
~~~
sudo systemctl start psb
~~~


РАЗРАБОТЧИКИ
<h4>Иван Ермолов - Data-Scientist https://t.me/ivan_20190721 </h4>
<h4>Денис Шайхльбарин - Android https://t.me/BrightOS </h4>
<h4>Арсен Сабирзянов - Backend https://t.me/arpakit </h4>
<h4>Илья Хакимов - Frontend https://t.me/ilyakhakimov03 </h4>
<h4>Рустам Афанасьев - Project manager, Analytic https://t.me/rcr_tg </h4>



<h3>Android Client</h3>
https://github.com/BrightOS/Newton-PSB-Divar-Android
