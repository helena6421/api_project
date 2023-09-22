# Обучающие продукты с уроками и студентами

## Проект написан на Python 3.10
## Используемые библиотеки:
    django
    djangorestframework
    djoser

Версии указаны в requirements.txt

## API
Api доступно только аутентифицированным пользователям.

Api endpoints:
    
    Те, которые включены в djoser c приставкой /api/auth/
    https://djoser.readthedocs.io/en/latest/getting_started.html

Для аутентификации:

    /api/auth/token/login/
    {"username":"admin", "password":"admin"}

Создание продукта:
    
    POST /api/products/
    ** owner подставится из request.user

Создание записи доступа пользователя к продукту:
    
    POST /api/products/1/add_student_to_product/
    {"student":1}

Создание нового урока:

    POST /api/lessons/
    {"name":"First lesson","url_video":"https://www.youtube.com/","duration_video":1, "products": [1]}    

Создание записи просмотра:

    POST /api/lessons/1/seen/
    {"viewing_in_seconds":81}

    Пример ответа (пользователь подставляется автоматически из request):
    {
    "id": 8,
    "student": 1,
    "lesson": 1,
    "viewing_datetime": "2023-09-21T15:40:46.115871Z",
    "status": true
    }

Выведение списка всех уроков по **всем** продуктам, к которым пользователь имеет доступ, с выведением информации о статусе и времени просмотра:

    GET /api/products/get_all_by_products/
    Пример ответа:
    [
    {
        "id": 2,
        "lessons": [
            {
                "id": 13,
                "name": "1",
                "url_video": "https://www.youtube.com/",
                "duration_video": 1,
                "views": [
                    {
                        "id": 1,
                        "viewing_datetime": "2023-09-21T14:21:59.055555Z",
                        "status": false
                    },
                    {
                        "id": 3,
                        "viewing_datetime": "2023-09-21T15:27:54.132040Z",
                        "status": false
                    },
                    {
                        "id": 5,
                        "viewing_datetime": "2023-09-21T15:31:08.355621Z",
                        "status": false
                    }
                ]
            },
            {
                "id": 14,
                "name": "1",
                "url_video": "https://www.youtube.com/",
                "duration_video": 1,
                "views": []
            }
        ]
    },
    {
        "id": 3,
        "lessons": []
    }
    ]


Выведение списка уроков по **конкретному** продукту, к которому пользователь имеет доступ, с выведением информации о статусе и времени просмотра, а также датой последнего просмотра ролика.

    GET /api/products/2/get_all_by_single_product/
    Пример ответа:
    {
    "id": 2,
    "lessons": [
        {
            "id": 13,
            "name": "1",
            "url_video": "https://www.youtube.com/",
            "duration_video": 1,
            "last_view": "2023-09-21T15:31:08.355621Z",
            "views": [
                {
                    "id": 1,
                    "viewing_datetime": "2023-09-21T14:21:59.055555Z",
                    "status": false
                },
                {
                    "id": 3,
                    "viewing_datetime": "2023-09-21T15:27:54.132040Z",
                    "status": false
                },
                {
                    "id": 5,
                    "viewing_datetime": "2023-09-21T15:31:08.355621Z",
                    "status": false
                }
            ]
        },
        {
            "id": 14,
            "name": "1",
            "url_video": "https://www.youtube.com/",
            "duration_video": 1,
            "last_view": false,
            "views": []
        }
    ]
    }


Список всех продуктов на платформе,c информацией:
  1. Количество просмотренных уроков от всех учеников.
  2. Сколько в сумме все ученики потратили времени на просмотр роликов. #todo
  3. Количество учеников занимающихся на продукте.
  4. Процент приобретения продукта (рассчитывается исходя из количества
   полученных доступов к продукту деленное на общее количество
   пользователей на платформе).
   
    GET api/products/get_statistic_products/
    Пример ответа:
    [
    {
        "id": 2,
        "viewed_lessons": 1,
        "count_time_video": 30,
        "count_students": 1,
        "percent_get_product": 50
    },
    {
        "id": 3,
        "viewed_lessons": 0,
        "count_time_video": 0,
        "count_students": 1,
        "percent_get_product": 50
    },
    {
        "id": 4,
        "viewed_lessons": 0,
        "count_time_video": 0,
        "count_students": 0,
        "percent_get_product": 0
    },
    {
        "id": 5,
        "viewed_lessons": 0,
        "count_time_video": 0,
        "count_students": 0,
        "percent_get_product": 0
    },
    {
        "id": 6,
        "viewed_lessons": 0,
        "count_time_video": 0,
        "count_students": 0,
        "percent_get_product": 0
    },
    {
        "id": 7,
        "viewed_lessons": 0,
        "count_time_video": 0,
        "count_students": 0,
        "percent_get_product": 0
    }
    ]

login 

    admin
password 
    
    admin

Автор: <a href="https://github.com/helena6421/">Матвеева А.С.</a>
