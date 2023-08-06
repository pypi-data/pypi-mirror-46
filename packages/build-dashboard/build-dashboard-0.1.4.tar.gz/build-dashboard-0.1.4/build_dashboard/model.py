"""
Module containing the model classes for buildbot_dashboard
"""
from aiohttp import TCPConnector, UnixConnector, request, ClientSession
from json import loads, dumps
import asyncio
from build_dashboard import logger
from cachetools import TTLCache

class BuildbotModel(object):
    """
    The Buildbot model that is provided to the user inferface. It wraps
    a Builbot client that is used for accessing the REST API.
    
    Args:
        client (:obj:`BuildbotClient`): BuildbotClient for interactions
            with the Buildbot REST API

    Attributes:
        client (:obj:`BuildbotClient`): BuildbotClient for interactions
            with the Buildbot REST API
    """

    def __init__(self, client):
        self.client = client
        self._builders = {}
        self._selected_builder = None
        self._selected_build = None
        self._selected_log = None
        self._steps = TTLCache(10, 60)
        self._logs = TTLCache(10, 60)

    def __del__(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.client.close())

    def select_builder(self, builderid):
        if builderid in self._builders:
            self._selected_builder = self._builders[builderid]
        else:
            self._selected_builder = None
    
    @property
    def builder(self):
        return self._selected_builder

    def select_build(self, buildid):
        """Selects the build of selected build
        """
        self._selected_build = None
        for build in self._selected_builder['builds']:
            if build['buildid'] == buildid:
                self._selected_build = build
                break

    @property
    def build(self):
        return self._selected_build

    @property
    def steps(self):
        if self._selected_build is not None:
            buildid = self._selected_build.get('buildid')
            if buildid is not None:
                try:
                    return self._steps[buildid]
                except KeyError:
                    loop = asyncio.get_event_loop()
                    steps = loop.run_until_complete(self.client.get_steps(buildid))
                    self._steps[buildid] = steps
                    return steps
            else:
                logger.debug('Build id not found.')
        else:
            return []

    async def __mergeBuilderAndBuilds(self, builder):
        builds = await self.client.builds(builder['builderid'])
        builder['builds'] = builds 
        return builder
    
    def select_log(self, stepid):
        self._selected_log = None
        try:
            self._selected_log = self._logs[stepid]
        except KeyError:
            loop = asyncio.get_event_loop()
            self._selected_log = loop.run_until_complete(self.client.get_logs(stepid))

    @property
    def log(self):
        return self._selected_log

    def run_force_scheduler(self, builderid):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.client.run_force_scheduler(builderid)) 

    async def update(self):
        """Performs a single update to the model
        """
        logger.debug('Updating model')
        builders = await self.client.builders()
        done, pending = await asyncio.wait([self.__mergeBuilderAndBuilds(builder) 
                    for builder in builders ])
        self._builders = { task.result()['builderid']:task.result() for task in done }
    
    def builders(self):
        """Get cached builders
        """
        return list(self._builders.values());

    def builds(self, builderid):
        """Get cached builds for builders

        Args:
            builderid (int): The id of the builder for which to retrieve builds.
        """
        return self._builders['builderid']['builds']

class BuildbotClient(object):
    """
    The Buildbot HTTP client used for accessing the REST API of Buildbot.
    
    Note:
        This client assumes the Buildbot is using API v2.

    Args:
        path (str, optional): The path to the UNIX domain socket, if using one.
        protocol (str, optional): The protocol of the REST API. Defaults to http.
        host (str, optional): The hostname of the REST API. Defaults to localhost.

    Attributes:
        session (:obj:`ClientSession`): Connection session to Buildbot REST API
        base_address (str): Base URI of the REST API.
    """
    def __init__(self, path=None, protocol='http', host='localhost'):

        if path is None:
            conn = TCPConnector(limit=30)
        else:
            conn = UnixConnector(path=path)
        self.session = ClientSession(connector=conn) 
        self.base_address = protocol + '://' + host + '/api/v2'

    async def get_steps(self, buildid):
        results = await self._get('/builds/' + str(buildid) + '/steps')
        return results['steps']
    
    async def get_logs(self, stepid):
        results = await self._get('/steps/' + str(stepid) + '/logs')
        logid = results['logs'][0]['logid']
        results = await self._get('/logs/' + str(logid) + '/contents')
        content = results['logchunks'][0]['content']
        return content

    async def get_force_schedulers(self, builderid):
       results = await self._get('/builders/' + str(builderid) + '/forceschedulers')
       return results['forceschedulers']

    async def run_force_scheduler(self, builderid):
        results = await self.get_force_schedulers(builderid)
        result = False
        if len(results) > 0:
            name = results[0]['name']
            result = await self._post_jsonrpc('/forceschedulers/' + str(name), body={'method': 'force', 'params': {}})
            logger.debug(result)
        return result

    async def _post_jsonrpc(self, address, body):
        message = {
            'jsonrpc': '2.0',
            'id': 1
        }
        return await self._post(address, body={**message, **body})

    async def _post(self, address, body):
        logger.debug(body)
        response = await self.session.post(self.base_address + address, json=body)
        text = await response.text()
        result = loads(text)
        return result

    async def _get(self, address):
        """ A template for asynchronous gets to REST API 
        
        Args:
            address (str): The relative path to the API requested

        Returns:
            A :obj:`dict` representing the response.
        """
        response = await self.session.get(self.base_address + address)
        text = await response.text()
        result = loads(text)
        return result
   
    async def builders(self):
        """ Requests builders endpoint from Buildbot REST API
        
        Returns:
            A :obj:`dict` representing the response.
        """
        results = await self._get('/builders')
        return results['builders']

    async def builds(self, builderid):
        """ Requests build endpoint of a particular build from Buildbot REST API.
        
        Args:
            builderid (str): The id of the builder

        Returns:
            A :obj:`dict` representing the response.
        """
        results = await self._get('/builders/' + str(builderid) + '/builds')
        return results['builds']
    
    async def close(self):
        """ Closes the underlying :obj:`ClientSession` """
        await self.session.close()
