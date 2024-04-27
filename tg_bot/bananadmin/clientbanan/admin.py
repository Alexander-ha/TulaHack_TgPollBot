from django.contrib import admin

from .models import Respondent, Response


admin.site.site_header = 'Бот для опросов'


class ResponseInline(admin.StackedInline):
    model = Response
    max_num = 0
    can_delete = False
    fields = ("create_table",)
    readonly_fields = ("create_table",)

# Регистрируем модели

@admin.register(Respondent)
class RespondentAdmin(admin.ModelAdmin):
    search_fields = ("id", "first_name", "last_name", "username")
    fields = ("first_name", "last_name", "username", "count_responses", "get_responses")
    list_display = ("first_name", "last_name", "username", "count_responses", "get_responses")
    readonly_fields = ("first_name", "last_name", "username", "count_responses", "get_responses")
  #  list_select_related = ("responses",)
    inlines = (ResponseInline,)
