"""Get information about bike sharing in Pisa.

Available bikes in bike sharing stations.
"""

# Standard library modules
import asyncio
import datetime
import math

# Third party modules
import davtelepot
from davtelepot.utilities import (
    async_wrapper, CachedPage, extract, get_cleaned_text,
    line_drawing_unordered_list, make_button, make_inline_keyboard,
    make_lines_of_buttons
)

default_location = None

_URL = "http://www.ciclopi.eu/frmLeStazioni.aspx"

ciclopi_webpage = CachedPage.get(
    _URL,
    datetime.timedelta(seconds=15),
    mode='html'
)

UNIT_TO_KM = {
    'km': 1,
    'm': 1000,
    'mi': 0.621371192,
    'nmi': 0.539956803,
    'ft': 3280.839895013,
    'in': 39370.078740158
}

CICLOPI_SORTING_CHOICES = {
    0: dict(
        id='center',
        symbol='🏛'
    ),
    1: dict(
        id='alphabetical',
        symbol='🔤'
    ),
    2: dict(
        id='position',
        symbol='🧭'
    ),
    3: dict(
        id='custom',
        symbol='⭐️'
    )
}

CICLOPI_STATIONS_TO_SHOW = {
    -1: dict(
        id='fav',
        symbol='⭐️'
    ),
    0: dict(
        id='all',
        symbol='💯'
    ),
    3: dict(
        id='3',
        symbol='3️⃣'
    ),
    5: dict(
        id='5',
        symbol='5️⃣'
    ),
    10: dict(
        id='10',
        symbol='🔟'
    )
}


def haversine_distance(lat1, lon1, lat2, lon2, degrees='dec', unit='m'):
    """
    Calculate the great circle distance between two points on Earth.

    (specified in decimal degrees)
    """
    assert unit in UNIT_TO_KM, "Invalid distance unit of measurement!"
    assert degrees in ['dec', 'rad'], "Invalid angle unit of measurement!"
    # Convert decimal degrees to radians
    if degrees == 'dec':
        lon1, lat1, lon2, lat2 = map(
            math.radians,
            [lon1, lat1, lon2, lat2]
        )
    average_earth_radius = 6371.0088 * UNIT_TO_KM[unit]
    return (
        2
        * average_earth_radius
        * math.asin(
            math.sqrt(
                math.sin((lat2 - lat1) * 0.5) ** 2
                + math.cos(lat1)
                * math.cos(lat2)
                * math.sin((lon2 - lon1) * 0.5) ** 2
            )
        )
    )


class Location:
    """Location in world map."""

    def __init__(self, coordinates):
        """Check and set instance attributes."""
        assert type(coordinates) is tuple, "`coordinates` must be a tuple"
        assert (
                len(coordinates) == 2
                and all(type(c) is float for c in coordinates)
        ), "`coordinates` must be two floats"
        self._coordinates = coordinates

    @property
    def coordinates(self):
        """Return a tuple (latitude, longitude)."""
        return self._coordinates

    @property
    def latitude(self):
        """Return latitude."""
        return self._coordinates[0]

    @property
    def longitude(self):
        """Return longitude."""
        return self._coordinates[1]

    def get_distance(self, other, *args, **kwargs):
        """Return the distance between two `Location`s."""
        return haversine_distance(
            self.latitude, self.longitude,
            other.latitude, other.longitude,
            *args, **kwargs
        )


