# Copyright 2019 PT Nodeflux Teknologi Indonesia.
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
    nodeflux.cloud.clients.image_analytic_client
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implements the image analytic client.
"""
from typing import List, Iterator, Iterable

from nodeflux.analytics.v1beta1 import analytic_pb2
from nodeflux.api.v1beta1 import image_analytic_pb2
from nodeflux.cloud.requests import ImageAnalyticRequest
from nodeflux.cloud.transports import ImageAnalyticGrpcTransport


class ImageAnalyticClient:
    """Client for Nodeflux Cloud Analytic API."""

    def __init__(
            self,
            transport: ImageAnalyticGrpcTransport = None,
    ) -> None:
        """Initialize the image analytic client.

        If no arguments are given, a secure gRPC transport will be used to
        call the API.

        Every requests are authenticated with credentials from the
        `NODEFLUX_ACCESS_KEY` and `NODEFLUX_SECRET_KEY` combination or the
        `NODEFLUX_CREDENTIALS_FILE` environment variable.

        The `transport` argument can be used to use a custom transport and
        credentials.

        Keyword Arguments:
            transport {ImageAnalyticGrpcTransport} -- custom transport (default: {None})
        """
        if transport:
            self.transport = transport
        else:
            self.transport = ImageAnalyticGrpcTransport()

    def batch_image_analytic(
            self,
            requests: List[ImageAnalyticRequest],
    ) -> image_analytic_pb2.BatchImageAnalyticResponse:
        """Invoke image analytic to a list of `ImageAnalyticRequest`.

        Arguments:
            requests {List[ImageAnalyticRequest]} -- list of requests to be
                                                     analyzed

        Returns:
            image_analytic_pb2.BatchImageAnalyticResponse -- analytic result
        """
        request_iterator = _image_analytic_request_iterator(requests)
        response = image_analytic_pb2.BatchImageAnalyticResponse()

        for resp in self.transport.stream_image_analytic(request_iterator):
            response.responses.extend([resp])

        return response

    def stream_image_analytic(
            self,
            requests: Iterator[ImageAnalyticRequest],
    ) -> Iterator[image_analytic_pb2.ImageAnalyticResponse]:
        """Invoke image analytic from an iterator that yields ImageAnalyticRequest.

        Arguments:
            requests {Iterator[ImageAnalyticRequest]} -- An iterator that yields
                                                         ImageAnalyticRequest

        Returns:
            Iterator[image_analytic_pb2.ImageAnalyticResponse] -- An iterator of analytic result
        """
        request_iterator = _image_analytic_request_iterator(requests)

        return self.transport.stream_image_analytic(request_iterator)


def _image_analytic_request_iterator(
        requests: Iterable[ImageAnalyticRequest]
) -> Iterable[image_analytic_pb2.ImageAnalyticRequest]:
    for request in requests:
        image_analytic_request = image_analytic_pb2.ImageAnalyticRequest()
        image_analytic_request.image.content = request.image
        image_analytic_request.analytics.extend(
            [analytic_pb2.Analytic(type=a) for a in request.analytics])

        yield image_analytic_request
