import os
import numpy as np
import collections
from database import *
Camera = collections.namedtuple(
    "Camera", ["id", "model", "width", "height", "params"])
def read_cameras_text(path):
    """
    see: src/base/reconstruction.cc
        void Reconstruction::WriteCamerasText(const std::string& path)
        void Reconstruction::ReadCacamerasmerasText(const std::string& path)
    """
    cameras = {}
    with open(path, "r") as fid:
        while True:
            line = fid.readline()
            if not line:
                break
            line = line.strip()
            if len(line) > 0 and line[0] != "#":
                elems = line.split()
                # camera_id = int(elems[0])
                name = elems[0]
                print(name)
                model = elems[1]
                width = int(elems[2])
                height = int(elems[3])
                params = np.array(tuple(map(float, elems[4:])))
                cameras[name] = Camera(id=name, model=model,
                                            width=width, height=height,
                                            params=params)
    return cameras
def create_db():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--database_path", default="database.db")
    parser.add_argument("--frame_selected")
    parser.add_argument("--database_intrinsics")
    args = parser.parse_args()
    if os.path.exists(args.database_path):
        print("ERROR: database path already exists -- will not modify it.")
        return

    cameras = read_cameras_text(args.database_intrinsics)
    db = COLMAPDatabase.connect(args.database_path)
    db.create_tables()
    model = 2

    with open(args.frame_selected, "r") as fid:
        while True:
            line = fid.readline()
            if (not line) :
                break
            if len(line) > 0 :
                line = line.strip()
                print("now line::",line)
                # line = line[0]
                print("now line:", line)
                now_camera = cameras[line]
                camera_id = db.add_camera(model, now_camera.width, now_camera.height,now_camera.params) 
                image_id = db.add_image(line, camera_id)   

        print("last line:", line)
        

    db.commit()
    db.close()

if __name__ == "__main__":
    create_db()