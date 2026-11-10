# REVIEW PHẢN BIỆN VÀ LỘ TRÌNH CHỈNH SỬA BÀI BÁO

**Bài báo:** *Waypoint Trajectory Tracking Control of a Quadcopter Using Proximal Policy Optimization*  
**Tài liệu review:** `3199-11465-1-5-20261106.pdf` (4 trang)  
**Bản thảo đối chiếu:** `TRAJECTORY TRACKING CONTROL OF A QUADCOPTER USING PROXIMAL POLICY OPTIMIZATION(2).docx` (14 trang)  
**Kết luận của phản biện:** **Major Revision** (Sửa chữa lớn).

> Tài liệu này gồm hai phần: (A) chuyển nội dung nhận xét của phản biện sang tiếng Việt, giữ cấu trúc và đầy đủ các ý chính; (B) sắp xếp các đầu việc chỉnh sửa theo mức độ từ dễ đến khó. Phần phân loại mức độ là lộ trình thực hiện được xây dựng từ các nhận xét trong review và tình trạng thể hiện trong bản thảo hiện tại.

---

# A. TOÀN BỘ NỘI DUNG REVIEW

## 1. Tính cấp thiết, ý nghĩa khoa học và thực tiễn

Điều khiển quadcopter bám theo quỹ đạo bằng học tăng cường sâu (Deep Reinforcement Learning - DRL) là một chủ đề có tính thời sự. Việc tác giả sử dụng Proximal Policy Optimization (PPO) làm bộ điều khiển vận tốc ở cấp cao, trong khi vòng điều khiển ổn định bên trong được đảm nhiệm bởi flight controller, là một hướng tiếp cận hợp lý.

Tuy nhiên, phần **Introduction chưa xác định được khoảng trống nghiên cứu (research gap)**. Bài báo có trích dẫn các nghiên cứu DRL sử dụng DDPG và SAC, nhưng chưa đề cập đầy đủ các nghiên cứu trước đây đã áp dụng PPO cho những bài toán tương tự, đồng thời chưa làm rõ phương pháp trong bài báo khác biệt như thế nào so với các nghiên cứu đó.

Lập luận cho rằng các phương pháp điều khiển cổ điển cần một mô hình chuyên biệt và phải tinh chỉnh tham số chưa đủ thuyết phục. Bản thân phương pháp được đề xuất vẫn sử dụng flight controller có sẵn trong ProjectAirSim; ngoài ra, PPO cũng cần được huấn luyện lại khi cấu hình hệ thống thay đổi.

Ý nghĩa thực tiễn hiện còn hạn chế vì toàn bộ kết quả chỉ đến từ mô phỏng, chưa xét đến nhiễu cảm biến, bộ ước lượng trạng thái, độ trễ hoặc gió, và chưa có thí nghiệm trên nền tảng quadcopter thực tế.

## 2. Mục tiêu, phạm vi và phương pháp nghiên cứu

Mục tiêu nghiên cứu được trình bày rõ: PPO tạo ra các lệnh vận tốc trong hệ tọa độ NED từ vector trạng thái 15 chiều, sử dụng hàm phần thưởng gồm bốn thành phần, và được đánh giá trên quỹ đạo xoắn ốc gồm 40 waypoint so với phương pháp Carrot-Following (CF).

Phạm vi nghiên cứu được tác giả giới hạn tương đối rõ ràng: sử dụng ProjectAirSim, chỉ xét một quỹ đạo và không đưa nhiễu hoặc tác động bên ngoài vào mô phỏng.

Tuy nhiên, phương pháp nghiên cứu còn một số hạn chế sau:

### 2.1. Môi trường huấn luyện chưa được mô tả đầy đủ

Bài báo chưa nêu rõ:

- Quỹ đạo được sử dụng trong quá trình huấn luyện.
- Tập waypoint và các điều kiện ban đầu được sử dụng khi huấn luyện.
- Có áp dụng ngẫu nhiên hóa (randomization) trong quá trình huấn luyện hay không.
- Quỹ đạo xoắn ốc dùng để đánh giá có nằm trong tập huấn luyện hay không.

Do đó, chưa thể đưa ra kết luận về khả năng tổng quát hóa (generalization) của mô hình.

### 2.2. So sánh với Carrot-Following chưa công bằng

CF sử dụng tốc độ cố định 1.5 m/s, trong khi PPO được phép tạo lệnh vận tốc lên đến 3 m/s trên mỗi trục. Điều này tương đương độ lớn vận tốc tổng có thể đạt khoảng 5.2 m/s đối với PPO.

Tác giả đã thừa nhận sự khác biệt này, nhưng việc chỉ nêu hạn chế không thể thay thế cho một thí nghiệm có kiểm soát. Tham số khoảng nhìn trước (look-ahead distance) `L` của CF cũng chưa được cung cấp; do đó, chưa rõ tham số này đã được tinh chỉnh hay được chọn tùy ý.

### 2.3. Chỉ sử dụng một phương pháp đối chứng

Phần Introduction có đề cập PID, LQR, MPC, DDPG, TD3 và SAC, nhưng bài báo không thực hiện so sánh với bất kỳ phương pháp nào trong số đó.

Chỉ so sánh với CF là chưa đủ để kết luận về giá trị hoặc ưu thế của PPO.

### 2.4. Chỉ số sai số chưa phản ánh tiến độ bám quỹ đạo theo thời gian

