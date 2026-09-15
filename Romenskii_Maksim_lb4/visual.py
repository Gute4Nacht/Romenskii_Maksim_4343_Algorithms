import tkinter as tk

class KMPVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Визуализация алгоритма КМП")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.mode_var = tk.StringVar(value="search")
        self.log_steps = []
        self.current_step = 0
        self.is_running = False

        # Верхняя панель с выбором режима
        mode_frame = tk.Frame(root)
        mode_frame.pack(fill="x", padx=15, pady=10)
        tk.Label(mode_frame, text="Выберите режим:", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        tk.Radiobutton(mode_frame, text="Поиск подстроки", variable=self.mode_var, value="search",
                       command=self.reset_all).pack(side="left", padx=5)
        tk.Radiobutton(mode_frame, text="Циклический сдвиг", variable=self.mode_var, value="shift",
                       command=self.reset_all).pack(side="left", padx=5)

        # Панель ввода данных
        input_frame = tk.Frame(root)
        input_frame.pack(fill="x", padx=15, pady=5)
        
        tk.Label(input_frame, text="Образец (P):").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_p = tk.Entry(input_frame, width=65)
        self.entry_p.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(input_frame, text="Текст (T):").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_t = tk.Entry(input_frame, width=65)
        self.entry_t.grid(row=1, column=1, padx=5, pady=2)

        # Панель управления
        ctrl_frame = tk.Frame(root)
        ctrl_frame.pack(fill="x", padx=15, pady=10)
        
        tk.Button(ctrl_frame, text="Запуск", width=10, command=self.initialize).pack(side="left", padx=3)
        tk.Button(ctrl_frame, text="Следующий шаг", width=15, command=self.next_step).pack(side="left", padx=3)
        tk.Button(ctrl_frame, text="Автоматически", width=15, command=self.auto_play).pack(side="left", padx=3)
        tk.Button(ctrl_frame, text="Очистить", width=10, command=self.reset_all).pack(side="left", padx=3)

        # Область вывода
        out_frame = tk.Frame(root)
        out_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        tk.Label(out_frame, text="Протокол выполнения алгоритма:", anchor="w", font=("Arial", 9, "bold")).pack(fill="x")
        
        self.output_text = tk.Text(out_frame, font=("Courier New", 10), wrap="word")
        scrollbar = tk.Scrollbar(out_frame, command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        self.output_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def print_log(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)

    def reset_all(self):
        self.entry_p.delete(0, tk.END)
        self.entry_t.delete(0, tk.END)
        self.output_text.delete("1.0", tk.END)
        self.log_steps = []
        self.current_step = 0
        self.is_running = False

    def compute_prefix(self, pattern, log_list):
        m = len(pattern)
        pi_array = [0] * m
        log_list.append(f"Инициализация: pi[0] = 0")
        
        for i in range(1, m):
            j = pi_array[i - 1]
            while j > 0 and pattern[i] != pattern[j]:
                log_list.append(f"  i={i}: символ '{pattern[i]}' != '{pattern[j]}', откат j с {j} до {pi_array[j-1]}")
                j = pi_array[j - 1]
            
            if pattern[i] == pattern[j]:
                j += 1
                log_list.append(f"  i={i}: символ '{pattern[i]}' == '{pattern[j]}', j увеличивается до {j}")
            else:
                log_list.append(f"  i={i}: совпадений не найдено, j остается 0")
                
            pi_array[i] = j
            log_list.append(f"  Текущий массив pi: {pi_array}")
            
        return pi_array

    def prepare_search_steps(self, pattern, text):
        log_list = [f"=== Режим: Поиск подстроки ===", 
                    f"Образец: '{pattern}'", 
                    f"Текст: '{text}'", 
                    "--- Этап 1: Вычисление префикс-функции ---"]
        
        pi = self.compute_prefix(pattern, log_list)
        log_list.append(f"Итоговая префикс-функция: {pi}")
        log_list.append("--- Этап 2: Поиск в тексте ---")
        
        m, n = len(pattern), len(text)
        j = 0
        matches = []
        
        for i in range(n):
            while j > 0 and text[i] != pattern[j]:
                log_list.append(f"Текст[{i}]='{text[i]}' != Образец[{j}]='{pattern[j]}', откат j: {j} -> {pi[j-1]}")
                j = pi[j - 1]
                
            if text[i] == pattern[j]:
                j += 1
                
            if j == m:
                start_pos = i - m + 1
                matches.append(start_pos)
                log_list.append(f"*** Полное совпадение! Найдено на индексе: {start_pos} ***")
                j = pi[j - 1]
                
        result_str = ",".join(map(str, matches)) if matches else "-1"
        log_list.append(f"=== Результат: {result_str} ===")
        return log_list

    def prepare_shift_steps(self, str_a, str_b):
        if len(str_a) != len(str_b):
            return ["Ошибка: длины строк A и B не совпадают.", "=== Результат: -1 ==="]
        if not str_a:
            return ["=== Результат: 0 ==="]
            
        log_list = [f"=== Режим: Циклический сдвиг ===",
                    f"Строка A: '{str_a}'", 
                    f"Строка B: '{str_b}'", 
                    f"Виртуальная строка A+A: '{str_a + str_a}'",
                    "--- Этап 1: Префикс-функция для B ---"]
        
        pi = self.compute_prefix(str_b, log_list)
        log_list.append(f"Итоговая префикс-функция: {pi}")
        log_list.append("--- Этап 2: Поиск B в A+A ---")
        
        m, n = len(str_b), len(str_a)
        virtual_text = str_a + str_a
        j = 0
        
        for i in range(2 * n):
            while j > 0 and virtual_text[i] != str_b[j]:
                j = pi[j - 1]
                
            if virtual_text[i] == str_b[j]:
                j += 1
                
            if j == m:
                start_pos = i - m + 1
                if start_pos < n:
                    log_list.append(f"*** Совпадение найдено на индексе: {start_pos} (внутри первой A) ***")
                    log_list.append(f"=== Результат: {start_pos} ===")
                else:
                    log_list.append(f"Совпадение на индексе {start_pos} (выходит за границы первой A)")
                    log_list.append("=== Результат: -1 ===")
                return log_list
                
        log_list.append("Совпадений не найдено.")
        log_list.append("=== Результат: -1 ===")
        return log_list

    def initialize(self):
        self.output_text.delete("1.0", tk.END)
        self.log_steps = []
        self.current_step = 0
        self.is_running = False
        
        p_val = self.entry_p.get().strip()
        t_val = self.entry_t.get().strip()
        
        if self.mode_var.get() == "search":
            if not p_val or not t_val:
                self.print_log("Пожалуйста, заполните оба поля (Образец и Текст).")
                return
            self.log_steps = self.prepare_search_steps(p_val, t_val)
        else:
            self.log_steps = self.prepare_shift_steps(p_val, t_val)
            
        self.print_log("Инициализация завершена. Нажмите 'Следующий шаг' или 'Автоматически'.")

    def next_step(self):
        if self.current_step >= len(self.log_steps):
            return
        self.print_log(self.log_steps[self.current_step])
        self.current_step += 1

    def auto_play(self):
        self.is_running = True
        self._auto_tick()

    def _auto_tick(self):
        if not self.is_running or self.current_step >= len(self.log_steps):
            self.is_running = False
            return
        self.print_log(self.log_steps[self.current_step])
        self.current_step += 1
        self.root.after(400, self._auto_tick)


if __name__ == "__main__":
    root = tk.Tk()
    app = KMPVisualizer(root)
    root.mainloop()