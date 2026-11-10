# Phân tích phản biện và chiến lược phản hồi

## Phạm vi tài liệu

Tài liệu này là **hướng dẫn chiến lược phản hồi**, không phải thư phản biện hoàn chỉnh để sao chép nguyên văn. Mục tiêu là giúp tác giả quyết định việc nào cần sửa bản thảo, việc nào bắt buộc phải có bằng chứng mới và cách trả lời từng quan ngại một cách ngắn gọn, tôn trọng, có thể kiểm chứng.

### Nguồn đầu vào

- `REVIEW_AND_REVISION_ROADMAP.md`: toàn bộ nhận xét phản biện và lộ trình xử lý.
- `AUTHOR_GUIDELINES_REVIEW_CHECKLIST.md`: yêu cầu của tạp chí và giới hạn bổ sung **không quá 15 trang**.
- Bản thảo hiện có: kết quả mô phỏng, gồm PPO và Carrot-Following (CF), được sử dụng làm bằng chứng nền hiện hữu.

### Nguyên tắc trung thực

- Không đưa số liệu, kết quả thí nghiệm, thông tin cấu hình hoặc trích dẫn chưa kiểm tra vào thư phản hồi.
- Mọi hạng mục cần kiểm tra từ mã nguồn, log, cấu hình hoặc thí nghiệm mới được gắn **[TO VERIFY]**.
- Không trả lời một yêu cầu về bằng chứng thực nghiệm chỉ bằng lời hứa “future work”.
- Không dùng các câu phòng thủ như “reviewer misunderstood”, “the issue is trivial”, hoặc “the method is clearly superior”.

## 1. Hồ sơ tâm thế phản biện

### Phân loại

- **Nhóm chính:** Phản biện xây dựng, cụ thể (*Precise Constructive*).
- **Độ tin cậy:** Cao.
- **Nhóm phụ:** Hoài nghi vừa phải về bằng chứng thực nghiệm và phạm vi kết luận.

### Dấu hiệu nhận diện

| Tín hiệu | Mức độ | Bằng chứng từ nhận xét |
|---|---:|---|
| Tính xây dựng | 5/5 | Đưa ra các thí nghiệm cụ thể: giới hạn vận tốc tương đương, baseline thứ hai, ablation, nhiều seed. |
| Tính cụ thể | 5/5 | Chỉ rõ Section 3/4, Table I/II, Fig. 2/3, các phương trình và tham số cần bổ sung. |
| Tính khả thi | 5/5 | Nêu rõ cần báo cáo `L`, seed, mini-batch, mô tả controller, quỹ đạo và nhiễu/gió. |
| Mức độ nghiêm trọng | 4/5 | Khuyến nghị **Major Revision**; cho rằng bằng chứng hiện tại chưa đủ cho kết luận vượt trội. |
| Hoài nghi | 4/5 | Nhấn mạnh phép so sánh PPO–CF không công bằng, độ tin cậy seed chưa được chứng minh và novelty chưa được kiểm chứng. |
| Tính gay gắt | 2/5 | Vẫn công nhận chủ đề hợp lý, trình bày rõ ràng và tác giả đã nêu trung thực một số hạn chế. |

### Hàm ý chiến lược

Phản biện này có khả năng được thuyết phục bởi phản hồi **có cấu trúc, bám sát vị trí sửa trong bài và đi kèm bằng chứng định lượng**. Không nên dành nhiều dung lượng để biện hộ cho thiết kế hiện tại. Với các quan ngại về baseline, ablation, seed và generalization, chỉ giải thích bằng lời không đủ.

## 2. Chiến lược tổng thể

### 2.1. Mục tiêu phản hồi thực tế

1. Chuyển định vị bài báo từ “PPO vượt trội/tổng quát” thành **một nghiên cứu mô phỏng có kiểm soát về điều khiển vận tốc cấp cao cho bám chuỗi waypoint**.
2. Cung cấp ít nhất một gói bằng chứng trực tiếp cho ba rủi ro lớn nhất: **công bằng PPO–CF**, **đóng góp của waypoint kế tiếp/reward**, và **độ tin cậy qua các seed**.
3. Bổ sung mô tả đủ tái lập trước khi yêu cầu người phản biện tin vào các kết quả mới.
4. Sửa các lỗi hình thức và trích dẫn như điều kiện cần, nhưng không trình bày chúng như cách giải quyết Major Revision.

