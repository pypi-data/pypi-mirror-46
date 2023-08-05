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
from mastercardtransfer import ResourceConfig

class FundsTransfer(BaseObject):
    """
    
    """

    __config = {
        
        "80c7bd72-7242-4ab9-8aa0-68bbd9fbfa0a" : OperationConfig("/send/v1/partners/{partnerId}/funds-transfers", "create", [], []),
        
        "8f7736a2-e26b-4fe8-9acd-9e955b056bde" : OperationConfig("/send/v1/partners/{partnerId}/funds-transfers/{transferId}", "read", [], []),
        
        "fae74a6c-137b-4202-9ca4-a3125b102010" : OperationConfig("/send/v1/partners/{partnerId}/funds-transfers", "query", [], ["ref"]),
        
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
        Creates object of type FundsTransfer

        @param Dict mapObj, containing the required parameters to create a new object
        @return FundsTransfer of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("80c7bd72-7242-4ab9-8aa0-68bbd9fbfa0a", FundsTransfer(mapObj))










    @classmethod
    def readByID(cls,id,criteria=None):
        """
        Returns objects of type FundsTransfer by id and optional criteria
        @param str id
        @param dict criteria
        @return instance of FundsTransfer
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

        return BaseObject.execute("8f7736a2-e26b-4fe8-9acd-9e955b056bde", FundsTransfer(mapObj))







    @classmethod
    def readByReference(cls,criteria):
        """
        Query objects of type FundsTransfer by id and optional criteria
        @param type criteria
        @return FundsTransfer object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("fae74a6c-137b-4202-9ca4-a3125b102010", FundsTransfer(criteria))


