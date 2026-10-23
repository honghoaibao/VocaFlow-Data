# Quy tắc tiếp nối phiên làm việc — VocaFlow-Data

> **Bắt buộc đọc trước mỗi phiên sửa dữ liệu.** Tài liệu này là sổ nhớ bền vững của repository; không dựa riêng vào lịch sử chat để quyết định một việc đã làm hay chưa.

## Quy tắc cốt lõi

**Không làm lại, tạo lại, đăng lại hoặc triển khai song song công việc đã hoàn thành, trừ khi anh yêu cầu rõ ràng, yêu cầu đã thay đổi đáng kể, hoặc đã xác minh được lỗi/thiếu sót thực sự.**

Yêu cầu “tiếp tục”, “triển khai”, “cập nhật” chỉ cho phép xử lý phần được yêu cầu; không đồng nghĩa với việc làm lại những phần đã xong hay thêm nội dung trùng để thể hiện tiến độ.

Nếu kết quả đã tồn tại và hoạt động đúng, hãy xác minh nhanh rồi báo trạng thái và đường dẫn; **không sửa file chỉ để tạo ra thay đổi**.

## Checklist bắt buộc trước khi sửa

1. Đọc `AGENTS.md`, tài liệu này, README và các hướng dẫn liên quan.
2. Kiểm tra `main`, commit gần đây, PR đang mở/đã gộp và kết quả CI liên quan. PR tồn tại chưa có nghĩa là đã gộp; phải xác minh trạng thái.
3. Mở manifest/catalog hiện hành, file JSON liên quan, validator và URL ảnh. Không suy đoán dựa vào tên file hoặc lịch sử chat.
4. So sánh yêu cầu mới với sổ việc đã hoàn thành bên dưới.
5. Phân loại việc cần làm: **mới hoàn toàn**, **mở rộng một phần**, **sửa lỗi đã xác minh**, hoặc **đã hoàn tất**.

Thứ tự nguồn trạng thái đáng tin cậy: file/manifest hiện tại trên `main` → commit/PR đã xác minh và CI → sổ việc này → lịch sử chat.

## Quy tắc khi cập nhật nội dung

- **Không tạo bộ từ, bài viết, nguồn học, ảnh hoặc tài liệu trùng lặp.** Trước khi thêm, kiểm tra ID, tên file, ngày, URL, chủ đề và nội dung hiện hành.
- Nếu nội dung cần mở rộng, cập nhật nguồn chuẩn hiện có khi phù hợp; không tạo bản sao gần giống chỉ vì phiên mới không thấy lịch sử cũ.
- Không thay nội dung đã duyệt, đổi URL ảnh, thay giấy phép, hoặc viết lại bài đã xuất bản nếu yêu cầu không cần việc đó.
- Không chọn ảnh chỉ vì kết quả tìm kiếm đầu tiên. Tiếp tục dùng quy trình ở [image-source-and-url-workflow.md](image-source-and-url-workflow.md), kiểm tra trang nguồn/quyền sử dụng và chạy validator.
- Không đóng gói lại ảnh của bên thứ ba nếu điều khoản không cho phép. Không phỏng đoán giấy phép từ phần mở rộng URL.
- Không thay đổi manifest/catalog khi không có mục mới thực sự cần xuất bản. Nếu cần thêm, kiểm tra trùng trước, cập nhật đúng manifest và chạy `python3 tool/validate_content.py`.
- Không chỉnh sửa các phần không liên quan ngoài phạm vi yêu cầu.
- Không nói “đã kiểm thử”, “CI xanh”, “đã xuất bản” nếu chưa kiểm tra kết quả tương ứng.

## Khi trạng thái chưa rõ

- Nếu có thể xác minh bằng file, manifest, PR hoặc CI, hãy xác minh trước khi sửa.
- Nếu chỉ hoàn thành một phần, tiếp tục đúng phần còn thiếu và giữ nguyên phần đang hoạt động.
- Nếu phát hiện lỗi thật, ghi rõ bằng chứng rồi sửa tối thiểu để giải quyết lỗi.
- Nếu không thể xác minh được, không tạo bản sao theo phỏng đoán; nêu rõ điều chưa chắc chắn hoặc hỏi một câu trọng tâm.

## Sau khi hoàn thành việc

