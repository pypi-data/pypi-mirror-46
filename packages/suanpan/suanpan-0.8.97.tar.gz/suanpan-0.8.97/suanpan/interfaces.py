# coding=utf-8
from __future__ import absolute_import, print_function

import argparse
import base64
import functools
import itertools
import os
import re
import sys

from suanpan import objects
from suanpan.arguments import Bool
from suanpan.dw import dw
from suanpan.log import logger
from suanpan.mq import mq
from suanpan.mstorage import mstorage
from suanpan.storage import storage


class HasArguments(object):
    ENVIRONMENT_ARGUMENTS_KEYWORD = "SP_PARAM"
    ARGUMENTS = []

    @classmethod
    def getArgList(cls):
        return cls.getArgListFromEnv() or cls.getArgListFromCli()

    @classmethod
    def getArgListFromCli(cls):
        return sys.argv[1:]

    @classmethod
    def getArgListFromEnv(cls):
        argStringBase64 = os.environ.get(cls.ENVIRONMENT_ARGUMENTS_KEYWORD, "")
        logger.debug(
            "{}(Base64)='{}'".format(cls.ENVIRONMENT_ARGUMENTS_KEYWORD, argStringBase64)
        )
        try:
            argString = base64.b64decode(argStringBase64).decode()
        except Exception:
            argString = argStringBase64  # temporary fix for SP_PARAM(Base64)
        logger.debug("{}='{}'".format(cls.ENVIRONMENT_ARGUMENTS_KEYWORD, argString))
        regex = r"(--[\w-]+)\s+(?:(?P<quote>[\"\'])(.*?)(?P=quote)|([^\'\"\s]+))"
        groups = re.findall(regex, argString, flags=re.S)
        argv = list(
            itertools.chain(*[(group[0], group[-2] or group[-1]) for group in groups])
        )
        return argv

    def loadFormatArguments(self, context, restArgs=None, **kwargs):
        arguments = self.getArguments(**kwargs)
        args, restArgs = self._parseArguments(arguments, restArgs=restArgs)
        self._loadArguments(args, arguments)
        self._formatArguments(context, arguments)
        return arguments, restArgs

    def loadCleanArguments(self, context, restArgs=None, **kwargs):
        arguments = self.getArguments(**kwargs)
        args, restArgs = self._parseArguments(arguments, restArgs=restArgs)
        self._loadArguments(args, arguments)
        self._cleanArguments(context, arguments)
        return arguments, restArgs

    def loadGlobalArguments(self, restArgs=None, **kwargs):
        arguments = self.getGlobalArguments(**kwargs)
        args, restArgs = self._parseGlobalArguments(arguments, restArgs=restArgs)
        self._loadArguments(args, arguments)
        self._formatArguments(objects.Context(), arguments)
        return arguments, restArgs

    def saveArguments(self, context, arguments, results):
        return {
            argument.key: argument.save(context, result)
            for argument, result in zip(arguments, results)
        }

    def getArguments(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented!")

    def getGlobalArguments(self, *args, **kwargs):  # pylint: disable=unused-argument
        return self.ARGUMENTS

    @classmethod
    def _parseArguments(cls, arguments, restArgs=None, **kwargs):
        parser = argparse.ArgumentParser(**kwargs)
        for arg in arguments:
            arg.addParserArguments(parser)
        return parser.parse_known_args(restArgs)

    @classmethod
    def _parseGlobalArguments(cls, arguments, restArgs=None, **kwargs):
        parser = argparse.ArgumentParser(**kwargs)
        for arg in arguments:
            arg.addGlobalParserArguments(parser)
        return parser.parse_known_args(restArgs)

    @classmethod
    def _loadArguments(cls, args, arguments):
        return {arg.key: arg.load(args) for arg in arguments}

    @classmethod
    def _formatArguments(cls, context, arguments):
        return {arg.key: arg.format(context) for arg in arguments}

    @classmethod
    def _cleanArguments(cls, context, arguments):
        return {arg.key: arg.clean(context) for arg in arguments}

    @classmethod
    def defaultArgumentsFormat(cls, args, arguments):
        arguments = (arg.key.replace("-", "_") for arg in arguments)
        return {
            cls._defaultArgumentKeyFormat(arg): getattr(args, arg, None)
            for arg in arguments
        }

    @classmethod
    def _defaultArgumentKeyFormat(cls, key):
        return cls._toCamelCase(cls._removePrefix(key))

    @classmethod
    def _removePrefix(cls, string, delimiter="_", num=1):
        pieces = string.split(delimiter)
        pieces = pieces[num:] if len(pieces) > num else pieces
        return delimiter.join(pieces)

    @classmethod
    def _toCamelCase(cls, string, delimiter="_"):
        camelCaseUpper = lambda i, s: s[0].upper() + s[1:] if i and s else s
        return "".join(
            [camelCaseUpper(i, s) for i, s in enumerate(string.split(delimiter))]
        )

    @classmethod
    def argumentsDict(cls, arguments):
        result = {}
        for arg in arguments:
            keys = (arg.key, arg.alias)
            result.update({key: arg.value for key in keys if key})
        return result

    @classmethod
    def getArgumentValueFromDict(cls, data, arg):
        value = data.get(arg.alias)
        if value is not None:
            return value

        value = data.get(arg.key)
        if value is not None:
            return value

        return None

    @classmethod
    def hasArgumentValueFromDict(cls, data, arg):
        return arg.alias in data or arg.key in data


class HasBaseServices(HasArguments):
    ENABLED_BASE_SERVICES = {"mq", "mstorage", "dw", "storage"}

    def setBackendIfHasArgs(*keys):  # pylint: disable=no-method-argument
        def _wrap(func):
            @functools.wraps(func)
            def _dec(cls, sargs, *args, **kwargs):
                return (
                    func(cls, sargs, *args, **kwargs)
                    if all(getattr(sargs, key, None) is not None for key in keys)
                    else None
                )

            return _dec

        return _wrap

    @classmethod
    def setBaseServices(cls, args):
        mapping = {
            "mq": cls.setMQ,
            "mstorage": cls.setMStorage,
            "dw": cls.setDataWarehouse,
            "storage": cls.setStorage,
        }
        setters = {
            service: mapping.get(service) for service in cls.ENABLED_BASE_SERVICES
        }
        if not all(setters.values()):
            raise Exception(
                "Unknown base serivces: {}".format(
                    set(cls.ENABLED_BASE_SERVICES) - set(mapping.keys())
                )
            )
        backends = ((service, setter(args)) for service, setter in setters.items())
        baseServices = {service: backend for service, backend in backends if backend}
        logger.info("Base services init: {}".format(", ".join(baseServices.keys())))
        return baseServices

    def getGlobalArguments(self, *args, **kwargs):
        arguments = super(HasBaseServices, self).getGlobalArguments(*args, **kwargs)
        return arguments + self.getBaseServicesArguments()

    @classmethod
    def getBaseServicesArguments(cls):
        mapping = {
            "mq": mq.ARGUMENTS,
            "mstorage": mstorage.ARGUMENTS,
            "dw": dw.ARGUMENTS,
            "storage": storage.ARGUMENTS,
        }
        arguments = {
            service: mapping.get(service) for service in cls.ENABLED_BASE_SERVICES
        }
        if not all(arguments.values()):
            raise Exception(
                "Unknown base serivces: {}".format(
                    set(cls.ENABLED_BASE_SERVICES) - set(mapping.keys())
                )
            )
        return list(itertools.chain(*arguments.values()))

    @classmethod
    @setBackendIfHasArgs("mq_type")
    def setMQ(cls, args):
        return mq.setBackend(**cls.defaultArgumentsFormat(args, mq.ARGUMENTS))

    @classmethod
    @setBackendIfHasArgs("mstorage_type")
    def setMStorage(cls, args):
        return mstorage.setBackend(
            **cls.defaultArgumentsFormat(args, mstorage.ARGUMENTS)
        )

    @classmethod
    @setBackendIfHasArgs("dw_type")
    def setDataWarehouse(cls, args):
        return dw.setBackend(**cls.defaultArgumentsFormat(args, dw.ARGUMENTS))

    @classmethod
    @setBackendIfHasArgs("storage_type")
    def setStorage(cls, args):
        return storage.setBackend(**cls.defaultArgumentsFormat(args, storage.ARGUMENTS))


class HasLogger(objects.HasName):
    def __init__(self):
        super(HasLogger, self).__init__()
        logger.setLogger(self.name)

    @property
    def logger(self):
        return logger


class HasDevMode(HasArguments):
    DEV_ARGUMENTS = [Bool(key="debug", default=False)]

    def getGlobalArguments(self, *args, **kwargs):
        arguments = super(HasDevMode, self).getGlobalArguments(*args, **kwargs)
        return arguments + self.DEV_ARGUMENTS
