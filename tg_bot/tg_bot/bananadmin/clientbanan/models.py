from django.db import models
import jsonfield
from django.utils.html import format_html

# Создаем модели 

#1. Модель респондента
class Respondent(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name = 'id')
    first_name = models.CharField(max_length=128, blank=True, verbose_name = 'Имя')
    last_name = models.CharField(max_length=128, blank=True, verbose_name = 'Фамилия')
    username = models.CharField(max_length=128, blank=True,  verbose_name = 'Никнейм')

    @property
    def count_responses(self):
        return self.responses.filter(completed=True).count()

    @property
    def get_responses(self):
        return self.responses.filter(completed=True)


class Response(models.Model):
    #name = models.CharField(default = 'FirstQuestion',max_length=128, blank=True, verbose_name = 'Название опроса')
    step = models.SmallIntegerField(default=0, verbose_name = 'Шаг опроса')
    parts = jsonfield.JSONField(max_length=8192, default=dict, verbose_name = 'Детали опроса')
    respondent = models.ForeignKey(Respondent, related_name="responses", on_delete = models.CASCADE, verbose_name = 'Респондент')
    completed = models.BooleanField(default=False, verbose_name = 'Завершенные опросы')


    @property
    def create_table(self):
        table = "<table class='table'>"

        for question in self.parts:
            answer = self.parts[question]
            table += f"""
                <tr>
                    <td>{question}</td>
                    <td><b>{answer}</b></td>
                </tr>
            """

        table += "</table>"
        return format_html(table)


