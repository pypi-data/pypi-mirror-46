from tgt_grease.core import GreaseContainer
from bson.objectid import ObjectId
from .DeDuplication import Deduplication
import pymongo
import datetime
import sys


class Scheduling(object):
    """Central scheduling class for GREASE

    This class routes data to nodes within GREASE

    Attributes:
        ioc (GreaseContainer): IoC access for DeDuplication

    """

    def __init__(self, ioc=None):
        if isinstance(ioc, GreaseContainer):
            self.ioc = ioc
        else:
            self.ioc = GreaseContainer()
        self.ioc.ensureRegistration()

    def scheduleDetection(self, source, configName, data):
        """Schedule a Source Parse to detection

        This method will take a list of single dimension dictionaries and schedule them for detection

        Args:
            source (str): Name of the source
            configName (str): Configuration Data was sourced from
            data (list[dict]): Data to be scheduled for detection

        Returns:
            bool: Scheduling success

        """
        if len(data) is 0 or not isinstance(data, list):
            self.ioc.getLogger().trace(
                "Data provided empty or is not type list type: [{0}] len: [{1}]".format(
                    str(type(data)), len(data)),
                trace=True
            )
            return False
        self.ioc.getLogger().trace(
            "Preparing to schedule [{0}] source objects".format(len(data)), trace=True)
        sourceCollect = self.ioc.getCollection('SourceData')
        jServerCollect = self.ioc.getCollection('JobServer')
        # begin scheduling loop of each block
        for elem in data:
            if not isinstance(elem, dict):
                self.ioc.getLogger().warning(
                    "Element from data not of type dict! Got [{0}] DROPPED".format(
                        str(type(elem))),
                    notify=False
                )
                continue
            server, jobCount = self.determineDetectionServer()
            if server:
                sourceCollect.insert_one({
                    'grease_data': {
                        'sourcing': {
                            'server': ObjectId(self.ioc.getConfig().NodeIdentity)
                        },
                        'detection': {
                            'server': ObjectId(server),
                            'start': None,
                            'end': None,
                            'detection': {}
                        },
                        'scheduling': {
                            'server': None,
                            'start': None,
                            'end': None
                        },
                        'execution': {
                            'server': None,
                            'assignmentTime': None,
                            'completeTime': None,
                            'returnData': {},
                            'executionSuccess': False,
                            'commandSuccess': False,
                            'failures': 0
                        }
                    },
                    'source': str(source),
                    'configuration': str(configName),
                    'data': elem,
                    'createTime': datetime.datetime.utcnow(),
                    'expiry': Deduplication.generate_max_expiry_time(1)
                })
                jServerCollect.update_one({
                    '_id': ObjectId(server)},
                    {'$set': {'jobs': int(jobCount) + 1}}
                )
            else:
                self.ioc.getLogger().warning(
                    "Failed to find detection server for data object from source [{0}]; DROPPED".format(
                        source),
                    notify=False
                )
                self.ioc.getLogger().warning(
                    "Detection scheduling failed. Could not find detection server",
                    notify=False
                )
                return False
        return True

    def scheduleScheduling(self, objectId):
        """Schedule a source for job scheduling

        This method schedules a source for job scheduling

        Args:
            objectId (str): MongoDB ObjectId to schedule

        Returns:
            bool: If scheduling was successful

        """
        server, jobCount = self.determineSchedulingServer()
        if not server:
            self.ioc.getLogger().error("Failed to find scheduling server", notify=False)
            return False
        self.ioc.getCollection('SourceData').update_one(
            {'_id': ObjectId(objectId)},
            {
                '$set': {
                    'grease_data.scheduling.server': ObjectId(server),
                    'grease_data.scheduling.start': None,
                    'grease_data.scheduling.end': None
                }
            }
        )
        self.ioc.getCollection('SourceData').update_one({
            '_id': ObjectId(server)},
            {'$set': {'jobs': int(jobCount) + 1}}
        )
        return True

    def determineDetectionServer(self):
        """Determines detection server to use

        Finds the detection server available for a new detection job

        Returns:
            tuple: MongoDB Object ID of server & current job count

        """
        servers = [
            (server.get('_id'), server.get('jobs')) for server in self.ioc.getCollection('JobServer').find(
                {
                    'active': True,
                    'prototypes': 'detect',
                }
            )
        ]

        best_server = {}
        for (server, total_jobs) in servers:
            active_jobs = self.ioc.getCollection('SourceData').find(
                {
                    'grease_data.detection.server': server,
                    'grease_data.detection.end': None,
                }
            ).count()
            if active_jobs < best_server.get('active_jobs', sys.maxsize):
                best_server['_id'] = server
                best_server['total_jobs'] = total_jobs
                best_server['active_jobs'] = active_jobs

        if not best_server.get('_id'):
            self.ioc.getLogger().error("No active detection server found!")
            return "", 0

        return best_server.get('_id'), best_server.get('total_jobs')

    def determineSchedulingServer(self):
        """Determines scheduling server to use

        Finds the scheduling server available for a new scheduling job

        Returns:
            tuple: MongoDB Object ID of server & current job count

        """
        servers = [
            (server.get('_id'), server.get('jobs')) for server in self.ioc.getCollection('JobServer').find(
                {
                    'active': True,
                    'prototypes': 'schedule',
                }
            )
        ]

        best_server = {}
        for (server, total_jobs) in servers:
            active_jobs = self.ioc.getCollection('SourceData').find(
                {
                    'grease_data.scheduling.server': server,
                    'grease_data.scheduling.end': None,
                }
            ).count()
            if active_jobs < best_server.get('active_jobs', sys.maxsize):
                best_server['_id'] = server
                best_server['total_jobs'] = total_jobs
                best_server['active_jobs'] = active_jobs

        if not best_server.get('_id'):
            self.ioc.getLogger().error("No active scheduling server found!")
            return "", 0

        return best_server.get('_id'), best_server.get('total_jobs')

    def determineExecutionServer(self, role):
        """Determines execution server to use

        Finds the execution server available for a new execution job

        Returns:
            str: MongoDB Object ID of server; if one cannot be found then string will be empty

        """
        servers = [
            (server.get('_id'), server.get('jobs')) for server in self.ioc.getCollection('JobServer').find(
                {
                    'active': True,
                    'roles': str(role),
                }
            )
        ]

        best_server = {}
        for (server, total_jobs) in servers:
            active_jobs = self.ioc.getCollection('SourceData').find(
                {
                    'grease_data.execution.server': server,
                    'grease_data.execution.completeTime': None,
                    'grease_data.execution.failures': {'$lt': 6},
                }
            ).count()
            if active_jobs < best_server.get('active_jobs', sys.maxsize):
                best_server['_id'] = server
                best_server['total_jobs'] = total_jobs
                best_server['active_jobs'] = active_jobs

        if not best_server.get('_id'):
            self.ioc.getLogger().error("No active job server found with role {}!".format(role))
            return "", 0

        return best_server.get('_id'), best_server.get('total_jobs')