class Station(Location):
    """CicloPi bike sharing station."""

    stations = {
        1: dict(
            name='Aeroporto',
            coordinates=(43.699455, 10.400075),
        ),
        2: dict(
            name='Stazione F.S.',
            coordinates=(43.708627, 10.399051),
        ),
        3: dict(
            name='Comune Palazzo Blu',
            coordinates=(43.715541, 10.400505),
        ),
        4: dict(
            name='Teatro Tribunale',
            coordinates=(43.716391, 10.405136),
        ),
        5: dict(
            name='Borgo Stretto',
            coordinates=(43.718518, 10.402165),
        ),
        6: dict(
            name='Polo Marzotto',
            coordinates=(43.719772, 10.407291),
        ),
        7: dict(
            name='Duomo',
            coordinates=(43.722855, 10.391977),
        ),
        8: dict(
            name='Pietrasantina',
            coordinates=(43.729020, 10.392726),
        ),
        9: dict(
            name='Paparelli',
            coordinates=(43.724449, 10.410438),
        ),
        10: dict(
            name='Pratale',
            coordinates=(43.7212554, 10.4180257),
        ),
        11: dict(
            name='Ospedale Cisanello',
            coordinates=(43.705752, 10.441740),
        ),
        12: dict(
            name='Sms Biblioteca',
            coordinates=(43.706565, 10.419136),
        ),
        13: dict(
            name='Vittorio Emanuele',
            coordinates=(43.710182, 10.398751),
        ),
        14: dict(
            name='Palacongressi',
            coordinates=(43.710014, 10.410232),
        ),
        15: dict(
            name='Porta a Lucca',
            coordinates=(43.724247, 10.402269),
        ),
        16: dict(
            name='Solferino',
            coordinates=(43.715698, 10.394999),
        ),
        17: dict(
            name='San Rossore F.S.',
            coordinates=(43.718992, 10.384391),
        ),
        18: dict(
            name='Guerrazzi',
            coordinates=(43.710358, 10.405337),
        ),
        19: dict(
            name='Livornese',
            coordinates=(43.708114, 10.384021),
        ),
        20: dict(
            name='Cavalieri',
            coordinates=(43.719856, 10.400194),
        ),
        21: dict(
            name='M. Libertà',
            coordinates=(43.719821, 10.403021),
        ),
        22: dict(
            name='Galleria Gerace',
            coordinates=(43.710791, 10.420456),
        ),
        23: dict(
            name='C. Marchesi',
            coordinates=(43.714971, 10.419322),
        ),
        24: dict(
            name='CNR-Praticelli',
            coordinates=(43.719256, 10.424012),
        ),
        25: dict(
            name='Sesta Porta',
            coordinates=(43.709162, 10.395837),
        ),
        26: dict(
            name='Qualconia',
            coordinates=(43.713011, 10.394458),
        ),
        27: dict(
            name='Donatello',
            coordinates=(43.711715, 10.372480),
        ),
        28: dict(
            name='Spadoni',
            coordinates=(43.716850, 10.391347),
        ),
        29: dict(
            name='Nievo',
            coordinates=(43.738286, 10.400865),
        ),
        30: dict(
            name='Cisanello',
            coordinates=(43.701159, 10.438863),
        ),
        31: dict(
            name='Edificio 3',
            coordinates=(43.707869, 10.441698),
        ),
        32: dict(
            name='Edificio 6',
            coordinates=(43.709046, 10.442541),
        ),
        33: dict(
            name='Frascani',
            coordinates=(43.710157, 10.433339),
        ),
        34: dict(
            name='Chiarugi',
            coordinates=(43.726244, 10.412882),
        ),
        35: dict(
            name='Praticelli 2',
            coordinates=(43.719619, 10.427469),
        ),
        36: dict(
            name='Carducci',
            coordinates=(43.726700, 10.420562),
        ),
        37: dict(
            name='Garibaldi',
            coordinates=(43.718077, 10.418168),
        ),
        38: dict(
            name='Silvestro',
            coordinates=(43.714128, 10.409065),
        ),
        39: dict(
            name='Pardi',
            coordinates=(43.702273, 10.399793),
        ),
    }

    def __init__(self, id_=0, name='unknown', coordinates=(91.0, 181.0)):
        """Check and set instance attributes."""
        if id_ in self.__class__.stations:
            coordinates = self.__class__.stations[id_]['coordinates']
            name = self.__class__.stations[id_]['name']
        Location.__init__(self, coordinates)
        self._id = id_
        self._name = name
        self._active = True
        self._location = None
        self._description = ''
        self._distance = None
        self._bikes = 0
        self._free = 0

    @property
    def id(self):
        """Return station identification number."""
        return self._id

    @property
    def name(self):
        """Return station name."""
        return self._name

    @property
    def description(self):
        """Return station description."""
        return self._description

    @property
    def is_active(self):
        """Return True if station is active."""
        return self._active

    @property
    def location(self):
        """Return location from which distance should be evaluated."""
        if self._location is None:
            return default_location
        return self._location

    @property
    def distance(self):
        """Return distance from `self.location`.

        If distance is not evaluated yet, do it and store the result.
        Otherwise, return stored value.
        """
        if self._distance is None:
            self._distance = self.get_distance(self.location)
        return self._distance

    @property
    def bikes(self):
        """Return number of available bikes."""
        return self._bikes

    @property
    def free(self):
        """Return number of free slots."""
        return self._free

    def set_active(self, active):
        """Change station status to `active`.

        `active` should be either `True` or `False`.
        """
        assert type(active) is bool, "`active` should be a boolean."
        self._active = active

    def set_description(self, description):
        """Change station description to `description`.

        `description` should be a string.
        """
        assert type(description) is str, "`description` should be a boolean."
        self._description = description

    def set_location(self, location):
        """Change station location to `location`.

        `location` should be a Location object.
        """
        assert (
            isinstance(location, Location)
        ), "`location` should be a Location."
        self._location = location

    def set_bikes(self, bikes):
        """Change number of available `bikes`.

        `bikes` should be an int.
        """
        assert (
                type(bikes) is int
        ), "`bikes` should be an int."
        self._bikes = bikes

    def set_free(self, free):
        """Change number of `free` bike parking slots.

        `free` should be an int.
        """
        assert (
                type(free) is int
        ), "`free` should be an int."
        self._free = free

    @property
    def status(self):
        """Return station status to be shown to users.

        It includes distance, location, available bikes and free stalls.
        """
        if self.bikes + self.free == 0:
            bikes_and_stalls = "<i>⚠️ {{not_available}}</i>"
        else:
            bikes_and_stalls = f"🚲 {self.bikes}  |  🅿️ {self.free}"
        return (
            f"<b>{self.name}</b> | <i>{self.description}</i>\n"
            f"<code>   </code>{bikes_and_stalls}  | 📍 {self.distance:.0f} m"
        ).format(
            s=self
        )


def ciclopi_custom_sorter(custom_order):
    """Return a function to sort stations by a `custom_order`."""
    custom_values = {
        record['station']: record['value']
        for record in custom_order
    }

    def sorter(station):
        """Take a station and return its queue value.

        Stations will be sorted by queue value in ascending order.
        """
        if station.id in custom_values:
            return custom_values[station.id], station.name
        return 100, station.name

    return sorter


