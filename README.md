🚀 Orbital Docking Simulator: PID Control Project
Một hệ thống mô phỏng vật lý quỹ đạo thời gian thực được xây dựng bằng Python và Pygame. Dự án này tập trung vào việc áp dụng Tư duy Nguyên gốc (First Principles) để giải quyết bài toán điều khiển phi thuyền cập bến trạm vũ trụ bằng thuật toán PID Control.

🎯 Mục tiêu kỹ thuật
Mô phỏng Vật lý (Orbital Mechanics): Tính toán lực hấp dẫn Newton và cập nhật vector vận tốc theo phương pháp Euler.

Hệ thống Điều khiển (Control Theory): Sử dụng bộ điều khiển PID để tự động hóa quá trình đồng bộ quỹ đạo và cập bến (Docking).

Hệ thống Hạt (Particle System): Mô phỏng hỏa lực phản lực dựa trên vector hướng.

Giao diện Kỹ thuật: Tích hợp Radar kỹ thuật số và Dashboard theo dõi thông số thời gian thực.

🛠 Cài đặt và Chạy
Đảm bảo bạn đã cài đặt Python 3.x trên máy.

Cài đặt thư viện đồ họa:

Bash
pip install pygame-ce
Chạy ứng dụng:

Bash
python orbital_sim.py
🎮 Hướng dẫn điều khiển
Phím [A]: Kích hoạt/Ngắt hệ thống Tự động lái (Auto-Pilot).

Phím [R]: Reset nhiệm vụ (khi cạn nhiên liệu hoặc va chạm).

Phím [Mũi tên]: Điều khiển động cơ đẩy thủ công (Ghi đè Auto-Pilot).

🧠 Phân tích thuật toán
Hệ thống sử dụng bộ điều khiển PD (Proportional-Derivative) để giảm thiểu sai số khoảng cách giữa tàu và trạm:

P (Proportional): Tạo lực đẩy tỉ lệ thuận với khoảng cách đến trạm.

D (Derivative): Dự báo tốc độ tiếp cận để chủ động giảm tốc, tránh hiện tượng vọt lố (Overshoot) và va chạm mạnh.