Chỉ số sai số hiện tại chỉ đo sai số ngang (lateral error) so với đường polyline nối các waypoint. Sai số được tính bằng khoảng cách từ quadcopter đến điểm gần nhất trên polyline, chứ không phải sai số tại một thời điểm tương ứng với quỹ đạo tham chiếu theo thời gian.

Vì vậy, chỉ số này không phản ánh việc quadcopter có bám đúng tiến độ của quỹ đạo hay không, đồng thời không phụ thuộc vào việc hai phương pháp di chuyển nhanh hay chậm.

### 2.5. Chưa có thí nghiệm ablation cho hai thành phần quan trọng

Hai thành phần quan trọng chưa được kiểm chứng bằng thí nghiệm ablation là:

- Thông tin về waypoint kế tiếp trong vector trạng thái.
- Đóng góp riêng của từng thành phần trong hàm phần thưởng.

Chính tác giả cũng thừa nhận hạn chế này trong phần Discussion. Do các thí nghiệm mô phỏng tương đối thuận tiện để thực hiện, phản biện đề nghị nên tiến hành ngay thay vì để lại cho nghiên cứu tương lai.

## 3. Kết quả đạt được, đóng góp mới và giá trị khoa học

Các kết quả định lượng được trình bày nhất quán. PPO có:

- Thời gian hoàn thành: 16.91 s, so với 24.63 s của CF.
- RMSE: 0.082 m, so với 0.198 m của CF.
- MAE: 0.072 m, so với 0.194 m của CF.
- Sai số thấp hơn trên cả ba trục tọa độ.

Các giá trị này phù hợp với tỷ lệ cải thiện được nêu trong bài báo.

### 3.1. Mức độ mới của nghiên cứu còn khiêm tốn

Theo phản biện, tính mới của nghiên cứu hiện ở mức khiêm tốn vì:

- PPO là một thuật toán đã phổ biến.
- Kiến trúc phân cấp, trong đó RL tạo lệnh vận tốc còn flight controller bên trong đảm nhiệm ổn định, là cách tiếp cận đã được sử dụng phổ biến.
- Hàm phần thưởng kết hợp thành phần tiến gần mục tiêu và thành phần căn chỉnh hướng chuyển động cũng là cách thiết kế quen thuộc.

Thành phần có khả năng là điểm mới thực sự duy nhất là việc bổ sung sai số đến waypoint kế tiếp vào vector trạng thái. Tuy nhiên, bài báo chưa chứng minh được đóng góp riêng của thành phần này.

Vì vậy, giá trị khoa học hiện tại chủ yếu ở mức **chứng minh tính khả thi trong môi trường mô phỏng**, đúng như kết luận mà chính tác giả đã nêu.

### 3.2. Không nên xem thời gian hoàn thành là ưu thế riêng của PPO

Không nên xem kết quả thời gian hoàn thành ngắn hơn là một ưu thế nội tại của PPO vì:

- Giới hạn vận tốc của hai phương pháp khác nhau.
- Độ dài tối đa của mỗi episode chỉ là 400 bước, tương ứng 20 giây.
- Phần thưởng cuối cùng phụ thuộc vào thời gian còn lại.

Thiết kế huấn luyện như vậy có thể khiến chính sách được thúc đẩy phải di chuyển nhanh.

### 3.3. Độ tin cậy thống kê chưa được đánh giá đúng mức

Môi trường mô phỏng gần như tất định (nearly deterministic), do đó 10 lần chạy chỉ phản ánh nhiễu hoặc biến động của simulator, chứ chưa phản ánh độ biến thiên của thuật toán PPO.

Vì vậy, độ lệch chuẩn gần bằng 0 không có nhiều ý nghĩa để chứng minh tính ổn định của PPO. Nguồn biến thiên quan trọng hơn đến từ các seed huấn luyện khác nhau, trong khi bài báo chỉ huấn luyện một lần.

## 4. Số lượng tài liệu tham khảo trong nước và quốc tế

Bài báo có 21 tài liệu tham khảo; số thứ tự trích dẫn trong nội dung khớp với danh mục tài liệu tham khảo và các tài liệu thuộc giai đoạn 2016-2024.

Tuy nhiên, phản biện lưu ý các vấn đề sau:

### 4.1. Thiếu trích dẫn cho công cụ và phương pháp được sử dụng

Bài báo chưa trích dẫn các nguồn cho:

- ProjectAirSim.
- Gymnasium.
- Generalized Advantage Estimation (GAE), với `λ = 0.95`.

### 4.2. Nguồn trích dẫn cho CF chưa phù hợp

Bài báo sử dụng tên **Carrot-Following**, trong khi tài liệu tham khảo [21] đề cập đến thuật toán **Carrot Chasing**.

Cần trích dẫn nguồn gốc phù hợp của thuật toán, chẳng hạn công trình của Breivik-Fossen hoặc Sujit và cộng sự, đồng thời thống nhất cách gọi thuật toán trong toàn bài.

### 4.3. Định dạng danh mục tài liệu tham khảo chưa thống nhất

Một số tài liệu thiếu chữ cái viết tắt tên riêng của tác giả đầu tiên, ví dụ tài liệu [3] và [5].

Ngoài ra còn có lỗi ngắt từ trong các tài liệu tham khảo, ví dụ:

- `Mod elling`.
- `Tra jectory`.
- `Prox imal`.
- `un deractuated`.