def _get_stations(data, location):
    stations = []
    for _station in data.find_all(
            "li",
            attrs={"class": "rrItem"}
    ):
        station_name = _station.find(
            "span",
            attrs={"class": "Stazione"}
        ).text
        if 'Non operativa' in station_name:
            active = False
        else:
            active = True
        station_id = _station.find(
            "div",
            attrs={"class": "cssNumero"}
        ).text
        if (
                station_id is None
                or type(station_id) is not str
                or not station_id.isnumeric()
        ):
            station_id = 0
        else:
            station_id = int(station_id)
        station = Station(station_id)
        station.set_active(active)
        station.set_description(
            _station.find(
                "span",
                attrs={"class": "TableComune"}
            ).text.replace(
                'a`',
                'à'
            ).replace(
                'e`',
                'è'
            )
        )
        bikes_text = _station.find(
            "span",
            attrs={"class": "Red"}
        ).get_text('\t')
        if bikes_text.count('\t') < 1:
            bikes = 0
            free = 0
        else:
            bikes, free, *other = [
                int(
                    ''.join(
                        char
                        for char in s
                        if char.isnumeric()
                    )
                )
                for s in bikes_text.split('\t')
            ]
        station.set_bikes(bikes)
        station.set_free(free)
        station.set_location(location)
        stations.append(
            station
        )
    return stations


async def set_ciclopi_location(bot, update, user_record):
    """Take a location update and store it as CicloPi place.

    CicloPi stations will be sorted by distance from this place.
    """
    location = update['location']
    chat_id = update['chat']['id']
    telegram_id = update['from']['id']
    with bot.db as db:
        db['ciclopi'].upsert(
            dict(
                chat_id=chat_id,
                latitude=location['latitude'],
                longitude=location['longitude']
            ),
            ['chat_id']
        )
    await bot.send_message(
        chat_id=chat_id,
        text=bot.get_message(
            'ciclopi', 'set_position', 'success',
            update=update, user_record=user_record
        )
    )
    # Remove individual text message handler which was set to catch `/cancel`
    bot.remove_individual_text_message_handler(telegram_id)
    return await _ciclopi_command(bot, update, user_record)


async def cancel_ciclopi_location(bot, update, user_record):
    """Handle the situation in which a user does not send location on request.

    This function is set as individual text message handler when the bot
        requests user's location and is removed if user does send one.
        If not, return a proper message.
    """
    text = get_cleaned_text(bot=bot, update=update)
    # If user cancels operation, confirm that it was cancelled
    if text.lower() == 'annulla':
        return bot.get_message(
            'ciclopi', 'set_position', 'cancel',
            update=update, user_record=user_record
        )
    # If user writes something else, remind them how to set position later
    return bot.get_message(
        'ciclopi', 'set_position', 'cancel_and_remind',
        update=update, user_record=user_record
    )


