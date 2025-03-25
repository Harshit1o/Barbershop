# Barbershop Booking System

A modern Django-based barbershop booking system with AI-powered face shape detection and personalized hairstyle recommendations.

## Features

- 🔐 User Authentication (Register/Login)
- 📅 Appointment Scheduling
- 💳 Secure Payment Processing (Razorpay Integration)
- 🤖 AI-Powered Face Shape Detection
- 💇 Personalized Hairstyle Recommendations
- 📱 Responsive Design
- 🔄 Real-time Appointment Management
- 👤 User Dashboard

## Tech Stack

- Python 3.10+
- Django 4.2.1
- PostgreSQL
- OpenCV
- dlib
- scikit-learn
- Razorpay Payment Gateway
- Docker (optional)

## Prerequisites

- Python 3.10 or higher
- PostgreSQL
- Docker (optional, for containerized deployment)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Harshit1o/Barbershop.git
cd Barbershop
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download required face detection model files:
   - Download `shape_predictor_68_face_landmarks.dat` from [dlib's official model](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)
   - Download `haarcascade_frontalface_default.xml` from [OpenCV's GitHub](https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml)
   - Place both files in the `haircut_booking/bookings/` directory

5. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update the values in `.env` with your actual credentials:
```bash
cp .env.example .env
```

6. Run migrations:
```bash
python manage.py migrate
```

7. Create a superuser:
```bash
python manage.py createsuperuser
```

8. Run the development server:
```bash
python manage.py runserver
```

## Docker Deployment

1. Build the Docker image:
```bash
docker build -t barbershop .
```

2. Run the container:
```bash
docker run -p 8000:8000 barbershop
```

## Project Structure

```
Barbershop/
├── haircut_booking/          # Main project directory
│   ├── bookings/            # Main app directory
│   │   ├── templates/      # HTML templates
│   │   ├── models.py       # Database models
│   │   ├── views.py        # View logic
│   │   ├── forms.py        # Form definitions
│   │   └── face_shape_ai.py # AI implementation
│   └── haircut_booking/    # Project settings
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
└── README.md              # This file
```

## Features in Detail

### Face Shape Detection
The system uses OpenCV and dlib to detect facial landmarks and analyze face shape. It supports the following face shapes:
- Square
- Round
- Triangle
- Diamond
- Rectangular
- Oblong

### Hairstyle Recommendations
Based on the detected face shape, the system provides personalized hairstyle recommendations:
- Square: Short Pompadour, Side Part, Undercut
- Round: Angular Fringe, High Volume Top, Flat Top
- Triangle: Buzz Cut, Textured Crop, Side-Swept
- Diamond: Comb Over, Faux Hawk, Quiff
- Rectangular: Crew Cut, Pompadour, Short Textured
- Oblong: Side Part, Fringe, Layered Top

### Payment Integration
The system integrates with Razorpay for secure payment processing. Users can:
- Book appointments
- Make secure payments
- Receive payment confirmations
- View payment history

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenCV for face detection
- dlib for facial landmark detection
- Razorpay for payment processing
- Django community for the excellent framework

## Support

For support, please open an issue in the repository or contact the maintainers. 
