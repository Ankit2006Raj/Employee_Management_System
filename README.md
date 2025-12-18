# Employee Management System Pro 🏢

A comprehensive, production-ready Employee Management System built with Django and modern web technologies. This system provides complete HR management capabilities including employee records, departments, positions, attendance tracking, and leave management.

## ✨ Features

### Core Features
- **Employee Management**: Complete CRUD operations with detailed employee profiles
- **Department Management**: Organize employees into departments with managers
- **Position Management**: Define job positions with salary ranges
- **Leave Management**: Request, approve, and track employee leaves
- **Attendance Tracking**: Monitor employee attendance and work hours
- **Document Management**: Store and manage employee documents
- **Dashboard**: Real-time statistics and insights
- **Advanced Search & Filtering**: Find employees quickly with multiple filters
- **Export Functionality**: Export employee data to Excel

### Technical Features
- **REST API**: Full-featured REST API with Django REST Framework
- **Authentication & Authorization**: Role-based access control
- **Responsive Design**: Modern Bootstrap 5 UI that works on all devices
- **Database Optimization**: Indexed fields and optimized queries
- **File Upload**: Support for employee photos and documents
- **Pagination**: Efficient data loading with pagination
- **Form Validation**: Comprehensive client and server-side validation
- **Docker Support**: Easy deployment with Docker and Docker Compose
- **Production Ready**: Security best practices and production configurations

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL (optional, SQLite for development)
- Redis (optional, for caching)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd employee_management
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Load initial data (optional)**
```bash
python setup.py
```
This creates sample departments, positions, and employees.

8. **Run the development server**
```bash
python manage.py runserver
```

9. **Access the application**
- Web Interface: http://localhost:8000
- Admin Panel: http://localhost:8000/admin
- API Documentation: http://localhost:8000/api/schema/swagger-ui/

## 🐳 Docker Deployment

### Using Docker Compose

1. **Build and start containers**
```bash
docker-compose up -d --build
```

2. **Run migrations**
```bash
docker-compose exec web python manage.py migrate
```

3. **Create superuser**
```bash
docker-compose exec web python manage.py createsuperuser
```

4. **Access the application**
- Application: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## 📚 API Documentation

### Authentication
Token Authentication: Include `Authorization: Token your-token-here` in headers

### Main Endpoints
- **Employees**: `/api/employees/` - CRUD operations, dashboard stats, export
- **Departments**: `/api/departments/` - CRUD operations, employee lists
- **Positions**: `/api/positions/` - CRUD operations
- **Leave Requests**: `/api/leave-requests/` - CRUD, approve/reject
- **Attendance**: `/api/attendance/` - CRUD, bulk mark

### Interactive API Docs
- Swagger UI: http://localhost:8000/api/schema/swagger-ui/
- ReDoc: http://localhost:8000/api/schema/redoc/

## 🎨 Frontend Features

### Modern UI/UX Design
- **Modern Gradient Theme**: Beautiful purple-to-blue gradients throughout
- **Smooth Animations**: Professional animations using Animate.css
- **Dark Mode Support**: Toggle between light and dark themes
- **Fully Responsive**: Perfect on desktop, tablet, and mobile
- **WCAG AA Compliant**: Accessible to all users

### Key Components
- **Dashboard**: Animated stat cards, interactive Chart.js visualizations, recent activity feeds
- **Employee Directory**: Advanced search, gradient table headers, status badges with icons
- **Employee Profiles**: Large profile photo display, gradient cards, organized sections
- **Forms**: Real-time validation, loading states, clear error messages

### Technologies
- Bootstrap 5.3.2, Chart.js 4.4.0, Bootstrap Icons 1.11.2, Animate.css 4.1.1, Inter Font

## 🔒 Security Features

- CSRF Protection
- SQL Injection Prevention
- XSS Protection
- Secure Password Hashing
- Role-Based Access Control
- File Upload Validation
- HTTPS Support (Production)
- Security Headers
- Environment Variable Configuration

## 📊 Database Schema

### Main Models
- **Employee**: Complete employee information
- **Department**: Organizational departments
- **Position**: Job positions and titles
- **Attendance**: Daily attendance records
- **LeaveRequest**: Leave applications and approvals
- **EmployeeDocument**: Document storage

## 🧪 Testing

Run tests with:
```bash
python manage.py test
```

## 📈 Performance Optimization

- Database query optimization with select_related and prefetch_related
- Indexed database fields for faster queries
- Pagination for large datasets
- Static file compression
- Redis caching (optional)
- CDN for static assets

## 🛠️ Development

### Project Structure
```
employee_management/
├── employee/                      # Main Django app
│   ├── migrations/                # Database migrations
│   ├── static/employee/           # Static files (CSS, JS)
│   ├── templates/employee/        # HTML templates
│   ├── models.py                  # Database models
│   ├── views.py                   # Web views
│   ├── api_views.py               # REST API views
│   ├── serializers.py             # API serializers
│   ├── forms.py                   # Django forms
│   ├── permissions.py             # Custom permissions
│   ├── urls.py                    # URL routing
│   └── admin.py                   # Admin configuration
├── employee_management/           # Project settings
│   ├── settings.py                # Django settings
│   ├── urls.py                    # Root URL config
│   ├── wsgi.py                    # WSGI config
│   └── asgi.py                    # ASGI config
├── media/                         # User uploaded files
├── staticfiles/                   # Collected static files
├── .env.example                   # Environment template
├── .gitignore                     # Git ignore rules
├── cleanup.bat                    # Cache cleanup utility
├── docker-compose.yml             # Docker Compose config
├── Dockerfile                     # Docker configuration
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── setup.py                       # Initial data setup
└── README.md                      # Main documentation (this file)
```

### Adding New Features

1. Create models in `employee/models.py`
2. Create serializers in `employee/serializers.py`
3. Create API views in `employee/api_views.py`
4. Create web views in `employee/views.py`
5. Create templates in `employee/templates/`
6. Add URLs in `employee/urls.py`
7. Run migrations: `python manage.py makemigrations && python manage.py migrate`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 👥 Support

For support, email support@example.com or open an issue on GitHub.

## 🎯 Roadmap

- [ ] Email notifications
- [ ] Performance reviews module
- [ ] Payroll integration
- [ ] Mobile app
- [ ] Advanced reporting
- [ ] Multi-language support
- [ ] SSO integration
- [ ] Biometric attendance

---

Built with ❤️ using Django and Bootstrap
"# Employee_Management_System" 