### 2.2. Thứ tự triển khai nên dùng

1. **Chốt sự thật có thể xác minh:** xem mã nguồn, log và cấu hình để xác nhận dữ liệu huấn luyện, seed, bộ điều khiển trong, tham số PPO, `L`, quỹ đạo, state normalization và cách xử lý waypoint cuối.
2. **Chốt protocol mới trước khi chạy:** cùng giới hạn vận tốc, cùng quỹ đạo, cùng điều kiện khởi tạo, cùng metric và quy tắc tuning baseline.
3. **Chạy các thí nghiệm quyết định:** công bằng PPO–CF, ablation waypoint kế tiếp, ablation reward, nhiều seed; sau đó mới cân nhắc baseline thứ hai và nhiễu/quỹ đạo mới.
4. **Cập nhật bản thảo đồng bộ:** phương pháp → bảng/hình → kết quả → thảo luận → kết luận → tóm tắt.
5. **Viết thư phản hồi cuối:** từng mục theo cấu trúc *ghi nhận → hành động → bằng chứng → vị trí sửa*.

### 2.3. Ưu tiên bằng chứng

| Mức ưu tiên | Hạng mục | Lý do | Điều kiện để phản hồi thuyết phục |
|---|---|---|---|
| P0 | So sánh PPO–CF công bằng | Là phản biện trực tiếp đối với kết luận về thời gian và hiệu quả | Giới hạn vận tốc tương đương, `L` của CF, protocol tuning và số liệu chạy lại |
| P0 | Ablation waypoint kế tiếp và reward | Liên quan trực tiếp đến novelty và cơ chế phương pháp | Cùng điều kiện huấn luyện/đánh giá; bảng định lượng, không chỉ hình minh họa |
| P0 | Nhiều training seed | SD hiện tại không phản ánh bất định khi huấn luyện | Nhiều policy độc lập, báo cáo trung bình/độ lệch chuẩn và số seed |
| P1 | Baseline thứ hai | CF đơn lẻ chưa đủ cho định vị nghiên cứu | Một baseline phù hợp, cấu hình/tuning minh bạch |
| P1 | Quỹ đạo mới và nhiễu/gió | Là bằng chứng cho giới hạn/generalization | Kịch bản tách biệt, mô tả nhiễu/gió và kết luận được thu hẹp đúng mức |
| P1 | Tái lập và ký hiệu | Cần để người phản biện đánh giá đúng protocol | Thông tin có kiểm chứng từ mã nguồn/log và phương trình nhất quán |
| P2 | Chỉnh hình thức/citation | Bắt buộc cho chất lượng trình bày nhưng không thay thế bằng chứng | Nêu ngắn gọn các vị trí đã sửa |

### 2.4. Ràng buộc của tạp chí và 15 trang

- Bản thảo phải dùng để làm bằng chứng, không phải ghi nhật ký tất cả lần chạy. Chỉ giữ trong bài chính các bảng/hình quyết định cho P0/P1.
- Ưu tiên **một bảng tổng hợp** cho so sánh công bằng và baseline, **một bảng ablation**, và **một bảng hoặc biểu đồ nhiều seed** thay vì nhiều bảng lặp số liệu.
- Rút gọn phần giới thiệu, diễn giải lặp lại và mô tả không phục vụ tái lập để dành chỗ cho protocol và kết quả mới.
- Tóm tắt phải trong 150–250 từ, không có trích dẫn, và tối đa sáu từ khóa. Số liệu trong tóm tắt chỉ được cập nhật sau khi chốt kết quả cuối cùng.
- Hình/bảng phải tuân thủ quy tắc định dạng của tạp chí; không làm nhỏ chữ, co hình hoặc thay lề chỉ để đạt 15 trang.

## 3. Danh mục quan ngại của phản biện

