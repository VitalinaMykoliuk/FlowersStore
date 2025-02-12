from celery import shared_task
from django.db import connection


@shared_task
def clean_database():
    with conection.cursor() as cursor:
        cursor.execute('DELETE FROM cart_cartitem WHERE user_id IS NULL')
        cursor.execute('DELETE FROM django_session')