### 4.4. Phần PID thiếu nguồn tham khảo phù hợp

Nhận định chung về “PID and its variants” hiện chỉ được hỗ trợ bởi một bài báo về Fuzzy-PID. Cần bổ sung nguồn tham khảo phù hợp hơn cho PID và các biến thể của PID.

## 5. Mức độ phù hợp của tiêu đề, tóm tắt và từ khóa

Tiêu đề, tóm tắt và từ khóa nhìn chung phù hợp với nội dung bài báo. Tuy nhiên, cần điều chỉnh ba điểm:

### 5.1. Thuật ngữ

Thuật ngữ “trajectory tracking” thường được hiểu là bám một quỹ đạo được tham số hóa theo thời gian. Trong khi đó, nội dung bài báo thực chất là điều hướng qua một chuỗi waypoint (waypoint navigation hoặc path following); chỉ số sai số cũng là sai số ngang so với đường tham chiếu.

Do đó, cần thống nhất thuật ngữ được sử dụng trong bài báo.

### 5.2. Tiêu đề

Tiêu đề cần thể hiện rõ giới hạn **“in simulation”** để tránh tạo ấn tượng rằng phương pháp đã được triển khai trên hệ thống thực tế.

### 5.3. Tóm tắt

Abstract hiện chưa nêu các kết quả định lượng như thời gian hoàn thành, RMSE và MAE. Cần bổ sung các giá trị này, đồng thời ghi chú sự khác biệt về giới hạn vận tốc giữa hai phương pháp.

## 6. Lỗi và các điểm cần làm rõ

### 6.1. Phương trình và ký hiệu

1. **Trùng số thứ tự phương trình:** Phương trình (11) bị đánh số hai lần, trùng với số của phương trình vận tốc CF.
2. **Hai phương trình RMSE và MAE giống hệt nhau:** Phương trình (11) và (12) đang có cùng biểu thức. Cần kiểm tra và sửa để phương trình MAE thể hiện đúng định nghĩa MAE.
3. **Không thống nhất ký hiệu ngưỡng hoàn thành waypoint:** Ngưỡng hoàn thành waypoint được ký hiệu là `ε` trong phương trình (6), nhưng phần giải thích lại ghi `r_w = 0.2 m`. Trong khi đó, `ε = 0.2` cũng được dùng làm tham số clipping của PPO trong Table I. Ký hiệu waypoint cũng chưa thống nhất: `w_i` trong công thức (6) nhưng lại là `ω_i` trong phần mô tả; đồng thời chưa thống nhất `N` và `n`.
4. **Điều kiện an toàn chưa chặt chẽ:** Điều kiện “`φ or θ > π/2`” cần sử dụng giá trị tuyệt đối. Ngưỡng 90° được đánh giá là quá rộng; ngoài ra, bài báo chưa nêu ngưỡng xác định quadcopter đã đi quá xa waypoint.
5. **Chưa định nghĩa trạng thái tại waypoint cuối:** Khi quadcopter đang hướng đến waypoint cuối cùng (`i = n`), waypoint `i + 1` không tồn tại. Cần giải thích trạng thái được xác định như thế nào trong trường hợp này.
6. **Chưa giải thích hệ số trong hàm phần thưởng:** Các hệ số 10 và 15 trong phương trình (6), hệ số 30 trong phương trình (7), cùng các hệ số 5.0 và 0.2 trong phương trình (8) và (9) chưa được giải thích. Cần nêu cơ sở lựa chọn hoặc phân tích độ nhạy của các hệ số này.

### 6.2. Thiết lập huấn luyện

1. **Table I thiếu các tham số huấn luyện quan trọng**, bao gồm:
   - Kích thước mini-batch.
   - Entropy coefficient.
   - Value-function coefficient.
   - Số lượng môi trường chạy song song.
   - Thư viện triển khai PPO.
   - Random seed.
   - Phương pháp chuẩn hóa trạng thái: dùng thống kê cố định hay thống kê cập nhật trong quá trình chạy.

   Ngoài ra, cần giải thích cách xử lý góc yaw khi giá trị tiến gần `+π` hoặc `-π`.

2. **Chưa mô tả inner flight controller của ProjectAirSim:** Cần nêu loại bộ điều khiển, tần số hoạt động, các tham số và cách bộ điều khiển này thực thi các lệnh vận tốc.

### 6.3. Thí nghiệm và đánh giá

1. Cần mô tả rõ quỹ đạo xoắn ốc gồm bao nhiêu vòng, khoảng cách giữa các waypoint và profile vận tốc.
2. Cần chạy CF với giới hạn vận tốc tương đương; có thể đặt giới hạn vận tốc của PPO bằng 1.5 m/s hoặc điều chỉnh CF theo một giới hạn vận tốc tương đương. Mục đích là cô lập ảnh hưởng của chiến lược điều khiển.
3. Nên bổ sung ít nhất một thí nghiệm với quỹ đạo khác và có thêm nhiễu hoặc gió để hỗ trợ kết luận về tính tổng quát và tăng cường đóng góp của bài báo, nếu điều kiện cho phép.

### 6.4. Hình thức trình bày

