"""
Module containing the model classes for buildbot_dashboard
"""
from aiohttp import TCPConnector, UnixConnector, request, ClientSession
from json import loads
import asyncio
from build_dashboard import logger

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

    def __del__(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.client.close())
    
    async def __mergeBuilderAndBuilds(self, builder):
        builds = await self.client.builds(builder['builderid'])
        builder['builds'] = builds 
        return builder
 
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