async def _ciclopi_command(bot: davtelepot.bot.Bot, update, user_record, sent_message=None,
                           show_all=False):
    chat_id = update['chat']['id']
    default_stations_to_show = 5
    stations = []
    placeholder_id = bot.set_placeholder(
        timeout=datetime.timedelta(seconds=1),
        chat_id=chat_id,
        # sent_message=sent_message,
        # text="<i>{message}...</i>".format(
        #     message=bot.get_message(
        #         'ciclopi', 'command', 'updating',
        #         update=update, user_record=user_record
        #     )
        # )
    )
    ciclopi_data = await ciclopi_webpage.get_page()
    if ciclopi_data is None or isinstance(ciclopi_data, Exception):
        text = bot.get_message(
            'ciclopi', 'command', 'unavailable_website',
            update=update, user_record=user_record
        )
    else:
        with bot.db as db:
            ciclopi_record = db['ciclopi'].find_one(
                chat_id=chat_id
            )
            custom_order = list(
                db['ciclopi_custom_order'].find(
                    chat_id=chat_id
                )
            )
            if (
                    ciclopi_record is not None
                    and isinstance(ciclopi_record, dict)
                    and 'sorting' in ciclopi_record
                    and ciclopi_record['sorting'] in CICLOPI_SORTING_CHOICES
            ):
                sorting_code = ciclopi_record['sorting']
                if (
                        'latitude' in ciclopi_record
                        and ciclopi_record['latitude'] is not None
                        and 'longitude' in ciclopi_record
                        and ciclopi_record['longitude'] is not None
                ):
                    saved_place = Location(
                        (
                            ciclopi_record['latitude'],
                            ciclopi_record['longitude']
                        )
                    )
                else:
                    saved_place = default_location
            else:
                sorting_code = 0
            if (
                    ciclopi_record is not None
                    and isinstance(ciclopi_record, dict)
                    and 'stations_to_show' in ciclopi_record
                    and ciclopi_record['stations_to_show'] in CICLOPI_STATIONS_TO_SHOW
            ):
                stations_to_show = ciclopi_record[
                    'stations_to_show'
                ]
            else:
                stations_to_show = default_stations_to_show
        location = (
            saved_place if sorting_code != 0
            else default_location
        )
        sorting_method = (
            (lambda station: station.distance) if sorting_code in [0, 2]
            else (lambda station: station.name) if sorting_code == 1
            else ciclopi_custom_sorter(custom_order) if sorting_code == 3
            else (lambda station: 0)
        )
        stations = sorted(
            _get_stations(
                ciclopi_data,
                location
            ),
            key=sorting_method
        )
        if (
                stations_to_show == -1
                and not show_all
        ):
            stations = list(
                filter(
                    lambda station: station.id in [
                        record['station']
                        for record in custom_order
                    ],
                    stations
                )
            )
        if (
                stations_to_show > 0
                and sorting_code != 1
                and not show_all
        ):
            stations = stations[:stations_to_show]
        filter_label = ""
        if stations_to_show == -1:
            filter_label = bot.get_message(
                'ciclopi', 'filters', 'fav', 'all' if show_all else 'only',
                update=update, user_record=user_record
            )
        elif len(stations) < len(Station.stations):
            filter_label = bot.get_message(
                'ciclopi', 'filters', 'num',
                update=update, user_record=user_record,
                n=stations_to_show
            )
        if filter_label:
            filter_label = ' ({label})'.format(
                label=filter_label
            )
        text = (
            "🚲 {title} {order}"
            "{filter} {sort[symbol]}\n"
            "\n"
            "{stations_list}"
        ).format(
            title=bot.get_message(
                'ciclopi', 'command', 'title',
                update=update, user_record=user_record
            ),
            sort=CICLOPI_SORTING_CHOICES[sorting_code],
            order=bot.get_message(
                'ciclopi', 'sorting',
                CICLOPI_SORTING_CHOICES[sorting_code]['id'],
                'short_description',
                update=update, user_record=user_record
            ),
            filter=filter_label,
            stations_list=(
                '\n\n'.join(
                    station.status.format(
                        not_available=bot.get_message(
                            'ciclopi', 'status', 'not_available',
                            update=update, user_record=user_record
                        )
                    )
                    for station in stations
                ) if len(stations)
                else "<i>- {message} -</i>".format(
                    message=bot.get_message(
                        'ciclopi', 'command', 'no_station_available',
                        update=update, user_record=user_record
                    )
                )
            ),
        )
    if not text:
        return
    reply_markup = make_inline_keyboard(
        (
            [
                make_button(
                    text="💯 {message}".format(
                        message=bot.get_message(
                            'ciclopi', 'command', 'buttons', 'all',
                            update=update, user_record=user_record
                        )
                    ),
                    prefix='ciclopi:///',
                    data=['show', 'all']
                )
            ] if len(stations) < len(Station.stations)
            else [
                make_button(
                    "{sy} {message}".format(
                        message=(
                            bot.get_message(
                                'ciclopi', 'command', 'buttons', 'only_fav',
                                update=update, user_record=user_record
                            ) if stations_to_show == -1
                            else bot.get_message(
                                'ciclopi', 'command', 'buttons', 'first_n',
                                update=update, user_record=user_record,
                                n=stations_to_show
                            )
                        ),
                        sy=CICLOPI_STATIONS_TO_SHOW[stations_to_show]['symbol']
                    ),
                    prefix='ciclopi:///',
                    data=['show']
                )
            ] if show_all
            else []
        ) + [
            make_button(
                text=bot.get_message(
                    'ciclopi', 'command', 'buttons', 'update',
                    update=update, user_record=user_record
                ),
                prefix='ciclopi:///',
                data=(
                    ['show'] + (
                        [] if len(stations) < len(Station.stations)
                        else ['all']
                    )
                )
            ),
            make_button(
                text=bot.get_message(
                    'ciclopi', 'command', 'buttons', 'legend',
                    update=update, user_record=user_record
                ),
                prefix='ciclopi:///',
                data=['legend']
            ),
            make_button(
                text=bot.get_message(
                    'ciclopi', 'command', 'buttons', 'settings',
                    update=update, user_record=user_record
                ),
                prefix='ciclopi:///',
                data=['main']
            )
        ],
        2
    )
    parameters = dict(
        update=update,
        text=text,
        parse_mode='HTML',
        reply_markup=reply_markup
    )
    method = (
        bot.send_message
        if sent_message is None
        else bot.edit_message_text
    )
    await method(**parameters)
    # Mark request as done
    bot.placeholder_requests[placeholder_id] = 1
    return


def get_menu_back_buttons(bot, update, user_record,
                          include_back_to_settings=True):
    """Return a list of menu buttons to navigate back in the menu.

    `include_back_to_settings` : Bool
        Set it to True to include a 'back to settings' menu button.
    """
    if include_back_to_settings:
        buttons = [
            make_button(
                text="⚙️ {message}".format(
                    message=bot.get_message(
                        'ciclopi', 'button', 'back_to_settings',
                        update=update, user_record=user_record
                    )
                ),
                prefix='ciclopi:///',
                data=['main']
            )
        ]
    else:
        buttons = []
    buttons += [
        make_button(
            text="🚲 {message}".format(
                message=bot.get_message(
                    'ciclopi', 'button', 'back_to_stations',
                    update=update, user_record=user_record
                )
            ),
            prefix='ciclopi:///',
            data=['show']
        )
    ]
    return buttons


