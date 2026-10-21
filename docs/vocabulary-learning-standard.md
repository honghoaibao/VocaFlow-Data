# Chuẩn biên soạn bộ từ vựng VocaFlow

Tài liệu này là tiêu chuẩn bắt buộc cho mọi bộ từ mới và mọi lần cập nhật nội dung đã xuất bản. Mục tiêu là giúp người học nhớ nghĩa, nhận ra từ trong ngữ cảnh và tự sử dụng được từ, thay vì chỉ lướt qua danh sách từ.

## 1. Xác định mục tiêu và trình độ

- Chọn một chủ đề thống nhất, hữu ích với học sinh THPT, giao tiếp thường ngày hoặc mục tiêu thi tiếng Anh.
- Ghi trình độ CEFR phù hợp (A1–B2), mục tiêu học cụ thể và những tình huống người học sẽ gặp từ đó.
- Tránh trộn từ quá dễ và quá khó trong cùng bộ nếu chúng không phục vụ một mục tiêu chung.
- Ưu tiên từ/cụm từ phổ biến, collocation, phrasal verb và các dạng từ có thể dùng trong câu thực tế.
- Kiểm tra trùng ID giữa tất cả bộ từ trước khi xuất bản.

## 2. Trường dữ liệu bắt buộc

Mỗi bộ từ phải có schemaVersion 1, trạng thái published, id, topic, level, title, description, publishDate, imageUrl, imageAlt, imageCredit và danh sách words không rỗng. Mỗi mục từ cần có:

- **id:** duy nhất toàn kho, chữ thường, số và dấu gạch nối.
- **word:** từ hoặc cụm từ tiếng Anh chuẩn chính tả.
- **meaning:** nghĩa tiếng Việt rõ ràng, phù hợp ngữ cảnh.
- **partOfSpeech:** từ loại chính xác; với phrasal verb/cụm từ, ghi rõ nếu schema hiện tại hỗ trợ.
- **pronunciation:** phiên âm thống nhất giữa các mục (IPA khi có nguồn đáng tin cậy).
- **example:** câu tiếng Anh tự nhiên, đúng ngữ pháp, làm rõ đúng nghĩa cần học; không dịch máy cứng nhắc.
- **imageUrl, imageAlt, imageCredit:** ảnh HTTPS, mô tả có ý nghĩa và ghi nhận nguồn.

Nếu schema được mở rộng, phải cập nhật validator và tài liệu trước khi đưa trường mới vào nội dung phát hành.

## 3. Tiêu chuẩn ảnh minh họa — không dùng ảnh trùng

- Mỗi bìa bộ từ, mỗi mục từ và mỗi ảnh chèn trong bài viết là một vị trí ảnh riêng. Không tái sử dụng cùng URL Unsplash cho các vị trí khác nhau, kể cả ở hai bộ từ khác nhau.
- Bìa phải gợi đúng chủ đề chung; ảnh của từng mục phải giúp liên tưởng đến chính từ/cụm từ, không dùng một ảnh bàn học/sổ tay cho hàng loạt từ khác nghĩa.
- Đối chiếu ảnh thật trước khi xuất bản: ảnh tải được, chủ thể phù hợp với từ, không bị watermark và không phải thumbnail bên thứ ba khi chưa có quyền.
- Dùng URL HTTPS ổn định; thêm imageAlt ngắn gọn mô tả chủ thể/ý nghĩa trong ngữ cảnh và imageCredit nêu nguồn. Không để alt rỗng hoặc giữ alt của ảnh cũ sau khi thay ảnh.
- Kiểm tra trùng URL xuyên suốt các bìa bộ từ, ảnh từng từ, ảnh bìa bài viết và ảnh nằm trong thân bài. Validator sẽ từ chối URL tái sử dụng trong kho học tập.
- Không nhúng tệp riêng tư, token, thông tin tài khoản hoặc dữ liệu tiến độ cá nhân trong nội dung công khai.

## 4. Thiết kế một buổi học

VocaFlow không được quay lại màn hình giới thiệu dài trước mỗi buổi. Người học mở bộ từ là đi thẳng vào hoạt động học; có thể xem phần giải nghĩa của từ như một bước học thực sự, nhưng không thêm màn hình bắt đầu lặp lại.

Lộ trình thực hành mặc định:

1. **Ưu tiên ôn:** đưa từ đến hạn ôn lên trước.
2. **Gặp từ mới:** sau nhóm ôn đến hạn, ưu tiên từ chưa được ghi nhận trong lịch sử học của bộ.
3. **Nhớ nghĩa chủ động:** người học tự chọn nghĩa trước khi được xem phản hồi.
4. **Nhận diện ngữ cảnh:** chọn từ phù hợp với câu hoàn chỉnh; phương án nhiễu phải hợp lý nhưng không mơ hồ.
5. **Tự gõ từ:** nhớ và viết lại từ không có danh sách đáp án.
6. **Ghép cặp hoặc flashcard:** dùng như hoạt động bổ sung để đổi dạng truy hồi, không thay thế hoàn toàn việc tự nhớ.

Mỗi buổi nên giới hạn số từ theo thiết kế hiện hành của app, không tạo một bài quá dài chỉ để đưa nhiều từ hơn vào một lượt. Khi bộ có đủ từ, xáo thứ tự phương án nhưng không xáo mất mối liên hệ nghĩa–ví dụ–ảnh.

## 5. Lịch ôn thích ứng

- Trả lời sai hoặc không nhớ: đánh dấu cần ôn sớm; không coi là đã thành thạo.
- Trả lời đúng nhưng còn phân vân: dùng mức ôn thận trọng hơn.
- Trả lời đúng ổn định: kéo dài khoảng cách ôn dần.
- Chỉ ghi nhận mức thành thạo từ nhiều lần truy hồi ở các thời điểm khác nhau, không từ một lần trả lời đúng.
- Lưu từng kết quả ngay trên thiết bị. Đồng bộ cloud không được làm mất dữ liệu cục bộ hoặc trộn tiến độ giữa hai tài khoản.
- Khi xung đột lịch ôn cục bộ và cloud, giữ lần ôn mới hơn; nếu thời điểm bằng nhau, không âm thầm đẩy ngày ôn ra xa hơn.

## 6. Kiểm tra chất lượng trước xuất bản

1. Đọc soát chính tả, từ loại, nghĩa tiếng Việt, phát âm và ví dụ.
2. Kiểm tra mỗi ví dụ chứa cách dùng tự nhiên của từ mục tiêu.
3. Xác minh URL ảnh còn hoạt động, ảnh phù hợp và alt/credit không còn sót từ ảnh trước.
4. Kiểm tra không có URL ảnh lặp giữa các bộ từ và bài viết gốc.
5. Cập nhật manifest assets/content/index.json, đảm bảo ngày trong tên file khớp publishDate.
6. Chạy python3 tool/validate_content.py; sửa mọi lỗi trước khi merge.
7. Đồng bộ JSON đã duyệt vào app/src/main/assets/assets/ của app để bản offline dùng cùng nội dung.

Không xuất bản bộ từ mới khi chưa hoàn thành tất cả bước trên.
