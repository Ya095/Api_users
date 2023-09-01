# API для работы с пользователями и их ролями

<h3>Запуск приложения</h3>
Запустить можно командой:

```
make up
```  

Остановить: 

```
make down
```  

Для локальной разработки запустить ```make up_local```  
Остановить - ```make down_local```  
Так же необходимо запустить uvicorn: ```uvicorn main:app --reload```


<h3>Миграции</h3>
Для накатывания миграций, если файла alembic.ini ещё нет, нужно запустить в терминале команду:

```
alembic init migrations
```

После этого будет создана папка с миграциями и конфигурационный файл для алембика.

- В alembic.ini нужно задать адрес базы данных, в которую будем катать миграции.  
Подтягивать значения из .env файлов.  
Пример: ```sqlalchemy.url = postgresql://%(DB_USER)s:%(DB_PASS)s@%(DB_HOST)s:%(DB_PORT)s/%(DB_NAME)s```  
Не забыть сделать и для тестовой базы данных.
- Дальше идём в папку с миграциями и открываем env.py, там вносим изменения в блок, где написано 

```
from myapp import mymodel
```

Так же добавить следующие строки (после ```config = context.config```):

```
from settings import DB_HOST, DB_PORT, DB_USER, DB_NAME, DB_PASS

section = config.config_ini_section
config.set_section_option(section, "DB_HOST", DB_HOST)
config.set_section_option(section, "DB_PORT", DB_PORT)
config.set_section_option(section, "DB_USER", DB_USER)
config.set_section_option(section, "DB_NAME", DB_NAME)
config.set_section_option(section, "DB_PASS", DB_PASS)
```

- Дальше ввести: ```alembic revision --autogenerate -m "comment"``` (при каждом изменении модели)
- Будет создана миграция
- Дальше вводим: ```alembic upgrade heads```


Для того, что бы во время тестов нормально генерировались миграции нужно:

- сначала попробовать запустить тесты обычным образом. с первого раза все должно упасть
- если после падения в папке tests создались алембиковские файлы, то нужно прописать туда данные по миграхам
- если они не создались, то зайти из консоли в папку test и вызвать вручную команды на миграции, чтобы файлы появились
