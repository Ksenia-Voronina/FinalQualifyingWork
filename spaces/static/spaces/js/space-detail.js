// space-detail.js
document.addEventListener('DOMContentLoaded', function() {
    const calendarInput = document.getElementById('booking-calendar');
    const bookingBtn = document.getElementById('booking-btn');
    let currentDateKey = null;

    if (!calendarInput) return;

    // Создаём тултип
    let tooltip = document.querySelector('.calendar-tooltip');
    if (!tooltip) {
        tooltip = document.createElement('div');
        tooltip.className = 'calendar-tooltip';
        document.body.appendChild(tooltip);
    }

    function showTooltip(dayElement, message, isError = false) {
        if (!dayElement) return;
        const rect = dayElement.getBoundingClientRect();
        tooltip.textContent = message;
        tooltip.style.display = 'block';
        tooltip.style.left = `${rect.left + rect.width / 2}px`;
        tooltip.style.top = `${rect.top - 40}px`;
        tooltip.style.transform = 'translateX(-50%)';
        tooltip.style.backgroundColor = isError ? '#e53e3e' : '#1a2634';
        tooltip.style.whiteSpace = 'pre-line';
    }

    function hideTooltip() {
        tooltip.style.display = 'none';
    }

    function formatHour(hour) {
        return `${hour.toString().padStart(2, '0')}:00`;
    }

    function getTooltipMessage(dateKey, status) {
        if (status === 'full') {
            return '❌ Весь день занят\nДоступных часов нет';
        }
        if (status === 'partial') {
            const busyHours = (bookedHours && bookedHours[dateKey]) ? bookedHours[dateKey] : [];
            const WORK_START = 8;
            const WORK_END = 20;

            const allHours = [];
            for (let i = WORK_START; i < WORK_END; i++) allHours.push(i);
            const freeHours = allHours.filter(h => !busyHours.includes(h));

            if (freeHours.length === 0) {
                return '⚠️ Частичная занятость\nСвободных часов нет';
            }

            // Группировка в диапазоны
            const ranges = [];
            let start = freeHours[0];
            let end = freeHours[0];
            for (let i = 1; i < freeHours.length; i++) {
                if (freeHours[i] === end + 1) {
                    end = freeHours[i];
                } else {
                    ranges.push({ start: start, end: end + 1 });
                    start = freeHours[i];
                    end = freeHours[i];
                }
            }
            ranges.push({ start: start, end: end + 1 });

            const formattedRanges = ranges.map(range => {
                if (range.start + 1 === range.end) {
                    return formatHour(range.start);
                }
                return `${formatHour(range.start)}-${formatHour(range.end)}`;
            }).join(', ');

            return `⚠️ Частичная занятость\n🆓 Свободные часы: ${formattedRanges}`;
        }
        return '✅ Свободно\nМожно забронировать';
    }

    function getDayStatus(dateKey) {
        if (bookedDatesFull && bookedDatesFull.includes(dateKey)) {
            return 'full';
        }
        if (bookedDatesPartial && bookedDatesPartial.includes(dateKey)) {
            return 'partial';
        }
        return 'free';
    }

    function refreshDayStyles() {
        const days = document.querySelectorAll('.flatpickr-day');

        // Получаем месяц и год из календаря
        const monthElem = document.querySelector('.flatpickr-current-month');
        if (!monthElem) return;

        const monthYearText = monthElem.textContent;
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
            const status = getDayStatus(dateKey);

            // Сохраняем дату как атрибут для доступа при клике
            day.setAttribute('data-date-key', dateKey);
            day.setAttribute('data-status', status);

            // Применяем стили
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

            // Навешиваем обработчик клика напрямую
            day.onclick = function(e) {
                e.stopPropagation();
                const dateKey = this.getAttribute('data-date-key');
                const status = this.getAttribute('data-status');
                const msg = getTooltipMessage(dateKey, status);
                const isError = (status === 'full');
                showTooltip(this, msg, isError);

                if (status === 'full') {
                    bookingBtn.classList.add('disabled');
                    bookingBtn.href = '#';
                } else {
                    bookingBtn.classList.remove('disabled');
                    bookingBtn.href = `/bookings/create/${spaceId}/?date=${dateKey}`;
                }
            };
        });
    }

    // Инициализация календаря
    const calendar = flatpickr(calendarInput, {
        inline: true,
        dateFormat: "Y-m-d",
        minDate: "today",
        locale: "ru",
        firstDayOfWeek: 1,

        onChange: function(selectedDates, dateStr) {
            // Обновляем стили и обработчики
            setTimeout(refreshDayStyles, 10);

            const status = getDayStatus(dateStr);
            if (status === 'full') {
                bookingBtn.classList.add('disabled');
                bookingBtn.href = '#';
            } else {
                bookingBtn.classList.remove('disabled');
                bookingBtn.href = `/bookings/create/${spaceId}/?date=${dateStr}`;
            }
        }
    });

    // Первоначальное применение стилей
    setTimeout(refreshDayStyles, 100);

    // Обновляем при смене месяца
    document.addEventListener('click', function(e) {
        if (e.target.closest('.flatpickr-next-month') || e.target.closest('.flatpickr-prev-month')) {
            setTimeout(refreshDayStyles, 150);
        }
    });

    // Скрытие тултипа
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.flatpickr-day') && !e.target.closest('.flatpickr-calendar')) {
            hideTooltip();
        }
    });
});