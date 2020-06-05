"""Default messages for bot functions."""

authorization_denied_message = {
    'en': "You are not allowed to use this command, sorry.",
    'it': "Non disponi di autorizzazioni sufficienti per questa richiesta, spiacente.",
}

language_messages = {
    'language_command': {
        'name': {
            'en': "/language",
            'it': "/lingua"
        },
        'reply_keyboard_button': {
            'en': "Language 🗣",
            'it': "Lingua 🗣"
        },
        'alias': {
            'en': "Language 🗣",
            'it': "Lingua 🗣"
        },
        'description': {
            'en': "Change language settings",
            'it': "Cambia le impostazioni della lingua"
        }
    },
    'language_button': {
        'description': {
            'en': "Change language settings",
            'it': "Cambia le impostazioni della lingua"
        },
        'language_set': {
            'en': "Selected language: English 🇬🇧",
            'it': "Lingua selezionata: Italiano 🇮🇹"
        }
    },
    'language_panel': {
        'text': {
            'en': "<b>Choose a language</b>",
            'it': "<b>Seleziona una lingua</b>"
        }
    }
}

supported_languages = {
    'en': {
        'flag': '🇬🇧',
        'name': 'English'
    },
    'it': {
        'flag': '🇮🇹',
        'name': 'Italiano'
    }
}

