// Appointment Booking System

class AppointmentBookingSystem {
    constructor() {
        this.currentDate = new Date();
        this.selectedDate = null;
        this.selectedTime = null;
        this.appointments = this.loadAppointments();
        this.currentFilter = 'all';

        this.init();
    }

    init() {
        this.renderCalendar();
        this.setupEventListeners();
        this.renderAppointments();
    }

    // Calendar Functions
    renderCalendar() {
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();

        // Update month display
        const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'November', 'December'];
        document.getElementById('currentMonth').textContent = `${monthNames[month]} ${year}`;

        // Get first day of month and number of days
        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const daysInPrevMonth = new Date(year, month, 0).getDate();

        const calendarDays = document.getElementById('calendarDays');
        calendarDays.innerHTML = '';

        const today = new Date();
        today.setHours(0, 0, 0, 0);

        // Previous month days
        for (let i = firstDay - 1; i >= 0; i--) {
            const day = daysInPrevMonth - i;
            const dayElement = this.createDayElement(day, 'other-month');
            calendarDays.appendChild(dayElement);
        }

        // Current month days
        for (let day = 1; day <= daysInMonth; day++) {
            const date = new Date(year, month, day);
            date.setHours(0, 0, 0, 0);

            let classes = [];

            // Check if date is today
            if (date.getTime() === today.getTime()) {
                classes.push('today');
            }

            // Check if date is in the past
            if (date < today) {
                classes.push('disabled');
            }

            // Check if date is selected
            if (this.selectedDate &&
                date.getTime() === new Date(this.selectedDate).setHours(0, 0, 0, 0)) {
                classes.push('selected');
            }

            // Check if date has appointments
            if (this.hasAppointments(date)) {
                classes.push('has-appointments');
            }

            const dayElement = this.createDayElement(day, classes.join(' '), date);
            calendarDays.appendChild(dayElement);
        }

