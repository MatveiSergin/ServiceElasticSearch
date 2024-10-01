# Сервис обработки продуктов маркетплейса

## Обзор
Этот сервис обрабатывает данные продуктов маркетплейса в формате XML, загружает их в базу данных PostgreSQL, отправляет данные в Elasticsearch, извлекает похожие продукты с использованием Elasticsearch и обновляет базу данных с найденными аналогами. Сервис работает асинхронно и разработан для высокой производительности.

Пример данных из базы данных:
```json
{
  "offers": [
    {
      "uuid": "006ba645-b522-4040-825f-399c01669774",
      "title": "Гидрогелевая пленка на экран Samsung Galaxy S20 глянцевая, для защиты от царапин, ударов и потертостей, 1шт.",
      "brand": "MIETUBL",
      "similar_sku": [
        {
          "uuid": "dde56c11-f759-4e25-b26f-67497f236808",
          "title": "Гидрогелевая пленка на экран Doogee S98 глянцевая, для защиты от царапин, ударов и потертостей, 1шт.",
          "brand": "MIETUBL"
        },
        {
          "uuid": "249bef3d-591f-4853-a772-33088b4302c0",
          "title": "Гидрогелевая пленка на экран AGM H3 глянцевая, для защиты от царапин, ударов и потертостей, 1шт.",
          "brand": "MIETUBL"
        },
        {
          "uuid": "6a1ec915-78e8-4b86-b588-fe44d3592573",
          "title": "Гидрогелевая пленка на экран Blackview BV6000 глянцевая, для защиты от царапин, ударов и потертостей, 1шт.",
          "brand": "MIETUBL"
        }
      ]
    },
    {
      "uuid": "358b6cd2-17d8-4d39-9e66-f8d1ecce4d68",
      "title": "Смартфон Apple iPhone 16 128 ГБ, Dual: nano SIM + eSIM, белый",
      "brand": "Apple",
      "similar_sku": [
        {
          "uuid": "8494dd8e-2106-4ed5-b8ac-b5d2f6210f7e",
          "title": "Смартфон Apple iPhone 16 Plus 128 ГБ, Dual: nano SIM + eSIM, белый",
          "brand": "Apple"
        },
        {
          "uuid": "52431c95-64cc-41f0-830f-0c20611be22a",
          "title": "Смартфон Apple iPhone 16 128 ГБ, Dual: nano SIM + eSIM, черный",
          "brand": "Apple"
        },
        {
          "uuid": "9e108e28-03cb-48e4-bcf6-962da41da2fd",
          "title": "Смартфон Apple iPhone 16 128 ГБ, Dual: nano SIM + eSIM, зеленый",
          "brand": "Apple"
        }
      ]
    },
    {
      "uuid": "00834ce6-e72c-4fb7-98cd-50fbd1aca8ca",
      "title": "Чехол на Vivo V21e 4G / Виво V21e 4G с принтом Маленькие ромашки, прозрачный",
      "brand": "Awog",
      "similar_sku": [
        {
          "uuid": "4ea02011-74ce-42a7-8f28-3e0981f0f680",
          "title": "Чехол на Vivo V21e 4G / Виво V21e 4G с принтом Веселые ромашки",
          "brand": "Bright Case"
        },
        {
          "uuid": "184f1b54-b8ea-49d0-ae70-34d6cd82f11a",
          "title": "Чехол на Vivo V21e 4G / Виво V21e 4G с принтом Маленькие зверята",
          "brand": "Bright Case"
        },
        {
          "uuid": "bbddd39f-f94f-40b9-874d-82089bcb8ada",
          "title": "Чехол на Vivo V21e 4G / Виво V21e 4G с принтом Всявотца, прозрачный",
          "brand": "Awog"
        }
      ]
    },
    {
      "uuid": "050a8cca-274a-467e-9178-1d3e39e92f93",
      "title": "Чехол на Honor 6X / Хонор 6Х с принтом Красная маска самурая",
      "brand": "Awog",
      "similar_sku": [
        {
          "uuid": "a3d94e4f-6902-4651-899c-357b77e33318",
          "title": "Чехол на Honor 6X / Хонор 6Х с принтом Красная сакура, прозрачный",
          "brand": "Awog"
        },
        {
          "uuid": "80a4594b-2578-4807-ac3f-0d57ebf56b12",
          "title": "Чехол на Honor 6X / Хонор 6Х прозрачный",
          "brand": "Awog"
        },
        {
          "uuid": "57dffd93-5046-49a9-9de9-929e6340c23f",
          "title": "Чехол на Honor 6X / Хонор 6Х с принтом Доберман",
          "brand": "Awog"
        }
      ]
    },
    {
      "uuid": "53c03ec5-8637-438e-b322-2a8c8cfcdcb1",
      "title": "Игра Lords Of The Fallen Limited Edition для Xbox One",
      "brand": "City Interactive",
      "similar_sku": [
        {
          "uuid": "30b42b71-ecdf-4844-b36e-80a4a30ba38b",
          "title": "Игра Lords Of The Fallen Limited Edition для Xbox One",
          "brand": "CI Games"
        },
        {
          "uuid": "7f92db61-9f86-49a9-a8cf-ae847dbf10e0",
          "title": "Игра HITMAN - Game of the Year Edition Xbox One / Series S / Series X",
          "brand": "IO Interactive A/S"
        },
        {
          "uuid": "8cd100d7-8141-4633-ad39-6ec71fdbf554",
          "title": "Игра STAR WARS Jedi: Fallen Order Deluxe Edition Xbox One, Xbox Series S, Xbox Series X цифровой ключ",
          "brand": "Respawn Entertainment"
        }
      ]
    }
  ]
}
```
## Функции
- Парсит XML-выгрузку продуктов и сохраняет данные в базе данных PostgreSQL.
- Отправляет продукты в экземпляр Elasticsearch для возможностей полнотекстового поиска.
- Находит до 5 похожих продуктов для каждого товара с помощью запроса "more like this" в Elasticsearch и обновляет базу данных.
- Работает в Docker с PostgreSQL и Elasticsearch через `docker-compose`.

