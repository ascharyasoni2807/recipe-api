Deployed web link - https://recipe-api-b60t.onrender.com/admin/  
        Django admin credentials   
        email -  testadmin@gmail.com
        password -  test@1234

Deployed Swagger- https://recipe-api-b60t.onrender.com/


Steps to proceed 

1. Clone this repo
2. Install the Docker desktop / Docker Engine / or any another according to your machine
3. run the command -
      docker compose build
      docker compose up

4. This will create your app , you can login with given credentials above. 



Coverage reports  - 
<img width="563" alt="image" src="https://github.com/user-attachments/assets/263db07a-9a07-4097-8fe9-21cccd868889">

<img width="513" alt="image" src="https://github.com/user-attachments/assets/226a946a-ff46-4f88-8edd-fe644a78c973">

<img width="487" alt="image" src="https://github.com/user-attachments/assets/0d7ab818-24b8-4418-986b-0c1b3296fc7c">

<img width="484" alt="image" src="https://github.com/user-attachments/assets/191d754b-1a6a-4213-9100-15475c7891fe">

<img width="453" alt="image" src="https://github.com/user-attachments/assets/1adc9ab2-f52b-4f34-a73d-61080aa80372">




For email notifications - 

Create a user with your real email id ( so you will receive mail on that )  - >  then create a receipe by that user 
->  then hit the recipe like api / or directly add object in django admin receipe likes table ->  we are sending user email once in 24 hour as of now.



To test email function make changes here - 

In Celery.py  

    app.conf.beat_schedule = {
            'send-daily-notifications': {
                'task': 'recipe.tasks.send_daily_notifications',
                # for every 24 hour
                'schedule': crontab(hour="0", minute="0"),
                    },
    }

 change above one to this  for getting email in every one minute
'schedule':crontab(minute="*", hour="*") 


Result - <img width="1152" alt="image" src="https://github.com/user-attachments/assets/ad1ced25-944a-468c-8405-60122992e30d">

I have used celery for the first time , but ya receiving email and working fine.   The from email i have made new for test 