        // Next month days
        const totalCells = calendarDays.children.length;
        const remainingCells = 42 - totalCells; // 6 rows * 7 days
        for (let day = 1; day <= remainingCells; day++) {
            const dayElement = this.createDayElement(day, 'other-month');
            calendarDays.appendChild(dayElement);
        }
    }

    createDayElement(day, classes, date = null) {
        const dayElement = document.createElement('div');
        dayElement.className = `calendar-day ${classes}`;
        dayElement.textContent = day;

        if (date && !classes.includes('disabled') && !classes.includes('other-month')) {
            dayElement.addEventListener('click', () => this.selectDate(date));
        }

        return dayElement;
    }

    selectDate(date) {
        this.selectedDate = date;
        this.renderCalendar();
        this.showBookingForm();
    }

    hasAppointments(date) {
        const dateStr = this.formatDate(date);
        return this.appointments.some(apt => apt.date === dateStr);
    }

    // Booking Form Functions
    showBookingForm() {
        const formContainer = document.getElementById('bookingFormContainer');
        const selectedDateSpan = document.getElementById('selectedDate');

        selectedDateSpan.textContent = this.formatDateLong(this.selectedDate);
        formContainer.style.display = 'block';

        this.renderTimeSlots();
        formContainer.scrollIntoView({ behavior: 'smooth' });
    }

    hideBookingForm() {
        document.getElementById('bookingFormContainer').style.display = 'none';
        document.getElementById('appointmentForm').reset();
        this.selectedDate = null;
        this.selectedTime = null;
        this.renderCalendar();
    }

    renderTimeSlots() {
        const timeSlotsContainer = document.getElementById('timeSlots');
        timeSlotsContainer.innerHTML = '';

        const timeSlots = this.generateTimeSlots();
        const bookedSlots = this.getBookedSlots(this.selectedDate);

        timeSlots.forEach(time => {
            const slotElement = document.createElement('div');
            slotElement.className = 'time-slot';
            slotElement.textContent = time;

            if (bookedSlots.includes(time)) {
                slotElement.classList.add('booked');
            } else {
                slotElement.addEventListener('click', () => this.selectTimeSlot(time, slotElement));
            }

            timeSlotsContainer.appendChild(slotElement);
        });
    }

    generateTimeSlots() {
        const slots = [];
        const startHour = 9; // 9 AM
        const endHour = 17; // 5 PM

        for (let hour = startHour; hour < endHour; hour++) {
            slots.push(`${this.formatHour(hour)}:00`);
            slots.push(`${this.formatHour(hour)}:30`);
        }

        return slots;
    }

    formatHour(hour) {
        const period = hour >= 12 ? 'PM' : 'AM';
        const displayHour = hour > 12 ? hour - 12 : hour === 0 ? 12 : hour;
        return `${displayHour}:00 ${period}`.split(':')[0];
    }

    selectTimeSlot(time, element) {
        // Remove previous selection
        document.querySelectorAll('.time-slot').forEach(slot => {
            slot.classList.remove('selected');
        });

        // Add selection to clicked slot
        element.classList.add('selected');
        this.selectedTime = time;
    }

    getBookedSlots(date) {
        const dateStr = this.formatDate(date);
        return this.appointments
            .filter(apt => apt.date === dateStr)
            .map(apt => apt.time);
    }

    // Appointment Management
    bookAppointment(formData) {
        if (!this.selectedTime) {
            this.showNotification('Please select a time slot', 'error');
            return;
        }

        const appointment = {
            id: Date.now(),
            date: this.formatDate(this.selectedDate),
            time: this.selectedTime,
            name: formData.get('name'),
            email: formData.get('email'),
            phone: formData.get('phone'),
            service: formData.get('service'),
            notes: formData.get('notes') || '',
            createdAt: new Date().toISOString()
        };

        this.appointments.push(appointment);
        this.saveAppointments();

        this.showNotification('Appointment booked successfully!');
        this.hideBookingForm();
        this.renderAppointments();
    }

    cancelAppointment(id) {
        if (confirm('Are you sure you want to cancel this appointment?')) {
            this.appointments = this.appointments.filter(apt => apt.id !== id);
            this.saveAppointments();
            this.renderAppointments();
            this.renderCalendar();
            this.showNotification('Appointment cancelled successfully');
        }
    }

    renderAppointments() {
        const appointmentsList = document.getElementById('appointmentsList');

        let filteredAppointments = this.filterAppointments();

        if (filteredAppointments.length === 0) {
            appointmentsList.innerHTML = `
                <div class="empty-state">
                    <h3>No appointments found</h3>
                    <p>Book your first appointment using the calendar above</p>
                </div>
            `;
            return;
        }

        // Sort appointments by date and time
        filteredAppointments.sort((a, b) => {
            const dateA = new Date(a.date + ' ' + a.time);
            const dateB = new Date(b.date + ' ' + b.time);
            return dateA - dateB;
        });

        appointmentsList.innerHTML = filteredAppointments.map(apt => {
            const isPast = this.isAppointmentPast(apt);
            return `
                <div class="appointment-card ${isPast ? 'past' : ''}">
                    <div class="appointment-info">
                        <h4>${apt.name}</h4>
                        <div class="appointment-details">
                            <div class="appointment-detail">
                                <strong>Date:</strong> ${apt.date}
                            </div>
                            <div class="appointment-detail">
                                <strong>Time:</strong> ${apt.time}
                            </div>
                            <div class="appointment-detail">
                                <strong>Service:</strong> ${apt.service}
                            </div>
                            <div class="appointment-detail">
                                <strong>Email:</strong> ${apt.email}
                            </div>
                            <div class="appointment-detail">
                                <strong>Phone:</strong> ${apt.phone}
                            </div>
                            ${apt.notes ? `
                            <div class="appointment-detail" style="grid-column: 1 / -1;">
                                <strong>Notes:</strong> ${apt.notes}
                            </div>
                            ` : ''}
                        </div>
                    </div>
                    <div class="appointment-actions">
                        ${!isPast ? `
                            <button class="btn btn-danger" onclick="app.cancelAppointment(${apt.id})">
                                Cancel
                            </button>
                        ` : ''}
                    </div>
                </div>
            `;
        }).join('');
    }

    filterAppointments() {
        const now = new Date();

        switch (this.currentFilter) {
            case 'upcoming':
                return this.appointments.filter(apt => !this.isAppointmentPast(apt));
            case 'past':
                return this.appointments.filter(apt => this.isAppointmentPast(apt));
            default:
                return this.appointments;
        }
    }

    isAppointmentPast(appointment) {
        const aptDate = new Date(appointment.date + ' ' + appointment.time);
        return aptDate < new Date();
    }

    // Event Listeners
    setupEventListeners() {
        // Calendar navigation
        document.getElementById('prevMonth').addEventListener('click', () => {
            this.currentDate.setMonth(this.currentDate.getMonth() - 1);
            this.renderCalendar();
        });

        document.getElementById('nextMonth').addEventListener('click', () => {
            this.currentDate.setMonth(this.currentDate.getMonth() + 1);
            this.renderCalendar();
        });

        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tabName = e.target.dataset.tab;
                this.switchTab(tabName);
            });
        });

        // Form submission
        document.getElementById('appointmentForm').addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            this.bookAppointment(formData);
        });

        // Cancel booking
        document.getElementById('cancelBooking').addEventListener('click', () => {
            this.hideBookingForm();
        });

        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.currentFilter = e.target.dataset.filter;
                this.renderAppointments();
            });
        });
    }

    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.tab === tabName) {
                btn.classList.add('active');
            }
        });

        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');

        // Hide booking form when switching tabs
        if (tabName !== 'booking') {
            this.hideBookingForm();
        }
    }

    // Utility Functions
    formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    formatDateLong(date) {
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        return date.toLocaleDateString('en-US', options);
    }

    showNotification(message, type = 'success') {
        const notification = document.getElementById('notification');
        notification.textContent = message;
        notification.className = `notification ${type}`;
        notification.classList.add('show');

        setTimeout(() => {
            notification.classList.remove('show');
        }, 3000);
    }

    // Storage Functions
    saveAppointments() {
        localStorage.setItem('appointments', JSON.stringify(this.appointments));
    }

    loadAppointments() {
        const stored = localStorage.getItem('appointments');
        return stored ? JSON.parse(stored) : [];
    }
}

// Initialize the application
const app = new AppointmentBookingSystem();
