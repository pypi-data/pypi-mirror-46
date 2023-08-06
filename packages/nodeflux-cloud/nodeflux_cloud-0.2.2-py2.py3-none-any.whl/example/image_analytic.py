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
This example takes a jpeg image and send it to Nodeflux Cloud.
The result will be printed to stdout.

Run the example with the following command:

```
python image_analytic.py /path/to/your/image.jpg
```
"""
# pylint: disable=invalid-name

import argparse
from datetime import datetime

from nodeflux.cloud.clients import ImageAnalyticClient
from nodeflux.cloud.requests import ImageAnalyticRequest, AnalyticTypes


def image_analytic(image_path: str):
    """Open an image and send it to Nodeflux Cloud.

    Arguments:
        image_path {str} -- path to jpeg image file
    """
    client = ImageAnalyticClient()

    with open(image_path, 'rb') as image_file:
        image_content = image_file.read()

    requests = [
        ImageAnalyticRequest(
            image_content,
            [
                AnalyticTypes.FACE_DETECTION,
                AnalyticTypes.FACE_DEMOGRAPHY,
                AnalyticTypes.FACE_RECOGNITION,
                # AnalyticTypes.VEHICLE_DETECTION,
                # AnalyticTypes.LICENSE_PLATE_RECOGNITION,
            ],
        )
    ]

    for i in range(1000):
        start = datetime.now()
        response = client.batch_image_analytic(requests)
        # print(response)
        print(datetime.now() - start)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Nodeflux Cloud Image Analytic.')
    parser.add_argument('image_path', type=str, help='path to image file')
    args = parser.parse_args()

    image_analytic(args.image_path)
