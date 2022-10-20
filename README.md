# INSTALL
1. create .venv for environment for Python
2. install requirement.txt with pip install
3. python manage.py makemigrations demo && python manage.py migrate
4. python manage.py createsuperuser 
5. using python manage.py runserver
* It will run in default port, meaning you should connect with localhost:8000/api/ for running tests

# How to implement case
Ý tưởng:
Cài đặt django + django_rest framwork để có thể sử dụng serialize + token authen
* sau khi cài đặt => ngốn 2 ngày chỉ để setting => quyết định chọn ORM thường
* run được các api, handle các edge case(không quá tổng quát, chủ yếu là validate đầu vào)

* Ý tưởng cải tiến:
- Yêu cầu trong get balance là 5s: Sử dụng Queue cho các tác vụ deposit và withdrawn mục tiêu các request ko bị miss và balace của user sẽ không bị trường hợp edge case là âm hoặc cùng lúc deposit, withdrawn.
Trường hợp chạy multiple threads thì cần phải xác định phương pháp lock balance hoặc lock thread để tránh bug balance

- Caching request get balance => giảm đỗ trễ trong trường hợp yêu cầu quá nhiều
, caching các request khác để giảm tải

# Thanks
Cảm ơn anh Hưng và anh Nhã đã tham gia phỏng vấn với em. Dù nhận thêm cho mình một cơ hội nhưng theo đánh giá về độ hoàn thiện chưa cao, em tự tin rằng mình bỏ qua cơ hội này rồi.

Chân thành cảm ơn 2 anh đã dành thời gian. Bây giờ em đã nghĩ lại về con đường công việc(job path) mình đi, sâu vào một frontend engineer.
Sincerely
