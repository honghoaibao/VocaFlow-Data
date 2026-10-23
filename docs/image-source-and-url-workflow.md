# VocaFlow-Data — quy trình tìm ảnh đúng nghĩa, lấy PNG và quản lý giấy phép

Tài liệu này dành cho người biên tập nội dung. **Độ khớp với từ vựng và quyền sử dụng là hai điều kiện độc lập**: ảnh có giấy phép tốt nhưng không minh họa được từ thì vẫn không được chọn. Không tìm ảnh trong luồng runtime của ứng dụng.

## 1. Nguyên tắc quan trọng nhất: tìm theo chính từ vựng trước

Với mỗi mục từ, bắt đầu bằng từ/cụm từ tiếng Anh mà người học nhìn thấy trong bộ từ. Đừng bắt đầu bằng một chủ đề rộng hoặc một vật thể chỉ có liên hệ rất xa.

Thứ tự tìm kiếm bắt buộc:

1. **Từ/cụm từ chính xác:** dùng nguyên từ trong trường `word`, kể cả khi nó là dạng số nhiều hoặc một cụm từ.
2. **Biến thể gần nhất:** dạng số ít/số nhiều, dạng từ gốc, hoặc biến thể ngữ pháp cần thiết.
3. **Cụm từ thường đi cùng từ:** chọn theo đúng nghĩa cần minh họa trong trường `meaning` và câu `example`.
4. **Mô tả thị giác của chính nghĩa đó:** chỉ dùng khi tìm trực tiếp chưa ra ảnh phù hợp. Cụm mô tả phải diễn tả hành động/khái niệm thật sự, không phải liên tưởng tùy tiện.

### Ví dụ: từ “habits”

Tìm đúng từ trước:

```bash
python3 tool/find_image_candidates.py "habits" --limit 15 --output candidates-habits.json
```

Nếu kết quả không đạt, tiếp tục từng lượt và xem lại ảnh thật:

```bash
python3 tool/find_image_candidates.py "habit" --limit 15 --output candidates-habit.json
python3 tool/find_image_candidates.py "daily habits" --limit 15 --output candidates-daily-habits.json
python3 tool/find_image_candidates.py "healthy habits" --limit 15 --output candidates-healthy-habits.json
```

Chỉ dùng các lượt sau khi chúng phù hợp với nghĩa và câu ví dụ đang dạy. **Không tự động chấp nhận ảnh checklist, lịch, máy tính, người đang cười hoặc cây đang lớn chỉ vì chúng có thể gợi một ý liên quan.** Ví dụ, một checklist chung có thể biểu thị việc đánh dấu công việc, nhưng chưa chắc làm người học liên tưởng được đến “habits” (thói quen). Phải mở ảnh và đánh giá đúng nội dung nhìn thấy.

### Quy tắc cho từ trừu tượng

Có thể dùng biểu tượng hoặc hình ảnh mang tính khái niệm khi nghĩa khó chụp trực tiếp, nhưng sự liên tưởng phải rõ ràng, quen thuộc và ăn khớp với **nghĩa cụ thể trong bộ từ**. Không dùng một mối liên hệ chung chung để biện minh cho ảnh lệch nghĩa. Nếu chưa có ảnh đủ rõ, tiếp tục tìm bằng biến thể/cụm từ phù hợp hoặc để mục ảnh chờ duyệt; không chọn bừa cho đủ số lượng.

## 2. Công cụ tìm ứng viên

- `tool/find_image_candidates.py` tìm trên Wikimedia Commons, kiểm tra URL ảnh trực tiếp và trả về metadata nguồn/giấy phép. Công cụ **chỉ liệt kê ứng viên**, không tự chọn ảnh và không sửa bộ từ đã xuất bản.
- Chạy từ thư mục gốc repo:

```bash
python3 tool/find_image_candidates.py "habits" --limit 15 --output candidates-habits.json
```

- Mỗi truy vấn nên có tệp kết quả riêng để so sánh ứng viên giữa các từ khóa. Mặc định công cụ chỉ liệt kê ứng viên được đánh dấu Public Domain hoặc CC0.
- `--include-other-licenses` chỉ dùng để kiểm tra thêm ứng viên; **không** có nghĩa là được phép xuất bản.
- Exa/Parallel Search hoặc công cụ tìm kiếm khác có thể giúp khám phá thuật ngữ; nhưng tên kết quả hay hình xem trước không chứng minh được ý nghĩa, URL trực tiếp hoặc quyền sử dụng. Mọi ảnh cuối cùng đều phải qua bước kiểm tra thủ công và kiểm tra giấy phép.

## 3. Cổng kiểm duyệt độ liên quan

Mở chính tệp ảnh ở kích thước đủ lớn, không chỉ đọc tên tệp, tiêu đề, mô tả API hoặc xem thumbnail. So sánh ảnh với cả `word`, `meaning`, `example` và `topic`.

Dùng thang đánh giá nội bộ:

- **3 — Trực tiếp:** ảnh cho thấy chính đồ vật, hành động hoặc tình huống được từ diễn tả.
- **2 — Liên tưởng rõ:** biểu tượng/ẩn dụ quen thuộc giúp người học dễ liên tưởng đến đúng nghĩa trong ngữ cảnh.
- **1 — Liên hệ lỏng:** cần giải thích thêm hoặc phải suy luận nhiều bước mới nối được ảnh với từ.
- **0 — Không phù hợp:** ảnh đẹp hoặc đúng chủ đề rộng nhưng không giúp hiểu từ đang học.

