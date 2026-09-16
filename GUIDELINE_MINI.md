# Mini guideline - nhóm: L2-L3 (Nhóm 2A)  |  người gán: Nguyễn Đình Viễn (2A202602148)  |  ngày: 16/09/2026

> Điền file này **trong lúc** gán nhãn, không phải sau khi xong. Mỗi lần bạn dừng lại
> hơn 10 giây để phân vân, đó là một dòng phải ghi vào đây.

## 1. Luật bắt buộc (đã thống nhất cả lớp - không sửa)

- Bộ 17 điểm COCO, đúng tên, đúng thứ tự. Lấy từ file `.SVG` chung.
- Mọi người trong ảnh đều có **đủ 17 điểm**. Điểm không dùng được thì gắn cờ, không xoá.
- Trái/phải tính theo **cơ thể người**, không theo bức ảnh.
- Bị che, còn trong khung -> `v = 1`, **vẫn đặt chấm** ở vị trí ước lượng.
- Ra ngoài mép ảnh -> `v = 0`, **không** đặt chấm.
- Không dùng `Hidden` (`h`) - nó không được lưu vào file.

## 2. Luật của nhóm bạn (phải điền)

| Tình huống | Luật nhóm bạn chọn | Vì sao |
| --- | --- | --- |
| Hông của người mặc quần áo dài | Đặt tại vị trí mấu chuyển lớn xương đùi (ngang đáy thắt lưng / nếp gấp đáy quần), gắn cờ `v = 1` nếu áo trùm qua mông, gắn `v = 2` nếu nhìn rõ form quần ôm sát. | Quần áo dài che phủ hoàn toàn khớp hông thực tế, không có mốc bề mặt nhìn thấy trực diện nên phải dựa vào giải phẫu học cơ thể. |
| Tai bị tóc hoặc mũ bảo hiểm che một phần | Nếu thấy được ít nhất 1/3 vành tai hoặc phần dái tai thì gán `v = 2`. Nếu bị tóc hoặc quai mũ che khuất hoàn toàn thì ước lượng dựa trên đuôi mắt và góc hàm, gán `v = 1`. | Đảm bảo tính nhất quán giữa nhìn thấy thực sự và nội suy theo cấu trúc hộp sọ. |
| Người bị cắt ở mép ảnh (chỉ thấy từ hông trở lên) | Các khớp nằm ngoài biên ảnh (đầu gối, mắt cá chân) bắt buộc gắn cờ `v = 0` và đặt tọa độ `(0, 0)`, không kéo điểm ra ngoài canvas. | Tránh làm sai lệch kích thước bounding box và gây lỗi toạ độ vượt quá `[0, 1]` trong Ultralytics YOLO. |
| Cổ tay nằm sau tay lái / sau thân mình | Vẫn đặt chấm ước lượng dựa theo hướng kéo dài của xương cẳng tay và gắn cờ `v = 1`. | Cổ tay vẫn nằm trọn trong khung hình, model cần học được khả năng suy diễn tư thế khi bị vật thể che khuất. |
| Hai người chồng lên nhau | Gán dứt điểm từng người một (bật/tắt visibility của skeleton kia nếu cần), khớp của người nào thì neo sát vào mốc cơ thể của người đó, bị che thì để `v = 1`. | Tránh lỗi nghiêm trọng "nhầm người" (Lỗi 2 - Slide 46) khi kéo nhầm điểm sang cơ thể của người bên cạnh. |
| Người nhỏ đến mức nào thì không gán nữa | Mọi người có chiều cao bounding box từ 40 pixel trở lên đều phải gán đủ 17 điểm. | Bộ 20 ảnh core đều có kích thước đối tượng đủ lớn để nhận diện dáng người, không được tự ý bỏ sót người. |

## 3. Ba ca mơ hồ đã gặp (bắt buộc, ghi ít nhất 3)

### Ca 1 - ảnh `train_01.jpg`, người thứ `1`, khớp `left_ankle` / `right_ankle`

