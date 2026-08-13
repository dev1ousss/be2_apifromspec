### Пошаговая инструкция:

1. **Создайте виртуальное окружение Python:**
   ```bash
   python -m venv venv
   ```

2. **Активируйте виртуальное окружение (в PowerShell на Windows):**
   ```powershell
   ./venv/Scripts/Activate.ps1
   ```
   *Для macOS/Linux используйте:*
   ```powershell
   source venv/bin/activate
   ```

3. **Установите все необходимые зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Запустите базу данных PostgreSQL в Docker:**
   ```bash
   docker compose up -d
   ```
   *Параметр `-d` запустит контейнер в фоновом режиме.*

5. **Перейдите в папку с исходным кодом и запустите сервер приложений:**
   ```bash
   cd src
   uvicorn main:app --reload
   ```

6. **Откройте интерактивную документацию API:**
   Перейдите в браузере по адресу строго из ТЗ:  
   👉 **[click](http://127.0.0.1:8000/swagger/index.html)**