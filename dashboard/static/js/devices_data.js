document.addEventListener('DOMContentLoaded', () => {
    // === Константы и сопоставления ===
    const deviceTypeIcons = {
        'sensor': 'fas fa-microchip',
        'actuator': 'fas fa-cogs',
        'gateway': 'fas fa-network-wired',
        'other': 'fas fa-device'
    };

    // === DOM элементы ===
    const devicesContainer = document.getElementById('devicesContainer');
    let currentZoneName = null;

    // === Вспомогательные функции ===
    const getCookie = name => {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                return decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
        return null;
    };

    const formatDate = dateString => {
        if (!dateString) return '';
        if (dateString.match(/^\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}$/)) {
            return dateString;
        }
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return 'Некорректная дата';
        return date.toLocaleDateString('ru-RU', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    // === Создание карточки устройства ===
    const createDeviceCard = (device) => {
        const card = document.createElement('div');
        card.className = 'device-card';

        // Заголовок карточки
        const header = document.createElement('div');
        header.className = 'device-header';

        const icon = document.createElement('div');
        icon.className = 'device-icon';
        icon.innerHTML = `<i class="${deviceTypeIcons[device.model.device_type] || deviceTypeIcons.other}"></i>`;

        const title = document.createElement('div');
        title.className = 'device-title';

        const name = document.createElement('h3');
        name.className = 'device-name';
        name.textContent = device.name;

        const type = document.createElement('p');
        type.className = 'device-type';
        type.textContent = device.model.device_type;

        title.appendChild(name);
        title.appendChild(type);
        header.appendChild(icon);
        header.appendChild(title);

        // Информация об устройстве
        const info = document.createElement('div');
        info.className = 'device-info';

        const infoItems = [
            { label: 'Серийный номер', value: device.serial_number },
            { label: 'Тип подключения', value: device.connection_type },
            { label: 'MAC адрес', value: device.mac_address },
            { label: 'IP адрес', value: device.ip_address },
            { label: 'Версия прошивки', value: device.firmware_version },
            { label: 'Статус', value: device.is_active ? 'Активно' : 'Неактивно' },
            { label: 'Дата установки', value: device.installation_date ? formatDate(device.installation_date) : null },
            { label: 'Последнее обслуживание', value: device.last_maintenance ? formatDate(device.last_maintenance) : null },
            { label: 'Интервал обслуживания', value: device.maintenance_interval }
        ];

        infoItems.forEach(item => {
            if (item.value) {
                const infoItem = document.createElement('div');
                infoItem.className = 'device-info-item';

                const label = document.createElement('span');
                label.className = 'device-info-label';
                label.textContent = item.label;

                const value = document.createElement('span');
                value.className = 'device-info-value';
                value.textContent = item.value;

                infoItem.appendChild(label);
                infoItem.appendChild(value);
                info.appendChild(infoItem);
            }
        });

        // Информация о модели
        const model = document.createElement('div');
        model.className = 'device-model';

        const modelHeader = document.createElement('div');
        modelHeader.className = 'model-header';

        const modelTitle = document.createElement('h4');
        modelTitle.className = 'model-title';
        modelTitle.textContent = `Модель: ${device.model.name}`;

        const modelToggle = document.createElement('i');
        modelToggle.className = 'fas fa-chevron-down model-toggle';

        modelHeader.appendChild(modelTitle);
        modelHeader.appendChild(modelToggle);

        const modelDetails = document.createElement('div');
        modelDetails.className = 'model-details';

        const modelInfo = document.createElement('div');
        modelInfo.className = 'model-info';

        const modelInfoItems = [
            { label: 'Производитель', value: device.model.manufacturer },
            { label: 'Тип устройства', value: device.model.device_type },
            { label: 'Описание', value: device.model.description },
            { label: 'Дата создания', value: formatDate(device.model.created_at) },
            { label: 'Дата обновления', value: formatDate(device.model.updated_at) }
        ];

        modelInfoItems.forEach(item => {
            if (item.value) {
                const infoItem = document.createElement('div');
                infoItem.className = 'model-info-item';

                const label = document.createElement('span');
                label.className = 'model-info-label';
                label.textContent = item.label;

                const value = document.createElement('span');
                value.className = 'model-info-value';
                value.textContent = item.value;

                infoItem.appendChild(label);
                infoItem.appendChild(value);
                modelInfo.appendChild(infoItem);
            }
        });

        modelDetails.appendChild(modelInfo);
        model.appendChild(modelHeader);
        model.appendChild(modelDetails);

        // Обработчик клика по заголовку модели
        modelHeader.addEventListener('click', () => {
            modelDetails.classList.toggle('expanded');
            modelToggle.classList.toggle('expanded');
        });

        // Собираем карточку
        card.appendChild(header);
        card.appendChild(info);
        card.appendChild(model);

        return card;
    };

    // === Загрузка устройств зоны ===
    const loadZoneDevices = async (zoneName) => {
        try {
            const response = await fetch(`/api/v1/devices/zones_devices/?zone=${zoneName}`, {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                credentials: 'include'
            });

            if (!response.ok) throw new Error('Ошибка загрузки устройств');

            const devices = await response.json();
            
            if (!devices.length) {
                if (devicesContainer) {
                    devicesContainer.innerHTML = `
                        <div class="empty-state-container">
                            <div class="no-devices">
                                <i class="fas fa-microchip"></i>
                                <h3>Нет доступных устройств</h3>
                                <p>В этой зоне нет устройств</p>
                            </div>
                        </div>
                    `;
                }
                return;
            }

            // Очищаем контейнер
            if (devicesContainer) {
                devicesContainer.innerHTML = '';
                
                // Добавляем карточки устройств
                devices.forEach(device => {
                    const card = createDeviceCard(device);
                    devicesContainer.appendChild(card);
                });
            }
        } catch (error) {
            console.error('Error:', error);
            if (devicesContainer) {
                devicesContainer.innerHTML = `
                    <div class="empty-state-container">
                        <div class="error-state">
                            <i class="fas fa-exclamation-circle"></i>
                            <h3>Ошибка загрузки</h3>
                            <p>Не удалось загрузить список устройств</p>
                        </div>
                    </div>
                `;
            }
        }
    };

    // === Обработка событий ===
    document.addEventListener('zoneChanged', (event) => {
        const zoneName = event.detail.name;
        if (zoneName) {
            currentZoneName = zoneName;
            loadZoneDevices(zoneName);
        }
    });

    // === Инициализация ===
    if (devicesContainer) {
        // Очищаем контейнер при первой загрузке
        devicesContainer.innerHTML = `
            <div class="empty-state-container">
                <div class="no-devices">
                    <i class="fas fa-microchip"></i>
                    <h3>Выберите зону</h3>
                    <p>Для просмотра устройств выберите зону выше</p>
                </div>
            </div>
        `;
    }
});
