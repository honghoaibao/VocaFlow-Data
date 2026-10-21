# VocaFlow-Data

Kho dữ liệu công khai dành cho ứng dụng học tiếng Anh **VocaFlow**. Mã nguồn ứng dụng chính vẫn được quản lý trong repository riêng tư `honghoaibao/VocaFlow`.

Repository này chỉ lưu **dữ liệu JSON đã xuất bản**: gói từ vựng, bài viết do VocaFlow biên soạn và danh mục đường dẫn học tập đã được duyệt. Ứng dụng đọc các tệp qua HTTPS từ nhánh `main`; không cần và không được nhúng GitHub token vào APK.

## Nội dung đã xuất bản

- 7 bộ từ vựng: Daily Routines (A1), School Life (A1), Learning & Exam Skills (A2), Technology & Digital Life (A2), Environment & Climate (B1), Study Planning & Focus (A2), Everyday Communication & Problem Solving (A2).
- 20 liên kết đã duyệt, gồm tài liệu học và video. Đợt 2026-10-19 bổ sung video BBC Learning English về trí nhớ và trang từ vựng A1–A2 của British Council.
- 6 bài viết gốc do VocaFlow biên soạn. Nội dung gồm học từ vựng, hiện tại đơn, đọc hiểu, kế hoạch học 15 phút và bài hướng dẫn dài về xây dựng hệ thống học tiếng Anh bền vững (đăng ngày 2026-10-20), có ví dụ, bài tự luyện và 3 ảnh minh họa trong bài.
- Metadata ảnh: mỗi bìa bộ từ, từ vựng, bìa bài viết, ảnh trong bài và nguồn học đều có `imageUrl` (HTTPS), `imageAlt` và `imageCredit`. Ảnh trùng nguồn đã được thay bằng ảnh riêng; bộ kiểm tra dùng đường dẫn ảnh gốc (bỏ qua query crop) để ngăn ảnh lặp trở lại.
- Ứng dụng Android đọc các URL này để hiển thị ảnh và dùng bộ nhớ đệm ảnh của thiết bị. Khi ngoại tuyến, ảnh đã tải trước đó có thể tiếp tục hiển thị; dữ liệu JSON có bộ nhớ đệm riêng.
- Chuẩn biên tập: [docs/editorial-style-guide.md](docs/editorial-style-guide.md). Chuẩn tạo bộ từ: [docs/vocabulary-pack-authoring-guide.md](docs/vocabulary-pack-authoring-guide.md). Bài viết, ví dụ và câu luyện tập phải do VocaFlow tự biên soạn.

## Cấu trúc

```
assets/
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
2. Thêm `imageUrl`, `imageAlt` và `imageCredit` cho mỗi mục có ảnh. Mỗi nguồn ảnh phải riêng biệt, liên quan đến nội dung; query crop khác nhau không được tính là ảnh mới.
3. Kiểm tra JSON, schema, trạng thái xuất bản, ngày và metadata ảnh.
4. Thêm đường dẫn vào manifest tương ứng.
5. Chạy `python3 tool/validate_content.py`. Bộ kiểm tra xác minh JSON/schema, metadata ảnh và nguồn ảnh trùng trong toàn bộ nội dung xuất bản.
6. Commit lên `main`; VocaFlow sẽ tự tải nội dung khi mở app và cũng có nút cập nhật thủ công trong Hồ sơ & cài đặt. Nếu không có mạng hoặc nguồn không khả dụng, app giữ dữ liệu được đóng gói sẵn.

## Lưu ý

Dữ liệu học cá nhân được lưu trên thiết bị người dùng. Repository này không phải cơ sở dữ liệu tiến độ người học và không nhận thông tin cá nhân từ ứng dụng.
