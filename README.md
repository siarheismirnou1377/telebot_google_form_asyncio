## Асинхронный телеграм бот
Телеграм бот, который проверяет закрыта ли гугл форма для ответов (версия 2.0). Присылает сообщение об открытии или закрытии формы. Можно передавать ссылку на гугл форму и временно останавливать работу бота. Проект находится в стадии поддержки.

## Содержание
- [Технологии](#технологии)
- [Требования](#требования)
- [Развёртывание и запуск](#развёртывание-и-запуск)
- [FAQ](#faq)
- [Команда проекта](#команда-проекта)
- [Задонатить](#задонатить)

## Технологии
- [Python](https://www.python.org/)
- [Telegram](https://web.telegram.org/)
- [Aiogram](https://docs.aiogram.dev/en/dev-3.x/)

### Требования
Для установки и запуска проекта, необходим [Python](https://www.python.org/) v3.10+.
Так же нужно получить токен телеграм бота у отца ботов.

## Развёртывание и запуск
Чтобы установить данный проект, вам нужно:

- Установить Python версии не ниже 3.10.
Например для Linux Ubuntu:
```sh
$ sudo apt update
$ sudo apt-get install python3.10
```
- Установить pip.
Например для Linux Ubuntu:
```sh
$ sudo apt update
$ sudo apt install python3-pip
```
- Установить venv.
Например для Linux Ubuntu:
```sh
$ sudo apt update
$ sudo apt install -y python3-venv
```
- Установить git.
Например для Linux Ubuntu:
```sh
$ sudo apt update
$ sudo apt install git
```
- Создать в папке виртуальное окружение и запустить его.
Например для Linux Ubuntu:
```sh
$ python3 -m venv telebot_env
$ source telebot_env/bin/activate
```
- Создать папку с любым названием удобным для вас и инициализировать там git.
```sh
$ git init
```
- Склонировать себе репозиторий в папку.
```sh
$ git clone https://github.com/siarheismirnou1377/telebot_google_form_sync.git
```
- Установить зависимости.
Например для Linux Ubuntu:
```sh
$ pip3 install -r requirements.txt
```
- Открыть файл main.py. Вставить, полученный токен у отца ботов.
- Запустить файл main.py в консоли, с уже запущенным виртуальным окружением.
Например для Linux Ubuntu:
```sh
$ python3 main.py
```


## FAQ 
None

## Команда проекта
- [Сергей Смирнов.](https://www.linkedin.com/in/sergey-smirnov-8749a2237/) — Python Software Engineer

## Задонатить
Если у вас возникло желание меня поддержать -
[Boosty](https://boosty.to/bigsmirnovsky/donate) - Big Smirnovsky