1. Table I sử dụng số La Mã, trong khi Table 2 sử dụng số Ả Rập. Cần thống nhất cách đánh số bảng.
2. Các lỗi và điểm chưa nhất quán khác:
   - Tiêu đề `Dicussion` bị viết sai, cần sửa thành `Discussion`.
   - Caption của Fig. 2 có dấu chấm thừa.
   - Section 3.4 có hai câu trùng lặp nội dung về “PPO with an Actor-Critic architecture”.
   - Fig. 3 minh họa góc `θ_e`, nhưng góc này không được sử dụng trong thuật toán. Cần giải thích vai trò của góc hoặc điều chỉnh hình minh họa để tránh gây hiểu nhầm.

## 7. Kết luận của phản biện

<blockquote>
**Recommendation: Major Revision.** Bài báo được trình bày rõ ràng và các tác giả đã trung thực nêu ra những hạn chế của nghiên cứu. Tuy nhiên, các thí nghiệm hiện tại chưa đủ để hỗ trợ kết luận rằng phương pháp đề xuất vượt trội so với phương pháp đối chứng.
</blockquote>

Phản biện cũng gửi lời cảm ơn và cho biết các nhận xét, đề xuất nhằm giúp tác giả cải thiện bản thảo và nội dung nghiên cứu; quyết định cuối cùng thuộc về ban biên tập.

---

# B. LỘ TRÌNH SỬA CHỮA THEO MỨC ĐỘ TỪ DỄ ĐẾN KHÓ

## Tổng quan mức độ

| Mức | Độ khó | Nhóm công việc | Có cần chạy lại mô phỏng? |
|---|---|---|---|
| 1 | Dễ | Lỗi chính tả, định dạng, đánh số, sửa trùng lặp, bổ sung trích dẫn đã xác định được | Không |
| 2 | Dễ - trung bình | Sửa tiêu đề, Abstract, thuật ngữ, làm rõ phần mô tả và bổ sung thông tin cấu hình đã có | Thường không; cần kiểm tra log/mã nguồn |
| 3 | Trung bình - khó | Rà soát công thức, ký hiệu, điều kiện biên, giải thích thiết kế thuật toán và chỉ số đánh giá | Có thể cần tính toán/kiểm chứng lại |
| 4 | Khó | Thí nghiệm đối chứng công bằng, baseline bổ sung, nhiều seed và ablation | Có |
| 5 | Rất khó | Kiểm tra generalization, quỹ đạo mới và tác động của nhiễu/gió; cập nhật toàn bộ phân tích kết quả | Có, cần thiết kế và chạy thêm kịch bản |

**Lưu ý:** “Dễ đến khó” phản ánh khối lượng và độ phụ thuộc kỹ thuật, không đồng nghĩa mức độ quan trọng. Những thí nghiệm ở mức 4-5 có ảnh hưởng trực tiếp đến khả năng bảo vệ kết luận khoa học nên không nên bỏ qua chỉ vì khó thực hiện.

## Mức 1 - Các chỉnh sửa nhanh, ít phụ thuộc kỹ thuật

### 1.1. Sửa lỗi trình bày và lỗi đánh máy

- [ ] Sửa `Dicussion` thành `Discussion`.
- [ ] Xóa dấu chấm thừa trong caption Fig. 2.
- [ ] Xóa câu trùng lặp về kiến trúc Actor-Critic trong Section 3.4.
- [ ] Thống nhất cách đánh số bảng: Table I, Table II hoặc Table 1, Table 2 theo một quy chuẩn duy nhất.
- [ ] Sửa lỗi ngắt từ trong danh mục tài liệu tham khảo: `Mod elling`, `Tra jectory`, `Prox imal`, `un deractuated`.
- [ ] Bổ sung chữ cái viết tắt tên riêng còn thiếu ở tài liệu [3] và [5], sau khi kiểm tra thông tin thư mục gốc.

**Vị trí trong bản thảo:** Section 3.4; caption Fig. 2; Table I và Table 2; References.

### 1.2. Sửa đánh số và công thức bị trùng

- [ ] Kiểm tra lại toàn bộ thứ tự đánh số phương trình, đặc biệt phương trình vận tốc CF và phương trình RMSE cùng đang mang số (11).
- [ ] Sửa lỗi phương trình (11) và (12) có biểu thức giống nhau; bảo đảm phương trình MAE không bị sao chép nhầm từ RMSE.
- [ ] Sau khi sửa, cập nhật mọi chỗ dẫn chiếu đến phương trình trong nội dung.

**Vị trí:** Section 4.3 và Section 4.4.

### 1.3. Bổ sung các trích dẫn còn thiếu

- [ ] Bổ sung nguồn trích dẫn cho ProjectAirSim.
- [ ] Bổ sung nguồn trích dẫn cho Gymnasium.
- [ ] Bổ sung nguồn cho GAE và thông tin `λ = 0.95` theo tài liệu phù hợp.
- [ ] Bổ sung tài liệu nền tảng cho PID và các biến thể PID; không chỉ dựa vào một bài báo Fuzzy-PID để hỗ trợ nhận định chung.
- [ ] Kiểm tra nguồn gốc thuật toán CF: đối chiếu tên gọi `Carrot-Following` với tài liệu [21] về `Carrot Chasing`; bổ sung nguồn thuật toán phù hợp (phản biện gợi ý Breivik-Fossen hoặc Sujit và cộng sự) và thống nhất tên gọi.

**Vị trí:** Introduction, Section 3/4 và References.

> Đây là nhóm sửa nhanh nhưng cần kiểm tra nguồn gốc tài liệu cẩn thận; không tự điền thông tin thư mục khi chưa xác minh được nguồn.

