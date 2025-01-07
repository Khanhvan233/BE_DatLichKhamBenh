
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
- **Cách dùng** Mã hóa hình ảnh thành kiểu base64 rồi truyền xuống JSON nha .  


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
## /getAllAppointments
- **Mục đích:** Xem danh sách các cuộc hẹn đã được đặt sắp tư mới đến cũ
## /updateAppointmentStatus/id
- **Mục đích:** Xác nhận đặt lịch chuyển trạng thái từ 0 sang 1
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
## /getDoctorsByKhoa
- **Mục đích:** Tìm kiếm bác sĩ theo khoa
---
# Center Controller  
## /getAllCenter  
- **Mục đích:** Lấy danh sách tất cả trung tâm y tế trong hệ thống.   
## /searchCenter/name(json)  
- **Mục đích:** Tìm kiếm trung tâm theo tên.  
- truyển JSON vào URL 

# SignUp Controller  
## /register
- **Mục đích:** Đăng ký tài khoản cho user mới
# Client Account Controller 
##  /myINFO/id
- **Mục đích:** xem thông tin cá nhân ID này lấy từ khi người dùng đăng nhập vào hệ thống 
## /editMyInfo/id
- **Mục đích:** sửa thông tin cá nhân ID này lấy từ khi người dùng đăng nhập vào hệ thống 
# Booking Controller  
## /booking
- **Mục đích:** đặt lịch khám bệnh 
## /appointments/id
- **Mục đích:** xem danh sách lịch khám bệnh của mình đã đặt ID này lấy từ khi người dùng đăng nhập vào hệ thống 
