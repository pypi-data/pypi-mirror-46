from datetime import datetime
from typing import Union, List

from marshmallow import Schema, fields


class Image(object):
    def __init__(self, cover_type: str = None, url: str = None):
        self.cover_type = cover_type
        self.url = url


class Ratings(object):
    def __init__(self, votes: int = None, value: float = None):
        self.votes = votes
        self.value = value


class DiskSpace(object):
    def __init__(
        self,
        path: str = None,
        label: str = None,
        free_space: int = None,
        total_space: int = None,
    ):
        self.path = path
        self.label = label
        self.free_space = free_space
        self.total_space = total_space


class RootFolder(object):
    def __init__(
        self,
        path: str = None,
        free_space: int = None,
        unmapped_folders: List = None,
        id: int = None,
    ):
        self.path = path
        self.free_space = free_space
        self.unmapped_folders = unmapped_folders
        self.id = id


class SystemStatus(object):
    def __init__(
        self,
        version: str = None,
        build_time: datetime = None,
        is_debug: bool = None,
        is_production: bool = None,
        is_admin: bool = None,
        is_user_interactive: bool = None,
        startup_path: str = None,
        app_data: str = None,
        os_version: str = None,
        is_mono: bool = None,
        is_linux: bool = None,
        is_windows: bool = None,
        branch: str = None,
        authentication: bool = None,
        start_of_week: int = None,
        url_base: str = None,
    ):
        self.version = version
        self.build_time = build_time
        self.is_debug = is_debug
        self.is_production = is_production
        self.is_admin = is_admin
        self.is_user_interactive = is_user_interactive
        self.startup_path = startup_path
        self.app_data = app_data
        self.os_version = os_version
        self.is_mono = is_mono
        self.is_linux = is_linux
        self.is_windows = is_windows
        self.branch = branch
        self.authentication = authentication
        self.start_of_week = start_of_week
        self.url_base = url_base


class SonarrDateTime(fields.Field):
    OBJ_TYPE = "sonarrdatetime"

    default_error_messages = {
        "invalid": "Not a valid {obj_type}.",
        "format": '"{input}" cannot be formatted as a {obj_type}.',
    }

    def _serialize(
        self, value: datetime, attr: str, obj: dict, **kwargs: dict
    ) -> Union[str, None]:
        if value is None:
            return None

        try:
            date_format = self.get_format(kwargs.get("millis", False))
            return value.strftime(date_format)
        except (TypeError, AttributeError, ValueError):
            self.fail("format", input=value, obj_type=self.OBJ_TYPE)

    def _deserialize(
        self, value: str, attr: str, data: dict, **kwargs: dict
    ) -> datetime:
        if not value:  # Falsy values, e.g. '', None, [] are not valid
            raise self.fail("invalid", input=value, obj_type=self.OBJ_TYPE)

        try:
            has_millis = "." in value
            date_format = self.get_format(has_millis)
            if has_millis:
                return datetime.strptime(value[:-2], date_format)
            else:
                return datetime.strptime(value, date_format)

        except (TypeError, AttributeError, ValueError) as e:
            print(e)
            raise self.fail("invalid", input=value, obj_type=self.OBJ_TYPE)

    @staticmethod
    def get_format(millis: bool = False):
        return "%Y-%m-%dT%H:%M:%S.%f" if millis else "%Y-%m-%dT%H:%M:%SZ"


class ImageSchema(Schema):
    class Meta:
        unknown = "EXCLUDE"
        allow_none = False

    cover_type = fields.Str(data_key="coverType")
    url = fields.Str()

    def load(self, data, many=None, partial=None, unknown=None) -> Image:
        obj = super(Schema, self).load(data, many, partial, unknown)
        return Image(**obj)


class RatingsSchema(Schema):
    class Meta:
        unknown = "EXCLUDE"
        allow_none = False

    votes = fields.Int()
    value = fields.Float()

    def load(self, data, many=None, partial=None, unknown=None) -> Ratings:
        obj = super(Schema, self).load(data, many, partial, unknown)
        return Ratings(**obj)


class DiskSpaceSchema(Schema):
    class Meta:
        unknown = "EXCLUDE"
        allow_none = False

    path = fields.Str()
    label = fields.Str()
    free_space = fields.Int(data_key="freeSpace")
    total_space = fields.Int(data_key="totalSpace")

    def load(self, data, many=None, partial=None, unknown=None) -> DiskSpace:
        obj = super(Schema, self).load(data, many, partial, unknown)

        return DiskSpace(**obj)


class RootFolderSchema(Schema):
    class Meta:
        unknown = "EXCLUDE"
        allow_none = False

    path = fields.Str()
    free_space = fields.Int(data_key="freeSpace")
    unmapped_folders = fields.List(fields.Str(), data_key="unmappedFolders")
    id = fields.Int()

    def load(self, data, many=None, partial=None, unknown=None) -> RootFolder:
        obj = super(Schema, self).load(data, many, partial, unknown)

        return RootFolder(**obj)


class SystemStatusSchema(Schema):
    class Meta:
        unknown = "EXCLUDE"
        allow_none = False

    version = fields.Str()
    build_time = SonarrDateTime(data_key="buildTime")
    is_debug = fields.Bool(data_key="isDebug")
    is_production = fields.Bool(data_key="isProduction")
    is_admin = fields.Bool(data_key="isAdmin")
    is_user_interactive = fields.Bool(data_key="isUserInteractive")
    startup_path = fields.Str(data_key="startupPath")
    app_data = fields.Str(data_key="appData")
    os_version = fields.Str(data_key="osVersion")
    is_mono = fields.Bool(data_key="isMono")
    is_linux = fields.Bool(data_key="isLinux")
    is_windows = fields.Bool(data_key="isWindows")
    branch = fields.Str()
    authentication = fields.Bool()
    start_of_week = fields.Int(data_key="startOfWeek")
    url_base = fields.Str(data_key="urlBase")

    def load(self, data, many=None, partial=None, unknown=None) -> SystemStatus:
        obj = super(Schema, self).load(data, many, partial, unknown)

        return SystemStatus(**obj)
