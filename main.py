"""
This work is free. You can redistribute it and/or modify it under the
terms of the Do What The Fuck You Want To Public License, Version 2,
as published by Sam Hocevar. See http://www.wtfpl.net/ for more details.
"""

import os
import re
import requests
import datetime
from PIL import Image, ImageDraw

url = "https://cab-e-81.inf.ethz.ch/reservation/overview"
filename = os.path.dirname(os.path.realpath(__file__)) + "/reservations.png"

coordinates = [
    # Top left and bottom right corner of each table
    # Extracted with https://pixspy.com/
    ((0, 0), (0, 0)),          # 0

    ((210, 613), (257, 635)),  # 1
    ((260, 613), (307, 635)),  # 2
    ((310, 613), (357, 635)),  # 3
    ((234, 588), (281, 610)),  # 4
    ((284, 588), (331, 610)),  # 5

    ((84, 526), (106, 573)),   # 6
    ((109, 551), (156, 573)),  # 7
    ((109, 526), (156, 548)),  # 8

    ((210, 509), (257, 531)),  # 9
    ((260, 509), (307, 531)),  # 10
    ((310, 509), (357, 531)),  # 11
    ((234, 484), (281, 506)),  # 12
    ((284, 484), (331, 506)),  # 13

    ((84, 422), (106, 469)),   # 14
    ((109, 447), (156, 469)),  # 15
    ((109, 422), (156, 444)),  # 16

    ((210, 405), (257, 427)),  # 17
    ((260, 405), (307, 427)),  # 18
    ((310, 405), (357, 427)),  # 19
    ((234, 380), (281, 402)),  # 20
    ((284, 380), (331, 402)),  # 21

    ((84, 319), (106, 366)),   # 22
    ((109, 344), (156, 366)),  # 23
    ((109, 319), (156, 341)),  # 24

    ((210, 302), (257, 324)),  # 25
    ((260, 302), (307, 324)),  # 26
    ((310, 302), (357, 324)),  # 27
    ((234, 277), (281, 299)),  # 28
    ((284, 277), (331, 299)),  # 29

    ((84, 216), (106, 263)),   # 30
    ((109, 241), (156, 263)),  # 31
    ((109, 216), (156, 238)),  # 32

    ((210, 198), (257, 220)),  # 33
    ((260, 198), (307, 220)),  # 34
    ((310, 198), (357, 220)),  # 35
    ((234, 173), (281, 195)),  # 36
    ((284, 173), (331, 195)),  # 37

    ((84, 113), (106, 160)),   # 38
    ((109, 138), (156, 160)),  # 39
    ((109, 113), (156, 135)),  # 40

    ((234, 86), (281, 108)),   # 41
    ((284, 86), (331, 108))    # 42
]

if __name__ == '__main__':
    # Avoid trouble when script gets called from outside its directory
    img = Image.open(os.path.realpath(os.path.dirname(__file__)) + "/cab-e-81.png").convert("RGBA")

    # Create a new image to draw on
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    # Get HTML from overview page
    response = requests.get(url).text
    # First, rempove all line breaks and tabs
    response = re.sub("[\\n\\r\\t]+", "", response)
    # Then, remove excessive whitespaces
    response = re.sub("\\s{2,}", " ", response)

    # Get reservation states and place numbers from the HTML code
    pattern = "<div class=\"left (invalid )?\"><label(.+?)>cab-e81-(\\d{1,2})</label></div>"
    groups = re.findall(pattern, response)

    # For each group, check reservation state and draw rectangle
    for group in groups:
        invalid = group[0]
        i = int(group[2])
        # print(i, invalid)

        # Draw a semi-transparent rectangle
        # Red for reserved, Green for free desks
        color = (255, 0, 0, 128) if invalid else (0, 255, 0, 128)
        overlay_draw.rectangle(coordinates[i], fill=color)

    # Add timestamp in lower left corner
    text = "Last update: %s" % datetime.datetime.now().strftime("%d.%m.%Y, %H:%M:%S")
    overlay_draw.text((3, img.size[1]-13), text, (0, 0, 0, 200))

    # Add overlay to original image
    out = Image.alpha_composite(img, overlay)

    # Replace old file
    os.remove(filename)
    out.save(filename)
