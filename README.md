# 3DEvaLab

База знаний по AVEVA E3D и PML — практичные решения для инженеров.

## Что здесь есть

- 🔧 **How-to** — пошаговые руководства
- 🍳 **Recipes** — готовые сниппеты кода  
- 📚 **Reference** — справочник команд
- 🔤 **Глоссарий** — термины и понятия

## Быстрый старт

```bash
# Установка
python -m venv .venv
.\.venv\Scripts\activate  # Windows
pip install mkdocs-material mkdocs-awesome-pages-plugin

# Запуск
mkdocs serve
```

## Добавить статью

```bash
python scripts/new_article.py how-to "Название" "теги"
```

## Сайт

https://mikhalchankasm.github.io/3DEvaLab/

---

**Лицензия:** Текст — CC BY 4.0, код — MIT 