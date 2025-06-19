Back
Как запустить проект :
Создание оркужени в него  :
python -m venv .venv 
.venv\Scripts\activate
Загрузка библетека из файла     
 pip install -r requirements.txt   
Запуск программы:
python manage.py makemigrations  
python manage.py migrate  
python manage.py runserver 
Если проблемы с бд   : 
settings.py
Создаете такую бд  'DietApp',  
'PASSWORD': 'posgress'замените на свой пароль в posgres/                                                                                 
                                                                                                                                                                                  