## Mức 2 - Chỉnh sửa nội dung và bổ sung thông tin mô tả

### 2.1. Chỉnh tiêu đề, thuật ngữ và phạm vi tuyên bố

- [ ] Điều chỉnh tiêu đề để thể hiện nghiên cứu được thực hiện **trong mô phỏng**. Ví dụ có thể cân nhắc thêm cụm `in Simulation`.
- [ ] Rà soát cách dùng `trajectory tracking`, `waypoint navigation` và `path following`. Phản biện cho rằng bài báo đang điều hướng qua chuỗi waypoint và dùng sai số ngang so với đường polyline, do đó cần chọn thuật ngữ chính xác và dùng nhất quán.
- [ ] Đồng bộ thuật ngữ trong tiêu đề, Abstract, Keywords, Introduction, phương pháp, kết quả và Conclusion.
- [ ] Điều chỉnh các phát biểu về ưu thế của PPO để không tạo ấn tượng đã chứng minh khả năng triển khai thực tế hoặc ưu thế tổng quát.
- [ ] Nêu rõ phạm vi thực nghiệm: ProjectAirSim, quỹ đạo được khảo sát, chưa có nhiễu/gió, chưa có kiểm chứng trên quadcopter thực.

### 2.2. Viết lại Abstract theo kết quả định lượng

- [ ] Bổ sung thời gian hoàn thành trung bình: PPO 16.91 s và CF 24.63 s.
- [ ] Bổ sung RMSE trung bình: PPO 0.082 m và CF 0.198 m.
- [ ] Bổ sung MAE trung bình: PPO 0.072 m và CF 0.194 m.
- [ ] Nêu rõ giới hạn vận tốc của hai bộ điều khiển khác nhau: CF dùng tốc độ tham chiếu 1.5 m/s; PPO giới hạn từng thành phần vận tốc trong khoảng [-3, 3] m/s.
- [ ] Tránh diễn giải thời gian hoàn thành ngắn hơn là ưu thế nội tại của PPO khi chưa có thí nghiệm với giới hạn vận tốc tương đương.

**Vị trí:** Abstract ở trang đầu.

### 2.3. Bổ sung research gap và đối chiếu nghiên cứu PPO trước đây

- [ ] Bổ sung các nghiên cứu đã áp dụng PPO cho quadcopter hoặc các bài toán điều khiển/bám đường tương tự.
- [ ] So sánh rõ bài báo hiện tại với các nghiên cứu đó, thay vì chỉ liệt kê DDPG, SAC và các thuật toán DRL khác.
- [ ] Nêu rõ phần nào đã được biết đến và phần nào là điểm cần kiểm chứng trong nghiên cứu này.
- [ ] Không khẳng định novelty quá mức. Theo phản biện, việc đưa sai số đến waypoint kế tiếp vào state có thể là điểm khác biệt đáng chú ý, nhưng cần thí nghiệm chứng minh.

**Vị trí:** Introduction, đặc biệt đoạn tổng quan DRL và phần liệt kê đóng góp.

### 2.4. Làm rõ lập luận về ý nghĩa thực tiễn

- [ ] Xem lại lập luận rằng phương pháp cổ điển đòi hỏi mô hình chuyên biệt và tinh chỉnh tham số.
- [ ] Thừa nhận PPO vẫn phụ thuộc vào flight controller của ProjectAirSim và có thể phải huấn luyện lại khi cấu hình thay đổi.
- [ ] Phân biệt rõ đóng góp về tính khả thi trong mô phỏng với khả năng ứng dụng ngoài thực tế.
- [ ] Chuyển các tuyên bố chưa được kiểm chứng thành giới hạn nghiên cứu hoặc hướng phát triển tiếp theo.

### 2.5. Bổ sung mô tả quỹ đạo xoắn ốc

Cần kiểm tra dữ liệu tạo quỹ đạo hoặc mã nguồn để bổ sung:

- [ ] Số vòng xoắn của quỹ đạo.
- [ ] Khoảng cách hoặc quy luật phân bố giữa các waypoint.
- [ ] Profile vận tốc tham chiếu, nếu có.
- [ ] Những thông tin hình học cần thiết để người khác có thể tái tạo kịch bản mô phỏng.

**Vị trí:** Section 4.1/4.3 và phần mô tả kịch bản đánh giá ở Section 5.1.

### 2.6. Bổ sung thông tin huấn luyện có sẵn trong mã nguồn/log

- [ ] Bổ sung mini-batch size.
- [ ] Bổ sung entropy coefficient.
- [ ] Bổ sung value-function coefficient.
- [ ] Bổ sung số lượng parallel environments.
- [ ] Nêu thư viện/implementation PPO được sử dụng.
- [ ] Ghi rõ random seed đã dùng.
- [ ] Giải thích chuẩn hóa state bằng thống kê cố định hay running statistics.
- [ ] Giải thích cách biểu diễn hoặc xử lý góc yaw khi đi qua biên `+π` và `-π`.

**Vị trí:** Table I và Section 4.2; có thể bổ sung mô tả ngắn ngay sau bảng.

### 2.7. Mô tả inner flight controller trong ProjectAirSim