| ID | Loại quan ngại | Tóm tắt | Cần thí nghiệm mới? |
|---|---|---|---|
| R1.C1 | novelty + writing_clarity | Research gap PPO và khác biệt thực sự của bài chưa rõ | Không, nhưng cần literature review; ablation cho claim novelty |
| R1.C2 | scope_claim | So sánh với điều khiển cổ điển và ý nghĩa thực tiễn bị diễn giải quá mạnh | Không; cần thu hẹp claim |
| R1.C3 | evidence_gap | Môi trường huấn luyện, quỹ đạo và điều kiện đầu chưa đủ tái lập | Không nếu log/mã có sẵn |
| R1.C4 | baseline_fairness | PPO–CF không cùng giới hạn vận tốc; `L` chưa rõ | Có |
| R1.C5 | baseline_fairness | Chỉ có một baseline | Có, trừ khi có lý do kỹ thuật đã kiểm chứng để giới hạn scope |
| R1.C6 | theory + evidence_gap | RMSE/MAE hiện là sai số ngang, không đo tiến độ theo thời gian | Có thể; tối thiểu cần diễn giải lại đúng phạm vi |
| R1.C7 | novelty + evidence_gap | Next-waypoint state và từng thành phần reward chưa được ablation | Có |
| R1.C8 | scope_claim + evidence_gap | Thời gian hoàn thành bị nhiễu bởi tốc độ, episode và terminal reward | Có để duy trì claim về thời gian; nếu không phải rút claim |
| R1.C9 | evidence_gap | 10 rollout của một policy không thể hiện biến thiên training seed | Có |
| R1.C10 | writing_clarity | Trích dẫn công cụ/phương pháp, nguồn CF và định dạng tài liệu chưa đầy đủ | Không; cần xác minh thư mục |
| R1.C11 | scope_claim + writing_clarity | Thuật ngữ, tiêu đề, abstract và phạm vi “in simulation” cần khớp bằng chứng | Không |
| R1.C12 | theory + writing_clarity | Công thức, ký hiệu, an toàn, waypoint cuối và hệ số reward chưa rõ | Có thể cần kiểm tra code; không tự suy đoán |
| R1.C13 | evidence_gap | Thiếu hyperparameter PPO, flight controller, quỹ đạo, yaw handling | Không nếu cấu hình/log còn tồn tại |
| R1.C14 | evidence_gap | Generalization: quỹ đạo khác, nhiễu/gió, giới hạn mô phỏng | Có nếu muốn tuyên bố robustness/generalization |
| R1.C15 | writing_clarity | Lỗi bảng, caption, đoạn lặp và Fig. 3/`θ_e` | Không |

## 4. Hướng dẫn theo từng quan ngại

### R1.C1 — Research gap PPO và định vị tính mới

- **Loại:** `novelty` + `writing_clarity`.
- **Ưu tiên chiến lược:** `direct_address`, `paper_grounding`, `specific_evidence`, `controlled_concession`.
- **Mẫu phản hồi phù hợp:** A kết hợp C.
- **Điểm cần ghi nhận:** PPO và kiến trúc RL cấp cao/flight-controller cấp thấp không phải là điểm mới tự thân.
- **Hành động trong bản thảo:**
  - Bổ sung tổng quan có chọn lọc về PPO cho quadcopter hoặc bám đường/waypoint tương tự.
  - Thêm đoạn đối chiếu rõ: phần nào đã phổ biến, phần nào bài này kiểm tra.
  - Không gọi next-waypoint state là đóng góp đã được chứng minh nếu chưa có ablation.
- **Bằng chứng cần có:** bảng đối chiếu tài liệu–phương pháp trong Introduction hoặc phụ lục ngắn; kết quả ablation ở R1.C7 nếu vẫn nêu next-waypoint state là đóng góp.
- **Cấu trúc phản hồi:** ghi nhận thiếu research gap → chỉ rõ nghiên cứu PPO được bổ sung và vị trí → nêu claim đã thu hẹp → dẫn chiếu ablation nếu có.
- **Tránh:** “PPO chưa từng được áp dụng” hoặc “state 15 chiều là hoàn toàn mới” khi chưa có tổng quan kiểm chứng.

### R1.C2 — Phạm vi thực tiễn và so sánh với điều khiển cổ điển

