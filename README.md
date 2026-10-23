# VocaFlow-Data

## Tiếp nối phiên làm việc

Trước khi bổ sung hoặc sửa nội dung ở phiên mới, đọc [`AGENTS.md`](AGENTS.md) và [`docs/SESSION_CONTINUITY.md`](docs/SESSION_CONTINUITY.md). Quy tắc bắt buộc: không làm lại hoặc tạo bản trùng của việc đã hoàn thành; kiểm tra manifest, commit, PR và CI hiện tại trước khi thay đổi.

Kho dữ liệu công khai dành cho ứng dụng học tiếng Anh **VocaFlow**. Mã nguồn ứng dụng chính vẫn được quản lý trong repository riêng tư `honghoaibao/VocaFlow`.

Repository này lưu **dữ liệu JSON đã xuất bản, SVG gốc VocaFlow và ảnh PNG được cấp phép để tái phân phối**: bộ từ, bài viết do VocaFlow biên soạn, nguồn học đã duyệt và ảnh minh họa theo từng từ/chủ đề. Ứng dụng đọc qua HTTPS từ nhánh `main`; không cần và không được nhúng GitHub token vào APK.

## Nội dung đã xuất bản

- 7 bộ từ vựng: Daily Routines (A1), School Life (A1), Learning & Exam Skills (A2), Technology & Digital Life (A2), Environment & Climate (B1), Study Planning & Focus (A2), Everyday Communication & Problem Solving (A2).
- 20 liên kết đã duyệt, gồm tài liệu học và video. Đợt 2026-10-19 bổ sung video BBC Learning English về trí nhớ và trang từ vựng A1–A2 của British Council.
- 6 bài viết gốc do VocaFlow biên soạn. Nội dung gồm học từ vựng, hiện tại đơn, đọc hiểu, kế hoạch học 15 phút và bài hướng dẫn dài về xây dựng hệ thống học tiếng Anh bền vững (đăng ngày 2026-10-20), có ví dụ, bài tự luyện và 3 ảnh minh họa trong bài.
- Metadata ảnh: kho nội dung có 125 vị trí ảnh duy nhất: 109 URL minh họa SVG gốc VocaFlow, 11 ảnh PNG lấy từ Wikimedia Commons có giấy phép CC0 và lưu trực tiếp trong repo, 3 ảnh Commons CC0 hiện có và 2 thumbnail YouTube gắn với đúng video tương ứng. Mỗi vị trí ảnh có URL riêng; nguồn, tác giả và giấy phép của 11 PNG được lưu trong JSON. Validator kiểm tra URL trùng, file nội bộ bị thiếu và metadata nguồn/quyền.
- Ứng dụng Android đọc các URL này để hiển thị ảnh và dùng bộ nhớ đệm ảnh của thiết bị. Khi ngoại tuyến, ảnh đã tải trước đó có thể tiếp tục hiển thị; dữ liệu JSON có bộ nhớ đệm riêng.
- Quy trình URL ảnh và giấy phép: [docs/image-source-and-url-workflow.md](docs/image-source-and-url-workflow.md). Công cụ tìm ứng viên Wikimedia Commons: [tool/find_image_candidates.py](tool/find_image_candidates.py), chỉ xuất danh sách JSON để duyệt, không tự sửa nội dung. Chuẩn biên tập: [docs/editorial-style-guide.md](docs/editorial-style-guide.md). Chuẩn bộ từ: [docs/vocabulary-learning-standard.md](docs/vocabulary-learning-standard.md). Bài viết và ví dụ vẫn phải do VocaFlow tự viết.

## Cấu trúc

```
assets/
  illustrations/
    vocabulary/<pack-id>/<word-id>.svg or .png
    articles/<article-id>/cover.svg
    discovery/<resource-id>.svg
  content/
    index.json
  vocabulary/
    packs/
      <topic>_<level>_YYYY-MM-DD.json
  editorial/
    articles/
      <article>_<level>_YYYY-MM-DD.json
  discovery/
    catalog/
      index.json
      approved/
        links-approved-YYYY-MM-DD.json
```

## Quy tắc xuất bản

- Chỉ nội dung có `"status": "published"` mới được đưa vào manifest từ vựng/bài viết.
- Tên tệp và ngày trong trường `publishDate` phải khớp nhau theo định dạng ISO `YYYY-MM-DD`.
- Bài viết cần có `schemaVersion: 1`; không đưa dữ liệu người học, thông tin đăng nhập, token hoặc khóa bí mật vào repository.
- Liên kết khám phá phải dùng HTTPS, có `status: "approved"` và `approvedOn` khớp `approvalDate` của catalog.
- Sau khi thêm gói/bài viết, cập nhật `assets/content/index.json`. Sau khi thêm catalog liên kết đã duyệt, cập nhật `assets/discovery/catalog/index.json`.
- Chỉ xuất bản metadata và nội dung có quyền sử dụng phù hợp. Không sao chép toàn văn bài viết bên ngoài hoặc thumbnail khi chưa xác minh quyền.

## Cập nhật nội dung

1. Thêm tệp JSON mới vào đúng thư mục.
2. Dùng SVG gốc cho hình vector tự thiết kế. Với ảnh chụp hoặc ảnh minh họa lấy từ mạng, ưu tiên Wikimedia Commons CC0/Public Domain; mở trang nguồn và xác minh quyền tải lại, sau đó lưu tệp PNG đã xử lý trực tiếp trong `assets/illustrations/`. `imageUrl` phải trỏ tới tệp trong repo; giữ `imageSourceUrl`, `imageAuthor`, `imageLicense`, `imageLicenseUrl`, `imageRightsNote`, `imageAlt` và `imageCredit` để truy xuất nguồn. Không đưa URL ảnh của bên thứ ba vào nội dung phát hành khi có thể lưu tệp hợp pháp trong repo. Không dùng lại URL giữa bìa, mục từ, bài viết và nguồn học.
3. Kiểm tra JSON, schema, trạng thái xuất bản, ngày và metadata ảnh.
4. Thêm đường dẫn vào manifest tương ứng.
5. Chạy `python3 tool/validate_content.py` hoặc để GitHub Actions tự kiểm tra trước khi gộp.
6. Commit lên `main`; VocaFlow tự tải nội dung đã duyệt khi khởi động và dùng bản JSON đóng gói sẵn khi ngoại tuyến. Sau mỗi thay đổi nội dung, nhớ đồng bộ các JSON đã duyệt sang `app/src/main/assets/assets/` để đảm bảo hai nguồn nhất quán.

## Lưu ý

Dữ liệu học cá nhân được lưu trên thiết bị người dùng. Repository này không phải cơ sở dữ liệu tiến độ người học và không nhận thông tin cá nhân từ ứng dụng.
