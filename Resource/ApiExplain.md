
# Login Controller  
## /login  
- **Mục đích:** Đăng nhập bằng tài khoản **user**.  
## /doctor  
- **Mục đích:** Đăng nhập bằng tài khoản **doctor**.  
---
# Admin Controller (Tất cả các API ở đây đều sử dụng JWT)
## /addUser  
- **Mục đích:** Admin có thể thêm người dùng mới vào hệ thống.  
## /addDoctor  
- **Mục đích:** Admin thêm bác sĩ mới vào hệ thống.  

## /getUser/id(variable)  
- **Mục đích:** Lấy thông tin của người dùng theo ID.  
- `id` truyền vào URL.  
## /getAllUser  
- **Mục đích:** Lấy danh sách tất cả người dùng trong hệ thống.  
## /deleteUser/id(variable)  
- **Mục đích:** Xóa một người dùng theo ID.  
- `id` là giá trị truyền vào URL.  
## /deleteDoctor/id(variable)  
- **Mục đích:** Xóa một bác sĩ theo ID.  
- `id` truyền vào URL.  
## /editUser/id(variable)  
- **Mục đích:** Cập nhật thông tin người dùng.  
- `id` truyền vào URL.  
## /editDoctor/id(variable)  
- **Mục đích:** Cập nhật thông tin bác sĩ.  
- `id` truyền vào URL.  
---
# Doctor Controller  
## /getDoctor/id  
- **Mục đích:** Lấy thông tin chi tiết của một bác sĩ theo ID.  
- `id` truyền vào URL.  
## /getAllDoctor  
- **Mục đích:** Lấy danh sách tất cả bác sĩ trong hệ thống.  
## /searchDoctor/name(json)  
- **Mục đích:** Tìm kiếm bác sĩ theo tên.  
- truyển JSON vào URL 
---
# Center Controller  
## /getAllCenter  
- **Mục đích:** Lấy danh sách tất cả trung tâm y tế trong hệ thống.   
## /searchCenter/name(json)  
- **Mục đích:** Tìm kiếm trung tâm theo tên.  
- truyển JSON vào URL 

