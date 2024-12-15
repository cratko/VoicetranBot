import io
import librosa
import soundfile as sf
import speech_recognition as sr


def recognize_speech(voice_file: io.BytesIO) -> str:
    # Преобразуем голос в формат WAV с библиотеками librosa и soundfile.
    y, sr_rate = librosa.load(voice_file, sr=16000)
    voice_file.close()
    voice_file_wav = io.BytesIO()
    sf.write(voice_file_wav, y, sr_rate, format='WAV', subtype='PCM_16')
    voice_file_wav.seek(0)

    # Распознаем речь с помощью SpeechRecognition.
    recognizer = sr.Recognizer()
    with sr.AudioFile(voice_file_wav) as source:
        audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio, language='ru-RU')
            return text
        except sr.UnknownValueError:
            return "Не удалось распознать речь. Попробуйте еще раз"
        except sr.RequestError as e:
            return f"Ошибка подключения к серверу распознавания: {e}"