async def _ciclopi_button_main(bot, update, user_record):
    result, text, reply_markup = '', '', None
    text = (
        "⚙️ {settings_title} 🚲\n"
        "\n"
        "{settings_list}"
    ).format(
        settings_title=bot.get_message(
            'ciclopi', 'button', 'title',
            update=update, user_record=user_record
        ),
        settings_list='\n'.join(
            "- {symbol} {name}: {description}".format(
                symbol=bot.get_message(
                    'ciclopi', 'settings', setting, 'symbol',
                    update=update, user_record=user_record
                ),
                name=bot.get_message(
                    'ciclopi', 'settings', setting, 'name',
                    update=update, user_record=user_record
                ),
                description=bot.get_message(
                    'ciclopi', 'settings', setting, 'description',
                    update=update, user_record=user_record
                )
            )
            for setting in bot.messages['ciclopi']['settings']
        )
    )
    reply_markup = make_inline_keyboard(
        [
            make_button(
                text="{symbol} {name}".format(
                    symbol=bot.get_message(
                        'ciclopi', 'settings', setting, 'symbol',
                        update=update, user_record=user_record
                    ),
                    name=bot.get_message(
                        'ciclopi', 'settings', setting, 'name',
                        update=update, user_record=user_record
                    )
                ),
                prefix='ciclopi:///',
                data=[setting]
            )
            for setting in bot.messages['ciclopi']['settings']
        ] + get_menu_back_buttons(
            bot=bot, update=update, user_record=user_record,
            include_back_to_settings=False
        )
    )
    return result, text, reply_markup


async def _ciclopi_button_sort(bot, update, user_record, arguments):
    result, text, reply_markup = '', '', None
    chat_id = (
        update['message']['chat']['id'] if 'message' in update
        else update['chat']['id'] if 'chat' in update
        else 0
    )
    with bot.db as db:
        ciclopi_record = db['ciclopi'].find_one(
            chat_id=chat_id
        )
        if ciclopi_record is None:
            ciclopi_record = dict(
                chat_id=chat_id,
                sorting=0
            )
        if len(arguments) == 1:
            new_choice = (
                int(arguments[0])
                if arguments[0].isnumeric()
                else 0
            )
            if new_choice == ciclopi_record['sorting']:
                return bot.get_message(
                    'ciclopi', 'button', 'no_change',
                    update=update, user_record=user_record
                ), '', None
            elif new_choice not in CICLOPI_SORTING_CHOICES:
                return bot.get_message(
                    'ciclopi', 'button', 'unknown_option',
                    update=update, user_record=user_record
                ), '', None
            db['ciclopi'].upsert(
                dict(
                    chat_id=chat_id,
                    sorting=new_choice
                ),
                ['chat_id'],
                ensure=True
            )
            ciclopi_record['sorting'] = new_choice
            result = bot.get_message(
                'ciclopi', 'button', 'done',
                update=update, user_record=user_record
            )
    text = bot.get_message(
        'ciclopi', 'button', 'sorting_header',
        update=update, user_record=user_record
    ).format(
        options='\n'.join(
            "- {symbol} {name}: {description}".format(
                symbol=choice['symbol'],
                name=bot.get_message(
                    'ciclopi', 'sorting', choice['id'], 'name',
                    update=update, user_record=user_record
                ),
                description=bot.get_message(
                    'ciclopi', 'sorting', choice['id'], 'description',
                    update=update, user_record=user_record
                )
            )
            for choice in CICLOPI_SORTING_CHOICES.values()
        )
    )
    reply_markup = make_inline_keyboard(
        [
            make_button(
                text="{s} {name} {c[symbol]}".format(
                    c=choice,
                    s=(
                        '✅'
                        if code == ciclopi_record['sorting']
                        else '☑️'
                    ),
                    name=bot.get_message(
                        'ciclopi', 'sorting', choice['id'], 'name',
                        update=update, user_record=user_record
                    )
                ),
                prefix='ciclopi:///',
                data=['sort', code]
            )
            for code, choice in CICLOPI_SORTING_CHOICES.items()
        ] + get_menu_back_buttons(
            bot=bot, update=update, user_record=user_record,
            include_back_to_settings=True
        )
    )
    return result, text, reply_markup


