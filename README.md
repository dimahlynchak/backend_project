# Backend Project

Цей проект є простим бекенд-додатком на Flask, який включає Docker для контейнеризації.

## Передумови

Для запуску проекту локально вам потрібно мати встановлені такі інструменти:

- Python 3.11
- Docker
- Docker Compose

## Кроки для запуску

### 1. Клонування репозиторію
Клонуйте репозиторій на свій локальний комп'ютер:
```bash
git clone <URL_вашого_репозиторію>
cd backend_project
```
### 2. Налаштування віртуального середовища (необов'язково)
Якщо ви хочете запустити проект без Docker, ви можете використовувати віртуальне середовище Python.
```bash
python -m venv env
source env/bin/activate  # на Linux/MacOS
# або
env\Scripts\activate  # на Windows
```
### 3. Встановлення залежностей
Установіть необхідні пакети:
```bash
pip install -r requirements.txt
```
### 4. Запуск проекту без Docker
Для запуску Flask додатка локально:
```bash
export FLASK_APP=app  # на Linux/MacOS
# або
set FLASK_APP=app  # на Windows

flask run
```
Після цього додаток буде доступний за адресою: http://127.0.0.1:5000
### 5. Запуск проекту за допомогою Docker
Якщо ви хочете використовувати Docker, то спочатку виконайте наступні кроки:

Збудуйте Docker образ:
```bash
docker-compose build
```
Запустіть контейнер:
```bash
docker-compose up
```
Додаток буде доступний за адресою: http://localhost:5010.
### Перевірка працездатності
Для перевірки стану сервера перейдіть за адресою:

http://localhost:5010/healthcheck

Ви отримаєте відповідь з текстом Server is running!.


