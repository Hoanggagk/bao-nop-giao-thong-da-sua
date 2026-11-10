# Cấu trúc dự án

Dự án lưu bản thảo gốc ở định dạng Word và phiên bản bài báo đã được chuyển đổi sang Markdown để thuận tiện chỉnh sửa, quản lý hình ảnh, bảng biểu và dựng lại tài liệu hoàn chỉnh.

## Cây thư mục

```text
bao nop giao thong da sua/
|-- Blined.docx
|-- TRAJECTORY TRACKING CONTROL OF A QUADCOPTER USING PROXIMAL POLICY OPTIMIZATION.docx
|-- PROJECT_STRUCTURE.md
`-- waypoint_trajectory_tracking_ppo/
    |-- README.md
    |-- metadata.md
    |-- paper.md
    |-- CONVERSION_REPORT.md
    |-- REVIEW_AND_REVISION_ROADMAP.md
    |-- frontmatter/
    |   |-- title_authors.md
    |   |-- abstract.md
    |   `-- keywords.md
    |-- sections/
    |   |-- 01_introduction.md
    |   |-- 02_problem_formulation.md
    |   |-- 03_ppo_controller_design.md
    |   |-- 04_simulation_setup.md
    |   |-- 05_results_discussion.md
    |   `-- 06_conclusion.md
    |-- references/
    |   `-- references.md
    |-- assets/
    |   |-- figures/
    |   |   |-- utc_logo.jpeg
    |   |   |-- journal_logo.png
    |   |   |-- figure_01.png
    |   |   |-- figure_02.png
    |   |   |-- figure_03.png
    |   |   |-- figure_04.png
    |   |   |-- figure_05a.png
    |   |   |-- figure_05b.png
    |   |   |-- figure_06a.png
    |   |   |-- figure_06b.png
    |   |   |-- figure_07a.png
    |   |   `-- figure_07b.png
    |   `-- tables/
    |       |-- table_01_ppo_training_parameters.md
    |       `-- table_02_comparison_results.md
    `-- scripts/
        `-- build_paper.py
```

## Mô tả các thành phần

### Tài liệu gốc

- `Blined.docx`: một bản tài liệu Word của bài báo.
- `TRAJECTORY TRACKING CONTROL OF A QUADCOPTER USING PROXIMAL POLICY OPTIMIZATION.docx`: bản Word nguồn của bài báo về điều khiển bám quỹ đạo waypoint cho quadcopter bằng PPO.

### Thư mục bài báo Markdown

- `waypoint_trajectory_tracking_ppo/`: chứa toàn bộ phiên bản Markdown có thể chỉnh sửa.
- `README.md`: hướng dẫn tổng quan và cách dựng bài báo.
- `metadata.md`: thông tin mô tả quá trình chuyển đổi và bài báo.
- `paper.md`: bản bài báo hoàn chỉnh được sinh tự động từ các file thành phần.
- `CONVERSION_REPORT.md`: báo cáo kiểm tra độ đầy đủ và các vấn đề phát hiện khi chuyển đổi.
- `REVIEW_AND_REVISION_ROADMAP.md`: lộ trình rà soát và chỉnh sửa bài báo.

### Nội dung bài báo

- `frontmatter/`: tiêu đề, tác giả, tóm tắt và từ khóa.
- `sections/`: sáu phần nội dung chính, được đánh số theo thứ tự xuất hiện trong bài.
- `references/references.md`: danh mục tài liệu tham khảo.

### Tài nguyên

- `assets/figures/`: logo và các hình minh họa; các hình 5, 6 và 7 được chia thành hai panel `a` và `b`.
- `assets/tables/`: hai bảng dữ liệu khoa học ở dạng Markdown độc lập.

### Công cụ dựng tài liệu

- `scripts/build_paper.py`: ghép các file trong `frontmatter/`, `sections/` và `references/` theo đúng thứ tự để tạo lại `paper.md`; đồng thời điều chỉnh đường dẫn tài nguyên cho phù hợp với vị trí của file kết quả.

## Quy trình chỉnh sửa

1. Chỉnh sửa các file thành phần trong `frontmatter/`, `sections/` hoặc `references/`.
2. Không chỉnh sửa trực tiếp `paper.md`, vì file này được tạo tự động.
3. Từ thư mục `waypoint_trajectory_tracking_ppo`, chạy lệnh:

```powershell
python .\scripts\build_paper.py
```

4. Kiểm tra lại `paper.md`, các liên kết hình ảnh và bảng biểu sau khi dựng.
