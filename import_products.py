# coding=utf-8
from helper import *


def generate_csv_and_images_to_import(input_dir, result_dir, csv_name):
    # 把有目录层次的产品图片变成单层目录(因为wordpress的import只支持单层目录)
    # 变成单层目录的方法就是把目录名加到image的名字里
    # 同时增加产品信息到CSV里, 从而能被import到wordpress
    # import到wordpress的目录是根据时间定的 wp-contents/uploads/年份/月份, e.g. 2020/03
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)

    products_files_map = defaultdict(list)
    for root, dirs, files in os.walk(input_dir):
        if files:
            product_category = dir_to_product_category(root)
            product_files = []
            for f in files:
                full_path = os.path.join(root, f)
                if not skip_image(full_path):
                    product_files.append(full_path)
            products_files_map[product_category] = reorder_product_images(product_files)

    pprint.pprint(list(products_files_map.keys()))
    pprint.pprint(products_files_map)

    # 1 generate directory to be imported
    products_images_map = defaultdict(list)
    for product, files in products_files_map.items():
        for f in files:
            image_name = os.path.basename(f)
            new_image_name = "c"+product.replace(">", "a") + image_name.strip(".jpg") + "end.jpg"
            new_file_name = os.path.join(result_dir, new_image_name)
            copyfile(f, new_file_name)
            products_images_map[product].append(new_image_name)

    # 2 generate csv file
    generate_csv(products_images_map, csv_name)


if __name__ == "__main__":
    csv_name = "res.txt"
    result_dir = "product_images_to_import"
    input_dir = "product_images"
    generate_csv_and_images_to_import(input_dir, result_dir, csv_name)
    print(f"generate csv and product images in {csv_name} and {result_dir} ")
