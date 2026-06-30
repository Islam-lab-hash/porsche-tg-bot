# Porsche Telegram Bot MVP

Telegram-бот ищет проблемные Porsche Panamera GTS 2019 и Porsche 911 2019, оценивает повреждения, ремонт, импортные платежи, итоговую стоимость и score. MVP использует mock-источники, но структура уже разделяет Telegram, парсеры, расчёты, БД и конфиги.

## Что делает бот

- `/start` показывает описание и кнопки.
- `/budget 4000000` сохраняет бюджет.
- `/search` запускает ручной поиск по mock-источникам.
- `/lot https://...` пытается оценить конкретную ссылку.
- `/watch` и `/stop` подготовлены для мониторинга.
- Найденные объявления нормализуются, оцениваются и сохраняются в PostgreSQL при доступной БД.

## Как запустить локально

```bash
cd porsche_tg_bot
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

Для запуска бота без Docker нужна локальная PostgreSQL/Redis и корректный `DATABASE_URL`.

## Как настроить .env

Скопируй `.env.example` в `.env` и заполни:

```env
BOT_TOKEN=
OWNER_TELEGRAM_ID=
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/porsche_bot
REDIS_URL=redis://redis:6379/0
DEFAULT_BUDGET_RUB=4000000
DEFAULT_MONITORING_INTERVAL_MINUTES=60
OPENAI_API_KEY=
USE_VISION_ANALYSIS=false
```

Токен читается только из окружения. Не прошивай его в код.

## Как запустить миграции

```bash
alembic upgrade head
```

В Docker миграции запускаются автоматически перед ботом.

## Как запустить бота

```bash
docker compose up --build
```

Health-check API будет доступен на `http://localhost:8000/health`.

## Как добавить новый источник

1. Создай класс в `app/parsers/<source>.py`.
2. Реализуй интерфейс `BaseSourceParser`: `search()` и `parse_listing()`.
3. Добавь rate limit, retry, user-agent и обработку блокировок.
4. Подключи источник в `SearchPipeline.parsers`.
5. Возвращай `RawListing`, чтобы дальше работал общий normalizer.

## Как обновить ставки таможни и утильсбора

Ставки вынесены в `app/config/customs.yaml`. Перед реальным использованием обнови:

- пошлины по объёму двигателя;
- утильсбор;
- таможенный сбор;
- брокера, СБКТС/ЭПТС, ГЛОНАСС;
- доставку и комиссии.

Ставки утильсбора, пошлины и таможенных платежей могут меняться. Перед реальным использованием нужно обновлять конфиг по актуальным источникам.

## Ограничения MVP

- Реальные Авито/Авто.ру/Дром/Copart/IAAI заменены расширяемыми заглушками.
- VIN-отчёты, OCR, Vision AI и платежи не реализованы.
- Оценка ремонта приблизительная и не заменяет осмотр.
- Мониторинг имеет сервисный каркас, но полноценная логика дедупликации уведомлений будет следующим шагом.
