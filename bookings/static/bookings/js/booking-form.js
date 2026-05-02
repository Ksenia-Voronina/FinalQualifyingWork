// booking-form.js
document.addEventListener('DOMContentLoaded', function() {
    const startInput = document.getElementById('id_start_datetime');
    const endInput = document.getElementById('id_end_datetime');
    const durationSpan = document.getElementById('duration');
    const totalSpan = document.getElementById('total');
    const pricePerHour = parseFloat(document.getElementById('price-per-hour')?.dataset.price || 0);

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