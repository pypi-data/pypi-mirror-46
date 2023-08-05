import os

VALID_SECTIONS = ['default', 'development', 'test', 'homolog', 'staging', 'production']


class SettingsMeta(type):

    def __new__(meta, name, bases, attrs):

        if name == 'DefaultSettings':
            return super().__new__(meta, name, bases, attrs)

        _declared_options = {}

        base_options = meta.fetch_base_options(bases)

        # subclass declared options
        _explicit_options = {key: value for key, value in attrs.items() if key.isupper()}

        _declared_options.update(base_options)

        _declared_options.update(_explicit_options)

        API_ENV = _declared_options.get('API_ENV')

        base_dir = attrs.get('BASE_DIR')

        if not base_dir:
            raise Warning('Please put this line: "{}" into your setting class: "{}"'.format(
                'BASE_DIR = os.path.dirname(os.path.abspath(__file__))', name))

        #  Subclass config files  has higher priority
        config_files = list(map(lambda x: os.path.sep.join([base_dir, x]), attrs.get('_config_files', [])))

        print(name, config_files, '\n\n')
        # configuration options from configuration files
        file_options = meta.load_config_from_files(API_ENV, config_files)

        # build current class's all declared configuration options including all superclass
        # base_options.update(attrs)

        # override class's declared options with file configuration with validation also
        for key, value in file_options.items():
            print('file options:', key, value, '\n')
            setting_key = key.upper()
            if setting_key not in _declared_options:
                raise Exception('Configuration field {} should be declared in {} class'.format(setting_key, name))

            if value.startswith('$'):
                value = os.environ.get(value[1:], None)

            if value is not None:
                if value.isnumeric():
                    value = int(value)
                else:
                    try:
                        value = float(value)
                    except ValueError:
                        pass

            _explicit_options[setting_key] = value

        _declared_options.update(_explicit_options)

        # If subclass overload superclass's attribute, update super class
        for key, value in _declared_options.items():
            if not key.isupper():
                continue
            for base in bases:
                setattr(base, key, value)

        print(name, _declared_options, '\n\n')
        attrs.update(_declared_options)

        return super(SettingsMeta, meta).__new__(meta, name, bases, attrs)

    @classmethod
    def is_overload(cls, setting: str = None, base_settings: dict = None):
        return setting in base_settings

    @classmethod
    def fetch_base_options(cls, bases):
        base_config_attributes = {}
        for base in bases:
            base_config_attributes.update({key: value for key, value in base.__dict__.items() if key.isupper()})
        return base_config_attributes

    @classmethod
    def load_config_from_files(cls, env_name, files):
        from configparser import ConfigParser
        global_config = {}
        config = ConfigParser()
        for filename in files:
            if not os.path.exists(filename):
                raise Warning('Can not found config file: "{}"'.format(filename))
            config.read(filename)
            for section in config.sections():
                if section not in VALID_SECTIONS:
                    raise Exception('Invalid section {} in  {}'.format(section, filename))

            default_section = dict(config.items('default')) if config.has_section('default') else {}
            env_name_section = dict(config.items(env_name)) if config.has_section(env_name) else {}
            global_config.update(default_section)
            global_config.update(env_name_section)
        return global_config


class DefaultSettings(metaclass=SettingsMeta):
    """
    Default project global scope
    """
    _config_files = []

    API_ENV = os.environ.get('API_ENV', 'development')
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # API return data related configuration
    API_DEFAULT_LIMIT = 20
    API_MAXIMUM_LIMIT = 100

    DEBUG = True

    ############################################################
    # Mongo Database configuration template
    ############################################################
    MONGODB_URI = None
    DB_NAME = 'default_db'
    COLLECTION_NAME = 'default'

    @classmethod
    def mongo_config_for_collection(cls, collection_name: str = None):
        """
        Return a configuration object of MongoDBManager for given collection_name
        If collection_name in any configuration file then use the configured collection_name
        Else use the given collection_name instead
        """
        if collection_name is None:
            collection_name = cls.COLLECTION_NAME

        if not getattr(cls, collection_name, False):
            collection_name = collection_name
        else:
            collection_name = getattr(cls, collection_name)
        return {
            'MONGODB_URI': cls.MONGODB_URI,
            'DB_NAME': cls.DB_NAME,
            'COLLECTION_NAME': collection_name
        }

    ############################################################
    # AWS service configuration
    ############################################################
    AWS_REGION = 'us-west-2'
    BUCKET_NAME = None
    AWS_S3_EXPIRATION = 60 * 60 * 24

    @classmethod
    def aws_config(cls):
        """
        Return aws's configuration from environment variable 'API_ENV'
        """
        return {
            'AWS_REGION': cls.AWS_REGION,
            'BUCKET_NAME': cls.BUCKET_NAME
        }
