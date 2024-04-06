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
file_df = pd.read_csv('recognition_v1_accessKeys.csv')   # this is Anthony's credentials
# file_df = pd.read_csv('rekognition_v1_accessKeys.csv')      # this is Steve's credentials
access_key_id = file_df['Access key ID'].loc[file_df.index[0]]
secret_access_key = file_df['Secret access key'].loc[file_df.index[0]]
# print(f"access key = {access_key_id}   and secret access key =  {secret_access_key}")

# this client using boto3 is used to communicate with AWS's rekognition programs
# the client is an API -- Application Programming Interface
client = boto3.client('rekognition', region_name='us-east-1', aws_access_key_id=access_key_id,
                      aws_secret_access_key=secret_access_key)

photo = [
    "animals_one_color.jpg",
    "animals_grayscale.jpg",
    "totally_not_an_elephant.jpg",
    "group_of_animals.jpg",
    "five_people.jpg",
    "michel_anthony.jpg",
    "anthony.jpg",
    "anthony_steve.jpg",
    "michael_anthony_lisa.jpg",
    "michael.jpg"]
for i in range(len(photo)):
    look_at_photo = input(f"Would you like to look at {photo[i]}?")
    if look_at_photo == "n":
        continue
    with open(photo[i], 'rb') as image_file:
        source_bytes = image_file.read()

    detect_objects = client.detect_labels(Image={'Bytes': source_bytes})
    # pprint(detect_objects)

    pd.options.display.max_columns = 10
    detected_json_data_df = pd.json_normalize(detect_objects['Labels'])
    # print("The next print uses pprint with depth = 8")
    # pprint(detect_objects, depth=8)

    # print(detected_json_data_df[0:200])

    label_list = []
    boxlist = []
    image = Image.open(io.BytesIO(source_bytes))
    static_image = Image.open(io.BytesIO(source_bytes))
    draw = ImageDraw.Draw(image)

    for label in detect_objects['Labels']:
        # print(label['Name'])
        # print('confidences: ',
        # label['Confidence'])

        for instances in label['Instances']:
            if 'BoundingBox' in instances:
                # if label["Name"] == "Elephant":

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
                draw.line(points, width=5, fill='#69f5d9')

                points = (
                    (left, top - 50),
                    (left + width, top - 50),
                    (left + width, top),
                    (left, top),
                    (left, top - 50)
                )
                if box not in boxlist:
                    draw.line(points, width=5, fill='#69f5d9')
                    draw.text((left + 10, top - 30), label["Name"], fill="#000000")
                    box_name = label["Name"]
                    boxlist.append((box_name, box))
                    box_confidence = label["Confidence"]
                    label_list.append((box_name, box_confidence))
                    # print(boxlist)
    image.show()

    # for item in boxlist:
    #     print(item, "\n")
    label_list.sort()
    for thing in label_list:
        print(thing)

    label_choice = input("Do you want to see a certain label?")
    if label_choice == "y":
        multiple_labels = True
        while multiple_labels:
            choice_loop = True
            while choice_loop:
                different_label = input("Which label do you want to see?").title()
                print(different_label)
                for i in range(len(boxlist)):
                    if different_label in boxlist[i][0]:
                        choice_loop = False
                        break
            print(different_label)
            image = static_image
            draw = ImageDraw.Draw(image)
            # Get the box dimensions from the boxlist for the label chosen
            number_of_items_in_boxlist = len(boxlist)
            print(number_of_items_in_boxlist)
            for item in range(number_of_items_in_boxlist):
                if boxlist[item][0] == different_label:

                    # pprint(boxlist)
                    left = image.width * boxlist[item][1]['Left']
                    top = image.height * boxlist[item][1]['Top']
                    width = image.width * boxlist[item][1]['Width']
                    height = image.height * boxlist[item][1]['Height']
                    points = (
                                (left, top),
                                (left + width, top),
                                (left + width, top + height),
                                (left, top + height),
                                (left, top)
                            )
                    draw.line(points, width=5, fill='#69f5d9')

                    points = (
                        (left, top - 50),
                        (left + width, top - 50),
                        (left + width, top),
                        (left, top),
                        (left, top - 50)
                    )
                    if box not in boxlist:
                        draw.line(points, width=5, fill='#69f5d9')
                        draw.text((left + 10, top - 30), different_label, fill="#000000")
                        box_name = different_label
                        # print(boxlist)
            image.show()
            another_label = input("Do you want to see another label?").lower()
            print(another_label)
            if another_label != "y" and another_label != "yes":
                print("line 157")
                multiple_labels = False
