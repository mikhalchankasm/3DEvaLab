---
title: FMSYS — глобальный объект Forms & Menus System
tags: [pml, e3d, ui, forms, menus]
updated: 2025-08-01
level: intermediate
---

# FMSYS — глобальный объект Forms & Menus System

## Обзор

`!!FMSYS` создаётся ядром E3D/PDMS при старте и экспортируется как **глобальная переменная**.  
Он хранит «системные» методы для управления интерфейсом без прямого обращения к .NET или внутренним классм E3D.

**Основные возможности:**
- Управление макетами форм
- Переключение приложений  
- Индикатор прогресса
- Прерывание долгих операций

---

## 1. Навигация по открытому UI

### Получение списка форм
```pml
!!FMSYS.shownforms()
```
**Возвращает:** ARRAY из FORM-объектов всех отображаемых форм

### Проверка системных менюбаров
```pml
!!FMSYS.NOPMLUIBARS() → BOOLEAN
```
**Результат:** `TRUE` — бары отключены, добавлять пункты меню небезопасно

---

## 2. Управление макетом форм

### Установка гибкой сетки символов
```pml
!!FMSYS.SetDefaultFormLayout('VarChars')
```
**Эффект:** Все новые/повторно-показанные формы переходят в режим VarChars

### Проверка текущего режима
```pml
!!FMSYS.DefaultFormLayout()
```
**Возвращает:** `'VARCHARS'` или `'FIXCHARS'`

---

## 3. Переключение главного приложения

```pml
!!FMSYS.SetMain(!!newMainForm) → возвращает старый main-form
```
**Назначение:** Делает форму главным контейнером AppWare  
**Применение:** Можно временно «перехватить» управление и затем вернуть обратно

---

## 4. Индикатор прогресса и статус-бар

### Показать/обновить прогресс-бар
```pml
!!FMSYS.setProgress(45)
!!FMSYS.setProgressText('Routing…')
```
**Примечание:** 0 — скрыть бар; текстовое поле обновляется отдельно

### Считать текущее значение
```pml
!!FMSYS.Progress() → REAL (0–100)
!!FMSYS.ProgressText() → STRING
```
**Применение:** Полезно при вложенных расчётах

### Статус-строка главного окна
```pml
!!FMSYS.SetStatusText('Ready')
```
**Особенность:** Сообщение временное — система тоже пишет туда подсказки

---

## 5. Прерывание длительных операций

### Настройка прерывания
1. **Свяжите** кнопку-стоп с системой:
   ```pml
   !!FMSYS.setInterrupt(!!fmstop.stopButton)
   ```

2. В цикле периодически проверяйте:
   ```pml
   if (!!FMSYS.Interrupt()) then 
     return error 1 'Aborted' 
   endif
   ```

**Результат:** Пользователь может отменить скрипт, не блокируя UI

---

## 6. Мини-шпаргалка по методам

| Категория | Методы |
|-----------|--------|
| **Макет форм** | `SetDefaultFormLayout()`, `DefaultFormLayout()` |
| **Главное приложение** | `SetMain()`, `Progress()`, `ProgressText()` |
| **Прогресс-бар** | `setProgress()`, `setProgressText()` |
| **Прерывание** | `setInterrupt()`, `Interrupt()` |
| **Отладка UI** | `shownforms()`, `NOPMLUIBARS()` |

---

## 7. Практические советы

- **Всегда** сбрасывайте прогресс `0` после завершения задачи
- При пакетной обработке вызывайте `shownforms()` для диагностики «зависших» окон
- Не ставьте VarChars глобально при наличии старых «FixChars» форм

---

## 8. Примеры использования

### Пример 1: Автоматическая процедура построения геометрии
**Файл:** SGeometry.pmlfrm

```pml
!!fmsys.setInterrupt(!this.btAuto)
!!fmsys.setProgress(0 / !proc)

if !!fmsys.interrupt() then 
  return error 1 'Aborted' 
endif

!!fmsys.active3dview().prompt.val
```

**Что делает:**
- Регистрирует кнопку btAuto как Stop-gadget
- Обновляет индикатор прогресса (0–100%)
- Берёт текст приглашения из активного 3D-вида

### Пример 2: Работа с текущим документом
**Файл:** stljointcheck.pmlfrm

```pml
!fmsys = object FMSYS()
!form = !fmsys.currentDocument()
```

**Применение:** Получение ссылки на форму-документ в фокусе для изменения параметров вида

### Пример 3: Экспорт объёмного отчёта
**Файл:** pceRtwoExp.pmlobj

```pml
!!fmsys.setprogress(0)    # старт
!!fmsys.setprogress(25)   # шаг 1
!!fmsys.setprogress(50)   # шаг 2
!!fmsys.setprogress(75)   # шаг 3
!!fmsys.setprogress(100)  # завершение
```

**Цель:** Показать пользователю прогресс экспорта R-to-W

---

## 9. Типовые сценарии применения

### Длинные циклы / массовые операции
```pml
!!fmsys.setInterrupt(!!myForm.stopBtn)
!!fmsys.setProgress(0)

do !i from 1 to !n
  # долго считаете
  if !!fmsys.interrupt() then
    return error 1 'Aborted by user'
  endif
  !!fmsys.setProgress(100 * !i / !n)
enddo

!!fmsys.setProgress(0)    # убираем полосу
```

### Работа с контекстной формой
```pml
!doc = !!fmsys.currentDocument()
if !doc != Unset then
  # работаем с формой
endif
```

### Вывод подсказок с прогресс-баром
```pml
!!fmsys.setProgressText('Шаг ' & !i)
!!fmsys.setProgress(50)
```

---

## Сводка методов

| Метод | Назначение |
|-------|------------|
| `setProgress(real percent)` | Показывает/обновляет полоску прогресса (0 снимает бар) |
| `setProgressText(string)` | Пишет текст слева от полоски прогресса |
| `setInterrupt(gadget)` | Указывает кнопку для прерывания цикла |
| `interrupt()` | Возвращает TRUE при нажатии Stop-gadget |
| `currentDocument()` | Даёт ссылку на активную форму-документ |
| `active3dview()` | Возвращает объект текущего 3D-вида |