default_ciclopi_messages = {
    'help': {
        "name": "ciclopi",
        "label": {
            'en': "CicloPi 🚲",
            'it': "CicloPi 🚲",
        },
        "authorization_level": "everybody",
        "description": {
            'en': "Use /ciclopi command to know how many available bikes and "
                  "free stalls are available in each station.",
            'it': "Per vedere quante bici disponibili e quanti posti liberi "
                  "ci sono in ogni stazione CicloPi usa il comando /ciclopi.",
        },
    },
    'command': {
        'description': {
            'en': "CicloPi stations status",
            'it': "Stato delle stazioni CicloPi",
        },
        'reply_keyboard_button': {
            'en': "CicloPi 🚲",
            'it': "CicloPi 🚲",
        },
        'updating': {
            'en': "Updating",
            'it': "Aggiornamento in corso",
        },
        'unavailable_website': {
            'en': "CicloPi's website cannot be reached at the moment.\n"
                  "Please retry later :/",
            'it': "Il sito del CicloPi è momentaneamente irraggiungibile.\n"
                  "Riprova tra un po' :/",
        },
        'no_station_available': {
            'en': "No station available",
            'it': "Nessuna stazione",
        },
        'title': {
            'en': "CicloPi stations",
            'it': "Stazioni CicloPi",
        },
        'buttons': {
            'all': {
                'en': "All",
                'it': "Tutte",
            },
            'only_fav': {
                'en': "Favourites only",
                'it': "Solo preferite",
            },
            'first_n': {
                'en': "First {n}",
                'it': "Prime {n}",
            },
            'update': {
                'en': "🔄 Update",
                'it': "🔄 Aggiorna",
            },
            'legend': {
                'en': "📜 Legend",
                'it': "📜 Legenda",
            },
            'settings': {
                'en': "⚙️ Settings",
                'it': "⚙️ Impostazioni",
            },
        }
    },
    'settings': {
        'sort': {
            'name': {
                'en': "Order",
                'it': "Ordina"
            },
            'description': {
                'en': "customize CicloPi stations display order.",
                'it': "scegli in che ordine visualizzare le stazioni CicloPi."
            },
            'symbol': {
                'en': "⏬",
                'it': "⏬"
            }
        },
        'limit': {
            'name': {
                'en': "Number of stations",
                'it': "Numero di stazioni"
            },
            'description': {
                'en': "choose how many stations you want to view.",
                'it': "scegli quante stazioni visualizzare."
            },
            'symbol': {
                'en': "#️⃣",
                'it': "#️⃣"
            }
        },
        'fav': {
            'name': {
                'en': "Favourite stations",
                'it': "Stazioni preferite"
            },
            'description': {
                'en': "edit favourite stations.",
                'it': "cambia le tue stazioni preferite."
            },
            'symbol': {
                'en': "⭐️",
                'it': "⭐️"
            }
        },
        'setpos': {
            'name': {
                'en': "Set location",
                'it': "Cambia posizione",
            },
            'description': {
                'en': "set a location from which stations may be sorted by "
                      "distance.",
                'it': "imposta una posizione da cui ordinare le stazioni per "
                      "distanza."
                     },
            'symbol': {
                'en': "🧭",
                'it': "🧭"
            }
        }
    },
    'sorting': {
        'center': {
            'name': {
                'en': "City center",
                'it': "Borgo"
            },
            'description': {
                'en': "sorted by distance from city center (Borgo Stretto "
                      " station.)",
                'it': "in ordine di distanza crescente da Borgo Stretto."
            },
            'short_description': {
                'en': "by distance from city center",
                'it': "per distanza da Borgo Stretto"
            }
        },
        'alphabetical': {
            'name': {
                'en': "Alphabetical",
                'it': "Alfabetico"
            },
            'description': {
                'en': "in alphabetical order.",
                'it': "in ordine alfabetico."
            },
            'short_description': {
                'en': "by name",
                'it': "per nome"
            }
        },
        'position': {
            'name': {
                'en': "Position",
                'it': "Posizione"
            },
            'description': {
                'en': "sorted by distance from last set position. "
                      "City center position is set by default.",
                'it': "in ordine di distanza crescente dall'ultima posizione "
                      "inviata. Di default sarà Borgo Stretto."
            },
            'short_description': {
                'en': "by distance",
                'it': "per distanza"
            }
        },
        'custom': {
            'name': {
                'en': "Favourites",
                'it': "Preferite"
            },
            'description': {
                'en': "sorted by custom order.",
                'it': "nell'ordine che hai scelto."
            },
            'short_description': {
                'en': "customly ordered",
                'it': "in ordine personalizzato"
            },
        }
    },
    'filters': {
        'fav': {
            'name': {
                'en': "Only favourite stations",
                'it': "Solo le preferite"
            },
            'all': {
                'en': "favourite stations first",
                'it': "prima le preferite"
            },
            'only': {
                'en': "only favourite stations",
                'it': "solo le preferite"
            }
        },
        'num': {
            'en': "first {n}",
            'it': "prime {n}"
        },
        'all': {
            'name': {
                'en': "All stations",
                'it': "Tutte"
            },
        },
        '3': {
            'name': {
                'en': "3",
                'it': "3"
            },
        },
        '5': {
            'name': {
                'en': "5",
                'it': "5"
            },
        },
        '10': {
            'name': {
                'en': "10",
                'it': "10"
            },
        }
    },
    'status': {
        'not_available': {
            'en': "Not available",
            'it': "Non disponibile"
        }
    },
    'set_position': {
        'success': {
            'en': "Position set!\n"
                  "From now on, stations will be sorted by distance from "
                  "this position.",
            'it': "Ho salvato questa posizione!\n"
                  "D'ora in poi ordinerò le stazioni dalla più vicina alla "
                  "più lontana da qui."
        },
        'cancel': {
            'en': "Operation cancelled.",
            'it': "Operazione annullata."
        },
        'cancel_and_remind': {
            'en': "I could not understand your position.\n"
                  "Try again with /ciclopi > Settings > Set location",
            'it': "Non ho capito la tua posizione.\n"
                  "Per riprovare fai "
                  "/ciclopi > Impostazioni > Cambia posizione"
        }
    },
    'button': {
        'title': {
            'en': "CicloPi Settings",
            'it': "Impostazioni CicloPi"
        },
        'back_to_settings': {
            'en': "Back to settings",
            'it': "Torna alle impostazioni"
        },
        'back_to_stations': {
            'en': "Back to stations",
            'it': "Torna alle stazioni"
        },
        'legend': {
            'name': {
                'en': "Station name",
                'it': "Nome della stazione",
            },
            'distance': {
                'en': "Distance in meters",
                'it': "Distanza in m",
            },
            'description': {
                'en': "Station address",
                'it': "Indirizzo della stazione",
            },
            'bikes': {
                'en': "Available bikes",
                'it': "Bici disponibili",
            },
            'free': {
                'en': "Free parking stalls",
                'it': "Posti liberi",
            }
        },
        'no_change': {
            'en': "No change detected!",
            'it': "È già così!",
        },
        'unknown_option': {
            'en': "Unknown option!",
            'it': "Opzione sconosciuta!",
        },
        'done': {
            'en': "Done!",
            'it': "Fatto!",
        },
        'sorting_header': {
            'en': "📜 CicloPi stations display order 🚲\n\n"
                  "{{options}}\n\n"
                  "Choose a mode or go back to stations list using the "
                  "buttons.",
            'it': "📜 Ordine di visualizzazione delle stazioni CicloPi 🚲\n\n"
                  "{{options}}\n\n"
                  "Scegli una nuova modalità o torna all'elenco delle "
                  "stazioni usando i bottoni."
        },
        'limit_header': {
            'en': "📜 Number of CicloPi stations to show 🚲\n\n"
                  "{{options}}\n\n"
                  "Choose a mode or go back to stations list using the "
                  "buttons.",
            'it': "📜 Numero di stazioni CicloPi da mostrare 🚲\n\n"
                  "{{options}}\n\n"
                  "Scegli una nuova modalità o torna all'elenco delle "
                  "stazioni usando i bottoni."
        },
        'favourites': {
            'popup': {
                'en': "Touch a station to add or remove it",
                'it': "Tocca una stazione per aggiungerla o rimuoverla",
            },
            'header': {
                'en': "🚲 <b>Favourite stations</b> ⭐️\n"
                      "{options}\n\n"
                      "Add or remove your favourite stations.",
                'it': "🚲 <b>Stazioni preferite</b> ⭐️\n"
                      "{options}\n\n"
                      "Aggiungi o togli le tue stazioni preferite."
            },
            'sort': {
                'buttons': {
                    'change_order': {
                        'en': "🔃 Change order",
                        'it': "🔃 Riordina",
                    },
                    'edit': {
                        'en': "✏️ Edit favourite stations ⭐️",
                        'it': "✏️ Modifica stazioni preferite ⭐️",
                    },
                    'move_down': {
                        'en': "Move down ⬇️",
                        'it': "Sposta in basso ⬇️",
                    },
                    'move_up': {
                        'en': "Move up ⬆️",
                        'it': "Sposta in alto ⬆️",
                    },
                },
                'end': {
                    'en': "End of the line reached!",
                    'it': "Capolinea!",
                },
                'header': {
                    'en': "🚲 <b>Favourite stations</b> ⭐️\n"
                          "{options}\n\n"
                          "Add, remove or sort your favourite stations.",
                    'it': "🚲 <b>Stazioni preferite</b> ⭐️\n"
                          "{options}\n\n"
                          "Aggiungi, togli o riordina le tue stazioni "
                          "preferite.",
                },
            },
        },
        'location': {
            'popup': {
                'en': "Send a location!",
                'it': "Inviami una posizione!",
            },
            'instructions': {
                'en': "Send a location.\n"
                      "Use the button to send your current location.",
                'it': "Inviami una posizione.\n"
                      "Per inviare la tua posizione attuale, usa il "
                      "pulsante.",
            },
            'send_current_location': {
                'en': "Send current location",
                'it': "Invia la mia posizione",
            },
            'cancel': {
                'en': "Cancel",
                'it': "Annulla",
            },
        },
    }
}

