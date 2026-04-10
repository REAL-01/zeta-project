# LOL ETA TIPA ZETA PROJECT v0.0.3

**Жанр:** Пошаговая браузерная стратегия (Turn-based / RTS Economy).

**Технологии:** HTML5 Canvas, CSS3, Vanilla JavaScript (Single file, без внешних зависимостей сборщиков), Python (Django).

### MAX канал - https://max.ru/join/ohd-H_oinDbdV_SNDb4JUlDDSP86JSuGP3LAvMOYdnQ
### ПОДДЕРЖИ НАС!

---

## 🛠️ Инструкция по установке (Для всех платформ)

Проект использует backend на базе **Python (Django)**. Следуйте простым шагам ниже, чтобы запустить игру на вашем компьютере.

### 1. Предварительные требования
Убедитесь, что у вас установлен **Python 3.10+**. Скачать можно с [официального сайта](https://www.python.org/downloads/) (при установке на Windows обязательно поставьте галочку "Add Python to PATH").

### 2. Загрузка проекта
Склонируйте этот репозиторий к себе на компьютер или скачайте ZIP-архив и распакуйте его:
```bash
git clone https://github.com/REAL-01/zeta-project.git
cd zeta-project
```

### 3. Настройка окружения

**Для Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Для macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Подготовка базы данных
Примените необходимые миграции базы данных:
```bash
python manage.py makemigrations game
python manage.py migrate
```

### 5. Запуск сервера
Запустите локальный игровой сервер командой:
```bash
python manage.py runserver
```
После успешного запуска перейдите в браузере по адресу: **http://127.0.0.1:8000**

Готово! Вы великолепны.
