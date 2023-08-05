from datetime import datetime
from typing import List

from marshmallow import Schema, fields

from nzbclients.nzbdrone.common import Image, ImageSchema, Ratings, RatingsSchema

{
    "sourceType": "tmdb",
    "movieId": 1,
    "title": "Legally Blonde 1",
    "sourceId": 8835,
    "votes": 0,
    "voteCount": 0,
    "language": "english",
    "id": 1,
},


class AlternateTitle(object):
    def __init__(
        self,
        source_type: str = None,
        movie_id: int = None,
        title: str = None,
        source_id: int = None,
        votes: int = None,
        vote_count: int = None,
        language: str = None,
        id: int = None,
    ):
        self.source_type = source_type
        self.movie_id = movie_id
        self.title = title
        self.source_id = source_id
        self.votes = votes
        self.vote_count = vote_count
        self.language = language
        self.id = id


class Movie(object):
    def __init__(
        self,
        title: str = None,
        sort_title: str = None,
        size_on_disk: int = None,
        status: str = None,
        overview: str = None,
        in_cinemas: datetime = None,
        images: List[Image] = None,
        website: str = None,
        downloaded: bool = None,
        year: int = None,
        has_file: bool = None,
        you_tube_trailer_id: str = None,
        studio: str = None,
        path: str = None,
        profile_id: int = None,
        monitored: bool = None,
        minimum_availability: str = None,
        runtime: int = None,
        last_info_sync: datetime = None,
        clean_title: str = None,
        imdb_id: str = None,
        tmdb_id: int = None,
        title_slug: str = None,
        genres: List[str] = None,
        tags: List[str] = None,
        added: datetime = None,
        ratings: Ratings = None,
        alternative_titles: List[AlternateTitle] = None,
        quality_profile_id: int = None,
        id: int = None,
    ):
        self.title: str = title
        self.sort_title: str = sort_title
        self.size_on_disk: int = size_on_disk
        self.status: str = status
        self.overview: str = overview
        self.in_cinemas: datetime = in_cinemas
        self.images: List[Image] = images
        self.website: str = website
        self.downloaded: bool = downloaded
        self.year: int = year
        self.has_file: bool = has_file
        self.you_tube_trailer_id: str = you_tube_trailer_id
        self.studio: str = studio
        self.path: str = path
        self.profile_id: int = profile_id
        self.monitored: bool = monitored
        self.minimum_availability: str = minimum_availability
        self.runtime: int = runtime
        self.last_info_sync: datetime = last_info_sync
        self.clean_title: str = clean_title
        self.imdb_id: str = imdb_id
        self.tmdb_id: int = tmdb_id
        self.title_slug: str = title_slug
        self.genres: List[str] = genres
        self.tags: List[str] = tags
        self.added: datetime = added
        self.ratings: Ratings = ratings
        self.alternative_titles: List[AlternateTitle] = alternative_titles
        self.quality_profile_id: int = quality_profile_id
        self.id: int = id


class AlternateTitleSchema(Schema):
    class Meta:
        unknown = "EXCLUDE"
        allow_none = False

    source_type = fields.Str(data_key="sourceType")
    movie_id = fields.Int(data_key="movieId")
    title = fields.Str()
    source_id = fields.Int(data_key="sourceId")
    votes = fields.Int()
    vote_count = fields.Int(data_key="voteCount")
    language = fields.Str()
    id = fields.Int()

    def load(self, data, many=None, partial=None, unknown=None) -> AlternateTitle:
        obj = super(Schema, self).load(data, many, partial, unknown)

        return AlternateTitle(**obj)


class MovieSchema(Schema):
    class Meta:
        unknown = "EXCLUDE"
        allow_none = False

    title = fields.Str()
    sort_title = fields.Str(data_key="sortTitle")
    size_on_disk = fields.Int(data_key="sizeOnDisk")
    status = fields.Str()
    overview = fields.Str()
    in_cinemas = fields.DateTime()
    images = fields.List(fields.Nested(ImageSchema))
    website = fields.Str()
    downloaded = fields.Bool()
    year = fields.Int()
    has_file = fields.Bool(data_key="hasFile")
    you_tube_trailer_id = fields.Str("youTubeTrailerId")
    studio = fields.Str()
    path = fields.Str()
    profile_id = fields.Int(data_key="profileId")
    monitored = fields.Bool()
    minimum_availability = fields.Str(data_key="minimumAvailability")
    runtime = fields.Int()
    last_info_sync = fields.DateTime(data_key="lastInfoSync")
    clean_title = fields.Str(data_key="cleanTitle")
    imdb_id = fields.Str(data_key="imdbId")
    tmdb_id = fields.Int(data_key="tmdbId")
    title_slug = fields.Str(data_key="titleSlug")
    genres = fields.List(fields.Str())
    tags = fields.List(fields.Str())
    added = fields.DateTime()
    ratings = fields.Nested(RatingsSchema)
    alternative_titles = fields.List(
        fields.Nested(AlternateTitleSchema()), data_key="alternativeTitles"
    )
    quality_profile_id = fields.Int(data_key="qualityProfileId")
    id = fields.Int()

    def load(self, data, many=None, partial=None, unknown=None) -> Movie:
        obj = super(Schema, self).load(data, many, partial, unknown)
        return Movie(**obj)
