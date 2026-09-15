# TEAM — Day04, K4-L3B

**Làm nhóm.** Mỗi người tự viết và commit phần INDIVIDUAL của mình.

## Thông tin bài nộp

- Tên nhóm: IpadKid
- Người đại diện / MSSV: Ngô Tuấn Tùng - 2A202602826
- Tên repo: 
`K4B-Day-4-IpadKid`
- URL repo, nhánh nộp, commit chốt: https://github.com/tuantung26/K4B-Day-4-IpadKid
- Deadline áp dụng và link thông báo đổi hạn nếu có:

## Thành viên

| Họ và tên | MSSV | GitHub | Vai trò và công việc | File/commit/PR |
|---|---|---|---|---|
|Ngô Tuấn Tùng | 2A202602826 | tuantung26 | Team lead, Chạy 3 version và ghi logs, viết Report, adversarial cases | |
|Phùng Đình Triển | 2A202602837 | TrienPhung | Viết 10 case | |
|Cao Đức Hiệp | 2A202602550 | Hipscarer03 | Nâng cấp chat UI | |
|Phạm Đình Bảo Khôi | 2A202602434 | Palm-Pham | Sửa System Prompt và Sửa Tool yaml cải thiện qua các version | |

## Nhận xét chung

- Kết quả và bằng chứng: Ban đầu (v0) baseline đạt 70% case_accuracy (21/30). Sau quá trình tinh chỉnh, v2 đạt đỉnh 73.33% (22/30) nhờ cải thiện mô tả tools (xem log trong bảng B1 file REPORT.md). Đến v3, hệ thống ổn định ở mức 70% sau khi sửa các lỗi liên quan đến routing và boundary.
- Thay đổi hiệu quả nhất: Chỉnh sửa `tools.yaml` (ở v2) bằng cách làm rõ điều kiện gọi `lookup_user` và `inspect_device`, giúp agent giảm đáng kể lỗi chọn sai tool (wrong_tool). Cập nhật `system_prompt.md` (v1) cũng giúp ngăn chặn lỗi tạo ticket bừa bãi.
- Giới hạn còn lại: Agent thi thoảng vẫn mắc lỗi `wrong_boundary` ở các kịch bản multi-turn dài nếu người dùng thay đổi ý định giữa chừng, do agent bị mất ngữ cảnh (lost in middle).
- Cách phân công và tích hợp: Tùng phụ trách chạy test tự động sinh log. Khôi điều chỉnh prompt. Hiệp làm UI. Triển xây dựng các case test độc lập để đối chiếu. Cả team push và test trên cùng 1 branch `starter_v0`.

## INDIVIDUAL

Sao chép mục này cho từng thành viên.

### Ngô Tuấn Tùng — 2A202602826

- Phần việc và file/commit/PR: Team lead, Chạy 3 version và ghi logs, viết Report, adversarial cases `runs/v0_B_base_openrouter_20260915T184621977523.json`, `runs/v1_B_base_openai_20260915T204722114892.json`, `runs/v2_B_base_openai_20260915T205036318540.json`, `runs/v3_B_base_openai_20260915T205249160275.json`, file đã commit: TEAM.md, REPORT.md, version_log.csv.
- Quyết định, khó khăn và cách xử lý: không có
- Điều đã học: Chạy test, so sánh kết quả và so sánh các version. Các lỗi trong từng version và cách sửa.
- AI/công cụ đã dùng và cách kiểm tra: Auto agent, tool yaml, vps .
- Thời điểm đã tự nộp URL repo chung trên VLearn:

### Phùng Đình Triển — 2A202602837

- Phần việc và file/commit/PR: Viết 10 test case độc lập để kiểm tra và đối chiếu kết quả của agent; cập nhật phần reflection trong `TEAM.md`.
- Quyết định, khó khăn và cách xử lý: Một số case có thể khiến agent trả lời chưa đúng ý, nên điều chỉnh câu hỏi cho rõ ràng và kiểm tra lại kết quả sau khi chạy.
- Điều đã học: Biết cách xây dựng test case, kiểm tra output và đánh giá lỗi của agent.
- AI/công cụ đã dùng và cách kiểm tra: Sử dụng AI hỗ trợ xây dựng test case; chạy test và đối chiếu kết quả/log để kiểm tra.
- Thời điểm đã tự nộp URL repo chung trên VLearn: 15/09/2026, khoảng 23:30.

### Cao Đức Hiệp — 2A202602550

- Phần việc và file/commit/PR:
- Quyết định, khó khăn và cách xử lý:
- Điều đã học:
- AI/công cụ đã dùng và cách kiểm tra:
- Thời điểm đã tự nộp URL repo chung trên VLearn:

### Phạm Đình Bảo Khôi — 2A202602434

- Phần việc và file/commit/PR:
- Quyết định, khó khăn và cách xử lý:
- Điều đã học:
- AI/công cụ đã dùng và cách kiểm tra:
- Thời điểm đã tự nộp URL repo chung trên VLearn:

