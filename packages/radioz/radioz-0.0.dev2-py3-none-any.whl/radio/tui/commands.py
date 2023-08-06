from numbers import Number

from prompt_toolkit.contrib.regular_languages import compile
from prompt_toolkit.document import Document
from prompt_toolkit.application.current import get_app

from radio.core.log import logger

from radio.core.classes import radios
from radio.core.classes import radio_browser
from radio.core.classes import Station
from radio.core.player import Stop

from radio.tui.buffers import list_buffer
from radio.tui.buffers import display_buffer

from radio.handlers.exchange import display_now
from radio.handlers.exchange import play_now

COMMAND_GRAMMAR = compile(
    r"""(
        (?P<command>[^\s]+) \s+ (?P<subcommand>[^\s]+)  \s+  (?P<term>[^\s]+) |
        (?P<command>[^\s]+) \s+ (?P<term>[^\s]+) |
        (?P<command>[^\s!]+)
    )"""
)

COMMAND_TO_HANDLER = {}


def has_command_handler(command):
    return command in COMMAND_TO_HANDLER


def call_command_handler(command, **kwargs):
    COMMAND_TO_HANDLER[command](**kwargs)


def get_commands():
    return COMMAND_TO_HANDLER.keys()


def get_command_help(command):
    return COMMAND_TO_HANDLER[command].__doc__


def handle_command(event, **kwargs):
    # logger.info(event.current_buffer.name)
    # logger.info(event.current_buffer.text)

    def is_help(text):
        if not text:
            return
        test = text.split("|")[0]
        test = test.replace(" ", "")
        return not test.isnumeric()

    if is_help(kwargs.get("text")):
        return  # TODO handle_help()

    # lida com o evento do command_prompt (buffer)
    if event.current_buffer.name == "command_buffer":

        # !!!!! lida com o evento do command_prompt (buffer)
        input_string = event.current_buffer.text

        match = COMMAND_GRAMMAR.match(input_string)

        if match is None:
            return

        # pós processo grammar
        variables = match.variables()

        command = variables.get("command")

        kwargs.update({"variables": variables, "event": event})
        if has_command_handler(command):
            call_command_handler(command, **kwargs)

    # lida com o evento da list_view !!!! (não é buffer)
    if event.current_buffer.name == "list_buffer":
        call_command_handler("play", **kwargs)


def cmd(name):
    """
    Decorator to register commands in this namespace
    """

    def decorator(func):
        COMMAND_TO_HANDLER[name] = func

    return decorator


@cmd("exit")
def exit(**kwargs):
    """ exit Ctrl + Q"""
    get_app().exit()


@cmd("play")
def play(**kwargs):
    def get_playable_station():
        # TODO
        pass

    index = kwargs.get("index", None)
    # toca a partir da list_view
    if isinstance(index, Number):
        obj = radios.get_obj(kwargs.get("index"))
    else:
        # toca a partir do command prompt
        variables = kwargs.get("variables")
        command = "{}_{}".format("stations", variables.get("subcommand"))
        term = variables.get("term")
        data = getattr(radio_browser, command)(term)
        obj = Station(**data[0])

    play_now.put(obj)
    display_now.put(obj.show_info())
    logger.info("playing...")


@cmd("stop")
def stop(**kwargs):
    """ exit Ctrl + S"""
    # TODO: implementar tecla de atalho para executar o comando stop
    play_now.put(Stop())


@cmd("bytag")
def bytag(**kwargs):
    variables = kwargs.get("variables")
    term = variables.get("term")
    radios.data = radio_browser.stations_bytag(term)
    list_buffer.reset(Document(radios.content, 0))


@cmd("stations")
def stations(**kwargs):
    variables = kwargs.get("variables")
    command = "{}_{}".format(variables.get("command"), variables.get("subcommand"))
    term = variables.get("term")
    radios.data = getattr(radio_browser, command)(term)
    list_buffer.reset(Document(radios.content, 0))


@cmd("list")
def stations(**kwargs):
    variables = kwargs.get("variables")
    command = "{}_{}".format(variables.get("command"), variables.get("subcommand"))
    term = variables.get("term")
    command = "stations_" + command.split("_")[1]  # stations_bytag -> list_bytag
    radios.data = getattr(radio_browser, command)(term)
    list_buffer.reset(Document(radios.content, 0))


@cmd("rec")
def stations(**kwrags):
    """records a radio station in the background"""
    # TODO:
    logger.info(kwrags)


@cmd("info")
def info(**kwargs):
    """ show info about station """
    pass


@cmd("help")
def help(**kwargs):
    """ show help """
    # https://stackoverflow.com/questions/21503865/how-to-denote-that-a-command-line-argument-is-optional-when-printing-usage
    commands = """Command List\n
play byid <id>\n
stop\n
rec byid <id>

list bycodec <codec>
list bycodecexact <codecexact>
list bycountry <country>
list bycountryexact <countryexact>
list byid <id>
list bylanguage <language>
list bylanguageexact <languageexact>
list byname <name>
list bynameexact <nameexact>
list bystate <state>
list bystateexact <stateexact>
list bytag <tag>
list bytagexact <tag>
list byuuid <uuid>
list tags\n

exit

Press `Ctrl + UP` or `Ctrl + Down` to move the focus; Press `Ctrl + Q` to quit.\n
"""
    list_buffer.reset(Document(commands), 0)
    list_buffer._set_cursor_position(0)
