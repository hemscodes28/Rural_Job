# Rural Job Finder

A comprehensive web application designed to address unemployment in rural areas by connecting job seekers with local opportunities that match their skills and preferences.

## Problem Statement

Unemployment in rural areas often stems from a lack of job awareness rather than skills. This project develops a web application to help rural job seekers find nearby opportunities matching their skills, promoting employment and self-reliance.

## Features

### User Authentication
- Secure user registration and login
- Password hashing for security

### User Profile Management
- Biodata input for personal information
- Resume upload (PDF only, max 16MB)
- Skills and job preferences specification

### Job Recommendations
- Personalized job suggestions based on user skills and preferences
- Matching algorithm that compares user preferences with job requirements

### Job Browsing
- View all available job opportunities
- Detailed job information including location, salary, and requirements

### Application Tracking
- Apply to jobs with one-click application
- Track application status and history

### Responsive Design
- Modern, mobile-friendly interface using Bootstrap
- Clean and intuitive user experience

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy
- **Frontend**: HTML, CSS, Bootstrap 4
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **File Uploads**: Werkzeug

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `python app.py`

## Usage

1. **Sign Up**: Create an account with your email and password
2. **Complete Profile**: Add your biodata, upload resume, and specify skills/preferences
3. **View Recommendations**: Check your dashboard for personalized job suggestions
4. **Browse Jobs**: Explore all available opportunities
5. **Apply**: Submit applications to jobs that interest you
6. **Track Applications**: Monitor your application status

## Data

The application uses synthetic job data with 20+ job opportunities across various rural locations, covering diverse skills from farming and teaching to IT and healthcare.

## Modules

1. **Authentication Module**: Login/Signup functionality
2. **Profile Module**: User profile management and resume uploads
3. **Dashboard Module**: Personalized job recommendations
4. **Jobs Module**: Job browsing and search
5. **Applications Module**: Application tracking and management

## Future Enhancements

- Advanced recommendation algorithms using machine learning
- Location-based job matching with maps
- Employer dashboard for posting jobs
- Email notifications for application updates
- Integration with real job boards and APIs

## Contributing

This project serves as a community service initiative to promote employment in rural areas. Contributions and feedback are welcome to improve the platform's effectiveness.

## License

This project is open-source and available under the MIT License.