- **Loại:** `scope_claim`.
- **Ưu tiên chiến lược:** `controlled_concession`, `clarification_quality`, `paper_grounding`.
- **Mẫu phản hồi phù hợp:** C.
- **Điểm cần ghi nhận:** PPO vẫn phụ thuộc flight controller và có thể phải huấn luyện lại khi cấu hình thay đổi; kết quả chỉ là mô phỏng, chưa có noise, delay, wind hoặc thử nghiệm thật.
- **Hành động trong bản thảo:** thay các phát biểu tổng quát bằng định vị “feasibility in ProjectAirSim under the investigated conditions”; đưa hạn chế vào Introduction, Discussion và Conclusion.
- **Bằng chứng hiện có có thể dùng:** bản thảo hiện đã thừa nhận khác biệt giới hạn vận tốc và giới hạn mô phỏng; cần cập nhật vị trí chính xác sau khi sửa **[TO VERIFY]**.
- **Cấu trúc phản hồi:** công nhận giới hạn → nêu chính xác các claim đã thu hẹp → nêu ranh giới đóng góp còn lại.
- **Tránh:** hứa hẹn triển khai quadcopter thật nếu không có thí nghiệm đó.

### R1.C3 — Mô tả môi trường huấn luyện và dữ liệu đánh giá

- **Loại:** `evidence_gap`.
- **Ưu tiên chiến lược:** `clarification_quality`, `paper_grounding`, `specific_evidence`.
- **Mẫu phản hồi phù hợp:** A.
- **Hành động cần thiết:** xác minh từ code/log và ghi rõ quỹ đạo huấn luyện, tập waypoint, điều kiện đầu, randomization, và việc quỹ đạo xoắn ốc đánh giá có nằm trong training hay không.
- **Bằng chứng cần có:** mô tả protocol, bảng cấu hình hoặc sơ đồ tạo quỹ đạo; mỗi thông số phải có nguồn kiểm tra được **[TO VERIFY]**.
- **Cấu trúc phản hồi:** nêu từng thông tin mới được bổ sung → chỉ vị trí Section/Table → phát biểu generalization được điều chỉnh theo kết quả xác minh.
- **Tránh:** gọi quỹ đạo đánh giá là “unseen” nếu chưa kiểm tra tập huấn luyện.

### R1.C4 — Công bằng của so sánh PPO–CF

- **Loại:** `baseline_fairness`.
- **Ưu tiên chiến lược:** `new_experiment_strength`, `specific_evidence`, `paper_grounding`, `direct_address`.
- **Mẫu phản hồi phù hợp:** B.
- **Điểm cần ghi nhận:** CF có tốc độ 1.5 m/s trong khi PPO bị chặn theo từng trục ±3 m/s; kết quả completion time hiện tại không cô lập chiến lược điều khiển.
- **Thí nghiệm tối thiểu:**
  1. Chọn một luật giới hạn vận tốc chung, ghi rõ độ lớn hay giới hạn từng trục.
  2. Công bố look-ahead distance `L` của CF và tiêu chí chọn/tuning `L`.
  3. Dùng cùng quỹ đạo, điều kiện đầu, episode protocol, metric và cách tính sai số cho hai phương pháp.
  4. Báo cáo completion time, RMSE, MAE và tỷ lệ hoàn thành sau khi chạy lại.
- **Bằng chứng trả lời:** bảng mới với từng phương pháp/cấu hình; thông số `L`; vị trí bảng/hình trong bài **[TO VERIFY]**.
- **Cấu trúc phản hồi:** đồng ý đây là confound → mô tả protocol mới → báo cáo số liệu thật → giới hạn kết luận chỉ trong điều kiện đã kiểm soát.
- **Tránh:** dùng lại các số 16.91 s và 24.63 s để bảo vệ ưu thế tốc độ; các số đó thuộc cấu hình không tương đương.

### R1.C5 — Thiếu baseline thứ hai

