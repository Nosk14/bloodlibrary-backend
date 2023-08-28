from django.contrib import admin
from decks.models import TournamentDeck
from decks.clients import VEKNClient, VTESDecksClient


class TournamentDeckAdmin(admin.ModelAdmin):
    actions = ["load_decks"]
    list_filter = ["country", "author", "year"]

    def load_decks(self, request, queryset):
        vtesdecks = VTESDecksClient()
        vekn = VEKNClient()

        limit = 50
        offset = 0

        while True:
            decks_to_add = []
            deck_list = vtesdecks.get_tournament_decks(offset, limit, years=[2016, 2999])
            for deck in deck_list['decks']:
                vtesdecks_info = vtesdecks.get_deck_info(deck["id"])
                event_id = vtesdecks_info['url'].split('/')[-1] if 'url' in vtesdecks_info else vtesdecks_info['id'].split('-')[-1]
                vekn_info = vekn.get_event(event_id)

                if not vekn_info:
                    continue

                tournament_deck = TournamentDeck(
                    name=vtesdecks_info['name'],
                    author=vtesdecks_info['author'],
                    vekn_id=vekn_info['event_id'],
                    vtesdecks_id=vtesdecks_info['id'],
                    country=vekn_info['venue_country'],
                    num_players=vtesdecks_info['players'] if 'players' in vtesdecks_info else len(vekn_info['players']),
                    year=vtesdecks_info['year'],
                    vtesdecks_link='https://vtesdecks.com/deck/' + vtesdecks_info['id']
                )
                decks_to_add.append(tournament_deck)

            TournamentDeck.objects.bulk_create(
                decks_to_add,
                update_conflicts=True,
                unique_fields=['vtesdecks_id'],
                update_fields=['vtesdecks_id']
            )

            offset += limit
            if offset > deck_list['total']:
                break


admin.site.register(TournamentDeck, TournamentDeckAdmin)
