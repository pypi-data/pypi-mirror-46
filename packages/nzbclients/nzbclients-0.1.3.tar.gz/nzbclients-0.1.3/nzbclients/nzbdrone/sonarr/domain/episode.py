from datetime import date, datetime

from marshmallow import Schema, fields

from nzbclients.nzbdrone.common import SonarrDateTime


class Episode(object):
    def __init__(
        self,
        series_id: int = None,
        episode_file_id: int = None,
        season_number: int = None,
        episode_number: int = None,
        title: str = None,
        air_date: date = None,
        air_date_utc: datetime = None,
        overview: str = None,
        has_file: bool = None,
        monitored: bool = None,
        scene_episode_number: int = None,
        scene_season_number: int = None,
        tv_db_episode_id: int = None,
        absolute_episode_number: int = None,
        downloading: bool = None,
        id: int = None,
    ):
        self.series_id: int = series_id
        self.episode_file_id: int = episode_file_id
        self.season_number: int = season_number
        self.episode_number: int = episode_number
        self.title: str = title
        self.air_date: date = air_date
        self.air_date_utc: datetime = air_date_utc
        self.overview: str = overview
        self.has_file: bool = has_file
        self.monitored: bool = monitored
        self.scene_episode_number: int = scene_episode_number
        self.scene_season_number: int = scene_season_number
        self.tv_db_episode_id: int = tv_db_episode_id
        self.absolute_episode_number: int = absolute_episode_number
        self.downloading: bool = downloading
        self.id: int = id


class EpisodeSchema(Schema):
    class Meta:
        unknown = "EXCLUDE"
        allow_none = False

    series_id = fields.Int(data_key="seriesId")
    episode_file_id = fields.Int(data_key="episodeFileId")
    season_number = fields.Int(data_key="seasonNumber")
    episode_number = fields.Int(data_key="episodeNumber")
    title = fields.Str()
    air_date = fields.Date(data_key="airDate")
    air_date_utc = SonarrDateTime(data_key="airDateUtc")
    overview = fields.Str()
    has_file = fields.Bool(data_key="hasFile")
    monitored = fields.Bool()
    scene_episode_number = fields.Int(data_key="sceneEpisodeNumber")
    scene_season_number = fields.Int(data_key="sceneSeasonNumber")
    tv_db_episode_id = fields.Int(data_key="tvDbEpisodeId")
    absolute_episode_number = fields.Int(data_key="absoluteEpisodeNumber")
    downloading = fields.Bool()
    id = fields.Int()

    def load(self, data, many=None, partial=None, unknown=None) -> Episode:
        obj = super(Schema, self).load(data, many, partial, unknown)
        return Episode(**obj)
