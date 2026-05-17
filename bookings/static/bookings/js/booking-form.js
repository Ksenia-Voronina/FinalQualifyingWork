// booking-form.js
document.addEventListener('DOMContentLoaded', function() {
    const startInput = document.getElementById('id_start_datetime');
    const endInput = document.getElementById('id_end_datetime');
    const durationSpan = document.getElementById('duration');
    const totalSpan = document.getElementById('total');
    const pricePerHour = parseFloat(document.getElementById('price-per-hour')?.dataset.price || 0);

    // Расчёт стоимости
    function calculateTotal() {
        if (startInput && endInput && startInput.value && endInput.value) {
            const start = new Date(startInput.value);
            const end = new Date(endInput.value);
            const duration = (end - start) / (1000 * 3600);
            if (duration > 0) {
                durationSpan.textContent = duration.toFixed(1);
                totalSpan.textContent = (duration * pricePerHour).toFixed(0);
                return;
            }
        }
        if (durationSpan) durationSpan.textContent = '0';
        if (totalSpan) totalSpan.textContent = '0';
    }

    // Прокрутка к первому полю с ошибкой
    function scrollToFirstError() {
        // Ищем поля с ошибками
        const errorFields = document.querySelectorAll('.error-field, .time-booking-wrapper.has-error');
        if (errorFields.length > 0) {
            const firstError = errorFields[0];
            firstError.scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });
            return true;
        }

        // Ищем сообщения об ошибках
        const errorMessages = document.querySelectorAll('.form-error, .time-booking-error');
        if (errorMessages.length > 0) {
            const firstMessage = errorMessages[0];
            firstMessage.scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });
            // Подсветка сообщения об ошибке
            firstMessage.style.transition = 'background-color 0.3s ease';
            firstMessage.style.backgroundColor = '#fff5f5';
            setTimeout(() => {
                firstMessage.style.backgroundColor = '';
            }, 2000);
            return true;
        }
        return false;
    }

    // Вызываем прокрутку при загрузке страницы (если есть ошибки после отправки формы)
    scrollToFirstError();

    if (startInput) {
        startInput.addEventListener('change', calculateTotal);
        startInput.addEventListener('input', calculateTotal);
    }
    if (endInput) {
        endInput.addEventListener('change', calculateTotal);
        endInput.addEventListener('input', calculateTotal);
    }

    calculateTotal();
});