default_help_messages = {
    'help_command': {
        'header': {
            'en': "<b>{bot.name} commands</b>\n\n"
                  "{commands}",
            'it': "<b>Comandi di {bot.name}</b>\n\n"
                  "{commands}",
        },
        'text': {
            'en': "<b>📖 {bot.name} guide</b>\n\n"
                  "Welcome!\n"
                  "To visit a guide section, press the corresponding button.\n"
                  "To view all available commands, see section "
                  "<code>Commands</code>.\n\n"
                  "Bot author and administrator: @Davte",
            'it': "<b>📖 Guida di {bot.name}\n\n</b>"
                  "Benvenuto!\n"
                  "Per leggere una sezione della guida premi il bottone "
                  "corrispondente.\n"
                  "Per conoscere  tutti i comandi "
                  "disponibili, visita l'apposita sezione della guida "
                  "premendo il pulsante <code>Comandi</code>.\n\n"
                  "Autore e amministratore del bot: @Davte"
        },
        'reply_keyboard_button': {
            'en': "Help 📖",
            'it': "Guida 📖"
        },
        'description': {
            'en': "Help",
            'it': "Aiuto"
        },
        'access_denied_message': {
            'en': "Ask for authorization. If your request is accepted, send "
                  "/help command again to read the guide.",
            'it': "Chiedi di essere autorizzato: se la tua richiesta "
                  "verrà accolta, ripeti il comando /help per leggere "
                  "il messaggio di aiuto."
        },
        'back_to_help_menu': {
            'en': "Back to guide menu 📖",
            'it': "Torna al menu Guida 📖",
        },
    },
    'commands_button_label': {
            'en': "Commands 🤖",
            'it': "Comandi 🤖",
    },
}

unknown_command_message = {
    'en': "Unknown command! Touch /help to read the guide and available commands.",
    'it': "Comando sconosciuto! Fai /help per leggere la guida e i comandi."
}
