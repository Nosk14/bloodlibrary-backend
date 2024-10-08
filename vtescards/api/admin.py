from django.contrib import admin
from api.models import Card, CardSet, Set


class CardSetInline(admin.TabularInline):
    model = CardSet
    extra = 1
    exclude = ('info',)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'alias')
    filter_horizontal = ('publish_sets',)
    inlines = (CardSetInline,)


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    inlines = (CardSetInline,)


@admin.register(CardSet)
class CardSetAdmin(admin.ModelAdmin):
    list_display = ('card', 'set', 'info', 'image')