async def _ciclopi_button_limit(bot, update, user_record, arguments):
    result, text, reply_markup = '', '', None
    chat_id = (
        update['message']['chat']['id'] if 'message' in update
        else update['chat']['id'] if 'chat' in update
        else 0
    )
    with bot.db as db:
        ciclopi_record = db['ciclopi'].find_one(
            chat_id=chat_id
        )
        if ciclopi_record is None or 'stations_to_show' not in ciclopi_record:
            ciclopi_record = dict(
                chat_id=chat_id,
                stations_to_show=5
            )
        if len(arguments) == 1:
            new_choice = (
                int(arguments[0])
                if arguments[0].lstrip('+-').isnumeric()
                else 0
            )
            if new_choice == ciclopi_record['stations_to_show']:
                return bot.get_message(
                    'ciclopi', 'button', 'no_change',
                    update=update, user_record=user_record
                ), '', None
            elif new_choice not in CICLOPI_STATIONS_TO_SHOW:
                return bot.get_message(
                    'ciclopi', 'button', 'unknown_option',
                    update=update, user_record=user_record
                ), '', None
            db['ciclopi'].upsert(
                dict(
                    chat_id=chat_id,
                    stations_to_show=new_choice
                ),
                ['chat_id'],
                ensure=True
            )
            ciclopi_record['stations_to_show'] = new_choice
            result = bot.get_message(
                'ciclopi', 'button', 'done',
                update=update, user_record=user_record
            )
    text = bot.get_message(
        'ciclopi', 'button', 'limit_header',
        update=update, user_record=user_record
    ).format(
        options='\n'.join(
            "- {symbol} {name}".format(
                symbol=choice['symbol'],
                name=bot.get_message(
                    'ciclopi', 'filters', choice['id'], 'name',
                    update=update, user_record=user_record
                )
            )
            for choice in CICLOPI_STATIONS_TO_SHOW.values()
        )
    )
    reply_markup = make_inline_keyboard(
        [
            make_button(
                text="{s} {name} {symbol}".format(
                    symbol=choice['symbol'],
                    name=bot.get_message(
                        'ciclopi', 'filters', choice['id'], 'name',
                        update=update, user_record=user_record
                    ),
                    s=(
                        '✅'
                        if code == ciclopi_record['stations_to_show']
                        else '☑️'
                    )
                ),
                prefix='ciclopi:///',
                data=['limit', code]
            )
            for code, choice in CICLOPI_STATIONS_TO_SHOW.items()
        ] + get_menu_back_buttons(
            bot=bot, update=update, user_record=user_record,
            include_back_to_settings=True
        )
    )
    return result, text, reply_markup


async def _ciclopi_button_show(bot, update, user_record, arguments):
    result, text, reply_markup = '', '', None
    fake_update = update['message']
    fake_update['from'] = update['from']
    asyncio.ensure_future(
        _ciclopi_command(
            bot=bot,
            update=fake_update,
            user_record=user_record,
            sent_message=fake_update,
            show_all=(
                True if len(arguments) == 1 and arguments[0] == 'all'
                else False
            )
        )
    )
    return result, text, reply_markup


async def _ciclopi_button_legend(bot, update, user_record):
    result, text, reply_markup = '', '', None
    text = (
        "<b>{s[name]}</b> | <i>{s[description]}</i>\n"
        "<code>  </code>🚲 {s[bikes]}  |  🅿️ {s[free]}  | 📍 {s[distance]}"
    ).format(
        s={
            key: bot.get_message(
                'ciclopi', 'button', 'legend', key,
                update=update, user_record=user_record
            )
            for key in ('name', 'distance', 'description', 'bikes', 'free')
        }
    )
    reply_markup = make_inline_keyboard(
        get_menu_back_buttons(
            bot=bot, update=update, user_record=user_record,
            include_back_to_settings=True
        )
    )
    return result, text, reply_markup


async def _ciclopi_button_favourites_add(bot, update, user_record, arguments,
                                         order_record, ordered_stations):
    result = bot.get_message(
        'ciclopi', 'button', 'favourites', 'popup',
        update=update, user_record=user_record
    )
    if len(arguments) == 2 and arguments[1].isnumeric():
        station_id = int(arguments[1])
        chat_id = (
            update['message']['chat']['id'] if 'message' in update
            else update['chat']['id'] if 'chat' in update
            else 0
        )
        with bot.db as db:
            if station_id in (s.id for s in ordered_stations):  # Remove
                # Find `old_record` to be removed
                for old_record in order_record:
                    if old_record['station'] == station_id:
                        break
                db.query(
                    """UPDATE ciclopi_custom_order
                    SET value = value - 1
                    WHERE chat_id = {chat_id}
                        AND value > {val}
                    """.format(
                        chat_id=chat_id,
                        val=old_record['value']
                    )
                )
                db['ciclopi_custom_order'].delete(
                    id=old_record['id']
                )
                ordered_stations = list(
                    filter(
                        (lambda s: s.id != station_id),
                        ordered_stations
                    )
                )
            else:  # Add
                new_record = dict(
                    chat_id=chat_id,
                    station=station_id,
                    value=(len(order_record) + 1)
                )
                db['ciclopi_custom_order'].upsert(
                    new_record,
                    ['chat_id', 'station'],
                    ensure=True
                )
                order_record.append(new_record)
                ordered_stations.append(
                    Station(station_id)
                )
    text = bot.get_message(
        'ciclopi', 'button', 'favourites', 'header',
        update=update, user_record=user_record,
        options=line_drawing_unordered_list(
            [
                station.name
                for station in ordered_stations
            ]
        )
    )
    reply_markup = dict(
        inline_keyboard=make_lines_of_buttons(
            [
                make_button(
                    text=(
                        "{sy} {n}"
                    ).format(
                        sy=(
                            '✅' if station_id in [
                                s.id for s in ordered_stations
                            ]
                            else '☑️'
                        ),
                        n=station['name']
                    ),
                    prefix='ciclopi:///',
                    data=['fav', 'add', station_id]
                )
                for station_id, station in sorted(
                    Station.stations.items(),
                    key=lambda t: t[1]['name']  # Sort by station_name
                )
            ],
            3
        ) + make_lines_of_buttons(
            [
                make_button(
                    text=bot.get_message(
                        'ciclopi', 'button', 'favourites', 'sort', 'buttons',
                        'change_order',
                        update=update, user_record=user_record
                    ),
                    prefix="ciclopi:///",
                    data=["fav"]
                )
            ] + get_menu_back_buttons(
                bot=bot, update=update, user_record=user_record,
                include_back_to_settings=True
            ),
            3
        )
    )
    return result, text, reply_markup


