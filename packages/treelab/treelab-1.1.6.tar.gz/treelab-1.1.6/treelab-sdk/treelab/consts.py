from enum import Enum
from typing import TypeVar


class GRPCConfig:
    ip = "127.0.0.1:3001"
    TOKEN = "budTest"


class GenericType:
    T = TypeVar('T')
    PT = TypeVar('PT')
    O = TypeVar('O')


class FieldType(Enum):
    TEXT = 'TEXT'
    FOREIGN_KEY = 'FOREIGN_KEY'
    Number = 'Number'
    RECODE_REFERENCE = 'Record Reference'
    SINGLE_SELECT = 'Single Select'
    MULTI_SELECT = 'Multi-Select'


class ViewType(Enum):
    GRID = 'GRID'


class TableField(Enum):
    tableData = 'tableData'
    viewDatas = 'viewDatas'
    rows = 'rows'
    id = 'id'
    cells = 'cells'
    columnId = 'columnId'
    value = 'value'
    cell_type = 'type'
    text = 'text'


class Source(Enum):
    EXTERNAL_API = 'EXTERNAL_API'
    USER = 'USER'


class Color(Enum):
    lightRed = 'lightRed'
    blue = 'blue',
    red = 'red'
    gray = 'gray'
    magenta = 'magenta'
    yellow = 'yellow'
    orange = 'orange'
    green = 'green'
    black = 'black'
    pink = 'pink'
    purple = 'purple'
    lightBlue = 'lightBlue'
    lightGray = 'lightGray'
    lightMagenta = 'lightMagenta'
    lightYellow = 'lightYellow'
    lightOrange = 'lightOrange'
    lightGreen = 'lightGreen'
    lightBlack = 'lightBlack'
    lightPink = 'lightPink'
    lightPurple = 'lightPurple'


class Icon(Enum):
    briefcase = 'briefcase'
    untitle = 'untitle'
    asterisk = 'asterisk'
    barChart = 'barChart'
    check = 'check'
    circleBlank = 'circleBlank'
    cloud = 'cloud'
    barcode = 'barcode'
    beaker = 'beaker'
    bell = 'bell'
    bolt = 'bolt'
    book = 'book'
    bug = 'bug'
    building = 'building'
    bullhorn = 'bullhorn'
    calculator = 'calculator'
    calendar = 'calendar'
    camera = 'camera'
    sun = 'sun'
    flow = 'flow'
    coffee = 'coffee'
    handUp = 'handUp'
    anchor = 'anchor'
    cogs = 'cogs'
    comment = 'comment'
    compass = 'compass'
    creditCard = 'creditCard'
    dashboard = 'dashboard'
    edit = 'edit'
    food = 'food'
