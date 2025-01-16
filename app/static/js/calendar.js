// JavaScript to Generate a Dynamic Calendar
document.addEventListener("DOMContentLoaded", function () {
    const calendar = document.getElementById("calendar");
    const today = new Date();

    // Get current month and year
    const month = today.getMonth(); // 0-indexed
    const year = today.getFullYear();

    // Days of the week
    const daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

    // Number of days in the current month
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    // First day of the month
    const firstDay = new Date(year, month, 1).getDay();

    // Add the days of the week to the calendar
    daysOfWeek.forEach(day => {
        const dayElement = document.createElement("div");
        dayElement.className = "day";
        dayElement.innerText = day;
        calendar.appendChild(dayElement);
    });

    // Add empty slots for days before the first day of the month
    for (let i = 0; i < firstDay; i++) {
        const emptySlot = document.createElement("div");
        emptySlot.className = "day";
        calendar.appendChild(emptySlot);
    }

    // Add days of the month to the calendar
    for (let day = 1; day <= daysInMonth; day++) {
        const dayElement = document.createElement("div");
        dayElement.className = "day";

        // Highlight today's date
        if (day === today.getDate()) {
            dayElement.classList.add("today");
        }

        dayElement.innerText = day;
        calendar.appendChild(dayElement);
    }
});
