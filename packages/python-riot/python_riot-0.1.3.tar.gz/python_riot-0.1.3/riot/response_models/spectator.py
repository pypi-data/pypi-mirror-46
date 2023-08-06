from marshmallow import Schema, fields

from . import RiotSchema


class BannedChampion(RiotSchema):
    pickTurn = fields.Integer()
    championId = fields.Integer()
    teamId = fields.Integer()


class Observer(RiotSchema):
    encryptionKey = fields.String()


class GameCustomizationObject(RiotSchema):
    category = fields.String()
    content = fields.String()


class Perks(RiotSchema):
    perkStyle = fields.Integer()
    perkIds = fields.List(fields.Integer())
    perkSubStyle = fields.Integer()


class CurrentGameParticipant(RiotSchema):
    profileIconId = fields.Integer()
    championId = fields.Integer()
    summonerName = fields.String()
    gameCustomizationObjects = fields.Nested(GameCustomizationObject, many=True)
    bot = fields.Boolean()
    perks = fields.Nested(Perks, many=False)
    spell2Id = fields.Integer()
    teamId = fields.Integer()
    spell1Id = fields.Integer()
    summonerId = fields.String()


class ActiveGameBySummoner(RiotSchema):
    gameId = fields.Integer()
    gameStartTime = fields.Integer()
    platformId = fields.String()
    gameMode = fields.String()
    mapId = fields.Integer()
    gameType = fields.String()
    bannedChampions = fields.Nested(BannedChampion, many=True)
    observers = fields.Nested(Observer, many=False)
    participants = fields.Nested(CurrentGameParticipant, many=True)

