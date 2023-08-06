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
    nodeflux.cloud.requests.image_analytic_request
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implements the image analytic request.
"""

from datetime import datetime
from typing import List, Dict

from nodeflux.cloud.requests.types import AnalyticTypes


class ImageAnalyticRequest:  # pylint: disable=too-few-public-methods
    """Request data for image analytic request.

    A request consists of a jpeg image and a list of analytic types to be
    performed. Optionally, labels and timestamp can be used to add context to
    the request.
    """

    def __init__(self,
                 image: bytes,
                 analytics: List[AnalyticTypes],
                 labels: Dict[str, str] = None,
                 timestamp: datetime = datetime.now()) -> None:
        """Constructs an ImageAnalyticRequest

        Arguments:
            image {bytes} -- jpeg encoded image
            analytics {List[AnalyticTypes]} -- list of analytic types to be performed

        Keyword Arguments:
            labels {Dict[str, str]} -- labels of the image (default: {None})
            timestamp {datetime} -- timestamp of the image (default: {datetime.now()})

        Returns:
            None -- [description]
        """
        self.image = image
        self.analytics = analytics
        self.labels = labels
        self.timestamp = timestamp
