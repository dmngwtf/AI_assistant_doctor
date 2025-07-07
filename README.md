
# 🤖 Medical Bot / Медицинский Бот

A Telegram bot that helps users identify possible medical diagnoses based on symptoms provided via **text or voice input**.  
Бот Telegram, который помогает определить возможные диагнозы на основе симптомов, отправленных **текстом или голосом**.

---

## 🚀 Setup Instructions / Инструкции по установке

### 1. Clone the repository / Клонирование репозитория

```bash
git clone <repository_url>
cd medical_bot
````

### 2. Install dependencies / Установка зависимостей

Ensure Python 3.8+ is installed / Убедитесь, что установлен Python версии 3.8 или выше:

```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg / Установка FFmpeg

FFmpeg is required for audio processing / FFmpeg необходим для обработки аудио:

* **macOS**:

  ```bash
  brew install ffmpeg
  ```
* **Windows**:
  [Download FFmpeg](https://ffmpeg.org/download.html) and add to PATH / скачайте с сайта и добавьте в PATH.

### 4. Download Vosk model / Загрузка модели Vosk

* Download the Russian Vosk model (`vosk-model-ru-0.22`) from [Vosk Models](https://alphacephei.com/vosk/models).
* Place it in the project root or update the `VOSK_MODEL_PATH` in `config/config.py`.

Скачайте русскую модель Vosk и разместите её в корне проекта или укажите путь в `config/config.py`.

### 5. Configure the bot / Настройка бота

Edit `config/config.py` and add:

* Your Telegram Bot Token
* Grok API keys for diagnosis

Отредактируйте `config/config.py`, добавив:

* Токен вашего Telegram-бота
* API-ключи для сервиса Grok

### 6. Run the bot / Запуск бота

```bash
python main.py
```

---

## 💬 Usage / Использование

1. Start the bot with the `/start` command.
   Запустите бота командой `/start`.

2. Send symptoms via **text** (e.g., `кашель, температура`) or **voice message**.
   Отправьте симптомы **текстом** или **голосом**.

3. The bot may ask for more symptoms, then provide a **preliminary diagnosis** and **recommendations**.
   Бот может запросить дополнительные симптомы, а затем предложит **возможный диагноз** и **рекомендации**.

---

## 📁 Project Structure / Структура проекта

```
medical_bot/
├── config/           # Configuration settings / Настройки
├── utils/            # Utility functions / Вспомогательные функции
├── services/         # Business logic / Логика обработки данных
├── handlers/         # Bot message handlers / Обработчики сообщений
├── main.py           # Bot entry point / Точка входа
├── requirements.txt  # Project dependencies / Зависимости
```

---