- Mơ hồ ở chỗ nào: Bức ảnh bị cắt ngang ở bắp chân dưới, mắt cá chân nằm sát mép dưới bức ảnh, phân vân giữa gán `v = 1` (ước lượng chấm sát mép) hay `v = 0` (ngoài khung).
- Bạn quyết thế nào: Quyết định chọn `v = 0 (Outside)` và đặt toạ độ `(0, 0)`.
- Vì sao: Do mép cắt của ảnh đã cắt ngang ống đồng, mắt cá chân nằm hoàn toàn bên ngoài khung hình ($y > 427$ px). Theo luật cốt lõi, điểm ra ngoài biên ảnh bắt buộc là `v = 0`.
- Nếu người khác quyết ngược lại thì model học sai cái gì: Nếu người khác để `v = 1` và chấm sát mép ảnh, model sẽ bị dạy sai rằng mắt cá chân người nằm ngay trên bắp chân, làm méo mó tỉ lệ giải phẫu chân.

### Ca 2 - ảnh `train_15.jpg`, người thứ `1`, khớp `left_shoulder` / `right_shoulder`

- Mơ hồ ở chỗ nào: Người đứng hơi nghiêng và quay mặt về phía trước, rất dễ nhầm lẫn vai bên trái của bức ảnh với vai trái của đối tượng.
- Bạn quyết thế nào: Chọn vai bên phải bức ảnh là `left_shoulder` và vai bên trái bức ảnh là `right_shoulder`.
- Vì sao: Tuân thủ quy tắc số 1: Trái/phải tính theo giải phẫu cơ thể người, không tính theo hướng nhìn của người gán nhãn.
- Nếu người khác quyết ngược lại thì model học sai cái gì: Model sẽ bị lỗi `dao_trai_phai`. Khi áp dụng data augmentation lật ảnh ngang (`fliplr=0.5`), model sẽ bị dạy cái sai hai lần và không bao giờ học được tư thế đúng.

### Ca 3 - ảnh `train_14.jpg`, người thứ `1`, khớp `right_wrist`

- Mơ hồ ở chỗ nào: Hai người đứng sát nhau và tay đan chéo, khó phân biệt cổ tay phải của người thứ nhất hay là của người thứ hai.
- Bạn quyết thế nào: Phóng to 200%, dò theo đường thẳng từ vai phải $\rightarrow$ khuỷu tay phải $\rightarrow$ xác định cổ tay của đúng người đó, gán `v = 1` do bị bàn tay người kia che khuất một phần.
- Vì sao: Để tránh lỗi "nhầm người", mốc xương phải liên tục từ gốc chi đến ngọn chi.
- Nếu người khác quyết ngược lại thì model học sai cái gì: Model sẽ học một bộ xương có tay bị kéo dãn bất thường sang cơ thể người bên cạnh, phá hỏng khả năng phân tách thực thể (instance separation) của pose estimation.

## 4. Sau khi so visibility report với bạn cùng nhóm

- Khớp lệch `%v=1` nhiều nhất: `right_wrist` (bạn `17%` / họ `7%`, lệch `10%`) và `left_hip` (bạn `17%` / họ `28%`, lệch `11%`).
- Nguyên nhân là **guideline chưa rõ** hay **một trong hai bên gán sai**: Chủ yếu do **guideline ban đầu chưa mô tả cụ thể trường hợp tay đút túi quần** (một bên gán `v=1` vì vẫn ước lượng được mốc cổ tay, bên kia tưởng mất dấu nên gán `v=0`).
- Luật mới bổ sung vào mục 2 sau khi thống nhất: *"Khớp còn nằm trong giới hạn khung hình dù bị che khuất bởi túi áo/quần hay thân mình thì bắt buộc ước lượng đặt chấm và gán `v = 1`; cờ `v = 0` chỉ dùng duy nhất khi khớp thực sự bị cắt ra khỏi mép bức ảnh."*
