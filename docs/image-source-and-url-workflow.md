# VocaFlow-Data — quy trình lấy URL ảnh trực tiếp và quản lý giấy phép

Quy trình này dành cho người biên tập nội dung. Không chạy tìm ảnh hoặc truy vấn API ảnh trong luồng runtime của ứng dụng.

## 1. Trường metadata

Mỗi ảnh phải có imageUrl, imageAlt và imageCredit. Ảnh bên thứ ba phải lưu thêm imageSourceUrl và imageRightsNote; khi nguồn có giấy phép rõ ràng, lưu imageLicense, imageLicenseUrl và imageAuthor. imageUrl là URL ảnh trực tiếp; imageSourceUrl là trang hồ sơ/nguồn ảnh.

Ảnh SVG do VocaFlow tạo phải nằm tại assets/illustrations/ với đường dẫn riêng cho từng vị trí, có alt text phù hợp và imageCredit ghi rõ VocaFlow Original Illustration. Không trỏ nhiều mục từ khác nhau về cùng một URL chỉ vì chủ đề gần nhau.

## 2. Tìm kiếm và xác minh ứng viên

- Exa/Parallel Search dùng để khám phá từ khóa hoặc trang nguồn, không dùng kết quả tìm kiếm làm URL ảnh cuối cùng.
- Wikimedia Commons API là công cụ lấy URL trực tiếp và metadata giấy phép. Công cụ tool/find_image_candidates.py tự truy vấn API, kiểm tra HTTP/MIME của URL ảnh rồi xuất danh sách JSON để người biên tập xem xét.
- Chạy từ thư mục gốc:

~~~~bash
python3 tool/find_image_candidates.py "solar panels wind turbines landscape" --limit 10 --output candidates-renewable-energy.json
~~~~

- Mặc định chỉ liệt kê ứng viên Public Domain hoặc CC0. Tùy chọn --include-other-licenses chỉ để xem các ứng viên khác, không đồng nghĩa được phép xuất bản.
- Mở trang hồ sơ của từng ảnh; xác nhận hình ảnh đúng nghĩa, độ phân giải phù hợp, không có watermark/giới hạn và điều kiện giấy phép cho phép mục đích sử dụng dự kiến.
- Kiểm tra URL trực tiếp trả HTTP 200/206 cùng Content-Type bắt đầu bằng image/. Nếu trả text/html, từ chối URL đó.
- Lưu URL do API trả về nguyên vẹn, gồm tham số query nếu có. Không dự đoán URL từ tên file.

## 3. Quy tắc giấy phép

Public Domain/CC0 được ưu tiên cho quy trình hiện tại. Vẫn lưu nguồn và tác giả nếu có. CC BY, CC BY-SA, NC, ND, GFDL và các giấy phép thiếu/không rõ metadata phải được xem xét riêng; không tự động đưa vào nội dung phát hành. CC BY/SA có nghĩa vụ ghi công và/hoặc điều kiện bổ sung; chỉ sử dụng khi nhóm đã kiểm tra điều kiện và app có thể hiển thị thông tin được yêu cầu.

Unsplash và Pexels cần dùng URL từ API chính thức và tuân thủ quy định hotlink/ghi nguồn. Không đưa API key vào APK; chỉ dùng qua công cụ biên tập được bảo vệ hoặc backend. Không mirror ảnh bên thứ ba vào GitHub nếu điều khoản nguồn không cho phép sao chép/lưu trữ.

## 4. Quy tắc độ chính xác và trùng ảnh

1. Viết mô tả thị giác cụ thể cho từng từ, không tìm một từ đa nghĩa đứng riêng.
2. Mở ảnh thật và đối chiếu với word, meaning, example và topic.
3. Bìa bộ từ phải phản ánh chủ đề chung; từng từ phải có hình minh họa riêng, đúng nghĩa. Với từ trừu tượng có thể dùng SVG tự thiết kế.
4. Không tái sử dụng URL ở bìa, từ vựng, bài viết hoặc thumbnail nguồn học khác.
5. Viết imageAlt theo đúng chủ thể ảnh; không sao chép alt text cũ sau khi thay hình.
6. Lưu provenance và rights note cho mọi ảnh không phải tài sản gốc của VocaFlow.
7. Chạy python3 tool/validate_content.py trước khi mở PR; CI phải qua.

## 5. Xuất bản

1. Sửa JSON trong assets/vocabulary/packs/, assets/editorial/articles/ hoặc assets/discovery/catalog/approved/.
2. Cập nhật manifest/catalog phù hợp.
3. Kiểm tra không có URL trùng, thiếu metadata, file SVG nội bộ bị thiếu hoặc URL bên ngoài thiếu nguồn/rights note.
4. Đồng bộ JSON đã duyệt vào app/src/main/assets/assets/ trong repository VocaFlow.
5. Chạy validator và build Android; chỉ sau đó mới gộp PR.
6. Không xóa/ghi đè tệp ảnh đã xuất bản ở cùng URL. Tạo đường dẫn mới khi thay hình để tránh cache cũ.

## Tham khảo chính thức

- Wikimedia Commons API: https://api.wikimedia.org/wiki/Documentation/Code_samples/Images_and_media
- MediaWiki Imageinfo: https://www.mediawiki.org/wiki/API:Imageinfo
- Creative Commons: https://creativecommons.org/reusing-cc-licensed-content/
- Unsplash API: https://help.unsplash.com/en/articles/2511245-unsplash-api-guidelines
- Pexels API: https://www.pexels.com/api/documentation/
- Cloudinary Upload API: https://cloudinary.com/documentation/upload_images
