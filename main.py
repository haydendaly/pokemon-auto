import os
import re
import json

directory = "./images"
metadata_dir = "./metadata"
readme_file = "README.md"

image_dict = {}

for filename in os.listdir(directory):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp")):
        base = re.match("(.*?)(_([0-9]+))?$", os.path.splitext(filename)[0])
        root, _, _ = base.groups()
        if root not in image_dict:
            image_dict[root] = []
        image_dict[root].append(filename)

new_table_rows = []
for name in sorted(image_dict.keys()):
    images = image_dict[name]
    name_capitalized = " ".join([word.capitalize()
                                for word in name.split("_")])
    images_md = ''.join(
        [f'<img src="https://cdn.jsdelivr.net/gh/haydendaly/pokemon-auto/images/{image}" width="400" alt="{name_capitalized}"><br>' for image in images])

    metadata_file = f"{metadata_dir}/{name}.json"
    name_with_link = name_capitalized
    description = ""
    attribution = ""
    if os.path.exists(metadata_file):
        with open(metadata_file, "r") as json_file:
            metadata = json.load(json_file)
            url = metadata.get("url", "")
            if url != "":
                name_with_link = f"[{name_capitalized}]({url})"
            description = metadata.get("description", "")
            attribution_data = metadata.get("attribution", None)

            if attribution_data:
                attribution_name = attribution_data.get("name", "")
                attribution_url = attribution_data.get("url", "")

                if attribution_url != "":
                    attribution = f"[{attribution_name}]({attribution_url})"
                else:
                    attribution = attribution_name

    table_row = f'| {name_with_link} |<br> {images_md} | {description} | {attribution} |\n'
    new_table_rows.append(table_row)

with open(readme_file, "r") as file:
    lines = file.readlines()

autographs_index = next(i for i, line in enumerate(
    lines) if line.strip() == "## Autographs")
table_end_index = next(i for i, line in enumerate(
    lines[autographs_index:]) if line.strip() == "") + autographs_index

lines = lines[:autographs_index + 4] + new_table_rows + ["\n"]

with open(readme_file, "w") as file:
    file.writelines(lines)
