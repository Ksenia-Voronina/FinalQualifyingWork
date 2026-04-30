document.addEventListener('DOMContentLoaded', function() {
    const calendarInput = document.getElementById('booking-calendar');
    const bookingBtn = document.getElementById('booking-btn');
    let selectedDate = null;  // ← Добавлено: переменная для хранения выбранной даты

    if (!calendarInput) return;

    // Создаём элемент для всплывающей подсказки
    let tooltip = document.querySelector('.calendar-tooltip');
    if (!tooltip) {
        tooltip = document.createElement('div');
        tooltip.className = 'calendar-tooltip';
        document.body.appendChild(tooltip);
    }

    function showTooltip(element, message, isError = false) {
        const rect = element.getBoundingClientRect();
        tooltip.textContent = message;
        tooltip.style.display = 'block';
        tooltip.style.left = `${rect.left + rect.width / 2}px`;
        tooltip.style.top = `${rect.top - 35}px`;
        tooltip.style.transform = 'translateX(-50%)';
        tooltip.style.backgroundColor = isError ? '#e53e3e' : '#1a2634';

        // Скрываем через 3 секунды
        setTimeout(() => {
            tooltip.style.display = 'none';
        }, 3000);
    }

    function hideTooltip() {
        tooltip.style.display = 'none';
    }

    function getDateStatus(dateKey) {
        if (bookedDatesFull && bookedDatesFull.includes(dateKey)) {
            return 'full';
        } else if (bookedDatesPartial && bookedDatesPartial.includes(dateKey)) {
            return 'partial';
        }
        return 'free';
    }

    function getTooltipMessage(status) {
        if (status === 'full') {
            return '❌ Этот день полностью занят\nВыберите другую дату';
        } else if (status === 'partial') {
            return '⚠️ В этот день есть свободные часы\nВыберите время на следующем шаге';
        }
        return '✅ Свободный день\nМожно забронировать';
    }

    function applyHighlightToDays() {
        const days = document.querySelectorAll('.flatpickr-day');

        const currentMonthElem = document.querySelector('.flatpickr-current-month');
        if (!currentMonthElem) return;

        const monthYearText = currentMonthElem.textContent;
        const monthMatch = monthYearText.match(/([а-я]+)/i);
        const yearMatch = monthYearText.match(/(\d{4})/);

        if (!monthMatch || !yearMatch) return;

        const months = {
            'январь': 1, 'февраль': 2, 'март': 3, 'апрель': 4,
            'май': 5, 'июнь': 6, 'июль': 7, 'август': 8,
            'сентябрь': 9, 'октябрь': 10, 'ноябрь': 11, 'декабрь': 12
        };
        const month = months[monthMatch[1].toLowerCase()];
        const year = yearMatch[1];

        days.forEach(day => {
            if (day.classList.contains('prevMonthDay') || day.classList.contains('nextMonthDay')) return;

            const dayNumber = parseInt(day.textContent);
            if (isNaN(dayNumber)) return;

            const monthStr = month.toString().padStart(2, '0');
            const dayStr = dayNumber.toString().padStart(2, '0');
            const dateKey = `${year}-${monthStr}-${dayStr}`;

            const status = getDateStatus(dateKey);

            day.classList.remove('full-day', 'partial-day');

            if (status === 'full') {
                day.classList.add('full-day');
                day.style.backgroundColor = '#e2e8f0';
                day.style.color = '#94a3b8';
            } else if (status === 'partial') {
                day.classList.add('partial-day');
                day.style.backgroundColor = '#fef9c3';
                day.style.color = '#854d0e';
            } else {
                day.style.backgroundColor = '';
                day.style.color = '';
            }

            // Добавляем обработчик клика для показа подсказки и сохранения даты
            day.removeEventListener('click', day._clickHandler);
            day._clickHandler = function(e) {
                e.stopPropagation();
                const msg = getTooltipMessage(status);
                const isError = (status === 'full');
                showTooltip(day, msg, isError);

                // Сохраняем выбранную дату
                if (status !== 'full') {
                    selectedDate = dateKey;
                    // Обновляем ссылку на кнопке
                    bookingBtn.href = `/bookings/create/${spaceId}/?date=${selectedDate}`;
                    bookingBtn.classList.remove('disabled');
                } else {
                    bookingBtn.classList.add('disabled');
                    bookingBtn.href = "#";
                }
            };
            day.addEventListener('click', day._clickHandler);
        });
    }

    const calendar = flatpickr(calendarInput, {
        inline: true,
        dateFormat: "Y-m-d",
        minDate: "today",
        locale: "ru",
        firstDayOfWeek: 1,

        onChange: function(selectedDates, dateStr) {
            if (selectedDates.length && selectedDates[0]) {
                const status = getDateStatus(dateStr);

                if (status === 'full') {
                    bookingBtn.classList.add('disabled');
                    bookingBtn.href = "#";
                    showTooltip(calendarInput.nextElementSibling, getTooltipMessage(status), true);
                } else {
                    selectedDate = dateStr;  // ← ДОБАВЛЕНО: сохраняем дату
                    bookingBtn.classList.remove('disabled');
                    bookingBtn.href = `/bookings/create/${spaceId}/?date=${dateStr}`;
                    showTooltip(calendarInput.nextElementSibling, getTooltipMessage(status), false);
                }
            }
        }
    });

    setTimeout(applyHighlightToDays, 100);

    document.querySelectorAll('.flatpickr-next-month, .flatpickr-prev-month').forEach(btn => {
        btn.addEventListener('click', function() {
            setTimeout(applyHighlightToDays, 150);
        });
    });
});