from importlib import import_module
from straight.plugin.loaders import ModuleLoader


class AppLoader(ModuleLoader):

    def __init__(self, subtype=None):
        self.subtype = None
        self._cache = []
        super(AppLoader, self).__init__()

    def _fill_cache(self, namespace):
        super(AppLoader, self)._fill_cache(namespace)
        self._cache = filter(self._meta, self._cache)

    def register(self, *args, **kwargs):
        " Load and register modules. "

        result = []

        submodule = kwargs.pop('submodule', None)
        logger = kwargs.pop('logger', None)

        for mod in self:

            if logger:
                logger.info("Register module: %s" % mod.__name__)

            if submodule:
                mod = self.import_module('%s.%s' % (mod.__name__, submodule))

            meta = self._meta(mod)
            meta and meta(*args, **kwargs)

            result.append(mod)

        return result

    def __iter__(self):
        return iter(self._cache)

    @staticmethod
    def _meta(mod):
        return getattr(mod, 'loader_meta', None)

    @staticmethod
    def import_module(path):
        try:
            return import_module(path)
        except ImportError:
            return None


loader = AppLoader()
loader.load(__name__.split('.')[0])


# pymode:lint_ignore=F0401
