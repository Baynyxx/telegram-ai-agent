import time
import tkinter as tk
import threading


def notify(title, message, top_offset=30, opacity=0.85):
    """
    Показывает полупрозрачное уведомление сверху по центру.
    Клики проходят сквозь окно (можно нажимать кнопки под ним).
    top_offset – отступ от верха, opacity – прозрачность (0.0–1.0).
    """
    WIDTH = 420
    HEIGHT = 120
    BG = "#161616"
    TRANSPARENT = "#00ff00"
    SHOW_TIME = 1500
    UPDATE_INTERVAL = 500

    def move_animation(window, start_y, end_y):
        steps = 15
        for i in range(steps):
            y = start_y + (end_y - start_y) * (i + 1) / steps
            screen_width = window.winfo_screenwidth()
            x = (screen_width - WIDTH) // 2
            window.geometry(f"{WIDTH}x{HEIGHT}+{x}+{int(y)}")
            time.sleep(0.01)

    def fade_out(window):
        alpha = opacity
        while alpha > 0:
            alpha -= 0.08
            try:
                window.attributes("-alpha", alpha)
            except:
                break
            time.sleep(0.02)
        window.destroy()

    def keep_centered(window, end_y):
        def update():
            if not window.winfo_exists():
                return
            screen_width = window.winfo_screenwidth()
            x = (screen_width - WIDTH) // 2
            window.geometry(f"{WIDTH}x{HEIGHT}+{x}+{end_y}")
            window.after(UPDATE_INTERVAL, update)
        window.after(100, update)

    def create():
        root = tk.Tk()
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.attributes("-alpha", opacity)          # полупрозрачность
        root.configure(bg=TRANSPARENT)
        root.attributes("-transparentcolor", TRANSPARENT)
        root.attributes("-disabled", True)          # клики проходят сквозь

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        start_y = -HEIGHT
        end_y = top_offset
        x = (screen_width - WIDTH) // 2

        root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{start_y}")

        canvas = tk.Canvas(
            root,
            width=WIDTH,
            height=HEIGHT,
            bg=TRANSPARENT,
            highlightthickness=0
        )
        canvas.pack()

        def create_round_rect(x1, y1, x2, y2, r, **kw):
            return canvas.create_polygon(
                [x1 + r, y1, x2 - r, y1, x2, y1, x2, y2, x2 - r, y2, x1 + r, y2, x1, y2, x1, y1],
                smooth=True,
                **kw
            )

        create_round_rect(3, 3, WIDTH - 3, HEIGHT - 3, 18, fill=BG)

        canvas.create_text(
            WIDTH // 2, 35,
            text=title,
            fill="white",
            font=("Aptos Display", 18, "bold"),
            anchor="center"
        )
        canvas.create_text(
            WIDTH // 2, 75,
            text=message,
            fill="#dddddd",
            font=("Aptos", 14),
            width=340,
            justify="center",
            anchor="center"
        )

        # анимация появления
        threading.Thread(target=move_animation, args=(root, start_y, end_y), daemon=True).start()

        # периодическое обновление центрирования
        root.after(int((15 * 0.01) * 1000) + 50, lambda: keep_centered(root, end_y))

        # автозакрытие
        def close():
            fade_out(root)

        root.after(SHOW_TIME, close)
        root.mainloop()

    threading.Thread(target=create, daemon=True).start()