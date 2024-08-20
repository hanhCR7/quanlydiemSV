from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import or_, cast, String


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:hanh2003Az@localhost:5432/webpy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# tạo bảng


# Bảng sinh viên
class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    student_code = db.Column(db.String(10))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    major = db.Column(db.String(255))
    score = db.Column(db.Float)


#Bảng khoa
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    credits = db.Column(db.Integer)
    description = db.Column(db.Text)


#Bảng giảng viên
class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50))
    office_location = db.Column(db.String(50))
    email = db.Column(db.String(50))


# BẢng đăng ký học
class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    grade = db.Column(db.String(5))

# Trang chủ
@app.route('/')
def home():
    students = Student.query.all()
    return render_template('home.html', students=students)


# Trang hiện thị danh sach sinh viên 
@app.route('/svlist')
def svlist():
    students = Student.query.all()
    return render_template('svlist.html', students=students)


# Thêm sinh viên mới
@app.route('/add_student', methods=['POST'])
def add_student():
    new_student = Student(
        name=request.form['name'],
        student_code=request.form['student_code'],
        age=request.form['age'],
        gender=request.form['gender'],
        major=request.form['major'],
        score=request.form['score']
    )
    db.session.add(new_student)
    db.session.commit()
    return redirect(url_for('svlist'))


# chỉnh sủa thông tin sinh viên
@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.student_code=request.form['student_code']
        student.age = request.form['age']
        student.gender = request.form['gender']
        student.major = request.form['major']
        student.score = request.form['score']
        db.session.commit()
        return redirect(url_for('svlist'))
    return render_template('edit_student.html', student=student)


# Xóa sinh viên
@app.route('/delete_student/<int:student_id>', methods=['GET', 'POST'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        db.session.delete(student)
        db.session.commit()
        return redirect(url_for('svlist'))  
    return render_template('delete_student.html', student=student)


# Tìm kiếm sinh viên
@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        search_term = request.form.get('search_term', '')
        students = Student.query.filter(
            or_(
                cast(Student.id, String).ilike(f"%{search_term}%"),
                Student.name.ilike(f"%{search_term}%"),
                Student.student_code.ilike(f"%{search_term}%"),
                Student.gender.ilike(f"%{search_term}%"),
                Student.major.ilike(f"%{search_term}%")
            )
        ).all()
        return render_template('search.html', students=students, search_term=search_term)
    else:
        students = Student.query.all()
        return render_template('search.html', students=students)
    
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

