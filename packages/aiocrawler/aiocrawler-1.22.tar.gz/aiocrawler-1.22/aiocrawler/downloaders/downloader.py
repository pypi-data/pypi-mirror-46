# coding: utf-8
from typing import Union
from aiocrawler import Request
from aiocrawler import Response
from aiocrawler import BaseSettings


class BaseDownloader(object):
    def __init__(self, settings: BaseSettings):
        self.settings = settings
        self.logger = settings.LOGGER

    async def get_response(self, request: Request) -> Union[Response, Exception, None]:
        raise NotImplementedError('{} get_response is not define'.format(self.__class__.__name__))
