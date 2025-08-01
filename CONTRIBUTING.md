# Контрибьютинг

## Стиль и правила

### Структура статей
- Один файл = одна тема
- Обязательный заголовок H1
- Метаданные в YAML-front matter
- Разделы: Контекст, Пошагово, Пример кода, Замечания

### Код
- Кодовые блоки помечать языком: `pml`, `python`, `bash`, `powershell`, `yaml`
- Минимально воспроизводимые примеры
- Комментарии на русском

### Изображения
- Класть в `docs/assets/img/`
- Ссылаться относительными путями
- Оптимизировать размер

## Процесс

### Локальная разработка
```bash
# Установка зависимостей
python -m venv .venv
. .venv/bin/activate  # Windows: .\.venv\Scripts\activate
pip install mkdocs-material mkdocs-mermaid2 mkdocs-awesome-pages-plugin \
            mkdocs-git-revision-date-localized-plugin mkdocs-minify-plugin

# Запуск локального сервера
mkdocs serve

# Проверка линтером
npx markdownlint-cli2 **/*.md
```

### Создание новой статьи
```bash
python scripts/new_article.py how-to "Название статьи" "тег1,тег2"
```

### Коммиты
Используйте [Conventional Commits](https://www.conventionalcommits.org/):
- `docs(how-to): добавить кейс по автоматизации`
- `fix(recipes): исправить синтаксис в сниппете`
- `feat(reference): добавить справочник команд`

## Качество

- Не копируйте дословно закрытые тексты AVEVA
- Делайте конспект своими словами + внешняя ссылка
- Любой внешний пример — с меткой источника
- Проверяйте работоспособность примеров кода

## Pull Request

1. Создайте ветку от `main`
2. Внесите изменения
3. Проверьте локально: `mkdocs serve`
4. Создайте PR с описанием изменений
5. Дождитесь проверок CI 