- [ ] Nêu loại flight controller hoặc cấu trúc các vòng điều khiển bên trong.
- [ ] Nêu tần số điều khiển.
- [ ] Nêu các tham số liên quan mà tác giả đã cấu hình.
- [ ] Mô tả cách các lệnh vận tốc NED từ PPO được tiếp nhận và chuyển thành lệnh điều khiển cấp thấp.

**Vị trí:** Section 4.1 hoặc Section 3, ngay sau phần mô tả kiến trúc phân cấp.

## Mức 3 - Chỉnh sửa kỹ thuật, định nghĩa và cách đánh giá

### 3.1. Chuẩn hóa ký hiệu và điều kiện biên trong thuật toán

- [ ] Phân biệt ký hiệu bán kính hoàn thành waypoint với tham số clipping của PPO. Không dùng cùng ký hiệu `ε` cho hai ý nghĩa khác nhau.
- [ ] Thống nhất ký hiệu `w_i`/`ω_i` và `N`/`n` trong toàn bài.
- [ ] Sửa điều kiện an toàn góc roll/pitch theo giá trị tuyệt đối như phản biện yêu cầu.
- [ ] Định nghĩa ngưỡng cụ thể cho điều kiện quadcopter đi quá xa waypoint.
- [ ] Giải thích trạng thái khi `i = n` và không tồn tại waypoint `i + 1`.
- [ ] Kiểm tra tính nhất quán giữa công thức, phần giải thích và cách triển khai thực tế trong code.

**Vị trí:** Section 3.1 và Section 3.3, đặc biệt các phương trình (6)-(9).

### 3.2. Giải thích hệ số của reward function

Cần giải thích cơ sở lựa chọn các hệ số:

- [ ] 10 và 15 trong phương trình (6).
- [ ] 30 trong phương trình (7).
- [ ] 5.0 trong phương trình (8).
- [ ] 0.2 trong phương trình (9).

Có thể trình bày cơ sở lựa chọn dựa trên thiết kế thực nghiệm, sự cân bằng thang đo giữa các thành phần hoặc kết quả kiểm tra độ nhạy. Tuy nhiên, nếu phản biện yêu cầu chứng minh ảnh hưởng của từng thành phần thì chỉ giải thích bằng lời là chưa đủ; cần kết hợp với ablation ở Mức 4.

### 3.3. Làm rõ hình Fig. 3 và góc `θ_e`

- [ ] Xác định góc `θ_e` có được sử dụng trong thuật toán CF thực tế hay chỉ được vẽ để minh họa quan hệ hình học.
- [ ] Nếu không được sử dụng, ghi rõ điều đó trong caption hoặc phần mô tả và cân nhắc bỏ ký hiệu gây hiểu nhầm.
- [ ] Nếu có sử dụng, bổ sung định nghĩa và cách nó tham gia vào thuật toán.

### 3.4. Rà soát cách diễn giải chỉ số sai số

- [ ] Nêu rõ chỉ số hiện tại là khoảng cách từ vị trí quadcopter đến điểm gần nhất trên polyline nối các waypoint.
- [ ] Không diễn giải chỉ số này như một thước đo đầy đủ cho sai số bám quỹ đạo theo thời gian.
- [ ] Bổ sung hoặc thảo luận một chỉ số có xét đến thời gian/tiến độ dọc quỹ đạo để đánh giá liệu phương pháp có đi đúng tiến độ tham chiếu hay không.
- [ ] Tính toán lại các chỉ số nếu định nghĩa metric được thay đổi; sử dụng cùng một quy trình cho PPO và CF.

**Vị trí:** Section 4.4 và phần Results/Discussion.

### 3.5. Kiểm tra tác động của thiết kế episode và phần thưởng cuối

- [ ] Phân tích ảnh hưởng của giới hạn 400 bước (20 s) đến hành vi chính sách.
- [ ] Kiểm tra ảnh hưởng của phần thưởng cuối phụ thuộc số bước còn lại.
- [ ] Tránh kết luận thời gian hoàn thành nhanh là ưu thế của PPO nếu thiết kế reward và episode đã trực tiếp khuyến khích hoàn thành nhanh.
- [ ] Nếu điều chỉnh reward/episode, cần huấn luyện và đánh giá lại, không chỉ sửa phần giải thích.

## Mức 4 - Các thí nghiệm đối chứng và kiểm chứng thành phần

Đây là nhóm công việc quan trọng, tác động trực tiếp đến tính thuyết phục của kết quả.

### 4.1. Làm công bằng phép so sánh PPO và CF

- [ ] Chọn cùng giới hạn độ lớn vận tốc hoặc thiết lập vận tốc tương đương cho hai phương pháp.
- [ ] Có thể thực hiện theo một trong hai hướng mà phản biện gợi ý: giới hạn PPO ở 1.5 m/s hoặc điều chỉnh CF theo giới hạn vận tốc tương đương.
- [ ] Cung cấp giá trị look-ahead distance `L` của CF.
- [ ] Mô tả cách lựa chọn/tinh chỉnh `L`, tránh để tham số này có vẻ được chọn tùy ý.
- [ ] Chạy lại các thí nghiệm so sánh và cập nhật thời gian hoàn thành, RMSE, MAE, đồ thị và phần thảo luận.
- [ ] Chỉ đưa ra kết luận về hiệu quả của chiến lược điều khiển sau khi đã kiểm soát được khác biệt về vận tốc.