def move_favorite_station(
        bot, chat_id, action, station_id,
        order_record
):
    """Move a station in `chat_id`-associated custom order.

    `bot`: Bot object, having a `.db` property.
    `action`: should be `up` or `down`
    `order_record`: list of records about `chat_id`-associated custom order.
    """
    assert action in ('up', 'down'), "Invalid action!"
    for old_record in order_record:
        if old_record['station'] == station_id:
            break
    else:  # Error: no record found
        return
    with bot.db as db:
        if action == 'down':
            db.query(
                """UPDATE ciclopi_custom_order
                SET value = 500
                WHERE chat_id = {chat_id}
                    AND value = {val} + 1
                """.format(
                    chat_id=chat_id,
                    val=old_record['value']
                )
            )
            db.query(
                """UPDATE ciclopi_custom_order
                SET value = value + 1
                WHERE chat_id = {chat_id}
                    AND value = {val}
                """.format(
                    chat_id=chat_id,
                    val=old_record['value']
                )
            )
            db.query(
                """UPDATE ciclopi_custom_order
                SET value = {val}
                WHERE chat_id = {chat_id}
                    AND value = 500
                """.format(
                    chat_id=chat_id,
                    val=old_record['value']
                )
            )
        elif action == 'up':
            db.query(
                """UPDATE ciclopi_custom_order
                SET value = 500
                WHERE chat_id = {chat_id}
                    AND value = {val} - 1
                """.format(
                    chat_id=chat_id,
                    val=old_record['value']
                )
            )
            db.query(
                """UPDATE ciclopi_custom_order
                SET value = value - 1
                WHERE chat_id = {chat_id}
                    AND value = {val}
                """.format(
                    chat_id=chat_id,
                    val=old_record['value']
                )
            )
            db.query(
                """UPDATE ciclopi_custom_order
                SET value = {val}
                WHERE chat_id = {chat_id}
                    AND value = 500
                """.format(
                    chat_id=chat_id,
                    val=old_record['value']
                )
            )
        order_record = list(
            db['ciclopi_custom_order'].find(
                chat_id=chat_id,
                order_by=['value']
            )
        )
        ordered_stations = [
            Station(record['station'])
            for record in order_record
        ]
    return order_record, ordered_stations


async def _ciclopi_button_favourites(bot, update, user_record, arguments):
    result, text, reply_markup = '', '', None
    action = (
        arguments[0] if len(arguments) > 0
        else 'up'
    )
    chat_id = (
        update['message']['chat']['id'] if 'message' in update
        else update['chat']['id'] if 'chat' in update
        else 0
    )
    with bot.db as db:
        order_record = list(
            db['ciclopi_custom_order'].find(
                chat_id=chat_id,
                order_by=['value']
            )
        )
        ordered_stations = [
            Station(record['station'])
            for record in order_record
        ]
    if action == 'add':
        return await _ciclopi_button_favourites_add(
            bot, update, user_record, arguments,
            order_record, ordered_stations
        )
    elif action == 'dummy':
        return bot.get_message(
            'ciclopi', 'button', 'favourites', 'sort', 'end',
            update=update, user_record=user_record
        ), '', None
    elif action == 'set' and len(arguments) > 1:
        action = arguments[1]
    elif (
            action in ['up', 'down']
            and len(arguments) > 1
            and arguments[1].isnumeric()
    ):
        station_id = int(arguments[1])
        order_record, ordered_stations = move_favorite_station(
            bot, chat_id, action, station_id,
            order_record
        )
    text = bot.get_message(
        'ciclopi', 'button', 'favourites', 'sort', 'header',
        update=update, user_record=user_record,
        options=line_drawing_unordered_list(
            [
                station.name
                for station in ordered_stations
            ]
        )
    )
    reply_markup = dict(
        inline_keyboard=[
                            [
                                make_button(
                                    text="{s.name} {sy}".format(
                                        sy=(
                                            '⬆️' if (
                                                    action == 'up'
                                                    and n != 1
                                            ) else '⬇️' if (
                                                    action == 'down'
                                                    and n != len(ordered_stations)
                                            ) else '⏹'
                                        ),
                                        s=station
                                    ),
                                    prefix='ciclopi:///',
                                    data=[
                                        'fav',
                                        (
                                            action if (
                                                              action == 'up'
                                                              and n != 1
                                                      ) or (
                                                              action == 'down'
                                                              and n != len(ordered_stations)
                                                      )
                                            else 'dummy'
                                        ),
                                        station.id
                                    ]
                                )
                            ]
                            for n, station in enumerate(ordered_stations, 1)
                        ] + [
                            [
                                make_button(
                                    text=bot.get_message(
                                        'ciclopi', 'button', 'favourites', 'sort', 'buttons',
                                        'edit',
                                        update=update, user_record=user_record
                                    ),
                                    prefix='ciclopi:///',
                                    data=['fav', 'add']
                                )
                            ]
                        ] + [
                            [
                                (
                                    make_button(
                                        text=bot.get_message(
                                            'ciclopi', 'button', 'favourites', 'sort',
                                            'buttons', 'move_down',
                                            update=update, user_record=user_record
                                        ),
                                        prefix='ciclopi:///',
                                        data=['fav', 'set', 'down']
                                    ) if action == 'up'
                                    else make_button(
                                        text=bot.get_message(
                                            'ciclopi', 'button', 'favourites', 'sort',
                                            'buttons', 'move_up',
                                            update=update, user_record=user_record
                                        ),
                                        prefix='ciclopi:///',
                                        data=['fav', 'set', 'up']
                                    )
                                )
                            ]
                        ] + [
                            get_menu_back_buttons(
                                bot=bot, update=update, user_record=user_record,
                                include_back_to_settings=True
                            )
                        ]
    )
    return result, text, reply_markup


