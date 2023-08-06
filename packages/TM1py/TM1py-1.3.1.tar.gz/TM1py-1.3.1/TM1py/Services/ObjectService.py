# -*- coding: utf-8 -*-

from TM1py.Exceptions import TM1pyException


class ObjectService:
    """ Parentclass for all Object Services
    
    """
    def __init__(self, rest_service):
        """ Constructor, Create an instance of ObjectService
        
        :param rest_service: 
        """
        self._rest = rest_service

    def determine_actual_object_name(self, object_class, object_name):
        request = "/api/v1/{}?$filter=tolower(replace(Name, ' ', '')) eq '{}'".format(
            object_class,
            object_name.replace(" ", "").lower())
        response = self._rest.GET(request)
        if len(response.json()["value"]) == 0:
            raise ValueError("Object '{}' of type '{}' doesn't exist".format(object_name, object_class))
        return response.json()["value"][0]["Name"]

    def _exists(self, request):
        """ Check if ressource exists in the TM1 Server
        
        :param request: 
        :return: 
        """
        try:
            self._rest.GET(request)
            return True
        except TM1pyException as e:
            if e._status_code == 404:
                return False
            raise e

    @property
    def version(self):
        return self._rest._version






































