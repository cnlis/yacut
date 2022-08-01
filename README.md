## Проект YaCut ##

Сервис укорачивания ссылок с возможностью предложения своего варианта короткой 
ссылки. Если ссылка не предложена - генерируется случайная короткая ссылка 
длиной 6 символов. Поддерживается как веб-интерфейс, так и REST API для доступа
к сервису.

**Порядок установки**

Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/cnlis/yacut.git
cd yacut
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv venv
```
* Если у вас Linux/MacOS
    ```
    source venv/bin/activate
    ```
* Если у вас Windows
    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

API обслуживает два эндпоинта:
* Создание короткой ссылки 

  **POST /api/id/**

  Тело запроса
  ```json
  {
    "url": "string",
    "custom_id": "string"
  }
  ```

* Получение url по короткой ссылке

  **GET /api/id/<<string:short_id>>/**

  Ответ сервера
  ```json
  {
    "url": "string"
  }
  ```
**Полная спецификация к API приведена в файле openapi.yml**

*Автор: Кирилл Лисицынский (https://github.com/cnlis/)*
