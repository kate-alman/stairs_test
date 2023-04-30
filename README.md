### Древовидное меню <br>
<p>
<img src="https://1000marcas.net/wp-content/uploads/2021/06/Django-Logo.png" title="Django" height="100"/>
</p>

**Установка зависимостей**    
```pip install -r requirements.txt```    

**Изменение рабочего каталога на директорию с приложением**       
```cd test_menu```    

**Запуск приложения**      
```python manage.py runserver```        

**Можно воспользоваться тестовой базой из репозитория**     
```python manage.py migrate```     

**Загрузка templatestags**       
```{% load common_tags %}```      

**Отрисовка меню**        
```{% draw_menu 'Название меню' %}```    

**Доступ к админке http://127.0.0.1:8000/admin/**        
```
login - admin      
password - admin
```
или     
**Создать нового суперпользователя**      
```python manage.py createsuperuser```    