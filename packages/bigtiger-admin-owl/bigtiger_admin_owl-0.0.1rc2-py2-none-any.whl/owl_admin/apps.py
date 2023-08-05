from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from django.conf import settings


def _def_settings():
    setattr(settings, 'LOGOUT_URL', '/')
    setattr(settings, 'LOGIN_REDIRECT_URL', '/main/')
    setattr(settings, 'PERMISSIONS_SESSION_KEY', '_auth_user_permissions')

    setattr(settings, 'SESSION_ENGINE', 'django_sae.session.backends.db')
    setattr(settings, 'AUTHENTICATION_BACKENDS',
            ('django_sae.auth.backends.ModelBackend',))

    if not hasattr(settings, 'SAE_ACCESS_TOKEN_SECRET'):
        setattr(settings, 'SAE_ACCESS_TOKEN_SECRET', 'linkeddt.com')

    if not hasattr(settings, 'SYS_CONFIG_BACKEND'):
        setattr(settings, 'SYS_CONFIG_BACKEND',
                'bigtree_config.backends.ModelBackend')
    if not hasattr(settings, 'USER_LOG_BACKEND'):
        setattr(settings, 'USER_LOG_BACKEND',
                'bigtree_log.backends.ModelBackend')
    if not hasattr(settings, 'BIGTREE_API_ACCESS_TOKEN_SECRET'):
        setattr(settings, 'BIGTREE_API_ACCESS_TOKEN_SECRET', 'linkeddt.com')


_def_settings()


class OwlAdminConfig(AppConfig):
    name = 'owl_admin'
    verbose_name = _("OwlAdmin")

    def ready(self):
        pass
