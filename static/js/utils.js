    // Функция для копирования текста с использованием промисов
    function copyToClipboard(text) {
        if (!navigator.clipboard) {
            // Если API недоступно, выводим ошибку
            // alert('API буфера обмена недоступно в этом браузере.');
            // sendMessageToDjango('API буфера обмена недоступно в этом браузере.')
            sendMessage('API буфера обмена недоступно в этом браузере.')
            return;
        }

        // Вызываем writeText(), который возвращает промис
        navigator.clipboard.writeText(text)
            .then(function() {
                // Этот код выполнится, если промис разрешился (успешное копирование)
                // alert('Текст успешно скопирован!');
                // sendMessageToDjango('!!!Текст успешно скопирован!');
                sendMessage('Текст успешно скопирован!');

            })
            .catch(function(err) {
                // Этот код выполнится, если промис был отклонён (ошибка копирования)
                console.error('Ошибка копирования:', err);
                // alert('Не удалось скопировать текст. Проверьте консоль.');
                // sendMessageToDjango('Не удалось скопировать текст. Проверьте консоль.');
                sendMessage('Не удалось скопировать текст. Проверьте консоль.');
            });
    }

    // Функция для копирования текста из поля ввода
    function copyFromInput() {
        const input = document.getElementById('id_code');
        copyToClipboard(input.value);
    }

    // Функция для копирования произвольного текста
    function copyArbitraryText(text) {
        copyToClipboard(text);
    }