**Chỉ duyệt mức 2 hoặc 3.** Mức 0–1 phải bị loại và tìm phương án khác, kể cả khi ảnh đạt CC0. Nếu từ có nhiều nghĩa, chọn đúng nghĩa đang dạy chứ không chọn một ảnh hợp với nghĩa khác. Mỗi mục từ cần hình phù hợp riêng; không dùng cùng một URL cho nhiều từ chỉ vì chúng cùng chủ đề.

Bìa bộ từ chỉ cần thể hiện chủ đề chung. Tiêu chí bìa không được dùng để nới lỏng tiêu chí ngữ nghĩa cho ảnh của từng từ.

## 4. Xác minh nguồn, giấy phép và file ảnh

- Mở trang file Wikimedia Commons của **từng** ứng viên được chọn và xác minh giấy phép trên chính trang đó. Ưu tiên CC0/Public Domain; không suy đoán quyền từ URL, tên tác giả hoặc kết quả tìm kiếm.
- Kiểm tra ảnh không bị watermark, không có giới hạn ngoài dự kiến và có chất lượng/độ phân giải phù hợp. Giấy phép hợp lệ không thay thế bước kiểm duyệt độ liên quan ở mục 3.
- Kiểm tra URL ảnh trực tiếp trả HTTP 200/206 cùng `Content-Type` bắt đầu bằng `image/`. Nếu trả `text/html`, từ chối URL đó.
- Không đoán URL từ tên file. Giữ nguyên URL do API trả về khi xác minh nguồn.
- Không mirror/tải lưu ảnh bên thứ ba nếu điều khoản không cho phép. Với quy trình PNG lưu trong repo, chỉ nhập ảnh có quyền tái phân phối rõ ràng đã kiểm chứng.
- `CC BY`, `CC BY-SA`, `NC`, `ND`, `GFDL` và giấy phép thiếu/không rõ metadata không được tự động duyệt. Chỉ sử dụng sau khi kiểm tra nghĩa vụ cụ thể và khả năng đáp ứng của ứng dụng.

## 5. Lưu PNG và metadata vào VocaFlow-Data

Khi đã qua **cả hai cổng** — độ liên quan tối thiểu 2/3 và quyền sử dụng hợp lệ — hãy lưu file ảnh được phép tái phân phối vào repo, xử lý/cắt ảnh nếu cần và bảo đảm tệp đầu ra thật sự là PNG.

Mỗi bản ghi ảnh bên ngoài phải lưu tối thiểu:

- `imageUrl`: URL PNG cuối cùng trong repo VocaFlow-Data, không phải URL ảnh của nhà cung cấp bên thứ ba ở runtime.
- `imageAlt`: mô tả đúng chủ thể/hành động trong ảnh.
- `imageCredit`, `imageSourceUrl`, `imageAuthor`, `imageLicense`, `imageLicenseUrl`, `imageRightsNote`: metadata nguồn và quyền sử dụng.
- Dùng URL riêng cho từng vị trí ảnh. Khi thay ảnh đã xuất bản, tạo đường dẫn mới để tránh cache giữ ảnh cũ.

Ảnh SVG gốc do VocaFlow tự thiết kế là loại tài sản khác; không dùng SVG tự vẽ để lách qua bước tìm/kiểm duyệt PNG theo yêu cầu của một đợt cập nhật ảnh lấy từ mạng.

## 6. Kiểm tra trước khi xuất bản

1. Đối chiếu lại ảnh ở kích thước lớn với từ, nghĩa, câu ví dụ và chủ đề.
2. Đánh giá độ liên quan 0–3; chỉ tiếp tục với mức 2–3.
3. Xác minh trang nguồn, giấy phép và URL ảnh trực tiếp.
4. Kiểm tra `imageAlt` cùng toàn bộ provenance/rights metadata.
5. Kiểm tra không trùng URL, lưu PNG được cấp phép vào đúng thư mục và cập nhật JSON chuẩn trong `assets/vocabulary/packs/`, `assets/editorial/articles/` hoặc `assets/discovery/catalog/approved/` khi phù hợp.
6. Cập nhật manifest/catalog phù hợp, đồng bộ JSON đã duyệt sang repo Android và chạy `python3 tool/validate_content.py`. Chờ CI kiểm tra thành công trước khi gộp.

Không đánh đổi độ liên quan để tiết kiệm thời gian, lấp đủ số lượng ảnh hoặc giữ một ảnh đã chọn trước đó.

## Tham khảo chính thức

- Wikimedia Commons API: https://api.wikimedia.org/wiki/Documentation/Code_samples/Images_and_media
- MediaWiki Imageinfo: https://www.mediawiki.org/wiki/API:Imageinfo
- Creative Commons: https://creativecommons.org/reusing-cc-licensed-content/
- Unsplash API: https://help.unsplash.com/en/articles/2511245-unsplash-api-guidelines
- Pexels API: https://www.pexels.com/api/documentation/
- Cloudinary Upload API: https://cloudinary.com/documentation/upload_images