**Lý do quan trọng:** Bản thảo hiện tại đã thừa nhận PPO và CF dùng giới hạn vận tốc khác nhau, nhưng phản biện yêu cầu một thí nghiệm có kiểm soát chứ không chỉ ghi chú hạn chế này.

### 4.2. Bổ sung baseline thứ hai

- [ ] Lựa chọn ít nhất một phương pháp đối chứng bổ sung phù hợp với điều kiện mô phỏng và phạm vi bài báo.
- [ ] Có thể cân nhắc một phương pháp thuộc nhóm điều khiển cổ điển (PID/LQR/MPC) hoặc một phương pháp DRL khác đã được đề cập trong Introduction (DDPG/TD3/SAC).
- [ ] Mô tả cấu hình và cách tinh chỉnh baseline để phép so sánh có ý nghĩa.
- [ ] Dùng cùng quỹ đạo, cấu hình quadcopter và điều kiện đánh giá khi có thể.
- [ ] Bổ sung kết quả vào bảng/đồ thị và giới hạn kết luận theo phạm vi thí nghiệm thực hiện.

**Lưu ý:** Phản biện chỉ ra rằng một baseline là chưa đủ; không có nghĩa bắt buộc phải triển khai tất cả PID, LQR, MPC, DDPG, TD3 và SAC. Nên chọn phương pháp khả thi và giải thích lý do lựa chọn.

### 4.3. Thực hiện ablation cho thông tin waypoint kế tiếp

- [ ] Tạo một cấu hình PPO không sử dụng thông tin sai số đến waypoint kế tiếp.
- [ ] Giữ các điều kiện huấn luyện và đánh giá khác giống cấu hình đầy đủ.
- [ ] So sánh kết quả để xác định việc bổ sung waypoint kế tiếp có cải thiện sai số hoặc hành vi chuyển tiếp giữa waypoint hay không.
- [ ] Báo cáo kết quả định lượng, không chỉ suy luận từ quỹ đạo minh họa.

### 4.4. Thực hiện ablation cho các thành phần reward

- [ ] Xác định cấu hình reward đầy đủ làm mốc.
- [ ] Loại bỏ lần lượt từng thành phần hoặc xây dựng các cấu hình ablation có kiểm soát để đánh giá đóng góp của từng thành phần.
- [ ] Giữ các điều kiện huấn luyện/đánh giá nhất quán giữa các cấu hình.
- [ ] Báo cáo ảnh hưởng đến khả năng hoàn thành waypoint, tracking error, tính an toàn và hành vi chuyển động.
- [ ] Dùng kết quả ablation để giải thích vai trò của waypoint-approach reward và velocity-alignment reward, thay vì chỉ khẳng định chúng giúp giảm reward sparsity.

### 4.5. Đánh giá độ biến thiên giữa các lần huấn luyện

- [ ] Huấn luyện PPO với nhiều random seed độc lập.
- [ ] Đánh giá từng policy đã huấn luyện trên cùng bộ kịch bản kiểm thử.
- [ ] Phân biệt rõ độ biến thiên giữa các lần chạy đánh giá của một policy cố định với độ biến thiên giữa các policy được huấn luyện từ seed khác nhau.
- [ ] Báo cáo trung bình và độ lệch chuẩn phù hợp với số lần huấn luyện/thử nghiệm thực tế.

**Lý do:** 10 lần chạy hiện tại dùng cùng bộ trọng số PPO nên chưa phản ánh độ nhạy của quá trình học đối với random seed.

## Mức 5 - Mở rộng đánh giá tính tổng quát và độ bền vững

### 5.1. Kiểm chứng generalization của PPO

- [ ] Làm rõ quỹ đạo huấn luyện, waypoint và điều kiện ban đầu.
- [ ] Xác định rõ quỹ đạo xoắn ốc hiện tại có xuất hiện trong tập huấn luyện hay không.
- [ ] Thiết kế ít nhất một kịch bản đánh giá tách biệt với dữ liệu/quỹ đạo huấn luyện để kiểm tra khả năng tổng quát hóa.
- [ ] Nếu dùng randomization trong huấn luyện, mô tả phạm vi và tham số được ngẫu nhiên hóa.

### 5.2. Bổ sung quỹ đạo và điều kiện nhiễu/gió

- [ ] Xây dựng ít nhất một quỹ đạo có hình học khác với quỹ đạo xoắn ốc hiện tại.
- [ ] Thêm điều kiện có nhiễu hoặc gió theo đề xuất của phản biện.
- [ ] Nêu rõ loại nhiễu/gió, cường độ và cách đưa vào mô phỏng.
- [ ] Đánh giá PPO và baseline trong cùng điều kiện để kiểm tra khả năng duy trì hiệu suất.
- [ ] Cập nhật phần Results, Discussion và Conclusion theo kết quả mới.

### 5.3. Giới hạn kết luận về khả năng triển khai thực tế

- [ ] Nếu chưa thể thử nghiệm trên quadcopter thực, không được trình bày kết quả mô phỏng như bằng chứng cho hiệu quả triển khai thực tế.
- [ ] Nêu rõ các yếu tố chưa được mô hình hóa/kiểm tra: sensor noise, state estimator, delay, wind và sai khác mô hình.
- [ ] Xem thử nghiệm trên nền tảng thực là hướng phát triển tiếp theo nếu điều kiện hiện tại chưa cho phép.

---

# C. THỨ TỰ TRIỂN KHAI ĐỀ XUẤT