async def _ciclopi_button_setpos(bot, update, user_record):
    result, text, reply_markup = '', '', None
    chat_id = (
        update['message']['chat']['id'] if 'message' in update
        else update['chat']['id'] if 'chat' in update
        else 0
    )
    result = bot.get_message(
        'ciclopi', 'button', 'location', 'popup',
        update=update, user_record=user_record
    )
    bot.set_individual_location_handler(
        await async_wrapper(
            set_ciclopi_location
        ),
        update
    )
    bot.set_individual_text_message_handler(
        cancel_ciclopi_location,
        update
    )
    asyncio.ensure_future(
        bot.send_message(
            chat_id=chat_id,
            text=bot.get_message(
                'ciclopi', 'button', 'location', 'instructions',
                update=update, user_record=user_record
            ),
            reply_markup=dict(
                keyboard=[
                    [
                        dict(
                            text=bot.get_message(
                                'ciclopi', 'button', 'location',
                                'send_current_location',
                                update=update, user_record=user_record
                            ),
                            request_location=True
                        )
                    ],
                    [
                        dict(
                            text=bot.get_message(
                                'ciclopi', 'button', 'location', 'cancel',
                                update=update, user_record=user_record
                            ),
                        )
                    ]
                ],
                resize_keyboard=True
            )
        )
    )
    return result, text, reply_markup


_ciclopi_button_routing_table = {
    'main': _ciclopi_button_main,
    'sort': _ciclopi_button_sort,
    'limit': _ciclopi_button_limit,
    'show': _ciclopi_button_show,
    'setpos': _ciclopi_button_setpos,
    'legend': _ciclopi_button_legend,
    'fav': _ciclopi_button_favourites
}


async def _ciclopi_button(bot, update, user_record):
    data = update['data']
    command, *arguments = extract(data, ':///').split('|')
    if command in _ciclopi_button_routing_table:
        result, text, reply_markup = await _ciclopi_button_routing_table[
            command
        ](
            bot, update, user_record, arguments
        )
    else:
        return
    if text:
        return dict(
            text=result,
            edit=dict(
                text=text,
                parse_mode='HTML',
                reply_markup=reply_markup
            )
        )
    return result


def init(telegram_bot, ciclopi_messages=None,
         _default_location=(43.718518, 10.402165)):
    """Take a bot and assign CicloPi-related commands to it.

    `ciclopi_messages` : dict
        Multilanguage dictionary with all CicloPi-related messages.

    `default_location` : tuple (float, float)
        Tuple of coordinates (latitude, longitude) of default location.
        Defaults to Borgo Stretto CicloPi station.
    """
    # Define a global `default_location` variable holding default location
    global default_location
    default_location = Location(_default_location)
    telegram_bot.ciclopi_default_location = default_location

    db = telegram_bot.db
    if 'ciclopi_stations' not in db.tables:
        db['ciclopi_stations'].insert_many(
            sorted(
                [
                    dict(
                        station_id=station_id,
                        name=station['name'],
                        latitude=station['coordinates'][0],
                        longitude=station['coordinates'][1]
                    )
                    for station_id, station in Station.stations.items()
                ],
                key=(lambda station: station['station_id'])
            )
        )
    if 'ciclopi' not in db.tables:
        db['ciclopi'].insert(
            dict(
                chat_id=0,
                sorting=0,
                latitude=0.0,
                longitude=0.0,
                stations_to_show=-1
            )
        )

    if ciclopi_messages is None:
        try:
            from .messages import default_ciclopi_messages as ciclopi_messages
        except ImportError:
            ciclopi_messages = {}
    telegram_bot.messages['ciclopi'] = ciclopi_messages

    @telegram_bot.command(command='/ciclopi', aliases=["CicloPi 🚲", "🚲 CicloPi 🔴"],
                          reply_keyboard_button=(
                                  telegram_bot.messages['ciclopi']['command']['reply_keyboard_button']
                          ),
                          show_in_keyboard=True,
                          description=(
                                  telegram_bot.messages['ciclopi']['command']['description']
                          ),
                          help_section=telegram_bot.messages['ciclopi']['help'],
                          authorization_level='everybody')
    async def ciclopi_command(bot, update, user_record):
        return await _ciclopi_command(bot, update, user_record)

    @telegram_bot.button(prefix='ciclopi:///', authorization_level='everybody')
    async def ciclopi_button(bot, update, user_record):
        return await _ciclopi_button(bot, update, user_record)
