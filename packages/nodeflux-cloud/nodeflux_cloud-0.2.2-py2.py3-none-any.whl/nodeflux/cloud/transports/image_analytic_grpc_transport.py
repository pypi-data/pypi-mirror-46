# Copyright 2018 PT Nodeflux Teknologi Indonesia.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
    nodeflux.cloud.transports.image_analytic_grpc_transport
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implements the gRPC transport for ImageAnalytic API.
"""

from typing import Iterator

import grpc

from nodeflux.cloud.auth.credentials import Credentials
from nodeflux.cloud.transports.grpc_auth import AuthMetadataPlugin
from nodeflux.api.v1beta1.image_analytic_pb2 import (
    ImageAnalyticRequest,
    ImageAnalyticResponse,
)
from nodeflux.api.v1beta1.image_analytic_pb2_grpc import ImageAnalyticStub


class ImageAnalyticGrpcTransport:  # pylint: disable=too-few-public-methods
    """Use gRPC transport for the Image Analytic API."""

    def __init__(
            self,
            channel: grpc.Channel = None,
            credentials: Credentials = None,
            address: str = "api.cloud.nodeflux.io",
    ):
        """Initialize the gRPC transport.

        If no arguments are given, a secure gRPC channel will be created
        with credentials from the `NODEFLUX_ACCESS_KEY` and
        `NODEFLUX_SECRET_KEY` combination or the `NODEFLUX_CREDENTIALS_FILE`
        environment variable.

        Keyword Arguments:
            channel {grpc.Channel} -- custom gRPC chanel (default: {None})
            credentials {Credentials} -- custom credentials  (default: {None})
            address {str} -- Nodeflux Cloud API host (default: {"api.cloud.nodeflux.io"})
        """
        if channel is not None and credentials is not None:
            raise ValueError(
                "The `channel` and `credentials` arguments are mutually "
                "exclusive.")

        if credentials is None:
            credentials = Credentials()

        if channel is None:
            channel_credentials = _create_call_credentials(credentials)
            channel = grpc.secure_channel(address, channel_credentials)

        self._channel = channel
        self._stub = ImageAnalyticStub(self._channel)

    def stream_image_analytic(self, requests: Iterator[ImageAnalyticRequest]
                              ) -> Iterator[ImageAnalyticResponse]:
        """Invoke the Image Analytic API with bidirectional gRPC streaming.

        Arguments:
            requests {Iterator[ImageAnalyticRequest]} -- An iterator that yields
                                                         ImageAnalyticRequest

        Returns:
            Iterator[ImageAnalyticResponse] -- An iterator of ImageAnalyticResponse
        """
        return self._stub.StreamImageAnalytic(requests)


def _create_call_credentials(credentials: Credentials) -> grpc.CallCredentials:
    ssl_credentials = grpc.ssl_channel_credentials()

    metadata_plugin = AuthMetadataPlugin(credentials)
    auth_credentials = grpc.metadata_call_credentials(metadata_plugin)

    return grpc.composite_channel_credentials(ssl_credentials,
                                              auth_credentials)
