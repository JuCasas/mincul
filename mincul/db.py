LOCAL = {
    'NAME': 'mincul',
    'USER': 'postgres',
    'PASSWORD': 'p0stgr3s742Fa!',
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
