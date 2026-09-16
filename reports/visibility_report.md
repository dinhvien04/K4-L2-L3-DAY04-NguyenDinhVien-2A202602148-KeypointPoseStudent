# Visibility report

- Thư mục nhãn: `dataset\labels\train`
- 20 ảnh, 29 skeleton, trung bình 16.17 khớp có v > 0 mỗi người
- Tổng: v=2 433 | v=1 36 | v=0 24

| # | Khớp | v=2 | v=1 | v=0 | %v=1 |
| ---: | --- | ---: | ---: | ---: | ---: |
| 0 | nose | 28 | 1 | 0 | 3% |
| 1 | left_eye | 28 | 1 | 0 | 3% |
| 2 | right_eye | 27 | 1 | 1 | 3% |
| 3 | left_ear | 26 | 3 | 0 | 10% |
| 4 | right_ear | 23 | 5 | 1 | 17% |
| 5 | left_shoulder | 27 | 2 | 0 | 7% |
| 6 | right_shoulder | 29 | 0 | 0 | 0% |
| 7 | left_elbow | 29 | 0 | 0 | 0% |
| 8 | right_elbow | 29 | 0 | 0 | 0% |
| 9 | left_wrist | 26 | 3 | 0 | 10% |
| 10 | right_wrist | 23 | 5 | 1 | 17% |
| 11 | left_hip | 24 | 5 | 0 | 17% |
| 12 | right_hip | 28 | 1 | 0 | 3% |
| 13 | left_knee | 26 | 0 | 3 | 0% |
| 14 | right_knee | 25 | 0 | 4 | 0% |
| 15 | left_ankle | 18 | 4 | 7 | 14% |
| 16 | right_ankle | 17 | 5 | 7 | 17% |

## Đọc bảng này thế nào

1. Khớp nào có **%v=1 cao**: khớp hay bị che. Cổ tay và hông thường là hai vị trí cần xem lại guideline trước khi kết luận.
2. Khớp nào có **v=0 cao bất thường**: mọi người đang dùng Outside ở chỗ đáng lẽ là Occluded. Đó là lỗi số 3 của slide 46, và nó xoá thẳng khớp đó khỏi bảng điểm OKS.
3. Khi so hai người: **lệch lớn = bất đồng về guideline**, không phải về bức ảnh. Sửa guideline trước, sửa nhãn sau.
