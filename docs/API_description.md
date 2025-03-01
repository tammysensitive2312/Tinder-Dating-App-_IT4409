# Thiết kế API cho Tinder

## Mục lục
- [I. Các API chính có thể có](#i-các-api-chính-có-thể-có)
  - [User-side API](#user-side-api)
  - [Admin-side API](#admin-side-api)
- [II. Mô tả chi tiết API](#ii-mô-tả-chi-tiết-api)
  - [1. Authentication & Authorization API](#1-authentication--authorization-api)
  - [2. Profile Management API](#2-profile-management-api)
  - [3. Swipe & Match API](#3-swipe--match-api)
  - [4. Chat API (WebSocket)](#4-chat-api-websocket)
  - [5. Notification API (SSE)](#5-notification-api-sse)
  - [6. Location & Discovery API](#6-location--discovery-api)
  - [7. Subscription & Payment API](#7-subscription--payment-api)
  - [8. Analytics API](#8-analytics-api)
  - [9. Admin API](#9-admin-api)
  - [10. Third-Party Integration API](#10-third-party-integration-api)

---

## I. Các API chính có thể có: 

### User-side API

1. Authentication & Authorization API
* Đăng ký/ Tạo tài khoản
- POST /auth/signup: Tạo tài khoản bằng email/SĐT/mạng xã hội
- POST /auth/oauth/{provide}: Đăng nhập bằng bên thứ 3 tin cậy
* Xác thực
- POST /auth/login: Đăng nhập bằng email/mật khẩu
- POST /auth/refresh-token: làm mới token (với jwt)
- POST /auth/logout: Đăng xuất
* Quên mật khẩu
- POST /auth/reset-password: Yêu cầu đặt lại mật khẩu
- PUT /auth/reset-password: Xác nhận mã OTP và đổi mật khẩu
2. Profile Management API
* Thông tin cá nhân
- GET /profile/me: Lấy thông tin về profile của người dùng
- PUT /profile/me: Cập nhật thông tin (tên, mô tả, giới tính, etc.)
* Hình ảnh
- POST /profile/me/photos: Tải lên ảnh đại diện
- DELETE /profile/me/photos/{photoId}: xóa ảnh
* Thiết lập tìm kiếm
- PUT /profile/preferences: Cập nhật tuổi/khoảng cách/giới tính mục tiêu.
3. Swipe & Match API
* Lấy danh sách đề xuất
- GET /recommendations: Trả về các profile để swipe
* Thao tác swipe
- POST /swipe/{userId}/like: Swipe phải (thích)
- POST /swipe/{userId}/dislike: Swipe trái (bỏ qua)
* Quản lý match
- GET /matches: Danh sách các match 
- DELETE /matches/{matchId}: hủy match
4. Chat API
* Kết nối WebSocket
- wss://api.datingapp.com/chat/ws:
  - CLient kết nối qua WebSocket
  - Server quản lý các kết nối dựa trên userId hoặc matchId
5. Notification API
* Kết nối SSE
- GET /sse/notifications: CLient mở kết nối SSE và nhận thông báo real-time
6. Location & Discovery API
* Cập nhật vị trí
- POST /location: Gửi tọa độ GPS hiện tại
* Tìm kiếm theo khu vực
- GET /discovery?radis=...: Lọc profile theo khoảng cách
7. Subscription & Payment API'
* Gói Premium
- GET /subscriptions/plans: Danh sách gói (Tinder Plus/Gold).
- POST /subscriptions: Mua gói premium.
* In-app purchases
- POST /purchases/boosts: Mua Boost.
- POST /purchases/super-likes: Mua Super Likes.

### Admin-side API 
8. Analytics API
* Thống kê người dùng
- GET /analytics/swipes: Số lượt swipe theo ngày.
- GET /analytics/matches: Tỷ lệ match.
* Dữ liệu kinh doanh 
- GET /analytics/revenue: Doanh thu từ gói premium.
9. Admin API
* Quản lý người dùng
- DELETE /admin/users/{userId}: Ban tài khoản.
- GET /admin/reports: Danh sách báo cáo
* Hệ thống
- GET /admin/health: Kiếm tra trạng thái server
10. Third-Party Integration API
* Kết nối mạng xã hội
- GET /integrations/instagram: Hiển thị ảnh Instagram.
- GET /integrations/spotify: Hiển thị bài hát yêu thích.

---

## II. Mô tả chi tiết API

### 1. Authentication & Authorization API

| **API**                   | **Method** | **Endpoint**             | **Input**                                           | **Output**                                 |
|---------------------------|------------|--------------------------|-----------------------------------------------------|--------------------------------------------|
| Đăng ký tài khoản         | POST       | `/auth/signup`           | `{ email: string, password: string, name: string }` | `{ id: string, token: string }`            |
| Đăng nhập bằng OAuth      | POST       | `/auth/oauth/{provider}` | `{ access_token: string }`                          | `{ id: string, token: string }`            |
| Đăng nhập bằng email      | POST       | `/auth/login`            | `{ email: string, password: string }`               | `{ token: string, refresh_token: string }` |
| Làm mới token             | POST       | `/auth/refresh-token`    | Header: `refresh_token: string`                     | `{ new_token: string }`                    |
| Yêu cầu đặt lại mật khẩu  | POST       | `/auth/reset-password`   | `{ email: string }`                                 | `{ otp_expiry: string }`                   |
| Xác nhận đặt lại mật khẩu | PUT        | `/auth/reset-password`   | `{ otp: string, new_password: string }`             | `{ status: "success" }`                    |

### Chi tiết Input và Output của Authentication & Authorization API

#### 1. Đăng ký tài khoản (`POST /auth/signup`)

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**                                            |
|------------|--------------------|------------------|--------------|------------------------------------------------------|
| 1          | `email`            | `string`         | Có           | Email của người dùng, dùng để đăng nhập và liên lạc. |
| 2          | `password`         | `string`         | Có           | Mật khẩu của người dùng, tối thiểu 8 ký tự.          |
| 3          | `name`             | `string`         | Có           | Tên hiển thị của người dùng trên ứng dụng.           |

**Output:**

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Mô tả**                                         |
|------------|--------------------|------------------|---------------------------------------------------|
| 1          | `id`               | `string`         | ID duy nhất của người dùng trong hệ thống.        |
| 2          | `token`            | `string`         | JWT token dùng để xác thực các request tiếp theo. |

---

#### 2. Đăng nhập bằng OAuth (`POST /auth/oauth/{provider}`)

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**                                                     |
|------------|--------------------|------------------|--------------|---------------------------------------------------------------|
| 1          | `access_token`     | `string`         | Có           | Access token từ nhà cung cấp OAuth (Google, Facebook, Apple). |

**Output:**

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Mô tả**                                         |
|------------|--------------------|------------------|---------------------------------------------------|
| 1          | `id`               | `string`         | ID duy nhất của người dùng trong hệ thống.        |
| 2          | `token`            | `string`         | JWT token dùng để xác thực các request tiếp theo. |

---

#### 3. Đăng nhập bằng email (`POST /auth/login`)

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**                        |
|------------|--------------------|------------------|--------------|----------------------------------|
| 1          | `email`            | `string`         | Có           | Email đã đăng ký của người dùng. |
| 2          | `password`         | `string`         | Có           | Mật khẩu của người dùng.         |

**Output:**

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Mô tả**                                            |
|------------|--------------------|------------------|------------------------------------------------------|
| 1          | `token`            | `string`         | JWT token dùng để xác thực các request tiếp theo.    |
| 2          | `refresh_token`    | `string`         | Refresh token dùng để lấy lại JWT token khi hết hạn. |

---

#### 4. Làm mới token (`POST /auth/refresh-token`)

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**                                        |
|------------|--------------------|------------------|--------------|--------------------------------------------------|
| 1          | `refresh_token`    | `string`         | Có           | Refresh token được cấp khi đăng nhập thành công. |

**Output:**

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Mô tả**                                             |
|------------|--------------------|------------------|-------------------------------------------------------|
| 1          | `new_token`        | `string`         | JWT token mới dùng để xác thực các request tiếp theo. |

---

#### 5. Yêu cầu đặt lại mật khẩu (`POST /auth/reset-password`)

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**                        |
|------------|--------------------|------------------|--------------|----------------------------------|
| 1          | `email`            | `string`         | Có           | Email đã đăng ký của người dùng. |

**Output:**

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Mô tả**                                          |
|------------|--------------------|------------------|----------------------------------------------------|
| 1          | `otp_expiry`       | `string`         | Thời gian hết hạn của mã OTP (định dạng ISO 8601). |

---

#### 6. Xác nhận đặt lại mật khẩu (`PUT /auth/reset-password`)

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**                                       |
|------------|--------------------|------------------|--------------|-------------------------------------------------|
| 1          | `otp`              | `string`         | Có           | Mã OTP được gửi đến email của người dùng.       |
| 2          | `new_password`     | `string`         | Có           | Mật khẩu mới của người dùng, tối thiểu 8 ký tự. |

**Output:**

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Mô tả**                                                      |
|------------|--------------------|------------------|----------------------------------------------------------------|
| 1          | `status`           | `string`         | Trạng thái của request, giá trị là `"success"` nếu thành công. |

---

### 2. Profile Management API

| **API**                     | **Method** | **Endpoint**           | **Input**                                      | **Output**                                                             |
|-----------------------------|------------|------------------------|------------------------------------------------|------------------------------------------------------------------------|
| Lấy thông tin profile       | GET        | `/profile/me`          | Header: `token: string`                        | `{ name: string, bio: string, photos: [string], preferences: object }` |
| Cập nhật thông tin profile  | PUT        | `/profile/me`          | `{ bio: string, gender: string, job: string }` | `{ updated_profile: object }`                                          |
| Tải lên ảnh đại diện        | POST       | `/profile/me/photos`   | FormData: `image: file`                        | `{ photo_id: string, url: string }`                                    |
| Cập nhật thiết lập tìm kiếm | PUT        | `/profile/preferences` | `{ max_age: number, max_distance: number }`    | `{ updated_prefs: object }`                                            |

### Chi tiết Input và Output của Profile Management API

#### 1. Lấy thông tin profile (`GET /profile/me`)

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**                              |
|------------|--------------------|------------------|--------------|----------------------------------------|
| 1          | `token`            | `string`         | Có           | JWT token dùng để xác thực người dùng. |

**Output:**

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Mô tả**                                          |
|------------|--------------------|------------------|----------------------------------------------------|
| 1          | `name`             | `string`         | Tên hiển thị của người dùng.                       |
| 2          | `bio`              | `string`         | Mô tả ngắn về bản thân.                            |
| 3          | `photos`           | `[string]`       | Danh sách URL ảnh đại diện.                        |
| 4          | `preferences`      | `object`         | Thiết lập tìm kiếm (tuổi, khoảng cách, giới tính). |

---

#### 2. Cập nhật thông tin profile (`PUT /profile/me`)

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**                                     |
|------------|--------------------|------------------|--------------|-----------------------------------------------|
| 1          | `bio`              | `string`         | Không        | Mô tả ngắn về bản thân.                       |
| 2          | `gender`           | `string`         | Không        | Giới tính (ví dụ: "male", "female", "other"). |
| 3          | `job`              | `string`         | Không        | Nghề nghiệp của người dùng.                   |

**Output:**

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Mô tả**                           |
|------------|--------------------|------------------|-------------------------------------|
| 1          | `updated_profile`  | `object`         | Thông tin profile đã được cập nhật. |

---

#### 3. Tải lên ảnh đại diện (`POST /profile/me/photos`)

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**                               |
|------------|--------------------|------------------|--------------|-----------------------------------------|
| 1          | `image`            | `file`           | Có           | File ảnh đại diện (định dạng JPEG/PNG). |

**Output:**

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Mô tả**               |
|------------|--------------------|------------------|-------------------------|
| 1          | `photo_id`         | `string`         | ID của ảnh đã tải lên.  |
| 2          | `url`              | `string`         | URL của ảnh đã tải lên. |

---

#### 4. Cập nhật thiết lập tìm kiếm (`PUT /profile/preferences`)

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**                                 |
|------------|--------------------|------------------|--------------|-------------------------------------------|
| 1          | `max_age`          | `number`         | Không        | Tuổi tối đa của người dùng muốn tìm kiếm. |
| 2          | `max_distance`     | `number`         | Không        | Khoảng cách tối đa (đơn vị: km).          |

**Output:**

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Mô tả**                            |
|------------|--------------------|------------------|--------------------------------------|
| 1          | `updated_prefs`    | `object`         | Thiết lập tìm kiếm đã được cập nhật. |

---

### Swipe & Match API

| **API**               | **Method** | **Endpoint**           | **Input**               | **Output**                                                    |
|-----------------------|------------|------------------------|-------------------------|---------------------------------------------------------------|
| Lấy danh sách đề xuất | GET        | `/recommendations`     | Header: `token: string` | `{ users: [{ id: string, name: string, photos: [string] }] }` |
| Swipe phải (thích)    | POST       | `/swipe/{userId}/like` | Header: `token: string` | `{ is_match: boolean, match_id: string (nếu có) }`            |
| Lấy danh sách match   | GET        | `/matches`             | Header: `token: string` | `{ matches: [{ match_id: string, user: object }] }`           |

### Chi tiết Input và Output của Swipe & Match API

#### 1. Lấy danh sách đề xuất (`GET /recommendations`)

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**                              |
|------------|--------------------|------------------|--------------|----------------------------------------|
| 1          | `token`            | `string`         | Có           | JWT token dùng để xác thực người dùng. |

**Output:**

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Mô tả**                     |
|------------|--------------------|------------------|-------------------------------|
| 1          | `users`            | `[object]`       | Danh sách người dùng đề xuất. |
| 1.1        | `id`               | `string`         | ID của người dùng.            |
| 1.2        | `name`             | `string`         | Tên của người dùng.           |
| 1.3        | `photos`           | `[string]`       | Danh sách URL ảnh đại diện.   |

---

#### 2. Swipe phải (thích) (`POST /swipe/{userId}/like`)

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**                              |
|------------|--------------------|------------------|--------------|----------------------------------------|
| 1          | `token`            | `string`         | Có           | JWT token dùng để xác thực người dùng. |

**Output:**

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Mô tả**                                                          |
|------------|--------------------|------------------|--------------------------------------------------------------------|
| 1          | `is_match`         | `boolean`        | `true` nếu cả hai người dùng đều thích nhau, ngược lại là `false`. |
| 2          | `match_id`         | `string`         | ID của match (nếu có).                                             |

---

#### 3. Lấy danh sách match (`GET /matches`)

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**                              |
|------------|--------------------|------------------|--------------|----------------------------------------|
| 1          | `token`            | `string`         | Có           | JWT token dùng để xác thực người dùng. |

**Output:**

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Mô tả**                      |
|------------|--------------------|------------------|--------------------------------|
| 1          | `matches`          | `[object]`       | Danh sách các match.           |
| 1.1        | `match_id`         | `string`         | ID của match.                  |
| 1.2        | `user`             | `object`         | Thông tin người dùng đã match. |

---

### Chat API (WebSocket)

| **Event**        | **Input**                                                                | **Output**                                                                                  |
|------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| Gửi tin nhắn     | `{ event: "send_message", data: { match_id: string, content: string } }` | -                                                                                           |
| Nhận tin nhắn    | -                                                                        | `{ event: "new_message", data: { sender_id: string, content: string, timestamp: string } }` |
| Typing indicator | `{ event: "typing", data: { match_id: string, is_typing: boolean } }`    | -                                                                                           |

### Chi tiết Input và Output của Chat API (WebSocket)

#### 1. Gửi tin nhắn

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**          |
|------------|--------------------|------------------|--------------|--------------------|
| 1          | `match_id`         | `string`         | Có           | ID của match.      |
| 2          | `content`          | `string`         | Có           | Nội dung tin nhắn. |

---

#### 2. Nhận tin nhắn

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Mô tả**                                    |
|------------|--------------------|------------------|----------------------------------------------|
| 1          | `sender_id`        | `string`         | ID của người gửi.                            |
| 2          | `content`          | `string`         | Nội dung tin nhắn.                           |
| 3          | `timestamp`        | `string`         | Thời gian gửi tin nhắn (định dạng ISO 8601). |

---

#### 3. Typing indicator

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**                                            |
|------------|--------------------|------------------|--------------|------------------------------------------------------|
| 1          | `match_id`         | `string`         | Có           | ID của match.                                        |
| 2          | `is_typing`        | `boolean`        | Có           | `true` nếu đang nhập tin nhắn, `false` nếu dừng nhập |

---

### Notification API (SSE)

| **API**     | **Method** | **Endpoint**         | **Input**               | **Output**                                                                     |
|-------------|------------|----------------------|-------------------------|--------------------------------------------------------------------------------|
| Kết nối SSE | GET        | `/sse/notifications` | Header: `token: string` | Event Stream: `{ type: "new_match", data: { user_id: string, name: string } }` |

### Chi tiết Input và Output của Notification API (SSE)

#### 1. Kết nối SSE (`GET /sse/notifications`)

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**                              |
|------------|--------------------|------------------|--------------|----------------------------------------|
| 1          | `token`            | `string`         | Có           | JWT token dùng để xác thực người dùng. |

**Output:**

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Mô tả**                                                       |
|------------|--------------------|------------------|-----------------------------------------------------------------|
| 1          | `type`             | `string`         | Loại thông báo (ví dụ: "new_match").                            |
| 2          | `data`             | `object`         | Dữ liệu thông báo (ví dụ: `{ user_id: string, name: string }`). |


---

### Location & Discovery API

| **API**               | **Method** | **Endpoint** | **Input**                      | **Output**                                                    |
|-----------------------|------------|--------------|--------------------------------|---------------------------------------------------------------|
| Cập nhật vị trí       | POST       | `/location`  | `{ lat: number, lng: number }` | `{ status: "updated" }`                                       |
| Tìm kiếm theo khu vực | GET        | `/discovery` | Query: `radius: number`        | `{ users: [{ id: string, name: string, photos: [string] }] }` |

### Chi tiết Input và Output của Location & Discovery API

#### 1. Cập nhật vị trí (`POST /location`)

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**               |
|------------|--------------------|------------------|--------------|-------------------------|
| 1          | `lat`              | `number`         | Có           | Vĩ độ của người dùng.   |
| 2          | `lng`              | `number`         | Có           | Kinh độ của người dùng. |

**Output:**

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Mô tả**                               |
|------------|--------------------|------------------|-----------------------------------------|
| 1          | `status`           | `string`         | Trạng thái cập nhật (ví dụ: "updated"). |

---

#### 2. Tìm kiếm theo khu vực (`GET /discovery`)

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**                       |
|------------|--------------------|------------------|--------------|---------------------------------|
| 1          | `radius`           | `number`         | Có           | Bán kính tìm kiếm (đơn vị: km). |

**Output:**

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Mô tả**                           |
|------------|--------------------|------------------|-------------------------------------|
| 1          | `users`            | `[object]`       | Danh sách người dùng trong khu vực. |
| 1.1        | `id`               | `string`         | ID của người dùng.                  |
| 1.2        | `name`             | `string`         | Tên của người dùng.                 |
| 1.3        | `photos`           | `[string]`       | Danh sách URL ảnh đại diện.         |

---

### Subscription & Payment API

| **API**         | **Method** | **Endpoint**        | **Input**                                    | **Output**                |
|-----------------|------------|---------------------|----------------------------------------------|---------------------------|
| Mua gói premium | POST       | `/subscriptions`    | `{ plan_id: string, payment_token: string }` | `{ expiry_date: string }` |
| Mua Boost       | POST       | `/purchases/boosts` | `{ quantity: number }`                       | `{ boost_count: number }` |

### Chi tiết Input và Output của Subscription & Payment API

#### 1. Mua gói premium (`POST /subscriptions`)

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**                                                |
|------------|--------------------|------------------|--------------|----------------------------------------------------------|
| 1          | `plan_id`          | `string`         | Có           | ID của gói premium.                                      |
| 2          | `payment_token`    | `string`         | Có           | Token thanh toán từ hệ thống thanh toán (ví dụ: Stripe). |

**Output:**

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Mô tả**                                          |
|------------|--------------------|------------------|----------------------------------------------------|
| 1          | `expiry_date`      | `string`         | Ngày hết hạn của gói premium (định dạng ISO 8601). |

---

#### 2. Mua Boost (`POST /purchases/boosts`)

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**                |
|------------|--------------------|------------------|--------------|--------------------------|
| 1          | `quantity`         | `number`         | Có           | Số lượng Boost muốn mua. |

**Output:**

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Mô tả**                             |
|------------|--------------------|------------------|---------------------------------------|
| 1          | `boost_count`      | `number`         | Tổng số Boost hiện có của người dùng. |


---

### Analytics API

| **API**            | **Method** | **Endpoint**         | **Input**                     | **Output**                                                    |
|--------------------|------------|----------------------|-------------------------------|---------------------------------------------------------------|
| Thống kê swipe     | GET        | `/analytics/swipes`  | Header: `admin_token: string` | `{ date: string, total_swipes: number }`                      |
| Thống kê doanh thu | GET        | `/analytics/revenue` | Header: `admin_token: string` | `{ revenue_by_plan: [{ plan_id: string, revenue: number }] }` |

### Chi tiết Input và Output của Analytics API

#### 1. Thống kê swipe (`GET /analytics/swipes`)

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**                        |
|------------|--------------------|------------------|--------------|----------------------------------|
| 1          | `admin_token`      | `string`         | Có           | Token quản trị viên để xác thực. |

**Output:**

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Mô tả**                           |
|------------|--------------------|------------------|-------------------------------------|
| 1          | `date`             | `string`         | Ngày thống kê (định dạng ISO 8601). |
| 2          | `total_swipes`     | `number`         | Tổng số lượt swipe trong ngày.      |

---

#### 2. Thống kê doanh thu (`GET /analytics/revenue`)

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**                        |
|------------|--------------------|------------------|--------------|----------------------------------|
| 1          | `admin_token`      | `string`         | Có           | Token quản trị viên để xác thực. |

**Output:**

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Mô tả**                          |
|------------|--------------------|------------------|------------------------------------|
| 1          | `revenue_by_plan`  | `[object]`       | Danh sách doanh thu theo từng gói. |
| 1.1        | `plan_id`          | `string`         | ID của gói.                        |
| 1.2        | `revenue`          | `number`         | Doanh thu của gói.                 |

---

### Admin API

| **API**               | **Method** | **Endpoint**            | **Input**                     | **Output**                                             |
|-----------------------|------------|-------------------------|-------------------------------|--------------------------------------------------------|
| Ban tài khoản         | DELETE     | `/admin/users/{userId}` | Header: `admin_token: string` | `{ banned_user_id: string }`                           |
| Lấy danh sách báo cáo | GET        | `/admin/reports`        | Header: `admin_token: string` | `{ reports: [{ report_id: string, reason: string }] }` |

### Chi tiết Input và Output của Admin API

#### 1. Ban tài khoản (`DELETE /admin/users/{userId}`)

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**                        |
|------------|--------------------|------------------|--------------|----------------------------------|
| 1          | `admin_token`      | `string`         | Có           | Token quản trị viên để xác thực. |

**Output:**

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Mô tả**                    |
|------------|--------------------|------------------|------------------------------|
| 1          | `banned_user_id`   | `string`         | ID của người dùng đã bị ban. |

---

#### 2. Lấy danh sách báo cáo (`GET /admin/reports`)

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**                        |
|------------|--------------------|------------------|--------------|----------------------------------|
| 1          | `admin_token`      | `string`         | Có           | Token quản trị viên để xác thực. |

**Output:**

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Mô tả**              |
|------------|--------------------|------------------|------------------------|
| 1          | `reports`          | `[object]`       | Danh sách các báo cáo. |
| 1.1        | `report_id`        | `string`         | ID của báo cáo.        |
| 1.2        | `reason`           | `string`         | Lý do báo cáo.         |

---

### Third-Party Integration API

| **API**             | **Method** | **Endpoint**              | **Input**                         | **Output**                                           |
|---------------------|------------|---------------------------|-----------------------------------|------------------------------------------------------|
| Lấy ảnh Instagram   | GET        | `/integrations/instagram` | Header: `instagram_token: string` | `{ photos: [string] }`                               |
| Lấy bài hát Spotify | GET        | `/integrations/spotify`   | Header: `spotify_token: string`   | `{ top_tracks: [{ name: string, artist: string }] }` |

### Chi tiết Input và Output của Third-Party Integration API

#### 1. Lấy ảnh Instagram (`GET /integrations/instagram`)

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**                    |
|------------|--------------------|------------------|--------------|------------------------------|
| 1          | `instagram_token`  | `string`         | Có           | Token Instagram để xác thực. |

**Output:**

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Mô tả**                       |
|------------|--------------------|------------------|---------------------------------|
| 1          | `photos`           | `[string]`       | Danh sách URL ảnh từ Instagram. |

---

#### 2. Lấy bài hát Spotify (`GET /integrations/spotify`)

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Bắt buộc** | **Mô tả**                  |
|------------|--------------------|------------------|--------------|----------------------------|
| 1          | `spotify_token`    | `string`         | Có           | Token Spotify để xác thực. |

**Output:**

| **Thứ tự** | **Trường dữ liệu** | **Kiểu dữ liệu** | **Mô tả**                    |
|------------|--------------------|------------------|------------------------------|
| 1          | `top_tracks`       | `[object]`       | Danh sách bài hát yêu thích. |
| 1.1        | `name`             | `string`         | Tên bài hát.                 |
| 1.2        | `artist`           | `string`         | Tên nghệ sĩ.                 |