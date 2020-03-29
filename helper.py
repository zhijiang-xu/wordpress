# coding=utf-8
import os
from collections import defaultdict
from functools import reduce
import pprint
import csv
from PIL import Image
from shutil import copyfile
import datetime
from termcolor import cprint


# several constant
max_image_size = 1000 * 1000
main_image_name = "主图.jpg"


def skip_image(file_name):
    """
    忽略一些image, 不把它放到wordpress里
    比如image HW size 太大
    """
    image = Image.open(file_name)
    if reduce(lambda x, y: x * y, image.size) > max_image_size:
        return True
    if ".jpg" not in file_name:
        cprint(f"{file_name} is not jpg format, skip it", "red")
        return True
    return False


def reorder_product_images(files):
    """把product的主图放在前面"""
    tmp = [f for f in files if main_image_name in f]
    if tmp:
        files.remove(tmp[0])
        files = [tmp[0]] + files
    return files


def dir_to_product_category(dir_name):
    """e.g. string "a\b\1.c" will become "b>c"""
    dir_name = dir_name.split(os.sep)
    # 1 remove the root dir since its name is meanless
    dir_name = dir_name[1:]
    assert dir_name, "dir_name should not be null"
    # remove digit in names
    for index, val in enumerate(dir_name):
        if "." in val:
            if "度钨钢圆鼻刀" in val:
                print("hi")
            val = val.split(".")[1]  # remove sequence number, such as "1.c"'s "1."
        dir_name[index] = val
    res = ">".join(dir_name).replace(" ", "")
    return res


def image_link_after_import(file_name):
    """
    after imported, file will be put in directory by importing time,
    such as http://localhost:8080/wp-content/uploads/2020/03/1.jpg
    """
    prefix = "http://localhost:8080/wp-content/uploads"
    date = datetime.datetime.now()
    link = prefix + "/" \
           + str(date.year) + "/" + str(date.month).zfill(2) \
           + "/" + file_name
    return link


def generate_csv(products_images_map, csv_file):
    f = open(csv_file, 'w', encoding="utf-8")
    csv_writer = csv.writer(f, delimiter=',')
    keys = ["ID", "Name", "Categories", "Images", "Regular price"]  # can add "description", "price"
    csv_writer.writerow(keys)
    id = 1
    for product, images in products_images_map.items():
        images = ", ".join([image_link_after_import(i) for i in images])
        name = product.split(">")[1]
        category = product.split(">")[0]
        csv_writer.writerow([str(id), name, category, images, "999999"])
        id += 1

    f.close()

    pass


if __name__ == "__main__":
    image_link_after_import("2.jpg")
