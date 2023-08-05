from datetime import datetime
from typing import List

from marshmallow import Schema, fields

from nzbclients.nzbdrone.common import (
    Image,
    ImageSchema,
    Ratings,
    RatingsSchema,
    SonarrDateTime,
)


class AlternateTitle(object):
    def __init__(self, title: str = None, season_number: int = None):
        self.title = title
        self.season_number = season_number


class Statistics(object):
    def __init__(
        self,
        previous_airing: datetime = None,
        episode_file_count: int = None,
        episode_count: int = None,
        total_episode_count: int = None,
        size_on_disk: int = None,
        percent_of_episodes: int = None,
    ):
        self.previous_airing = previous_airing
        self.episode_file_count = episode_file_count
        self.episode_count = episode_count
        self.total_episode_count = total_episode_count
        self.size_on_disk = size_on_disk
        self.percent_of_episodes = percent_of_episodes


class Season(object):
    def __init__(
        self,
        season_number: int = None,
        monitored: bool = None,
        statistics: Statistics = None,
    ):
        self.season_number = season_number
        self.monitored = monitored
        self.statistics = statistics


class Series(object):
    def __init__(
        self,
        id: int = None,
        title: str = None,
        title_slug: str = None,
        alternate_titles: List[AlternateTitle] = None,
        quality_profile_id: int = None,
        sort_title: str = None,
        season_count: int = None,
        total_episode_count: int = None,
        episode_count: int = None,
        episode_file_count: int = None,
        size_on_disk: int = None,
        status: str = None,
        overview: str = None,
        previous_airing: datetime = None,
        network: str = None,
        air_time: str = None,
        images: List[Image] = None,
        seasons: List[Season] = None,
        year: int = None,
        path: str = None,
        profile_id: int = None,
        season_folder: bool = None,
        monitored: bool = None,
        use_scene_numbering: bool = None,
        runtime: int = None,
        tvdb_id: int = None,
        tv_rage_id: int = None,
        tv_maze_id: int = None,
        first_aired: datetime = None,
        last_info_sync: datetime = None,
        series_type: str = None,
        clean_title: str = None,
        imdb_id: str = None,
        certification: str = None,
        genres: List[str] = None,
        tags: List[str] = None,
        added: datetime = None,
        ratings: Ratings = None,
    ):
        self.id = id
        self.title = title
        self.title_slug = title_slug
        self.alternate_titles = alternate_titles
        self.quality_profile_id = quality_profile_id
        self.sort_title = sort_title
        self.season_count = season_count
        self.total_episode_count = total_episode_count
        self.episode_count = episode_count
        self.episode_file_count = episode_file_count
        self.size_on_disk = size_on_disk
        self.status = status
        self.overview = overview
        self.previous_airing = previous_airing
        self.network = network
        self.air_time = air_time
        self.images = images
        self.seasons = seasons
        self.year = year
        self.path = path
        self.profile_id = profile_id
        self.season_folder = season_folder
        self.monitored = monitored
        self.use_scene_numbering = use_scene_numbering
        self.runtime = runtime
        self.tvdb_id = tvdb_id
        self.tv_rage_id = tv_rage_id
        self.tv_maze_id = tv_maze_id
        self.first_aired = first_aired
        self.last_info_sync = last_info_sync
        self.series_type = series_type
        self.clean_title = clean_title
        self.imdb_id = imdb_id
        self.certification = certification
        self.genres = genres
        self.tags = tags
        self.added = added
        self.ratings = ratings


class AlternateTitleSchema(Schema):
    class Meta:
        unknown = "EXCLUDE"
        allow_none = False

    title = fields.Str()
    season_number = fields.Int(data_key="seasonNumber")

    def load(self, data, many=None, partial=None, unknown=None) -> AlternateTitle:
        obj = super(Schema, self).load(data, many, partial, unknown)

        return AlternateTitle(**obj)


class StatisticsSchema(Schema):
    class Meta:
        unknown = "EXCLUDE"
        allow_none = False

    previous_airing = SonarrDateTime(data_key="previousAiring")
    episode_file_count = fields.Int(data_key="episodeFileCount")
    episode_count = fields.Int(data_key="episodeCount")
    total_episode_count = fields.Int(data_key="totalEpisodeCount")
    size_on_disk = fields.Int(data_key="sizeOnDisk")
    percent_of_episodes = fields.Int(data_key="percentOfEpisodes")

    def load(self, data, many=None, partial=None, unknown=None) -> Statistics:
        obj = super(Schema, self).load(data, many, partial, unknown)
        return Statistics(**obj)


class SeasonSchema(Schema):
    class Meta:
        unknown = "EXCLUDE"
        allow_none = False

    season_number = fields.Int(data_key="seasonNumber")
    monitored = fields.Bool()
    statistics = fields.Nested(StatisticsSchema)

    def load(self, data, many=None, partial=None, unknown=None) -> Season:
        obj = super(Schema, self).load(data, many, partial, unknown)
        return Season(**obj)


class SeriesSchema(Schema):
    class Meta:
        unknown = "EXCLUDE"
        allow_none = False

    id = fields.Int()
    title = fields.Str(required=True)
    title_slug = fields.Str(data_key="titleSlug", required=True)
    alternate_titles = fields.List(
        fields.Nested(AlternateTitleSchema, data_key="alternateTitles")
    )
    quality_profile_id = fields.Int(data_key="qualityProfileId", required=True)
    sort_title = fields.Str(data_key="sortTitle")
    season_count = fields.Int(data_key="seasonCount")
    total_episode_count = fields.Int(data_key="totalEpisodeCount")
    episode_count = fields.Int(data_key="episodeCount")
    episode_file_count = fields.Int(data_key="episodeFileCount")
    size_on_disk = fields.Int(data_key="sizeOnDisk")
    status = fields.Str()
    overview = fields.Str()
    previous_airing = SonarrDateTime(data_key="previousAiring")
    network = fields.Str()
    air_time = fields.Str(data_key="airTime")
    images = fields.List(fields.Nested(ImageSchema, required=True, default=[]))
    seasons = fields.List(fields.Nested(SeasonSchema, required=True, default=[]))
    year = fields.Int()
    path = fields.Str(required=True)
    profile_id = fields.Int(data_key="profileId")
    season_folder = fields.Bool(data_key="seasonFolder")
    monitored = fields.Bool()
    use_scene_numbering = fields.Bool(data_key="useSceneNumbering")
    runtime = fields.Int()
    tvdb_id = fields.Int(data_key="tvdbId", required=True)
    tv_rage_id = fields.Int(data_key="tvRageId")
    tv_maze_id = fields.Int(data_key="tvMazeId")
    first_aired = SonarrDateTime(data_key="firstAired")
    last_info_sync = SonarrDateTime(data_key="lastInfoSync")
    series_type = fields.Str(data_key="seriesType")
    clean_title = fields.Str(data_key="cleanTitle")
    imdb_id = fields.Str(data_key="imdbId")
    certification = fields.Str()
    genres = fields.List(fields.Str())
    tags = fields.List(fields.Str())
    added = SonarrDateTime()
    ratings = fields.Nested(RatingsSchema)

    def load(self, data, many=None, partial=None, unknown=None) -> Series:
        obj = super(Schema, self).load(data, many, partial, unknown)
        return Series(**obj)
