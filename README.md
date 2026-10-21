# VocaFlow-Data

Kho dữ liệu công khai dành cho ứng dụng học tiếng Anh **VocaFlow**. Mã nguồn ứng dụng chính vẫn được quản lý trong repository riêng tư `honghoaibao/VocaFlow`.

Repository này lưu **dữ liệu JSON đã xuất bản và minh họa vector SVG gốc**: bộ từ, bài viết do VocaFlow biên soạn, nguồn học đã duyệt và ảnh minh họa theo từng từ/chủ đề. Ứng dụng đọc qua HTTPS từ nhánh `main`; không cần và không được nhúng GitHub token vào APK.

## Nội dung đã xuất bản

- 7 bộ từ vựng: Daily Routines (A1), School Life (A1), Learning & Exam Skills (A2), Technology & Digital Life (A2), Environment & Climate (B1), Study Planning & Focus (A2), Everyday Communication & Problem Solving (A2).
- 20 liên kết đã duyệt, gồm tài liệu học và video. Đợt 2026-10-19 bổ sung video BBC Learning English về trí nhớ và trang từ vựng A1–A2 của British Council.
- 6 bài viết gốc do VocaFlow biên soạn. Nội dung gồm học từ vựng, hiện tại đơn, đọc hiểu, kế hoạch học 15 phút và bài hướng dẫn dài về xây dựng hệ thống học tiếng Anh bền vững (đăng ngày 2026-10-20), có ví dụ, bài tự luyện và 3 ảnh minh họa trong bài.
- Metadata ảnh: 7 bộ từ, 88 mục từ, 6 bìa bài viết, 4 ảnh trong bài và 18 thumbnail nguồn học dùng minh họa SVG gốc VocaFlow, mỗi vị trí có URL riêng và mô tả đúng nội dung. Hai thumbnail YouTube riêng biệt được giữ nguyên cho đúng video tương ứng. Validator kiểm tra tính duy nhất xuyên suốt bộ từ, bài viết và nguồn học; URL bị dùng lại sẽ làm kiểm định thất bại.
- Ứng dụng Android đọc các URL này để hiển thị ảnh và dùng bộ nhớ đệm ảnh của thiết bị. Khi ngoại tuyến, ảnh đã tải trước đó có thể tiếp tục hiển thị; dữ liệu JSON có bộ nhớ đệm riêng.
- Chuẩn biên tập: [docs/editorial-style-guide.md](docs/editorial-style-guide.md). Chuẩn bộ từ: [docs/vocabulary-learning-standard.md](docs/vocabulary-learning-standard.md), gồm tiêu chí chọn từ, ảnh không trùng, hoạt động truy hồi và lịch ôn thích ứng. Bài viết và ví dụ vẫn phải do VocaFlow tự viết.

## Cấu trúc

```
assets/
  illustrations/
    vocabulary/<pack-id>/<word-id>.svg
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
2. Tạo hoặc chọn SVG gốc phù hợp trực tiếp với chủ đề/từ; thêm `imageUrl`, `imageAlt` và `imageCredit`. Không dùng lại URL giữa bìa, mục từ, bài viết và nguồn học. Chỉ giữ thumbnail bên thứ ba khi đó là ảnh của đúng video/nguồn.
3. Kiểm tra JSON, schema, trạng thái xuất bản, ngày và metadata ảnh.
4. Thêm đường dẫn vào manifest tương ứng.
5. Chạy `python3 tool/validate_content.py` hoặc để GitHub Actions tự kiểm tra trước khi gộp.
6. Commit lên `main`; VocaFlow tự tải nội dung đã duyệt khi khởi động và dùng bản JSON đóng gói sẵn khi ngoại tuyến. Sau mỗi thay đổi nội dung, nhớ đồng bộ các JSON đã duyệt sang `app/src/main/assets/assets/` để đảm bảo hai nguồn nhất quán.

## Lưu ý

Dữ liệu học cá nhân được lưu trên thiết bị người dùng. Repository này không phải cơ sở dữ liệu tiến độ người học và không nhận thông tin cá nhân từ ứng dụng.
