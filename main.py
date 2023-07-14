import os
import re
import json
import time
import shutil

directory = "./images"
metadata_dir = "./metadata"
readme_file = "README.md"
out_file = "OUT.md"

image_dict = {}
metadata_dict = {}

for filename in os.listdir(directory):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp")):
        base = re.match("(.*?)(_([0-9]+))?$", os.path.splitext(filename)[0])
        root, _, _ = base.groups()
        if root not in image_dict:
            image_dict[root] = []
        image_dict[root].append(filename)

for file in os.listdir(metadata_dir):
    if file.lower().endswith(".json"):
        base, _ = os.path.splitext(file)
        metadata_dict[base] = file

names = sorted(set(image_dict.keys()).union(metadata_dict.keys()))

time_stamp = str(int(time.time()))

out_img_dir = './out_images'
if not os.path.exists(out_img_dir):
    os.makedirs(out_img_dir)

for filename in os.listdir(out_img_dir):
    file_path = os.path.join(out_img_dir, filename)
    if os.path.getmtime(file_path) < time.time() - 1 * 86400:
        os.remove(file_path)

new_readme_rows = []
new_out_rows = []
for name in names:
    images = image_dict.get(name, [])
    name_capitalized = " ".join([word.capitalize()
                                for word in name.split("_")])

    out_images_md, readme_images_md = '', ''
    for image in images:
        # Copy and rename image
        src_file = os.path.join(directory, image)
        dst_file = os.path.join(out_img_dir, time_stamp+'_'+image)
        shutil.copy(src_file, dst_file)

        out_images_md += f'<img src="https://cdn.statically.io/gh/haydendaly/pokemon-auto@main/{dst_file}" width="400" alt="{name_capitalized}"><br>'
        readme_images_md += f'<img src="{dst_file}" width="400" alt="{name_capitalized}"><br>'

    metadata_file = f"{metadata_dir}/{name}.json"

    name_with_link = name_capitalized
    description = ""
    attribution = ""

    if name in metadata_dict:
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

    readme_row = f'| {name_with_link} |{readme_images_md} | {description} | {attribution} |\n'
    new_readme_rows.append(readme_row)

    out_row = f'| {name_with_link} |{out_images_md} | {description} | {attribution} |\n'
    new_out_rows.append(out_row)

with open(readme_file, "r") as file:
    lines = file.readlines()

autographs_index = next(i for i, line in enumerate(
    lines) if line.strip() == "## Autographs")
table_end_index = next(i for i, line in enumerate(
    lines[autographs_index:]) if line.strip() == "") + autographs_index

readme_lines = lines[:autographs_index + 4] + new_readme_rows + ["\n"]

with open(readme_file, "w") as file:
    file.writelines(readme_lines)

# write out file:
with open(out_file, "w") as file:
    file.writelines(new_out_rows)
