# VocaFlow-Data

Kho dữ liệu công khai dành cho ứng dụng học tiếng Anh **VocaFlow**. Mã nguồn ứng dụng chính vẫn được quản lý trong repository riêng tư `honghoaibao/VocaFlow`.

Repository này chỉ lưu **dữ liệu JSON đã xuất bản**: gói từ vựng, bài viết do VocaFlow biên soạn và danh mục đường dẫn học tập đã được duyệt. Ứng dụng đọc các tệp qua HTTPS từ nhánh `main`; không cần và không được nhúng GitHub token vào APK.

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
2. Kiểm tra JSON hợp lệ, schema, trạng thái xuất bản và ngày.
3. Thêm đường dẫn vào manifest tương ứng.
4. Chạy `python3 tool/validate_content.py` hoặc để GitHub Actions tự kiểm tra trước khi gộp.
5. Commit lên `main`.
6. Trong VocaFlow, mở **Khám phá** và dùng biểu tượng cập nhật nội dung để tải dữ liệu mới. Nếu không có mạng hoặc nguồn không khả dụng, app giữ dữ liệu được đóng gói sẵn.

## Lưu ý

Dữ liệu học cá nhân được lưu trên thiết bị người dùng. Repository này không phải cơ sở dữ liệu tiến độ người học và không nhận thông tin cá nhân từ ứng dụng.
