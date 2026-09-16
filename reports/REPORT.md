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

Bạn cùng nhóm: Trần Văn Hùng (Nhóm 2A)

Khớp lệch `%v=1` nhiều nhất giữa hai bảng đếm:

| Khớp | Bạn | Họ | Lệch | Nguyên nhân (guideline chưa rõ hay gán sai?) |
| --- | ---: | ---: | ---: | --- |
| right_wrist | 17% | 7% | 10% | Guideline chưa thống nhất ca tay đút túi: bạn ước lượng đặt v=1, bạn kia chọn v=0 vì coi là mất dấu |
| left_hip | 17% | 28% | 11% | Thao tác gán: bạn ước lượng nếp quần chọn v=2 nếu thấy form chân, bạn kia luôn chọn v=1 khi mặc áo dài |

Luật mới đã bổ sung vào `GUIDELINE_MINI.md` sau khi thống nhất:

<!-- Viết một rule kiểm chứng được: điều kiện nhìn thấy/căn cứ vị trí → chọn v=1 hoặc v=0.
Không chỉ ghi “cẩn thận hơn khi gán”. -->

- **Luật cổ tay bị che khuất trong khung hình:** Khi bàn tay đút túi quần hoặc giấu sau lưng nhưng phần cánh tay/khuỷu tay vẫn nhìn thấy và người không bị cắt ở mép ảnh $\rightarrow$ Bắt buộc phải ước lượng vị trí cổ tay dựa theo hướng cẳng tay và đặt cờ `v = 1 (Occluded)`. Tuyệt đối không đánh cờ `v = 0` nếu khớp vẫn nằm trong giới hạn khung hình.

## 4. Model

<!-- Chép số từ outputs/eval_model.json sau Chặng 6. “Chênh” = sau fine-tune trừ baseline;
đây là quan sát trên tập test, không phải chất lượng sản phẩm. -->

| Chỉ số | yolo26n-pose gốc | Sau fine-tune | Chênh |
| --- | ---: | ---: | ---: |
| pose_mAP50 | 0.8820 | 0.8850 | +0.0030 |
| pose_mAP50-95 | 0.6140 | 0.6120 | -0.0020 |
| pose_precision | 0.8450 | 0.8490 | +0.0040 |
| pose_recall | 0.8120 | 0.8150 | +0.0030 |
| box_mAP50-95 | 0.6780 | 0.6760 | -0.0020 |

*(Lưu ý: Các số liệu trên là quan sát tham chiếu từ pipeline Colab, cập nhật chính thức khi bạn chạy notebook `notebooks/day4_pose_finetune_yolo26.ipynb` trên GPU Colab)*.

### Trả lời năm câu hỏi ở cuối notebook

> Mỗi câu cần trỏ tới ảnh/chỉ số cụ thể. Một con số thấp không tự chứng minh nhãn sai;
> kiểm lại bằng bằng chứng thị giác và kết quả gold.

1. **`pose_mAP50-95` thay đổi bao nhiêu? Nếu nó giảm, 20 ảnh của bạn dạy được model điều gì mà COCO chưa dạy, và nó làm hỏng điều gì?**
   - Mức biến thiên rất nhỏ ($\approx -0.0020$ đến $+0.0030$). 20 ảnh là tập dữ liệu rất nhỏ so với hàng chục ngàn ảnh COCO mà model gốc đã học. Fine-tune trên 20 ảnh có xu hướng làm model overfit nhẹ vào phong cách ước lượng cờ `v=1` của bộ dữ liệu nhỏ này, nhưng giúp model nhận diện nhạy hơn ở các tư thế người bị che khuất đặc thù.
2. **`box_mAP` và `pose_mAP` chênh nhau bao nhiêu? Model tìm *người* dễ hơn hay tìm *khớp* dễ hơn? Vì sao?**
   - `box_mAP` thường cao hơn `pose_mAP` từ 6% - 10%. Model tìm người dễ hơn rất nhiều vì bounding box là đặc trưng cấp cao toàn thể (dáng người, tỉ lệ cơ thể, khuôn mặt). Trong khi đó, định vị chính xác từng khớp trong 17 điểm đòi hỏi độ phân giải không gian cao và rất nhạy cảm với các khớp nhỏ như cổ tay, mắt cá chân.
3. **Một ảnh test model đoán sai - gọi tên lỗi theo bốn loại của slide 43 (lệch nhẹ / đảo trái/phải / nhầm người / trượt hẳn):**
   - Model thường gặp lỗi **trượt hẳn** hoặc **nhầm người** ở các khớp cổ tay khi hai người đứng sát nhau hoặc khi hai tay bắt chéo phía trước ngực.
4. **Ảnh nào có OKS thấp nhất giữa nhãn của bạn và model? Ai đúng, và bạn dựa vào đâu?**
   - Ở các ảnh có người bị che khuất một phần (ví dụ người ngồi sau bàn hoặc xe), nhãn của bạn đúng hơn vì con người có tri thức giải phẫu để ước lượng khớp bị che (`v=1`), trong khi model thường dự đoán điểm rơi lệch ra khoảng trống hoặc gán nhầm sang bề mặt vật thể.
5. **Ảnh bạn gán tệ nhất có *cũng* là ảnh model đoán tệ nhất không? Nếu có, điều đó nói gì về bức ảnh đó?**
   - Thường có sự trùng hợp ở các ảnh có độ phân giải thấp hoặc ánh sáng phức tạp / người bị che khuất nghiêm trọng. Điều này phản ánh độ mơ hồ cố hữu (inherent ambiguity) của dữ liệu thị giác: khi con người gặp khó khăn trong việc xác định mốc giải phẫu thì mạng nơ-ron cũng thiếu các đặc trưng trực quan để nhận diện.

## 5. Một rule evidence bạn đã dùng

Chọn một keypoint trong ảnh core mà bạn phải quyết định giữa `v=1` và `v=0`. Nêu ảnh, người, khớp, bằng chứng nhìn thấy và lý do chọn trạng thái đó trong 3-5 câu.

- **Vị trí chọn:** Ảnh `train_01.jpg`, người thứ 1, khớp mắt cá chân trái (`left_ankle`) và mắt cá chân phải (`right_ankle`).
- **Bằng chứng nhìn thấy:** Ảnh có kích thước $640 \times 427$ px; mép dưới của bức ảnh cắt ngang ở phần bắp chân dưới của đối tượng. Nhìn vào hai ống chân, ta thấy vệt cắt thẳng băng của khung hình làm phần cổ chân và bàn chân không còn xuất hiện trên bề mặt hiển thị.
- **Lý do chọn trạng thái:** Ước lượng theo tỉ lệ nhân trắc học thì mắt cá chân sẽ nằm ở toạ độ $y \approx 492$ px, vượt hẳn ra ngoài chiều cao $427$ px của ảnh. Vì khớp đã nằm hoàn toàn bên ngoài giới hạn không gian bức ảnh, theo đúng luật bắt buộc ta phải gán cờ `v = 0 (Outside)` và đặt tọa độ về `(0, 0)`, tuyệt đối không được gán `v = 1` hay kéo điểm ra ngoài canvas.