## Требования
- Python 3.11+
- Docker и Docker Compose
- PostgreSQL
- Elasticsearch

## Установка

1. **Клонируйте репозиторий**:
   
   ```bash
   git clone https://github.com/MatveiSergin/ServiceElasticSearch
   cd ServiceElasticSearch
   
2. **Наличие Docker**:
   Необходим Docker и Docker Compose для запуска сервисов.
3. **Переменные окружения**:
   Настройте переменные окружения: Создайте файл .env на основе следующего шаблона:
   ```bash
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=db DB_NAME=sku
   ELASTICSEARCH_URL=http://localhost:9200
   XML_FILE_PATH=file.xml
4. **Запуск приложения**:
   Запустите приложение: Используйте Docker Compose для запуска контейнеров PostgreSQL, Elasticsearch и приложения:
   ```bash
   docker-compose up --build

## Запуск сервиса
   Основная точка входа - файл src/main.py. Она включает два основных шага:
   - Обработка предложений: этот шаг читает XML-файл, парсит данные о продуктах и вставляет данные в PostgreSQL и Elasticsearch.
   - Обновление похожих SKU: этот шаг находит похожие продукты для каждого товара в базе данных с помощью Elasticsearch и обновляет поле similar_sku.

## Конфигурация
Приложение использует BaseSettings из Pydantic для управления конфигурацией. Оно автоматически загружает переменные окружения из файла .env в зависимости от платформы (Linux/Windows).

## Технологии
Python: Асинхронная обработка с использованием asyncio и asyncpg.
PostgreSQL: Реляционная база данных для хранения данных о продуктах.
Elasticsearch: Поисковая система для нахождения похожих продуктов.
Docker: Контейнеризация приложения и сервисов.
Pydantic: Управление конфигурацией и валидация типов.
Poetry: Управление зависимостями и упаковка.
