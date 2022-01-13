#!/usr/bin/python
import json
import os


def process_images():
    # traverse root directory, and list directories as dirs and files as files
    plate_list = []
    cntr = 0
    for root, dirs, files in os.walk("attachments"):
        path = root.split(os.sep)
        print((len(path) - 1) * '---', os.path.basename(root))
        for file in files:
            if file.lower().endswith(('.tiff', '.bmp', '.png', '.jpg', '.jpeg')):
                cntr += 1
                print(str(cntr) + len(path) * '---', file)
                output = os.popen("alpr -c eu -p it -n 2 -j " + os.path.join(root, file)).read()
                try:
                    json_output = json.loads(output)
                    # print(json_output)
                    results: list = json_output['results']
                    if len(results) > 0:
                        #
                        os.rename(os.path.join(root, file), os.path.join("plates/images", file))
                        for result in results:
                            candidates: list = result["candidates"]
                            for c in candidates:
                                plate: dict = {"file": file,
                                               "plate": c["plate"],
                                               "confidence": c["confidence"]}
                                plate_list.append(plate)
                    else:
                        os.remove(os.path.join(root, file))
                except ValueError as ve:
                    os.remove(os.path.join(root, file))
                    print(ve)
            else:
                os.remove(os.path.join(root, file))
    return plate_list
