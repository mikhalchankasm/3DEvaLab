#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import shutil
from pathlib import Path
from datetime import date

class ArticleManager:
    def __init__(self, root):
        self.root = root
        self.root.title("3DEvaLab Article Manager")
        self.root.geometry("600x700")
        
        # Путь к репозиторию
        self.repo_path = Path(r"D:\GitHub\3DEvaLab")
        self.docs_path = self.repo_path / "docs"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="3DEvaLab Article Manager", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Секция создания статьи
        self.create_article_section(main_frame)
        
        # Секция добавления изображений
        self.create_image_section(main_frame)
        
        # Секция коммита
        self.create_commit_section(main_frame)
        
        # Лог
        self.create_log_section(main_frame)
        
    def create_article_section(self, parent):
        # Заголовок секции
        section_label = ttk.Label(parent, text="1. Создание статьи", 
                                 font=("Arial", 12, "bold"))
        section_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Раздел
        ttk.Label(parent, text="Раздел:").grid(row=2, column=0, sticky=tk.W)
        self.section_var = tk.StringVar(value="how-to")
        section_combo = ttk.Combobox(parent, textvariable=self.section_var, 
                                    values=["getting-started", "how-to", "reference", "recipes", "glossary"],
                                    state="readonly", width=20)
        section_combo.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Название
        ttk.Label(parent, text="Название:").grid(row=3, column=0, sticky=tk.W)
        self.title_var = tk.StringVar()
        title_entry = ttk.Entry(parent, textvariable=self.title_var, width=40)
        title_entry.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Теги
        ttk.Label(parent, text="Теги (через запятую):").grid(row=4, column=0, sticky=tk.W)
        self.tags_var = tk.StringVar()
        tags_entry = ttk.Entry(parent, textvariable=self.tags_var, width=40)
        tags_entry.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Уровень
        ttk.Label(parent, text="Уровень:").grid(row=5, column=0, sticky=tk.W)
        self.level_var = tk.StringVar(value="basic")
        level_combo = ttk.Combobox(parent, textvariable=self.level_var,
                                  values=["basic", "intermediate", "advanced"],
                                  state="readonly", width=20)
        level_combo.grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # Кнопка создания
        create_btn = ttk.Button(parent, text="Создать статью", 
                               command=self.create_article)
        create_btn.grid(row=6, column=0, columnspan=2, pady=10)
        
    def create_image_section(self, parent):
        # Заголовок секции
        section_label = ttk.Label(parent, text="2. Добавление изображений", 
                                 font=("Arial", 12, "bold"))
        section_label.grid(row=7, column=0, columnspan=2, sticky=tk.W, pady=(20, 10))
        
        # Название статьи для изображений
        ttk.Label(parent, text="Название статьи:").grid(row=8, column=0, sticky=tk.W)
        self.image_article_var = tk.StringVar()
        image_article_entry = ttk.Entry(parent, textvariable=self.image_article_var, width=40)
        image_article_entry.grid(row=8, column=1, sticky=tk.W, pady=5)
        
        # Кнопка выбора файлов
        select_btn = ttk.Button(parent, text="Выбрать изображения", 
                               command=self.select_images)
        select_btn.grid(row=9, column=0, columnspan=2, pady=5)
        
        # Список выбранных файлов
        ttk.Label(parent, text="Выбранные файлы:").grid(row=10, column=0, sticky=tk.W)
        self.image_listbox = tk.Listbox(parent, height=4, width=50)
        self.image_listbox.grid(row=11, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Кнопка копирования
        copy_btn = ttk.Button(parent, text="Копировать в репозиторий", 
                             command=self.copy_images)
        copy_btn.grid(row=12, column=0, columnspan=2, pady=5)
        
        self.selected_images = []
        
    def create_commit_section(self, parent):
        # Заголовок секции
        section_label = ttk.Label(parent, text="3. Коммит изменений", 
                                 font=("Arial", 12, "bold"))
        section_label.grid(row=13, column=0, columnspan=2, sticky=tk.W, pady=(20, 10))
        
        # Сообщение коммита
        ttk.Label(parent, text="Сообщение коммита:").grid(row=14, column=0, sticky=tk.W)
        self.commit_msg_var = tk.StringVar()
        commit_entry = ttk.Entry(parent, textvariable=self.commit_msg_var, width=50)
        commit_entry.grid(row=14, column=1, sticky=tk.W, pady=5)
        
        # Кнопка коммита
        commit_btn = ttk.Button(parent, text="Сделать коммит", 
                               command=self.make_commit)
        commit_btn.grid(row=15, column=0, columnspan=2, pady=10)
        
    def create_log_section(self, parent):
        # Заголовок секции
        section_label = ttk.Label(parent, text="Лог операций", 
                                 font=("Arial", 12, "bold"))
        section_label.grid(row=16, column=0, columnspan=2, sticky=tk.W, pady=(20, 10))
        
        # Текстовое поле для лога
        self.log_text = tk.Text(parent, height=8, width=70)
        self.log_text.grid(row=17, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Скроллбар для лога
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=17, column=2, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
    def log(self, message):
        """Добавить сообщение в лог"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def create_article(self):
        """Создать новую статью"""
        try:
            section = self.section_var.get()
            title = self.title_var.get().strip()
            tags = self.tags_var.get().strip()
            level = self.level_var.get()
            
            if not title:
                messagebox.showerror("Ошибка", "Введите название статьи")
                return
                
            # Запуск скрипта создания статьи
            cmd = [
                "python", 
                str(self.repo_path / "scripts" / "new_article.py"),
                section, title, tags
            ]
            
            self.log(f"Создание статьи: {title}")
            result = subprocess.run(cmd, cwd=self.repo_path, 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log(f"✅ Статья создана: {result.stdout.strip()}")
                # Очистить поля
                self.title_var.set("")
                self.tags_var.set("")
                # Установить название для изображений
                self.image_article_var.set(title.lower().replace(" ", "-"))
            else:
                self.log(f"❌ Ошибка: {result.stderr}")
                messagebox.showerror("Ошибка", result.stderr)
                
        except Exception as e:
            self.log(f"❌ Исключение: {str(e)}")
            messagebox.showerror("Ошибка", str(e))
            
    def select_images(self):
        """Выбрать изображения"""
        files = filedialog.askopenfilenames(
            title="Выберите изображения",
            filetypes=[
                ("Изображения", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("Все файлы", "*.*")
            ]
        )
        
        if files:
            self.selected_images = list(files)
            self.image_listbox.delete(0, tk.END)
            for file in self.selected_images:
                self.image_listbox.insert(tk.END, os.path.basename(file))
            self.log(f"Выбрано {len(files)} изображений")
            
    def copy_images(self):
        """Скопировать изображения в репозиторий"""
        if not self.selected_images:
            messagebox.showwarning("Предупреждение", "Сначала выберите изображения")
            return
            
        article_name = self.image_article_var.get().strip()
        if not article_name:
            messagebox.showerror("Ошибка", "Введите название статьи для изображений")
            return
            
        try:
            # Создать папку для изображений
            img_dir = self.docs_path / "assets" / "img" / article_name
            img_dir.mkdir(parents=True, exist_ok=True)
            
            copied_files = []
            for src_file in self.selected_images:
                filename = os.path.basename(src_file)
                dst_file = img_dir / filename
                shutil.copy2(src_file, dst_file)
                copied_files.append(filename)
                
            self.log(f"✅ Скопировано {len(copied_files)} файлов в {img_dir}")
            self.log(f"Файлы: {', '.join(copied_files)}")
            
            # Очистить список
            self.selected_images = []
            self.image_listbox.delete(0, tk.END)
            
        except Exception as e:
            self.log(f"❌ Ошибка копирования: {str(e)}")
            messagebox.showerror("Ошибка", str(e))
            
    def make_commit(self):
        """Сделать коммит"""
        commit_msg = self.commit_msg_var.get().strip()
        if not commit_msg:
            messagebox.showerror("Ошибка", "Введите сообщение коммита")
            return
            
        try:
            # Добавить все файлы
            self.log("Добавление файлов в git...")
            result = subprocess.run(["git", "add", "."], cwd=self.repo_path,
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                self.log(f"❌ Ошибка git add: {result.stderr}")
                return
                
            # Сделать коммит
            self.log(f"Создание коммита: {commit_msg}")
            result = subprocess.run(["git", "commit", "-m", commit_msg], 
                                  cwd=self.repo_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("✅ Коммит создан успешно")
                self.commit_msg_var.set("")
                messagebox.showinfo("Успех", "Коммит создан! Теперь выполните git push в терминале.")
            else:
                self.log(f"❌ Ошибка коммита: {result.stderr}")
                messagebox.showerror("Ошибка", result.stderr)
                
        except Exception as e:
            self.log(f"❌ Исключение: {str(e)}")
            messagebox.showerror("Ошибка", str(e))

def main():
    root = tk.Tk()
    app = ArticleManager(root)
    root.mainloop()

if __name__ == "__main__":
    main() 