- **Loại:** `baseline_fairness`.
- **Ưu tiên chiến lược:** `new_experiment_strength`, `specific_evidence`, `controlled_concession`.
- **Mẫu phản hồi phù hợp:** B; nếu không thể bổ sung, C.
- **Khuyến nghị thực hiện:** chọn **một** baseline bổ sung khả thi và có liên hệ trực tiếp với scope (ví dụ PID/LQR/MPC hoặc một DRL baseline). Đừng mở rộng sang tất cả baseline được nhắc trong Introduction.
- **Protocol:** mô tả cấu hình, quy tắc tuning, cùng quỹ đạo/vehicle/environment và giới hạn vận tốc tương đương khi có thể.
- **Nếu không thể thực hiện:** không tranh luận rằng CF là đủ. Thu hẹp bài thành feasibility comparison against one geometric reference method, bỏ mọi claim bao quát về superiority; đây là phương án rủi ro cao và có thể không đáp ứng Major Revision.
- **Tránh:** so sánh với một baseline được tinh chỉnh sơ sài hoặc không ghi protocol tuning.

### R1.C6 — Ý nghĩa của RMSE/MAE và tiến độ theo thời gian

- **Loại:** `theory` + `evidence_gap`.
- **Ưu tiên chiến lược:** `clarification_quality`, `controlled_concession`, `specific_evidence`.
- **Mẫu phản hồi phù hợp:** A kết hợp C; B nếu bổ sung metric thời gian.
- **Điểm cần ghi nhận:** metric hiện tại là khoảng cách đến điểm gần nhất trên polyline, đo lệch ngang chứ không đo trajectory tracking được tham số hóa theo thời gian.
- **Hành động tối thiểu:** sửa định nghĩa metric; thay “trajectory-tracking accuracy” bằng thuật ngữ chính xác hơn; không dùng RMSE/MAE hiện tại để khẳng định bám đúng tiến độ.
- **Hành động mạnh hơn:** bổ sung metric tiến độ theo thời gian hoặc dọc cung quỹ đạo; chỉ làm nếu định nghĩa, dữ liệu tham chiếu và tính toán có thể kiểm chứng **[TO VERIFY]**.
- **Cấu trúc phản hồi:** xác nhận phạm vi metric → chỉ rõ phần định nghĩa/Discussion đã sửa → nếu có metric mới, báo cáo số liệu mới và tác động đến kết luận.
- **Tránh:** đổi tên metric nhưng vẫn diễn giải như accuracy theo thời gian.

### R1.C7 — Ablation cho waypoint kế tiếp và reward

- **Loại:** `novelty` + `evidence_gap`.
- **Ưu tiên chiến lược:** `new_experiment_strength`, `specific_evidence`, `paper_grounding`.
- **Mẫu phản hồi phù hợp:** B.
- **Thí nghiệm waypoint kế tiếp:** loại riêng sáu thành phần lỗi đến waypoint kế tiếp, giữ kiến trúc, tổng budget, seed, điều kiện huấn luyện và đánh giá giống cấu hình đầy đủ.
- **Thí nghiệm reward:** dùng reward đầy đủ làm mốc; loại từng thành phần theo protocol có kiểm soát hoặc xác định trước một bộ ablation rõ ràng.
- **Chỉ số cần báo cáo:** success/waypoint completion, tracking/path error, điều kiện an toàn, thời gian và chỉ số mượt nếu có; nêu rõ hạng mục nào được đo thực sự **[TO VERIFY]**.
- **Kết quả cần xuất hiện:** một bảng ablation tổng hợp trong bài chính, mô tả ngắn protocol, và thảo luận chỉ kết luận ở mức số liệu cho phép.
- **Tránh:** chỉ đưa đường bay đại diện; suy luận contribution từ việc “reward có vẻ dày hơn”; so sánh các cấu hình với seed/budget khác nhau.

### R1.C8 — Completion time bị nhiễu bởi speed limit, episode và terminal reward

- **Loại:** `scope_claim` + `evidence_gap`.
- **Ưu tiên chiến lược:** `controlled_concession`, `new_experiment_strength`, `specific_evidence`.
- **Mẫu phản hồi phù hợp:** B hoặc C.
- **Hành động ngay:** bỏ/thu hẹp claim “PPO is faster” dựa trên setup cũ.
- **Hành động cần để giữ claim thời gian:** dùng thí nghiệm công bằng R1.C4; phân tích role của 400 steps/20 s và terminal reward phụ thuộc số bước còn lại. Nếu sửa reward hoặc episode thì phải train/evaluate lại.
- **Cấu trúc phản hồi:** phân biệt rõ kết quả cũ là cấu hình triển khai, không phải superiority; cung cấp kết quả protocol mới nếu đã có.
- **Tránh:** lập luận rằng PPO được “thiết kế để nhanh” như bằng chứng cho ưu thế thuật toán.

