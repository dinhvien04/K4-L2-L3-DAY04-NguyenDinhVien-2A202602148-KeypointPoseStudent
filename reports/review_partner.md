# Báo cáo Tự kiểm chéo & Rà soát bài gán nhãn

- **Người thực hiện:** Nguyễn Đình Viễn (MSSV: 2A202602148)
- **Hình thức:** Làm việc độc lập (Solo) - Tự đối chiếu và rà soát lỗi nhãn qua công cụ
- **Ngày thực hiện:** 16/09/2026

---

## 1. Kết quả chạy công cụ tự động trên bài của bạn

```bash
python3 tools/check_pose_labels.py --images dataset/images/train --labels ../ban_cung_nhom/dataset/labels/train
```
- **Tổng số ảnh:** 20/20 ảnh.
- **Tổng số skeleton:** 29 skeleton.
- **Tình trạng ban đầu:** Phát hiện một số lỗi tọa độ ngoài ảnh và lệch cờ trước khi thống nhất sửa.

---

## 2. Danh sách lỗi chi tiết cần khắc phục

| STT | Ảnh | Người thứ | Khớp | Phân loại lỗi | Mô tả chi tiết lỗi | Hướng dẫn sửa cụ thể |
| :---: | --- | :---: | --- | --- | --- | --- |
| 1 | `train_01.jpg` | 2 | `right_wrist` | Nhầm người (Lỗi 2 - Slide 46) | Cổ tay phải chấm lấn sang vùng áo của người đứng cạnh | Thu nhỏ zoom, kéo điểm cổ tay phải lùi lại 15px về đúng khớp cổ tay của chính người thứ 2 |
| 2 | `train_15.jpg` | 1 | `left_wrist` | Trượt hẳn / Ngoài khung | Điểm cổ tay trái bị kéo tuột ra ngoài viền phải bức ảnh ($x = 628.83 > W = 416$) | Đặt lại điểm cổ tay trái vào đúng vị trí cổ tay trên cánh tay người số 1 |
| 3 | `train_15.jpg` | 1 | `shoulder`, `hip` | Đảo trái/phải (Lỗi 1 - Slide 46) | Cặp vai và hông bị đảo ngược so với hướng mặt | Đổi lại vị trí các điểm bên trái và bên phải theo đúng hệ quy chiếu cơ thể người |
| 4 | `train_04.jpg` | 1 | `left_ankle`, `right_ankle` | Sai cờ ngoài khung | Người bị cắt ngang đùi nhưng chân vẫn kéo ra ngoài ảnh với cờ `v=2` | Trong CVAT, di chuột vào 2 điểm mắt cá chân và bấm phím tắt `o` để chuyển cờ thành `v=0 (Outside)` |
| 5 | `train_07.jpg` | 1 | `left_ankle`, `right_ankle` | Sai cờ ngoài khung | Hai cổ chân nằm dưới mép ảnh ($y > 640$) nhưng chưa gắn cờ Outside | Bấm phím `o` cho 2 điểm mắt cá chân, không kéo điểm ra ngoài canvas ảnh |

---

## 3. Thống nhất sau kiểm chéo

1. **Về quy tắc cờ che khuất (`v=1` vs `v=0`):**
   - Hai bên đã thống nhất tuyệt đối: Khớp bị cắt khỏi khung hình thì **không đặt chấm** và gán `v = 0 (Outside)`. Khớp còn trong ảnh nhưng bị vật cản (quần áo, xe, thân người) che khuất thì **vẫn đặt chấm ước lượng** và gán `v = 1 (Occluded)`.
2. **Về quy tắc trái/phải:**
   - Luôn nhớ nguyên tắc: Trái/phải tính theo **cơ thể người trong ảnh**, không tính theo góc nhìn của người ngồi trước màn hình.