Để tránh sửa đi sửa lại, nên thực hiện theo trình tự sau:

1. **Chốt các thông tin gốc từ code và log:** cấu hình huấn luyện, random seed, state normalization, flight controller, quỹ đạo, waypoint, điều kiện ban đầu, CF look-ahead distance và các hệ số reward. Không nên viết bổ sung thông tin khi chưa xác minh.
2. **Sửa lỗi hình thức và trích dẫn:** xử lý toàn bộ Mức 1.
3. **Sửa nội dung và cách trình bày nghiên cứu:** tiêu đề, Abstract, research gap, terminology, mô tả môi trường và giới hạn nghiên cứu ở Mức 2.
4. **Chốt định nghĩa kỹ thuật:** ký hiệu, điều kiện biên, reward, metric và cách diễn giải kết quả ở Mức 3.
5. **Thiết kế kế hoạch thí nghiệm trước khi chạy:** xác định cấu hình so sánh công bằng, baseline bổ sung, ablation và số seed ở Mức 4.
6. **Chạy thí nghiệm mở rộng:** quỹ đạo mới, nhiễu/gió và kịch bản kiểm tra generalization ở Mức 5.
7. **Cập nhật lại toàn bộ kết quả:** bảng, hình, thống kê, Discussion, Conclusion và Abstract. Không giữ số liệu cũ nếu đã thay đổi thiết lập hoặc metric.
8. **Kiểm tra chéo bản thảo:** mọi nhận xét phải có phản hồi cụ thể; mọi thay đổi trong công thức, bảng, hình và kết quả phải được cập nhật đồng bộ.

## Những điểm cần ưu tiên nhất để vượt qua Major Revision

Nếu xét theo khả năng ảnh hưởng đến quyết định phản biện, ba vấn đề quan trọng nhất là:

1. **So sánh PPO-CF chưa công bằng:** cần thí nghiệm với giới hạn vận tốc tương đương; chỉ giải thích rằng hai cấu hình khác nhau là chưa đủ.
2. **Chưa chứng minh điểm mới của phương pháp:** cần ablation cho thông tin waypoint kế tiếp và từng thành phần reward.
3. **Chưa chứng minh tính tổng quát/độ tin cậy:** cần làm rõ tập huấn luyện, đánh giá trên quỹ đạo khác và điều kiện nhiễu/gió; đồng thời đánh giá ảnh hưởng của nhiều random seed.

Các lỗi chính tả, định dạng, trích dẫn và công thức trùng lặp nên được sửa trước vì tương đối nhanh. Tuy nhiên, việc hoàn thành các lỗi này một mình sẽ không giải quyết được những quan ngại chính khiến phản biện đề xuất **Major Revision**.

---

# D. ĐỐI CHIẾU NHANH VỚI BẢN THẢO WORD HIỆN TẠI

| Vấn đề phản biện | Vị trí tương ứng trong bản thảo hiện tại | Ghi chú khi sửa |
|---|---|---|
| Research gap và nghiên cứu PPO trước đây | Section 1 - Introduction | Đã nhắc đến PPO như thuật toán phổ biến, nhưng cần tổng quan nghiên cứu PPO cho bài toán tương tự và làm rõ khác biệt. |
| State 15 chiều, next waypoint | Section 3.1 | Cần mô tả trường hợp waypoint cuối và kiểm chứng đóng góp bằng ablation. |
| Reward gồm bốn thành phần | Section 3.3 | Cần giải thích hệ số và ablation từng thành phần. |
| Actor-Critic bị lặp ý | Section 3.4 | Có đoạn lặp nội dung về PPO với Actor-Critic. |
| Mô tả ProjectAirSim | Section 4.1 | Đã mô tả môi trường và cấu hình quadcopter, nhưng còn thiếu thông tin inner flight controller. |
| Tham số PPO | Section 4.2, Table I | Cần bổ sung các tham số còn thiếu theo cấu hình thực tế. |
| CF và giới hạn vận tốc | Section 4.3 | Bản thảo đã thừa nhận khác biệt 1.5 m/s và ±3 m/s; vẫn cần thí nghiệm công bằng. |
| Metric RMSE/MAE | Section 4.4 | Cần sửa lỗi phương trình và xem xét metric có xét tiến độ theo thời gian. |
| Kết quả và độ biến thiên | Section 5.1, Table 2 | 10 lần đánh giá dùng trọng số cố định; cần đánh giá nhiều training seeds. |
| Hạn chế, novelty và generalization | Section 5.2 - Discussion | Đã thừa nhận một số giới hạn, nhưng cần bổ sung bằng chứng thí nghiệm theo yêu cầu phản biện. |
| Kết luận | Section 6 - Conclusion | Cần cập nhật sau khi chạy thí nghiệm mới và giới hạn kết luận đúng với bằng chứng. |
| Danh mục tài liệu | References | Sửa nguồn CF, bổ sung ProjectAirSim/Gymnasium/GAE/PID và chuẩn hóa định dạng. |

**Ghi chú đối chiếu:** Bản thảo hiện tại đã có một số câu thừa nhận hạn chế, đặc biệt ở phần CF (khác giới hạn vận tốc), Discussion và Conclusion. Tuy nhiên, phản biện đang yêu cầu thêm bằng chứng thực nghiệm cho các vấn đề trọng yếu; việc bổ sung lời giải thích đơn thuần có thể chưa đáp ứng yêu cầu.
