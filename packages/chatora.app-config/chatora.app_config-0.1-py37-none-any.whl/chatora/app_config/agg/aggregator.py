__all__ = (
    'AppConfigAggregator',
)

import collections.abc
import contextlib
import copy
import functools
import io
import itertools
import pathlib
import runpy
import tempfile
import types
from urllib import parse as urllib_parse

import requests
import simplejson

from chatora.app_config.agg.constant import JAMMER_ATTR_NAME


class AppConfigAggregator:

    # Public interfaces
    jammer_attr_name = JAMMER_ATTR_NAME
    sources = ()

    # config = traits_api.Property(
    #     traits_api.DictStrAny,
    #     depends_on=[sources, initial_config, extra_config, jammer_attr_name],
    # )

    def __init__(self, sources=None, jammer_attr_name=JAMMER_ATTR_NAME):
        if sources:
            self.sources = tuple(sources)
        if jammer_attr_name:
            self.jammer_attr_name = jammer_attr_name
        return

    def __call__(self, sources=None, initial_config=None, extra_config=None, jammer_attr_name=None):
        if jammer_attr_name is None:
            jammer_attr_name = self.jammer_attr_name

        if initial_config is None:
            initial_config = {jammer_attr_name: True}
        else:
            initial_config = copy.deepcopy(initial_config)
            initial_config[jammer_attr_name] = True

        config = functools.reduce(
            self._resolve,
            sources or self.sources,
            initial_config,
        )
        if extra_config:
            config = self._process_mapping(
                config=config,
                mapping=extra_config,
            )

        config = {
            k: v
            for k,v in config.items()
            if isinstance(k, str) and k.startswith('_') is False
        }

        with contextlib.suppress(KeyError):
            del config[jammer_attr_name]

        return config

    # Private interfaces
    def _resolve(self, config, source):
        if isinstance(source, collections.abc.Mapping):
            return self._process_mapping(
                config=config,
                mapping=source,
            )
        elif isinstance(source, types.ModuleType):
            return self._process_module(
                config=config,
                mod_name=source.__name__,
            )
        elif isinstance(source, collections.abc.Callable):
            return self._process_callable(
                config=config,
                callable_=source,
            )
        elif isinstance(source, io.IOBase):
            return self._process_file(
                config=config,
                f=source,
            )
        elif isinstance(source, str):
            return self._process_text(
                coinfig=config,
                text=source,
            )
        elif isinstance(source, collections.abc.Iterable):
            return functools.reduce(
                self._resolve,
                source,
                config,
            )
        else:
            raise ValueError(f'Unknown source {source!r}')

    @staticmethod
    def _process_mapping(config, mapping):
        config.update({k: v for k, v in mapping.items()})
        return config

    def _process_module(self, config, mod_name):
        return self._resolve(
            config=config,
            source=runpy.run_module(
                mod_name=mod_name,
                init_globals=config,
                run_name=None,
                alter_sys=False,
            ),
        )

    def _process_callable(self, config, callable_):
        return self._resolve(
            config=config,
            source=callable_(),
        )

    def _process_file(self, config, f):
        return self._resolve(
            config=config,
            source=f.readlines(),
        )

    def _process_pyfile_path(self, config, path):
        return self._resolve(
            config=config,
            source=runpy.run_path(
                path_name=path,
                init_globals=config,
                run_name=None,
            ),
        )

    def _process_jsonfile_path(self, config, path):
        return self._resolve(
            config=config,
            source=simplejson.load(
                fp=pathlib.Path(path).open(
                    encoding='utf-8',
                ),
            ),
        )

    def _process_text(self, coinfig, text):
        split_uri = urllib_parse.urlsplit(text)
        scheme = split_uri.scheme

        if scheme == 'pymod':
            return self._process_module(
                config=coinfig,
                mod_name=split_uri.netloc,
            )
        elif scheme == 'pyfile':
            return self._process_pyfile_path(
                config=coinfig,
                path=split_uri.path,
            )
        elif scheme == 'jsonfile':
            return self._process_jsonfile_path(
                config=coinfig,
                path=split_uri.path,
            )
        elif scheme in map(lambda x: f'{x[0]}+{x[1]}', itertools.product(
            ('pyfile', 'json'),
            ('http', 'https'),
        )):
            sub_scheme, proto = scheme.split('+', 1)
            with tempfile.NamedTemporaryFile(
                mode='wt',
                encoding='utf-8',
                newline='\n',
                prefix=f'.{self.__class__.__name__}_{scheme}',
                dir='/tmp',
                delete=True,
            ) as f:
                f.file.write(
                    requests.get(
                        text.split('+', 1)[1],
                    ).text,
                )
                f.file.flush()

                return self._process_pyfile_path(
                    config=coinfig,
                    path=f.name,
                ) if sub_scheme == 'pyfile' else self._process_jsonfile_path(
                    config=coinfig,
                    path=f.name,
                )
        elif scheme in map(lambda x: f'{x[0]}+{x[1]}', itertools.product(
            ('etcdpyfile', 'etcdjson'),
            ('http', 'https'),
        )):
            sub_scheme, proto = scheme.split('+', 1)
            with tempfile.NamedTemporaryFile(
                mode='wt',
                encoding='utf-8',
                newline='\n',
                prefix=f'.{self.__class__.__name__}_{scheme}',
                dir='/tmp',
                delete=True,
            ) as f:
                f.file.write(
                    requests.get(
                        text.split('+', 1)[1],
                    ).json()['node']['value'],
                )
                f.file.flush()

                return self._process_pyfile_path(
                    config=coinfig,
                    path=f.name,
                ) if sub_scheme == 'etcdpyfile' else self._process_jsonfile_path(
                    config=coinfig,
                    path=f.name,
                )
        else:
            raise ValueError(f'Unknown source {text!r}')
