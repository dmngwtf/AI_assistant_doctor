Medical Bot
A Telegram bot that helps users identify possible medical diagnoses based on symptoms provided via text or voice input. The bot uses speech recognition, natural language processing, and an external API to process symptoms, predict diseases, and provide treatment recommendations.
Setup Instructions

Clone the repository:
git clone <repository_url>
cd medical_bot


Install dependencies: Ensure Python 3.8+ is installed, then run:
pip install -r requirements.txt


Install FFmpeg: FFmpeg is required for audio conversion. Install it on your system:

Ubuntu: sudo apt-get install ffmpeg
macOS: brew install ffmpeg
Windows: Download from FFmpeg website and add to PATH.


Download Vosk model: Download the Russian Vosk model (vosk-model-ru-0.22) from Vosk Models and place it in the project root or update the VOSK_MODEL_PATH in config/config.py.

Configure the bot: Update config/config.py with your Telegram bot token and API keys for the Grok API.

Run the bot:
python main.py



Usage

Start the bot with /start to receive a welcome message.
Send symptoms via text (e.g., "кашель, температура") or voice message.
The bot will ask for additional symptoms if needed and provide a diagnosis and recommendations.

Notes

This bot is for informational purposes only and does not replace professional medical advice.
Ensure API keys and tokens are kept secure and not exposed in version control.

Project Structure

config/: Configuration settings.
utils/: Utility functions for audio processing, API calls, and logging.
services/: Business logic for symptom processing, recommendations, and user state.
handlers/: Telegram bot message handlers.
main.py: Bot entry point.
requirements.txt: Project dependencies.

