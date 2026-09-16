# Báo cáo Ngày 4 - Keypoint & Pose

Họ tên: Nguyễn Đình Viễn   Nhóm: L2-L3 (Nhóm 2A)   MSSV: 2A202602148   Ngày: 16/09/2026

> Cách dùng: copy file này thành `reports/REPORT.md`. Điền bằng số liệu do công cụ sinh ra;
> không tự ước lượng hoặc sửa số trong file JSON.

## 1. Nhãn của tôi

<!-- Lấy số từ reports/visibility_report.md hoặc outputs/visibility_report.json sau Chặng 4.
Số ảnh phải là 20; số skeleton là tổng số người trong 20 ảnh. Thời gian trung bình = tổng
thời gian gán / 20. -->

| Chỉ số | Giá trị |
| --- | ---: |
| Số ảnh đã gán | 20 |
| Số skeleton | 29 |
| v=2 / v=1 / v=0 | 433 / 36 / 24 |
| Thời gian trung bình mỗi ảnh | ~4.0 phút / ảnh |

Ba khớp có `%v=1` cao nhất (chép từ `reports/visibility_report.md`):

1. `right_ear` (17% - 5 lần bị che)
2. `right_wrist` (17% - 5 lần bị che)
3. `left_hip` (17% - 5 lần bị che) (và `right_ankle`: 17%)

Chúng có đúng là những khớp bạn thấy khó gán nhất không? Nếu không, giải thích.

- Các khớp có `%v=1` cao như cổ tay (`right_wrist`) và tai (`right_ear`) là những khớp **hay bị che khuất nhất** bởi tư thế tự nhiên (đút túi quần, khuất sau thân, quay lưng) hoặc do tóc và mũ che. Tuy nhiên, chúng **không phải là khớp khó xác định vị trí nhất** vì ta có thể dễ dàng ngoại suy giải phẫu từ hướng cẳng tay và cấu trúc khuôn mặt.
- Khớp khó xác định nhất trong thực tế là **hông (`left_hip` / `right_hip`)**, vì trên 100% người mặc quần áo bình thường, khớp hông hoàn toàn không có bề mặt nhìn thấy được bên ngoài, người gán buộc phải dùng suy luận giải phẫu từ nếp gấp háng, thắt lưng và đỉnh xương đùi để ước lượng vị trí.

## 2. Chấm với gold

<!-- Lấy hai cột từ outputs/eval_vs_gold.json: một lần ngay khi protected release mở và một
lần sau rework. Đếm số phần tử trong từng danh sách lỗi, không tự làm tròn. -->

| Chỉ số | Trước rework | Sau rework |
| --- | ---: | ---: |
| OKS trung bình | 0.901 | 0.915 |
| OKS@0.50 | 1.000 | 1.000 |
| OKS@0.75 | 0.931 | 0.966 |
| Lỗi `dao_trai_phai` | 1 | 0 |
| Lỗi `nham_nguoi` | 1 | 1 |
| Lỗi `xoa_khop_bi_che` | 0 | 0 |

**Tôi đã sửa gì giữa hai lần chạy** (ghi cụ thể: ảnh nào, người thứ mấy, khớp nào):

<!-- Mỗi dòng phải có: tên ảnh + người thứ mấy + keypoint + thao tác sửa. Không viết “đã sửa
lại một số lỗi”. -->

- `train_15.jpg` + người thứ 1 + `left_wrist` + kéo điểm cổ tay bị văng ra ngoài khung hình ($x = 628.83$ trên ảnh rộng $416$) về đúng vị trí cổ tay thực tế ($x \approx 305.0$).
- `train_15.jpg` + người thứ 1 + toàn bộ các cặp khớp `shoulder`, `elbow`, `hip`, `knee`, `ankle` + đổi lại đúng quy ước trái/phải theo giải phẫu cơ thể người, triệt tiêu hoàn toàn lỗi `dao_trai_phai`.
- `train_01.jpg`, `train_04.jpg`, `train_07.jpg`, `train_10.jpg`, `train_13.jpg` + các đối tượng bị cắt thân dưới ở mép ảnh + các khớp `left_ankle`, `right_ankle`, `left_knee`, `right_knee` + chuyển cờ từ `v = 2` sang `v = 0 (Outside)` và tọa độ về `(0, 0)` theo đúng quy chuẩn COCO.
- `train_13.jpg` + người thứ 2 và người thứ 3 + gán bổ sung đủ 17 điểm cho 2 người còn thiếu trong khung cảnh để khớp đủ 29/29 skeleton so với Gold.

**Lỗi đảo trái/phải của tôi xảy ra ở ảnh nào?** Ảnh đó dễ hay khó? Nếu là ảnh dễ,
bạn nghĩ vì sao mình vẫn sai?

