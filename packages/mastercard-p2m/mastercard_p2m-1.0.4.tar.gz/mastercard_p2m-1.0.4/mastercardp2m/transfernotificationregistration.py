#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (c) 2016 MasterCard International Incorporated
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of
# conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or other materials
# provided with the distribution.
# Neither the name of the MasterCard International Incorporated nor the names of its
# contributors may be used to endorse or promote products derived from this software
# without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#


from __future__ import absolute_import
from mastercardapicore import BaseObject
from mastercardapicore import RequestMap
from mastercardapicore import OperationConfig
from mastercardapicore import OperationMetadata
from mastercardp2m import ResourceConfig

class TransferNotificationRegistration(BaseObject):
    """
    
    """

    __config = {
        
        "89eaf409-464e-47d7-8523-42382ed91a54" : OperationConfig("/send/v1/partners/{partnerId}/notification-registries", "create", [], []),
        
        "9c89c047-6460-44ee-9fba-dfada2142ee2" : OperationConfig("/send/v1/partners/{partnerId}/notification-registries/{account-reg-ref}", "delete", [], []),
        
        "73de7d51-1e6e-4148-8207-07bcb61ae5c3" : OperationConfig("/send/v1/partners/{partnerId}/notification-registries/{account-reg-ref}", "read", [], []),
        
        "0aca856a-a0ec-476a-aa5e-73eb51023b62" : OperationConfig("/send/v1/partners/{partnerId}/notification-registries/{account-reg-ref}", "update", [], []),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUID)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative(), ResourceConfig.getInstance().getContentTypeOverride())


    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type TransferNotificationRegistration

        @param Dict mapObj, containing the required parameters to create a new object
        @return TransferNotificationRegistration of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("89eaf409-464e-47d7-8523-42382ed91a54", TransferNotificationRegistration(mapObj))









    @classmethod
    def deleteById(cls,id,map=None):
        """
        Delete object of type TransferNotificationRegistration by id

        @param str id
        @return TransferNotificationRegistration of the response of the deleted instance.
        @raise ApiException: raised an exception from the response status
        """

        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if map:
            if (isinstance(map,RequestMap)):
                mapObj.setAll(map.getObject())
            else:
                mapObj.setAll(map)

        return BaseObject.execute("9c89c047-6460-44ee-9fba-dfada2142ee2", TransferNotificationRegistration(mapObj))

    def delete(self):
        """
        Delete object of type TransferNotificationRegistration

        @return TransferNotificationRegistration of the response of the deleted instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("9c89c047-6460-44ee-9fba-dfada2142ee2", self)







    @classmethod
    def readby(cls,id,criteria=None):
        """
        Returns objects of type TransferNotificationRegistration by id and optional criteria
        @param str id
        @param dict criteria
        @return instance of TransferNotificationRegistration
        @raise ApiException: raised an exception from the response status
        """
        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if criteria:
            if (isinstance(criteria,RequestMap)):
                mapObj.setAll(criteria.getObject())
            else:
                mapObj.setAll(criteria)

        return BaseObject.execute("73de7d51-1e6e-4148-8207-07bcb61ae5c3", TransferNotificationRegistration(mapObj))



    def update(self):
        """
        Updates an object of type TransferNotificationRegistration

        @return TransferNotificationRegistration object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("0aca856a-a0ec-476a-aa5e-73eb51023b62", self)






