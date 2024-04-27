import time

from django.core.management import BaseCommand

from clientbanan.bot import bot


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Запуск работы бота")
        try:
            bot.polling()
        except Exception as e:
            print(e)
            time.sleep(5)
            self.handle(*args, **options)