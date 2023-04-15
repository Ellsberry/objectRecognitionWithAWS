# This Python program is to perform object recognition using AWS
# Rishab Teaches Tech --  https://www.youtube.com/watch?v=Z-4JHOFPn0g


import boto3
import csv
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io
import json
from pprint import pprint

# Get the access codes to run the AWS  boto3 and rekognition programs
file_df = pd.read_csv('recognition_v1_accessKeys.csv')
access_key_id = file_df['Access key ID'].loc[file_df.index[0]]
secret_access_key = file_df['Secret access key'].loc[file_df.index[0]]
# print(f"access key = {access_key_id}   and secret access key =  {secret_access_key}")

client = boto3.client('rekognition', region_name='us-east-1', aws_access_key_id=access_key_id,
                      aws_secret_access_key=secret_access_key)

# photo = "michel_anthony.jpg"
# photo = "anthony.jpg"
# photo = "anthony_steve.jpg"
photo = "michael_anthony_lisa.jpg"
# photo = "michel.jpg"

with open(photo, 'rb') as image_file:
    source_bytes = image_file.read()

detect_objects = client.detect_labels(Image={'Bytes': source_bytes})
# print(detect_objects)

pd.options.display.max_columns = 10
detected_json_data_df = pd.json_normalize(detect_objects['Labels'])
# print("The next print uses pprint with depth = 8")
pprint(detect_objects, depth=8)

print(detected_json_data_df[0:200])


image = Image.open(io.BytesIO(source_bytes))
draw = ImageDraw.Draw(image)

for label in detect_objects['Labels']:
    print(label['Name'])
    print('confidences: ', label['Confidence'])

    for instances in label['Instances']:
        if 'BoundingBox' in instances:

            box = instances['BoundingBox']

            left = image.width * box['Left']
            top = image.height * box['Top']
            width = image.width * box['Width']
            height = image.height * box['Height']

            points = (
                        (left, top),
                        (left + width, top),
                        (left + width, top + height),
                        (left, top + height),
                        (left, top)
                    )
            draw.line(points, width=5, fill= '#69f5d9')

            points = (
                (left, top - 50),
                (left + width, top - 50),
                (left + width, top),
                (left, top),
                (left, top - 50)
            )

            draw.line(points, width=5, fill= '#69f5d9')
            draw.text((left + 10, top - 30), label["Name"])
image.show()
