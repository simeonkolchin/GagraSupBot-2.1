from enum import Enum

Token = '5332316874:AAE3PVTa8jOTMazPv0EuK2HssqvVDKzEYqI'
admins = [993699116, 490371324]

db_file = "database.vdb"

class States(Enum):
    S_START = '0'
    SendClaim = '1'
    WFMesT = '2'
    NewEventName = '3'
    NewEventText = '4'
    NewEventPrice = '5'

    EditNameEvent = '6'
    EditTextEvent = '7'
    EditPriceEvent = '8'

    SendMChatPhoto_1 = '9'
    SendMChatPhoto_2 = '10'

    SendMChatVideo_1 = '17'
    SendMChatVideo_2 = '18'

    SendMChatNoPhoto = '11'

    NewSaleName = '12'
    NewSaleText = '13'
    NewSaleTextNames = '14'
    NewSalePercent = '15'
    NewSaleDateDelta = '16'
