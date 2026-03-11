import os
import shutil


def copystatic():
    src_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(src_dir)

    static_path = os.path.join(root_dir, "static")
    public_path = os.path.join(root_dir, "public")

    if not os.path.exists(public_path):
        os.mkdir(public_path)
    else:
        print("Deleting public directory...")
        shutil.rmtree(public_path)
        os.mkdir(public_path)

    if not os.path.exists(static_path):
        raise Exception(f"No static folder exists with this path: {static_path}")

    statis_files = os.listdir(static_path)
    print("Copying static files to public directory...")
    copy_recursion(static_path, public_path, statis_files)


def copy_recursion(static_path, public_path, static_files):
    if len(static_files) == 0:
        raise Exception("No files to copy")

    for file in static_files:
        file_path = os.path.join(static_path, file)
        print(f" * {file_path} -> {public_path}")
        if os.path.isfile(file_path):
            shutil.copy2(file_path, public_path)
        else:
            subfolder_path = os.path.join(public_path, file)
            os.mkdir(subfolder_path)
            copy_recursion(file_path, subfolder_path, os.listdir(file_path))

    return
