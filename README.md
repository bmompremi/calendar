# Appointment Booking System

A modern, fully-functional appointment booking system with an interactive calendar interface. Built with vanilla JavaScript, HTML, and CSS - no frameworks required!

## Features

### Calendar Interface
- Interactive monthly calendar view
- Navigate between months
- Highlights current day
- Shows dates with existing appointments
- Prevents booking in the past

### Appointment Booking
- Select any future date from the calendar
- Choose from available time slots (9 AM - 5 PM)
- Time slots show as booked when unavailable
- Collect appointment details:
  - Full name
  - Email address
  - Phone number
  - Service type (Consultation, Follow-up, General, Emergency)
  - Additional notes

### Appointment Management
- View all appointments
- Filter by: All, Upcoming, or Past
- Detailed appointment cards showing all information
- Cancel upcoming appointments
- Past appointments are marked and cannot be cancelled

### Data Storage
- Uses browser localStorage for data persistence
- Appointments saved automatically
- Data persists across browser sessions

## Getting Started

### Prerequisites
- Node.js (v18 or higher)
- npm

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd calendar
```

2. Install dependencies:
```bash
npm install
```

3. Run development server:
```bash
npm run dev
```

4. Build for production:
```bash
npm run build
```

## Usage

### Booking an Appointment

1. Click on any future date in the calendar
2. Select an available time slot
3. Fill in your details:
   - Name
   - Email
   - Phone number
   - Select service type
   - Add any additional notes (optional)
4. Click "Book Appointment"

### Managing Appointments

1. Click the "Manage Appointments" tab
2. View all your appointments
3. Use filters to show:
   - All appointments
   - Upcoming appointments only
   - Past appointments only
4. Cancel upcoming appointments by clicking the "Cancel" button

## Deployment

The project includes a GitHub Actions workflow that automatically builds and deploys to GitHub Pages when you push to the main branch.

### Manual Deployment

To deploy manually:

1. Build the project:
```bash
npm run build
```

2. Deploy the `dist` folder to your hosting service

## Technology Stack

- **HTML5** - Structure
- **CSS3** - Styling with modern features (Grid, Flexbox, Animations)
- **JavaScript (ES6+)** - Application logic
- **Vite** - Build tool and development server
- **LocalStorage** - Data persistence

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Future Enhancements

Potential features for future versions:
- Backend integration with database
- Email notifications
- SMS reminders
- Multiple service providers
- Admin dashboard
- Payment integration
- Recurring appointments
- Calendar export (iCal)
- Multi-language support

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
