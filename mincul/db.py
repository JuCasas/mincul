LOCAL = {
    'NAME': 'mincul',
    'USER': 'postgres',
<<<<<<< HEAD
    'PASSWORD': 'posgres',
=======
    'PASSWORD': '12345',
>>>>>>> 52bb1650c21ecb30e99e7a9d100d8873269916b7
}
GAE = {
    'NAME': '',
    'USER': '',
    'PASSWORD': '',
    'HOST': '/cloudsql/...'
}
GAE_IP = ''


class PostgresDB:
    base = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'OPTIONS': {
                'options': '-c search_path=public'
            },
            'HOST': 'localhost',
            'PORT': '5432'
        }
    }

    @classmethod
    @property
    def local(cls):
        local = cls.base.copy()
        local['default'].update(LOCAL)
        return local

    @classmethod
    def get_gae(cls, raw_ip=False):
        gae = cls.base.copy()
        gae['default'].update(GAE)
        if raw_ip:
            gae['default']['HOST'] = GAE_IP
        return gae