### R1.C9 — Độ tin cậy thống kê và nhiều seed

- **Loại:** `evidence_gap`.
- **Ưu tiên chiến lược:** `new_experiment_strength`, `specific_evidence`, `clarification_quality`.
- **Mẫu phản hồi phù hợp:** B.
- **Thí nghiệm cần có:** huấn luyện nhiều policy với random seed độc lập; đánh giá từng policy trên cùng scenario; phân biệt variability của training với variability của rollout cho cùng policy.
- **Bằng chứng cần báo cáo:** số training seed, số evaluation rollouts/seed, mean ± SD hoặc interval phù hợp, và quy tắc tổng hợp **[TO VERIFY]**.
- **Cấu trúc phản hồi:** công nhận 10 rollout cũ không phải training-seed variance → mô tả protocol nhiều seed → báo cáo kết quả thật → sửa Discussion/Conclusion.
- **Tránh:** diễn giải SD gần 0 của 10 rollout cũ như bằng chứng robustness của PPO.

### R1.C10 — Trích dẫn, nguồn CF và định dạng tài liệu tham khảo

- **Loại:** `writing_clarity`.
- **Ưu tiên chiến lược:** `direct_address`, `clarification_quality`, `paper_grounding`.
- **Mẫu phản hồi phù hợp:** A.
- **Tình trạng cần kiểm tra:** bản Markdown đã sửa các lỗi định dạng rõ ràng và thêm nguồn PID, ProjectAirSim, Gymnasium, GAE; trước khi gửi Word phải đối chiếu lại với bản nộp cuối **[TO VERIFY]**.
- **Hành động còn lại:** kiểm tra nguồn gốc CF với cách gọi trong bài; mỗi tài liệu phải có đầy đủ tên tác giả, DOI khi có và dấu chấm kết thúc theo checklist tạp chí.
- **Cấu trúc phản hồi:** liệt kê ngắn từng nhóm nguồn được bổ sung/sửa, không cần biện luận dài.
- **Tránh:** khẳng định `λ = 0.95` là giá trị do tài liệu GAE bắt buộc nếu đó chỉ là hyperparameter do tác giả chọn.

### R1.C11 — Thuật ngữ, tiêu đề, abstract và phạm vi mô phỏng

- **Loại:** `scope_claim` + `writing_clarity`.
- **Ưu tiên chiến lược:** `controlled_concession`, `clarification_quality`, `paper_grounding`.
- **Mẫu phản hồi phù hợp:** C.
- **Hành động:**
  - Chọn nhất quán thuật ngữ phù hợp với metric và protocol: waypoint-sequence tracking/path following thay vì gợi ý trajectory tracking theo thời gian nếu chưa có metric tương ứng.
  - Thêm “in Simulation” vào tiêu đề hoặc định vị tương đương.
  - Cập nhật Abstract bằng các số cuối cùng; nêu khác biệt giới hạn vận tốc và không diễn giải completion time là intrinsic advantage khi chưa có controlled comparison.
  - Bảo đảm Abstract 150–250 từ, không trích dẫn, không bảng/hình và từ khóa tối đa sáu.
- **Tránh:** thay đổi tiêu đề/thuật ngữ ở một phần mà không đồng bộ toàn bài, figure/table/caption và response letter.

### R1.C12 — Công thức, ký hiệu, điều kiện biên và hệ số reward

