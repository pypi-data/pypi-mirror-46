
from marshmallow import Schema as MMSchema, ValidationError
from marshmallow import pre_dump, post_dump, pre_load, post_load, validates_schema
from marshmallow import fields, validate
from marshmallow import EXCLUDE as MM_EXCLUDE


_settings_schemas = []


class ColonSeparatedStringsField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ''

        return ':'.join(value)

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None

        return value.split(':')


class SettingsSchema(MMSchema):
    class Meta:
        unknown = MM_EXCLUDE


class CommonSchema(SettingsSchema):
    DEBUG = fields.Boolean()
    LISTEN = fields.String()
    PORT = fields.Integer()
    MAX_REQUEST_BODY_SIZE = fields.Integer()
    API_DOCS_PATH = fields.String()
    SECRET_KEY = fields.String()


# authentication

class ModelAuthenticationSchema(SettingsSchema):
    AUTHENTICATION_MODEL = fields.String()
    AUTHENTICATION_IDENTITY_FIELD = fields.String()
    AUTHENTICATION_SECRET_FIELD = fields.String()


class CookieAuthenticationSchema(SettingsSchema):
    AUTHENTICATION_COOKIE_NAME = fields.String()
    AUTHENTICATION_COOKIE_DOMAIN = fields.String()
    AUTHENTICATION_VALIDITY_SECONDS = fields.Number()


class JWTAuthenticationSchema(ModelAuthenticationSchema, CookieAuthenticationSchema):
    AUTHENTICATION_IDENTITY_CLAIM = fields.String()


class AllAuthenticationSchema(JWTAuthenticationSchema):
    AUTHENTICATION_BACKEND = fields.String()


# authorization

class RoleAuthorizationSchema(SettingsSchema):
    AUTHORIZATION_ROLE_FIELD = fields.String()


class ModelAuthorizationSchema(SettingsSchema):
    AUTHORIZATION_MODEL = fields.String()
    AUTHORIZATION_ACCOUNT_FIELD = fields.String()


class RightsAuthorizationSchema(ModelAuthorizationSchema):
    AUTHORIZATION_RESOURCE_FIELD = fields.String()
    AUTHORIZATION_OPERATIONS_FIELD = fields.String()


class AllAuthorizationSchema(RoleAuthorizationSchema,
                             RightsAuthorizationSchema):

    AUTHORIZATION_BACKEND = fields.String()


# cache

class LocMemCacheSchema(SettingsSchema):
    CACHE_MAX_ENTRIES = fields.Integer()


class RedisCacheSchema(SettingsSchema):
    CACHE_HOST = fields.String()
    CACHE_PORT = fields.Integer()
    CACHE_DB = fields.Integer()
    CACHE_PASSWORD = fields.String()


class AllCacheSchema(LocMemCacheSchema,
                     RedisCacheSchema):

    CACHE_BACKEND = fields.String()


# database

class SQLiteDatabaseSchema(SettingsSchema):
    DATABASE_NAME = fields.String()


class ServerDatabaseSchema(SettingsSchema):
    DATABASE_NAME = fields.String()
    DATABASE_HOST = fields.String()
    DATABASE_PORT = fields.Integer()
    DATABASE_USERNAME = fields.String()
    DATABASE_PASSWORD = fields.String()


class MySQLDatabaseSchema(ServerDatabaseSchema):
    pass


class PostgreSQLDatabaseSchema(ServerDatabaseSchema):
    pass


class AllDatabaseSchema(SQLiteDatabaseSchema,
                        MySQLDatabaseSchema,
                        PostgreSQLDatabaseSchema):

    DATABASE_BACKEND = fields.String()


# template

class Jinja2TemplateSchema(SettingsSchema):
    pass


class All2TemplateSchema(Jinja2TemplateSchema):
    TEMPLATE_BACKEND = fields.String()
    TEMPLATE_PATHS = ColonSeparatedStringsField()


# task queue

class RQTaskQueueSchema(SettingsSchema):
    TASK_QUEUE_HOST = fields.String()
    TASK_QUEUE_PORT = fields.Integer()
    TASK_QUEUE_DB = fields.Integer()
    TASK_QUEUE_PASSWORD = fields.String()
    TASK_QUEUE_POLL_RESULTS_INTERVAL = fields.Integer()


class AllTaskQueueSchema(RQTaskQueueSchema):
    TASK_QUEUE_BACKEND = fields.String()


# email

class SMTPEmailSchema(SettingsSchema):
    EMAIL_HOST = fields.String()
    EMAIL_PORT = fields.Integer()
    EMAIL_USERNAME = fields.String()
    EMAIL_PASSWORD = fields.String()
    EMAIL_USE_TLS = fields.Boolean()
    EMAIL_TIMEOUT = fields.Integer()


class AllEmailSchema(SMTPEmailSchema):
    EMAIL_BACKEND = fields.String()


def register_settings_schema(schema):
    _settings_schemas.append(schema)


def get_all_settings_schema():
    return type('AllSettingsSchema', tuple(_settings_schemas), {})


# put together known schemas

register_settings_schema(CommonSchema)
register_settings_schema(AllAuthenticationSchema)
register_settings_schema(AllAuthorizationSchema)
register_settings_schema(AllCacheSchema)
register_settings_schema(AllDatabaseSchema)
register_settings_schema(All2TemplateSchema)
register_settings_schema(AllTaskQueueSchema)
register_settings_schema(AllEmailSchema)
