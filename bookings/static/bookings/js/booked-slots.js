// booked-slots.js
document.addEventListener('DOMContentLoaded', function() {
    const startInput = document.getElementById('id_start_datetime');
    const infoContainer = document.getElementById('bookedSlotsInfo');

    if (!startInput || !infoContainer) return;

    const spaceId = parseInt(document.getElementById('space-id')?.dataset.id || 0);

    function updateBookedSlots() {
        if (!startInput.value) return;

        const dateStr = startInput.value.split('T')[0];

        infoContainer.style.opacity = '0.5';

        fetch(`/bookings/get-booked-slots/${spaceId}/?date=${dateStr}`)
            .then(response => response.json())
            .then(data => {
                infoContainer.style.opacity = '1';

                if (data.booked_slots && data.booked_slots.length > 0) {
                    let slotsHtml = '<div class="booked-slots-list">';
                    slotsHtml += '<div class="warning-header">';
                    slotsHtml += '<span class="warning-icon">⚠️</span>';
                    slotsHtml += '<span>Занятые интервалы на эту дату:</span>';
                    slotsHtml += '</div><ul>';
                    data.booked_slots.forEach(slot => {
                        slotsHtml += `<li>${slot.start} — ${slot.end}</li>`;
                    });
                    slotsHtml += '</ul>';
                    slotsHtml += '<p class="info-note">💡 Выберите свободное время в форме ниже</p>';
                    slotsHtml += '</div>';

                    infoContainer.innerHTML = `
                        <div class="info-header">
                            <span class="info-icon">📅</span>
                            <strong>Выбранная дата: ${new Date(dateStr).toLocaleDateString('ru-RU')}</strong>
                        </div>
                        ${slotsHtml}
                    `;
                } else {
                    infoContainer.innerHTML = `
                        <div class="info-header">
                            <span class="info-icon">📅</span>
                            <strong>Выбранная дата: ${new Date(dateStr).toLocaleDateString('ru-RU')}</strong>
                        </div>
                        <div class="free-slots-info">
                            <span class="success-icon">✅</span>
                            <span>На эту дату пока нет бронирований. Вы можете выбрать любое удобное время.</span>
                        </div>
                    `;
                }
            })
            .catch(error => {
                infoContainer.style.opacity = '1';
                console.error('Ошибка загрузки занятых слотов:', error);
            });
    }

    startInput.addEventListener('change', updateBookedSlots);
    startInput.addEventListener('blur', updateBookedSlots);

    // Вызываем при загрузке
    updateBookedSlots();
});