- **Loại:** `theory` + `writing_clarity`.
- **Ưu tiên chiến lược:** `clarification_quality`, `paper_grounding`, `controlled_concession`.
- **Mẫu phản hồi phù hợp:** A; C với các giới hạn chưa thể xác minh.
- **Tình trạng đã có thể ghi nhận:** lỗi trùng số phương trình và công thức MAE đã được chỉnh trong nguồn Markdown; cần kiểm tra lại bản Word cuối, toàn bộ cross-reference và công thức hiển thị **[TO VERIFY]**.
- **Hành động bắt buộc trước khi phản hồi:**
  - Tách ký hiệu radius waypoint khỏi PPO clipping parameter.
  - Thống nhất `w_i`/`ω_i` và `N`/`n`.
  - Xác minh điều kiện safety, ngưỡng “too far”, logic `i=n`, và implementation thực tế từ code/log.
  - Giải thích cơ sở các hệ số reward bằng thiết kế/scale đã được kiểm tra; không bịa sensitivity analysis.
- **Kết nối với R1.C7:** nếu claim rằng từng thành phần reward hữu ích, bằng chứng cuối cùng phải là ablation, không chỉ lời giải thích.
- **Tránh:** sửa ký hiệu trong bài nhưng không khớp cách triển khai; đưa threshold mới không có nguồn từ code/experiment.

### R1.C13 — Tái lập: PPO, flight controller, quỹ đạo và yaw

- **Loại:** `evidence_gap`.
- **Ưu tiên chiến lược:** `clarification_quality`, `paper_grounding`, `specific_evidence`.
- **Mẫu phản hồi phù hợp:** A.
- **Hành động:** tạo một bảng setup cô đọng: implementation/library, mini-batch, entropy/value coefficient, parallel environments, seed, state normalization, yaw representation/wrapping, controller trong, tần số và thông số do tác giả cấu hình.
- **Bằng chứng:** chỉ nhập các giá trị được lấy từ source/config/log **[TO VERIFY]**.
- **Giới hạn 15 trang:** chuyển thông số ít quan trọng hơn sang tệp bổ sung chỉ khi tạp chí cho phép; tuy nhiên bài chính vẫn phải có đủ thông tin thiết yếu để tái lập.
- **Tránh:** suy diễn chi tiết của ProjectAirSim thay cho mô tả cấu hình thực tế đã dùng.

### R1.C14 — Generalization, quỹ đạo khác và nhiễu/gió

- **Loại:** `evidence_gap` + `scope_claim`.
- **Ưu tiên chiến lược:** `new_experiment_strength`, `controlled_concession`, `specific_evidence`.
- **Mẫu phản hồi phù hợp:** B nếu có thí nghiệm; C nếu không.
- **Thí nghiệm tối thiểu đáng tin:** một quỹ đạo khác có hình học khác và ít nhất một điều kiện disturbance/noise/wind được định nghĩa rõ; đánh giá PPO và baseline theo protocol đã kiểm soát.
- **Nếu chưa thể chạy:** không viết như đã chứng minh generalization. Hãy thu hẹp claim về one helical trajectory in ProjectAirSim và nêu rõ noise, estimator, delay, wind, model mismatch, hardware validation nằm ngoài phạm vi.
- **Tránh:** dùng kết quả trên cùng quỹ đạo hoặc cùng training distribution để gọi là generalization.

### R1.C15 — Trình bày bảng/hình, caption và Fig. 3

- **Loại:** `writing_clarity`.
- **Ưu tiên chiến lược:** `direct_address`, `clarification_quality`, `paper_grounding`.
- **Mẫu phản hồi phù hợp:** A.
- **Tình trạng cần xác minh trong bản Word:** Table I/II thống nhất, `Discussion` đúng chính tả, Fig. 2 chỉ còn một dấu chấm, đoạn Actor–Critic không lặp, và Fig. 3 giải thích đúng vai trò `θ_e` **[TO VERIFY]**.
- **Hành động với `θ_e`:** nếu không tham gia luật điều khiển CF, ghi rõ đây chỉ là minh họa hình học hoặc bỏ khỏi hình; nếu có sử dụng, thêm định nghĩa và công thức.
- **Theo checklist tạp chí:** caption bảng ở trên, caption hình ở dưới, căn giữa, Times New Roman 11, có dấu chấm cuối caption; không viết tắt khi tham chiếu “Hình”/“Bảng”; hình rõ, ≥300 dpi và ở dạng vector theo yêu cầu.
- **Tránh:** giữ `θ_e` trong hình với chú thích mơ hồ.

