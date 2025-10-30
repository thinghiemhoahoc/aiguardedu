import joblib
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS # Cần thiết để cho phép frontend (index.html) gọi API

# Khởi tạo ứng dụng Flask
# Thiết lập tham số static_folder để Flask biết nơi tìm các tệp tĩnh
app = Flask(__name__, static_folder='static')
# Cho phép CORS cho tất cả các route, cần thiết để frontend (chạy trên trình duyệt) 
# gọi API backend
CORS(app)

# Tải mô hình khi ứng dụng khởi động
try:
    model_path = 'spam_classifier_model.joblib'
    # Đảm bảo bạn đã cài đặt joblib và scikit-learn
    model = joblib.load(model_path)
    print("Mô hình đã được tải thành công!")
except Exception as e:
    print(f"Lỗi khi tải mô hình: {e}")
    model = None

# --- Route phục vụ HTML (Trang chủ) ---
@app.route('/')
def serve_index():
    """
    Phục vụ tệp index.html từ thư mục static.
    """
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/message')
def serve_message():
    """
    Phục vụ tệp index.html từ thư mục static.
    """
    return send_from_directory(app.static_folder, 'message.html')

@app.route('/question')
def serve_question():
    """
    Phục vụ tệp index.html từ thư mục static.
    """
    return send_from_directory(app.static_folder, 'question.html')

@app.route('/scam_news')
def serve_scam_news():
    """
    Phục vụ tệp index.html từ thư mục static.
    """
    return send_from_directory(app.static_folder, 'scam_news.html')

@app.route('/scams.json')
def serve_get_scams():
    """
    Phục vụ tệp scams.json từ thư mục static.
    """
    return send_from_directory(app.static_folder, 'scams.json')

@app.route('/new.json')
def serve_get_news():
    """
    Phục vụ tệp new.json từ thư mục static.
    """
    return send_from_directory(app.static_folder, 'new.json')

# --- Route API dự đoán ---
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Mô hình chưa được tải. (Lỗi 500)'}), 500

    # Lấy dữ liệu từ yêu cầu POST
    data = request.get_json(silent=True)
    if not data or 'text' not in data:
        return jsonify({'error': 'Thiếu trường "text" trong dữ liệu đầu vào. (Lỗi 400)'}), 400

    text_input = [data['text']]

    try:
        # Chạy dự đoán
        prediction_result = model.predict(text_input)

        # Chuyển đổi kết quả sang string ('Safe' hoặc 'Scam')
        result_label = prediction_result[0]

        return jsonify({'status': 'success', 'prediction': result_label})
    except Exception as e:
        # Xử lý lỗi nếu việc dự đoán gặp sự cố (ví dụ: dữ liệu đầu vào không hợp lệ)
        return jsonify({'error': f'Lỗi khi dự đoán: {e}'}), 500


if __name__ == '__main__':
    # Chạy server. Sử dụng host '0.0.0.0' để dễ dàng truy cập trên mạng nội bộ.
    app.run(debug=True, host='0.0.0.0', port=5000)