Cập nhật sổ việc này **ngay trong cùng đợt thay đổi**. Cập nhật mục có sẵn nếu cùng một kết quả; chỉ thêm mục mới khi là một nhiệm vụ khác biệt.

Mẫu:

```markdown
### YYYY-MM-DD — Tên ngắn của công việc
- Trạng thái: hoàn tất / một phần / đang chặn
- File chuẩn đã sửa:
- PR / commit:
- Kiểm chứng thực tế:
- Giới hạn hoặc phần chưa kiểm chứng:
```

Chỉ ghi kết quả đã thực hiện và kiểm tra. Không biến dự định thành kết quả hoàn thành.

## Sổ việc đã hoàn thành — mốc 2026-10-22

### 1. Quy trình URL ảnh trực tiếp, nguồn và giấy phép
- **Trạng thái:** PR [#9](https://github.com/honghoaibao/VocaFlow-Data/pull/9) đã gộp.
- **Đã có:** `docs/image-source-and-url-workflow.md`, `tool/find_image_candidates.py` (tìm ứng viên Wikimedia Commons, trả URL ảnh trực tiếp và metadata), validator kiểm tra URL/metadata/quyền sử dụng/trùng lặp, cập nhật hướng dẫn và CI.
- **Không làm lại:** không tạo thêm một công cụ tìm ảnh hoặc tài liệu quy trình song song. Mở rộng công cụ hiện có khi có nhu cầu mới cụ thể.

### 2. Sửa số liệu danh mục ảnh trong README
- **Trạng thái:** PR [#10](https://github.com/honghoaibao/VocaFlow-Data/pull/10) đã gộp; CI kiểm tra sau khi gộp đã thành công theo kết quả được ghi nhận.
- **Đã có:** số liệu README khớp danh mục ảnh, phân biệt SVG gốc, ảnh CC0 Wikimedia Commons và thumbnail video.
- **Không làm lại:** đừng tạo PR khác chỉ để lặp lại điều chỉnh số liệu này. Chỉ sửa nếu số liệu hiện tại lệch so với manifest hoặc yêu cầu thay đổi.

### 3. Baseline nội dung và ảnh hiện hành
- **Trạng thái:** nội dung đã xuất bản, phải kiểm tra trước khi thêm mới.
- README ở mốc này ghi nhận **7 bộ từ, 6 bài viết, 20 liên kết khám phá đã duyệt và 125 vị trí ảnh**: 120 URL SVG gốc VocaFlow, 3 ảnh Wikimedia Commons CC0 đã kiểm tra và 2 thumbnail YouTube.
- Đây là số liệu theo thời điểm, không phải hằng số vĩnh viễn. Khi cần, đếm lại từ manifest/catalog thực tế.
- **Không làm lại:** không thêm lại cùng bộ từ/bài viết/liên kết hoặc tái sử dụng trùng URL ảnh. Nội dung mới phải thật sự mới, tuân thủ schema và vượt qua validator.

## Nguyên tắc cuối

**Kiểm tra trước, chỉ bổ sung phần còn thiếu hoặc phần được yêu cầu mới, xác minh kết quả rồi ghi lại để phiên sau không phải làm lại.**

### 2026-10-23 — Thay bộ SVG nháp bằng ảnh PNG CC0 lấy từ mạng cho Daily Routines A1
- **Trạng thái:** Đã gộp qua [PR #14](https://github.com/honghoaibao/VocaFlow-Data/pull/14), commit `9e603b7cb187387d5edf47c3e1d356067249b749`.
- **Phạm vi chuẩn:** Cập nhật bộ từ hiện có `assets/vocabulary/packs/daily_routines_a1_2026-10-18.json`; giữ ID bộ từ, tên tệp, ngày xuất bản, nghĩa, ví dụ và 10 ID từ.
- **Ảnh:** 11 tệp PNG thật (10 ảnh từ + 1 bìa), 720×480, được tải từ các trang file Wikimedia Commons đã duyệt và lưu tại `assets/illustrations/vocabulary/daily-routines-a1-photos-2026-10-23/`. URL hiển thị trong app đều trỏ về file trong VocaFlow-Data, không dùng URL trực tiếp của Wikimedia tại runtime.
- **Quyền sử dụng:** Mỗi bản ghi giữ `imageSourceUrl`, `imageAuthor`, `imageLicense`, `imageLicenseUrl`, `imageRightsNote`, `imageAlt` và `imageCredit`. Chỉ nhập các trang ghi CC0 1.0; các file đã tải được chuyển/cắt sang PNG tối ưu bằng Pillow. 11 ảnh mới có URL duy nhất, tổng dung lượng khoảng 3.7 MB.
- **Loại bỏ phương án nháp:** Thư mục `daily-routines-a1-refresh-2026-10-23/` chứa bộ SVG nháp trước đó đã bị xoá khỏi nhánh PR; không khôi phục hoặc tạo thêm bản SVG tương tự. Các hình SVG cũ ở thư mục chuẩn khác không bị thay đổi.
- **Kiểm chứng:** Import workflow [run #39943350273](https://github.com/honghoaibao/VocaFlow-Data/actions/runs/39943350273) thành công sau khi sửa bước staging để dùng được khi thư mục SVG đã bị xóa; validator trên nhánh thành công ở [run #39943350195](https://github.com/honghoaibao/VocaFlow-Data/actions/runs/39943350195). Sau khi gộp, data validator thành công trên `main` ở [run #39943529405](https://github.com/honghoaibao/VocaFlow-Data/actions/runs/39943529405). Đã xác minh trên `main` có đủ 11 PNG và pack JSON tham chiếu các URL PNG nội bộ.
- **Không làm lại:** Không tìm/đăng bộ ảnh thứ hai cho cùng pack; tiếp tục từ PR #14, xác minh PNG và giấy phép đã lưu rồi đồng bộ JSON sang repo Android.

### 2026-10-23 — Siết tiêu chí tìm ảnh theo chính từ vựng
- **Trạng thái:** Đã cập nhật tài liệu hướng dẫn hiện có; không nhập/thay ảnh và không sửa nội dung bộ từ trong đợt này.
- **File chuẩn đã sửa:** `docs/image-source-and-url-workflow.md`, `README.md`, `docs/SESSION_CONTINUITY.md`.
- **Quy tắc mới:** Bắt đầu tìm bằng đúng `word` (ví dụ `habits`); nếu chưa đạt mới thử dạng từ gần, collocation và cụm mô tả thị giác bám sát `meaning`/`example`. Chấm độ phù hợp 0–3; chỉ duyệt mức 2–3 (trực tiếp hoặc liên tưởng rõ). Độ liên quan và giấy phép là hai điều kiện bắt buộc độc lập.
- **Giới hạn:** Đây là thay đổi tài liệu. Chưa thay 11 PNG hiện hành và chưa xác nhận từng ảnh cũ đạt tiêu chí mới; cần kiểm tra chúng riêng trước khi quyết định thay ảnh.


### 2026-10-23 — Thay bộ PNG Daily Routines bằng ảnh khớp nghĩa hơn
- **Trạng thái:** Đang triển khai qua PR riêng; chỉ đánh dấu hoàn tất sau khi workflow nhập PNG, validator và đồng bộ Android đều thành công.
- **Phạm vi:** Giữ nguyên bộ từ, ID và nội dung học; thay ảnh của 10 mục từ cùng ảnh bìa bằng bộ PNG mới trong `assets/illustrations/vocabulary/daily-routines-a1-semantic-photos-2026-10-23/`.
- **Tiêu chí:** Tìm theo từ cần học trước; duyệt hình ảnh thực tế và đối chiếu nghĩa/câu ví dụ. Các ứng viên được khóa trong script chỉ lấy từ trang Wikimedia Commons có ghi CC0 1.0. Ảnh được tải về, chuyển sang PNG và app chỉ dùng URL trong repository.
- **Nguồn ảnh mới:** Habit cycle, Workflow progress, alarm clock (usually), Confidence and courage, Daily Planner Template, School Supplies, Student taking notes, Person taking notes, Cup of tea, Objetivos target, Breakfast menu a coffee and toasts (cover).
- **File chuẩn:** `tool/import_daily_routines_png.py`, `.github/workflows/import-daily-routines-png.yml`, pack JSON chuẩn và sau đó là bản JSON offline ở repository Android.
- **Kiểm chứng:** Chưa ghi là hoàn tất trước khi GitHub Actions thực sự tải đủ 11 nguồn, tạo PNG, chạy validator và CI Android thành công.
- **Giới hạn:** Một vài nghĩa trừu tượng như `confident` và `break` vẫn được minh họa bằng hình mang tính biểu tượng, không phải hành động được chụp trực tiếp.