## 5. Bố cục thư phản hồi sau khi hoàn tất sửa đổi

Chỉ viết thư phản hồi sau khi có số liệu/chi tiết đã được xác minh.

1. **Mở đầu, 2–3 câu:** cảm ơn; nói rõ bài đã được chỉnh sửa đáng kể; liệt kê ba thay đổi lớn nhất có bằng chứng thực tế.
2. **Bảng thay đổi trọng yếu:** công bằng PPO–CF, ablation, nhiều seed, phạm vi claim; chỉ dùng bảng này nếu tạp chí cho phép.
3. **Phản hồi từng mục R1.C1–R1.C15:** dùng đúng thứ tự trong review; mỗi mục dài vừa đủ để người phản biện đối chiếu.
4. **Cấu trúc mỗi mục:**
   - Ghi nhận chính xác quan ngại.
   - Hành động đã thực hiện.
   - Bằng chứng định lượng hoặc thông tin đã xác minh.
   - Vị trí sửa trong bản thảo: section, table, figure, equation hoặc appendix.
5. **Kết thúc:** nhắc lại phạm vi kết luận cuối cùng; không lặp lại lời hứa chưa thực hiện.

## 6. Ma trận quyết định: có thể phản hồi ngay hay phải chờ

| Nhóm nội dung | Có thể phản hồi sau khi kiểm tra bản thảo/log? | Phải có thí nghiệm mới để phản hồi đầy đủ? |
|---|---:|---:|
| Lỗi chính tả, caption, đánh số bảng/công thức, citation | Có | Không |
| Title, terminology, Abstract, scope claim | Có | Không, nếu thu hẹp claim |
| Hyperparameter, controller, trajectory, training setup | Có, nếu mã/log còn | Không |
| Fair PPO–CF completion-time comparison | Không | Có |
| Second baseline | Không | Có |
| Next-waypoint/reward ablation | Không | Có |
| Training-seed variability | Không | Có |
| Time/progress metric | Có thể thu hẹp diễn giải | Có, nếu muốn bổ sung metric mới |
| Generalization/noise/wind | Có thể thu hẹp diễn giải | Có, nếu muốn tuyên bố robustness/generalization |

## 7. Integrity gate trước khi gửi phản hồi

| Kiểm tra | Trạng thái cần đạt |
|---|---|
| Mỗi concern R1.C1–R1.C15 có một mục phản hồi | Bắt buộc |
| Mọi số liệu mới có bảng/hình và vị trí trong bản thảo | Bắt buộc |
| Các số liệu cũ không được dùng để suy rộng ngoài protocol cũ | Bắt buộc |
| Không có `[TO VERIFY]` còn sót trong thư phản hồi cuối | Bắt buộc |
| Không có lời hứa chung chung về future work thay cho bằng chứng | Bắt buộc |
| Các claim được đồng bộ giữa title, abstract, results, discussion, conclusion | Bắt buộc |
| Bản thảo ≤15 trang theo quy ước bổ sung của tác giả | Bắt buộc |
| Abstract 150–250 từ; tối đa 6 từ khóa; không trích dẫn trong abstract | Bắt buộc |
| Bản ẩn danh không tiết lộ tác giả qua lời cảm ơn, metadata, bảng/hình hay tài liệu bổ sung | Bắt buộc |

## 8. Kết luận chiến lược

Điểm mạnh có thể bảo vệ là tính khả thi của một policy PPO cấp cao phát lệnh vận tốc để đi qua chuỗi waypoint trong ProjectAirSim. Tuy nhiên, để thuyết phục phản biện chấp nhận bản sửa lớn, tác giả cần để **bằng chứng mới** dẫn dắt phản hồi: trước hết là phép so sánh tốc độ công bằng, ablation cho hai thành phần được nêu như đóng góp và đánh giá qua nhiều training seed. Nếu các thí nghiệm đó không thể hoàn thành, phản hồi vẫn nên sửa toàn bộ lỗi và mô tả còn thiếu, nhưng phải thu hẹp kết luận một cách rõ ràng; không nên cố bảo vệ các claim mà dữ liệu hiện tại không thể hỗ trợ.
