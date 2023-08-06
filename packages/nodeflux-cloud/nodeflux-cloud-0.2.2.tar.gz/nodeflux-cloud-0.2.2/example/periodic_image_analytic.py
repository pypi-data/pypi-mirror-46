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
This example periodically read frames from a video stream,
such as video file and a camera source, and send it to Nodeflux Cloud.
The result will be printed to stdout.

To use this example, you need to have opencv-python installed.
Run the example with the following command:

```
python periodic_image_analytic.py rtsp://some-video-stream --interval 1
```
"""
# pylint: disable=invalid-name

import argparse
import time
from typing import Iterator

import cv2

from nodeflux.cloud.clients import ImageAnalyticClient
from nodeflux.cloud.requests import ImageAnalyticRequest, AnalyticTypes

ANALYTICS = [
    AnalyticTypes.FACE_DETECTION,
    AnalyticTypes.FACE_DEMOGRAPHY,
    AnalyticTypes.FACE_RECOGNITION,
]


def periodic_image_analytic(stream: str, interval: int = 1):
    """Open an video stream and periodically send the frame to Nodeflux Cloud.

    Arguments:
        stream {str} -- video stream url or path

    Keyword Arguments:
        interval {int} -- interval to send the frame in second (default: {1})
    """

    client = ImageAnalyticClient()
    request_iterator = generate_request_from_stream(stream, interval)
    responses = client.stream_image_analytic(request_iterator)

    for response in responses:
        print("Face detections:", response.face_detections)
        print("Face demographycs:", response.face_demographics)
        print("Face recognitions:", response.face_recognitions)


def generate_request_from_stream(
        stream: str,
        interval: int = 1,
) -> Iterator[ImageAnalyticRequest]:
    """A generator that read video stream and yield an image analytic request.

    Arguments:
        stream {str} -- video stream url or path

    Keyword Arguments:
        interval {int} -- interval to send the frame in second (default: {1}) (default: {1})

    Returns:
        Iterator[ImageAnalyticRequest] -- iterator to image analytic requests
    """
    cap = cv2.VideoCapture(stream)

    last_retrieve = time.time()
    while True:
        cap.grab()

        if time.time() - last_retrieve > interval:
            ret, frame = cap.retrieve()

            if ret is False:
                break

            encoded_frame = cv2.imencode(
                ".jpg",  # encode frame to jpeg
                frame,
                [int(cv2.IMWRITE_JPEG_QUALITY), 60],  # set encoding quality
            )[1].tostring()

            yield ImageAnalyticRequest(encoded_frame, ANALYTICS)

            last_retrieve = time.time()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Periodic image analytic from video stream.')
    parser.add_argument('stream', type=str, help='video stream url or path')
    parser.add_argument(
        '--interval',
        type=float,
        help='interval to send the frame in second',
        default=1,
    )
    args = parser.parse_args()

    periodic_image_analytic(args.stream, args.interval)