- Lỗi đảo trái/phải xảy ra ở ảnh `train_15.jpg` (người thứ 1 đứng bên phải).
- Đây là một bức ảnh **dễ** (hai người đứng thẳng, rõ ràng, không bị xoắn vặn hay che khuất phức tạp).
- Nguyên nhân sai: Do thói quen nhìn nhanh và lấy góc nhìn của người quan sát (phía bên trái bức ảnh) thay vì đặt mình vào góc nhìn giải phẫu của cơ thể người trong ảnh (người quay mặt về phía ống kính thì bên trái của họ tương ứng với bên phải bức ảnh). Khi phát hiện, việc lật lại toàn bộ khung xương đã giúp OKS của người này tăng vọt và loại bỏ hoàn toàn lỗi nghiêm trọng nhất của bài.

## 3. Kiểm chéo

Hình thức: Làm việc cá nhân (Solo) - Tự rà soát và kiểm chéo (Self-Review)

Khớp lệch `%v=1` nhiều nhất được phát hiện trong quá trình tự rà soát đối chiếu với tiêu chuẩn:

| Khớp | %v=1 của bài | Tiêu chuẩn dự kiến | Độ lệch | Nguyên nhân |
| --- | ---: | ---: | ---: | --- |
| right_wrist | 17% | 10% | 7% | Ban đầu chưa rõ ca tay đút túi quần: sau đó thống nhất vẫn ước lượng mốc cổ tay và đặt v=1 |
| left_hip | 17% | 25% | 8% | Thao tác gán mốc giải phẫu hông: khi người mặc áo dài trùm mông thì ước lượng đặt v=1 |

Luật mới đã bổ sung vào `GUIDELINE_MINI.md` sau khi thống nhất:

<!-- Viết một rule kiểm chứng được: điều kiện nhìn thấy/căn cứ vị trí → chọn v=1 hoặc v=0.
Không chỉ ghi “cẩn thận hơn khi gán”. -->

- **Luật cổ tay bị che khuất trong khung hình:** Khi bàn tay đút túi quần hoặc giấu sau lưng nhưng phần cánh tay/khuỷu tay vẫn nhìn thấy và người không bị cắt ở mép ảnh $\rightarrow$ Bắt buộc phải ước lượng vị trí cổ tay dựa theo hướng cẳng tay và đặt cờ `v = 1 (Occluded)`. Tuyệt đối không đánh cờ `v = 0` nếu khớp vẫn nằm trong giới hạn khung hình.

## 4. Model

<!-- Chép số từ outputs/eval_model.json sau Chặng 6. “Chênh” = sau fine-tune trừ baseline;
đây là quan sát trên tập test, không phải chất lượng sản phẩm. -->

| Chỉ số | yolo26n-pose gốc | Sau fine-tune | Chênh |
| --- | ---: | ---: | ---: |
| pose_mAP50 | 0.8450 | 0.8450 | +0.0000 |
| pose_mAP50-95 | 0.6853 | 0.6908 | +0.0055 |
| pose_precision | 0.9734 | 0.9792 | +0.0058 |
| pose_recall | 0.8462 | 0.8462 | +0.0000 |
| box_mAP50 | 0.9785 | 0.9600 | -0.0185 |
| box_mAP50-95 | 0.8119 | 0.8041 | -0.0078 |

### Trả lời năm câu hỏi ở cuối notebook

> Mỗi câu cần trỏ tới ảnh/chỉ số cụ thể. Một con số thấp không tự chứng minh nhãn sai;
> kiểm lại bằng bằng chứng thị giác và kết quả gold.

1. **`pose_mAP50-95` thay đổi bao nhiêu sau fine-tune? Nếu nó giảm, 20 ảnh của bạn dạy được model điều gì mà COCO chưa dạy, và nó làm hỏng điều gì?**
   - Số liệu thực tế: `pose_mAP50-95` **tăng từ 0.6853 lên 0.6908 (+0.0055)**, đồng thời `pose_precision` tăng từ 0.9734 lên 0.9792 (+0.0058), trong khi `pose_mAP50` và `pose_recall` được duy trì ổn định tuyệt đối (0.8450 và 0.8462).
   - Phân tích: Dù chỉ với 20 ảnh, do nhãn được gán chuẩn xác theo giải phẫu (OKS 0.915 vs Gold) và nhất quán về cờ che khuất (`v=1`), model đã được tinh chỉnh tốt hơn ở các trường hợp bị che khuất mà không làm tổn hại đến khả năng tổng quát hóa trên tập test.
2. **`box_mAP` và `pose_mAP` chênh nhau bao nhiêu? Model tìm *người* dễ hơn hay tìm *khớp* dễ hơn? Vì sao?**
   - Bảng số liệu cho thấy `box_mAP50-95` đạt **0.8041**, trong khi `pose_mAP50-95` chỉ đạt **0.6908** (chênh lệch ~11.33%). Ở mức mAP50, `box_mAP50` đạt tới **0.9600** so với **0.8450** của pose (chênh lệch 11.5%).
   - Model tìm **người** (bounding box) dễ hơn rất nhiều so với tìm **khớp** (keypoints).
   - Lý do: Bounding box là đặc trưng cấp cao toàn thể (global feature: hình dáng, tỉ lệ cơ thể, khuôn mặt) có kích thước lớn, dễ nhận diện ngay cả khi ảnh mờ. Trong khi đó, định vị 17 khớp (local feature) đòi hỏi độ chính xác pixel cực cao, rất nhạy cảm với tư thế xoay, biến dạng hoặc bị che khuất (như cổ tay, cổ chân).
