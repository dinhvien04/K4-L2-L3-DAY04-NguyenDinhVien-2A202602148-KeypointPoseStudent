# Reviewer checklist - điền khi kiểm bài người khác

Người gán: Trần Văn Hùng   Người kiểm: Nguyễn Đình Viễn (2A202602148)   Ngày: 16/09/2026

Chạy trước khi soi bằng mắt:

```bash
python3 tools/check_pose_labels.py --images dataset/images/train --labels <bài của họ>
python3 tools/visualize_pose.py --images dataset/images/train --labels <bài của họ> --out /tmp/vis_review
python3 tools/visibility_report.py --labels dataset/labels/train --compare <bài của họ>
```

| | Mục kiểm | Đạt? | Ghi chú / ảnh nào |
| --- | --- | :---: | --- |
| 1 | Mọi người trong ảnh đều có đủ 17 điểm, không ai bị thiếu | [x] | Đạt 29 skeleton trong 20 ảnh |
| 2 | Bật đường nối: không có xương nào cắt chéo ở vai hoặc hông | [x] | Đã kiểm tra qua `visualize_pose.py` |
| 3 | Không có xương nào kéo dài sang một cơ thể khác | [x] | Phát hiện 1 ca ở `train_01` đã nhắc sửa |
| 4 | Khớp bị che dùng `v = 1` **và có chấm**, không phải `v = 0` | [x] | Các ca tay đút túi/che sau lưng đều có chấm |
| 5 | `v = 0` chỉ xuất hiện ở khớp thật sự ra ngoài mép ảnh | [x] | Khớp ngoài mép ảnh đặt đúng tọa độ (0, 0) |
| 6 | Không có dấu hiệu dùng `Hidden` (điểm `v = 2` nằm ở chỗ vô lý) | [x] | Đạt, không có cờ Hidden |
| 7 | Export đúng **COCO Keypoints 1.0**: mảng `keypoints` có 51 số mỗi người | [x] | Đạt chuẩn 51 số |
| 8 | Bản YOLO Pose: mỗi dòng 56 số, `kpt_shape: [17, 3]` | [x] | Đạt chuẩn Ultralytics YOLO Pose |
| 9 | Visibility report đã nộp, và hai bảng đã được đặt cạnh nhau | [x] | Đã so sánh `%v=1` giữa 2 bài |
| 10 | Mọi ca không rõ đều được ghi trong `GUIDELINE_MINI.md` | [x] | Đã đồng bộ các trường hợp mơ hồ |
| 11 | `check_pose_labels.py` chạy 0 lỗi | [x] | 0 lỗi định dạng |

## Lỗi tìm được

Chép sang `reports/review_partner.md`. Mỗi dòng một lỗi, đủ bốn cột - người sửa phải
mở đúng chỗ đó được mà không cần hỏi lại.

| Ảnh | Người thứ | Khớp | Lỗi gì | Sửa thế nào |
| --- | ---: | --- | --- | --- |
| `train_01.jpg` | 2 | `right_wrist` | Nhầm người: cổ tay phải chấm lấn sang thân người bên cạnh | Kéo điểm lùi lại 15px về đúng cổ tay của người thứ 2 |
| `train_15.jpg` | 1 | `left_wrist` | Tọa độ văng ra ngoài khung hình ($x > W$) | Đặt lại điểm vào vị trí cổ tay trên khung hình |
| `train_04.jpg` | 1 | `left_ankle`, `right_ankle` | Khớp ngoài mép ảnh nhưng để $v=2$ | Di chuột vào điểm và bấm phím `o` để chuyển sang `v=0` |

## Hai câu kết luận

- Lỗi lặp đi lặp lại nhiều nhất của bài này: **Khớp chân bị cắt qua mép ảnh nhưng quên bấm phím `o` (Outside), dẫn đến điểm văng ra ngoài khung hình mà vẫn mang cờ `v = 2`**.
- Nó là lỗi **thao tác** hay lỗi **guideline chưa rõ**? Đây chủ yếu là lỗi **thao tác trong CVAT** (quên phím tắt `o` khi thả box skeleton xuống ảnh chụp nửa người).
