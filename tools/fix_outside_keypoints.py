import json
from pathlib import Path

def fix_coco_json(coco_path: Path):
    data = json.loads(coco_path.read_text(encoding="utf-8"))
    images = {img["id"]: img for img in data["images"]}

    fixed_points = 0
    for ann in data["annotations"]:
        img = images.get(ann["image_id"])
        if not img:
            continue
        w, h = img["width"], img["height"]
        kps = ann.get("keypoints", [])
        
        # We don't auto-zero train_15's wrist if user wants to fix train_15 on CVAT,
        # but if we fix all out-of-boundary points in train_01, 04, 07, 10, 13:
        is_train_15 = (img.get("file_name") == "train_15.jpg")
        
        modified = False
        for i in range(17):
            x = kps[i * 3]
            y = kps[i * 3 + 1]
            v = kps[i * 3 + 2]
            
            # For cropped legs (train_01, 04, 07, 10, 13), coordinates are genuinely outside:
            if not is_train_15 and v > 0 and (x < 0 or x > w or y < 0 or y > h):
                kps[i * 3] = 0.0
                kps[i * 3 + 1] = 0.0
                kps[i * 3 + 2] = 0
                fixed_points += 1
                modified = True
                
        if modified:
            ann["keypoints"] = kps

    coco_path.write_text(json.dumps(data, indent=4, ensure_ascii=False), encoding="utf-8")
    print(f"Đã tự động sửa {fixed_points} khớp ngoài khung ảnh thành v=0 trong {coco_path}.")

if __name__ == "__main__":
    fix_coco_json(Path("annotations/coco_keypoints/person_keypoints_default.json"))