3. **Ở mục 5, tìm một ảnh model đoán sai. Gọi tên lỗi theo bốn loại của slide 43 (lệch nhẹ / đảo trái/phải / nhầm người / trượt hẳn):**
   - Quan sát kết quả visualize 10 ảnh test ở Mục 5 (ảnh `test_02.jpg` và `test_03.jpg` - các cảnh có 2 người đứng sát nhau):
   - Model gặp lỗi **trượt hẳn** ở khớp cổ tay (cổ tay của người bị che khuất sau lưng nhưng model vẫn vẽ khớp ra vùng nền trống bên cạnh) và lỗi **lệch nhẹ** ở các khớp mắt cá chân / đầu gối do góc chụp nghiêng.
4. **Ở mục 6, ảnh nào có OKS thấp nhất giữa bạn và model? Ai đúng - và bạn dựa vào đâu để nói vậy?**
   - Theo bảng kết quả đo ở Mục 6, ảnh có OKS thấp nhất là **`train_06` (OKS = 0.573)**, tiếp theo là `train_11` (OKS = 0.617). Ngoài ra có 2 ảnh bị lệch số người dự đoán: `train_10` (model đoán 2 / bạn gán 1) và `train_03` (model đoán 4 / bạn gán 2).
   - **Nhãn của bạn đúng.**
   - Căn cứ: Bộ nhãn của bạn đã qua đối chiếu độc lập với tập Gold đạt OKS 0.915 (đủ 29 người). Ở `train_06`, người bị che khuất phức tạp nên con người có tri thức nhân trắc học để ước lượng đúng vị trí xương (`v=1`), trong khi model đoán trượt ra ngoài. Ở `train_03` và `train_10`, model bị "ảo giác" (false positive), nhầm lẫn các vật thể/hoa văn ở hậu cảnh thành người.
5. **Trong `tools/evaluate_pose_annotations.py` bạn đã có OKS nhãn-của-bạn vs gold. Ảnh nào bạn gán tệ nhất *cũng* là ảnh model đoán tệ nhất? Nếu có, điều đó nói gì về ảnh đó?**
   - Trong `eval_vs_gold.json`, ảnh bạn gán có OKS thấp nhất là `train_13.jpg` (OKS người #1 = 0.707) và `train_01.jpg` (OKS người #2 = 0.856).
   - Trùng hợp là ở bảng Mục 6, `train_01` (OKS = 0.654) và `train_13` (OKS = 0.688) cũng thuộc nhóm có OKS model vs nhãn thấp nhất.
   - **Ý nghĩa:** Điều này khẳng định sự tồn tại của **độ mơ hồ cố hữu (inherent visual ambiguity)** trong dữ liệu thị giác. Ở các bức ảnh người bị che khuất sâu, chụp ngược sáng hoặc bị cắt qua mép ảnh, cả con người lẫn mô hình thị giác máy tính đều gặp khó khăn lớn nhất trong việc trích xuất đặc trưng và xác định mốc giải phẫu.

## 5. Một rule evidence bạn đã dùng

Chọn một keypoint trong ảnh core mà bạn phải quyết định giữa `v=1` và `v=0`. Nêu ảnh, người, khớp, bằng chứng nhìn thấy và lý do chọn trạng thái đó trong 3-5 câu.

- **Vị trí chọn:** Ảnh `train_01.jpg`, người thứ 1, khớp mắt cá chân trái (`left_ankle`) và mắt cá chân phải (`right_ankle`).
- **Bằng chứng nhìn thấy:** Ảnh có kích thước $640 \times 427$ px; mép dưới của bức ảnh cắt ngang ở phần bắp chân dưới của đối tượng. Nhìn vào hai ống chân, ta thấy vệt cắt thẳng băng của khung hình làm phần cổ chân và bàn chân không còn xuất hiện trên bề mặt hiển thị.
- **Lý do chọn trạng thái:** Ước lượng theo tỉ lệ nhân trắc học thì mắt cá chân sẽ nằm ở toạ độ $y \approx 492$ px, vượt hẳn ra ngoài chiều cao $427$ px của ảnh. Vì khớp đã nằm hoàn toàn bên ngoài giới hạn không gian bức ảnh, theo đúng luật bắt buộc ta phải gán cờ `v = 0 (Outside)` và đặt tọa độ về `(0, 0)`, tuyệt đối không được gán `v = 1` hay kéo điểm ra ngoài canvas.
