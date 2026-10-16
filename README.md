# Bài 4: Tự động triển khai ứng dụng Spring Boot (Container) lên VPS từ xa qua SSH

## Giới thiệu
Thực hiện tự động hóa quy trình CI/CD đẩy Docker Image từ GitHub Container Registry (GHCR) lên máy chủ VPS từ xa thông qua kết nối SSH bằng GitHub Actions workflow (`appleboy/ssh-action`).

## Cấu hình Secrets cần thiết trên GitHub Repository
Truy cập vào **Settings -> Secrets and variables -> Actions** và thêm các Repository Secrets sau:
- `SSH_HOST`: Địa chỉ IP công khai của máy chủ VPS.
- `SSH_USER`: Tên người dùng truy cập SSH (ví dụ: `ubuntu`, `root`).
- `SSH_KEY`: Nội dung Private Key để xác thực SSH.

## Cấu trúc Workflow (`deploy-vps.yml`)
1. **Job `build-image`**: Đăng nhập GHCR, tiến hành Build Docker Image và Push lên registry với tag `:latest`.
2. **Job `deploy-vps`**: Nối tiếp sau `build-image` (`needs: build-image`), sử dụng `appleboy/ssh-action@v1.0.3` truy cập VPS và chạy các lệnh:
   - Đăng nhập GHCR trên VPS bằng `GITHUB_TOKEN`.
   - Kéo Image mới nhất: `docker pull ghcr.io/<owner>/app:latest`.
   - Đừng và xóa container cũ (nếu có): `docker stop app || true && docker rm app || true`.
   - Khởi chạy container mới trên cổng `8080`: `docker run -d --name app -p 8080:8080 ghcr.io/<owner>/app:latest`.

## Kiểm tra triển khai thành công
Chạy công cụ kiểm tra sức khỏe của ứng dụng sau khi deploy bằng Python:
```bash
python main.py <VPS_IP>
```
Nếu kết quả trả về `HTTP Status Code: 200` và `UP`, ứng dụng đã hoạt động thành công.