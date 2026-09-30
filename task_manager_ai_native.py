try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    TK_AVAILABLE = True
except ImportError:  # pragma: no cover - solo ocurre en entornos sin GUI
    tk = None
    ttk = None
    messagebox = None
    TK_AVAILABLE = False


VALID_USERS = ("ana", "jorge", "jojo")
MAX_TITLE_LENGTH = 100

tasks = []


class TaskError(Exception):
    """Error de negocio del gestor de tareas (validación o acceso)."""


def validate_user(user):
    if user not in VALID_USERS:
        raise TaskError(f"Usuario no válido: {user!r}")
    return user


def validate_title(title):
    if not isinstance(title, str):
        raise TaskError("El título debe ser texto.")
    clean_title = title.strip()
    if not clean_title:
        raise TaskError("El título no puede estar vacío.")
    if len(clean_title) > MAX_TITLE_LENGTH:
        raise TaskError(
            f"El título no puede superar {MAX_TITLE_LENGTH} caracteres."
        )
    return clean_title


def validate_index(index):
    # DECISIÓN DEL DESARROLLADOR:
    # Se rechazan bool y negativos de forma explícita: True/False son
    # subclases de int y un índice negativo permitiría acceder a tareas
    # de forma confusa. Todo índice inválido se reporta con TaskError.
    if isinstance(index, bool) or not isinstance(index, int):
        raise TaskError("El índice debe ser un número entero.")
    if index < 0:
        raise TaskError("El índice no puede ser negativo.")
    return index


def add_task(title, user):
    validate_user(user)
    clean_title = validate_title(title)
    task = {
        "title": clean_title,
        "user": user,
        "completed": False
    }
    tasks.append(task)
    return task


def list_tasks(user):
    # CORRECCIÓN (fuga de información):
    # Antes devolvía la lista global `tasks`, por lo que cualquier
    # usuario veía las tareas de los demás. Ahora solo se devuelven
    # las tareas cuyo propietario es `user`.
    validate_user(user)
    return [task for task in tasks if task["user"] == user]


def _resolve_task(index, user):
    """Devuelve (posición_global, tarea) del índice visible para `user`.

    El índice que maneja la interfaz es el de la lista filtrada del
    usuario. Aquí se traduce a la posición real dentro de la lista
    global para poder modificar o eliminar la tarea correcta.
    """
    validate_user(user)
    validate_index(index)

    user_tasks = [
        (position, task)
        for position, task in enumerate(tasks)
        if task["user"] == user
    ]

    if index >= len(user_tasks):
        raise TaskError(
            f"Índice fuera de rango: {index}. "
            f"El usuario {user} tiene {len(user_tasks)} tarea(s)."
        )

    return user_tasks[index]


def complete_task(index, user):
    _, task = _resolve_task(index, user)
    task["completed"] = True
    return "Tarea completada"


def delete_task(index, user):
    position, _ = _resolve_task(index, user)
    tasks.pop(position)
    return "Tarea eliminada"


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("920x620")
        self.root.minsize(820, 560)

        self.setup_style()
        self.create_variables()
        self.create_layout()
        self.refresh_tasks()

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))
        style.configure("Subtitle.TLabel", font=("Segoe UI", 10))
        style.configure("Section.TLabel", font=("Segoe UI", 11, "bold"))
        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.configure("Treeview", rowheight=30, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def create_variables(self):
        self.current_user = tk.StringVar(value="ana")
        self.user_vars = {
            "ana": tk.BooleanVar(value=True),
            "jorge": tk.BooleanVar(value=False),
            "jojo": tk.BooleanVar(value=False)
        }
        self.task_title = tk.StringVar()
        self.task_index = tk.StringVar()
        self.status_text = tk.StringVar(value="Aplicación lista.")

    def create_layout(self):
        header = ttk.Frame(self.root, padding=(20, 15, 20, 5))
        header.pack(fill="x")

        ttk.Label(
            header,
            text="Task Manager",
            style="Title.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            header,
            text="Aplicación de gestión de tareas",
            style="Subtitle.TLabel"
        ).pack(anchor="w", pady=(2, 0))

        top = ttk.Frame(self.root, padding=(20, 10))
        top.pack(fill="x")

        user_box = ttk.LabelFrame(top, text="Usuario actual", padding=12)
        user_box.pack(side="left", fill="x", expand=True, padx=(0, 8))

        ttk.Label(
            user_box,
            text="Seleccione un usuario:"
        ).grid(row=0, column=0, sticky="w", padx=(0, 12))

        users_frame = ttk.Frame(user_box)
        users_frame.grid(row=0, column=1, sticky="w")

        # Tres usuarios disponibles. Aunque visualmente son Checkbuttons,
        # el programa mantiene solo un usuario activo a la vez.
        for column, user in enumerate(("ana", "jorge", "jojo")):
            ttk.Checkbutton(
                users_frame,
                text=user.capitalize(),
                variable=self.user_vars[user],
                command=lambda selected_user=user: self.select_user(selected_user)
            ).grid(row=0, column=column, padx=(0, 14), sticky="w")

        task_box = ttk.LabelFrame(top, text="Nueva tarea", padding=12)
        task_box.pack(side="left", fill="x", expand=True, padx=(8, 0))

        ttk.Label(task_box, text="Título:").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )

        ttk.Entry(
            task_box,
            textvariable=self.task_title,
            width=35
        ).grid(row=0, column=1, sticky="ew")

        ttk.Button(
            task_box,
            text="Crear tarea",
            style="Action.TButton",
            command=self.create_task
        ).grid(row=0, column=2, padx=(8, 0))

        task_box.columnconfigure(1, weight=1)

        table_frame = ttk.LabelFrame(
            self.root,
            text="Tareas registradas",
            padding=12
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(5, 10)
        )

        columns = ("index", "title", "user", "status")

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        self.tree.heading("index", text="#")
        self.tree.heading("title", text="Título")
        self.tree.heading("user", text="Usuario")
        self.tree.heading("status", text="Estado")

        self.tree.column("index", width=50, anchor="center")
        self.tree.column("title", width=430)
        self.tree.column("user", width=150, anchor="center")
        self.tree.column("status", width=130, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.on_task_selected
        )

        actions = ttk.LabelFrame(
            self.root,
            text="Acciones sobre tareas",
            padding=12
        )
        actions.pack(fill="x", padx=20, pady=(0, 10))

        ttk.Label(
            actions,
            text="Índice de tarea:"
        ).grid(row=0, column=0, padx=(0, 8))

        ttk.Entry(
            actions,
            textvariable=self.task_index,
            width=10
        ).grid(row=0, column=1, padx=(0, 12))

        ttk.Button(
            actions,
            text="Completar",
            style="Action.TButton",
            command=self.complete_selected
        ).grid(row=0, column=2, padx=5)

        ttk.Button(
            actions,
            text="Eliminar",
            style="Action.TButton",
            command=self.delete_selected
        ).grid(row=0, column=3, padx=5)

        ttk.Button(
            actions,
            text="Actualizar lista",
            command=self.refresh_tasks
        ).grid(row=0, column=4, padx=5)

        ttk.Button(
            actions,
            text="Limpiar índice",
            command=lambda: self.task_index.set("")
        ).grid(row=0, column=5, padx=5)

        ttk.Label(
            actions,
            text="Seleccione una tarea o escriba directamente su índice.",
            wraplength=420
        ).grid(
            row=1,
            column=0,
            columnspan=6,
            sticky="w",
            pady=(10, 0)
        )

        status = ttk.Frame(
            self.root,
            padding=(20, 5, 20, 15)
        )
        status.pack(fill="x")

        ttk.Label(
            status,
            textvariable=self.status_text
        ).pack(side="left")

        ttk.Button(
            status,
            text="Salir",
            command=self.root.destroy
        ).pack(side="right")

    def select_user(self, selected_user):
        # Mantiene una sola casilla activa y actualiza inmediatamente la lista.
        self.current_user.set(selected_user)

        for user, variable in self.user_vars.items():
            variable.set(user == selected_user)

        self.task_index.set("")
        self.refresh_tasks()

    def create_task(self):
        user = self.current_user.get()

        try:
            add_task(self.task_title.get(), user)
        except TaskError as error:
            messagebox.showwarning("Datos inválidos", str(error))
            return

        self.task_title.set("")
        self.refresh_tasks()

        self.status_text.set(
            f"Tarea creada para el usuario: {user}"
        )

    def get_index(self):
        # CORRECCIÓN:
        # Antes se hacía int() directamente y con la entrada vacía o no
        # numérica el callback fallaba sin control. Ahora se valida y se
        # lanza un TaskError con un mensaje comprensible.
        raw_value = self.task_index.get().strip()

        if not raw_value:
            raise TaskError(
                "Ingrese o seleccione el índice de una tarea."
            )

        try:
            return int(raw_value)
        except ValueError:
            raise TaskError("El índice debe ser un número entero.")

    def complete_selected(self):
        try:
            user = self.current_user.get()
            index = self.get_index()
            result = complete_task(index, user)
        except TaskError as error:
            messagebox.showwarning("Operación no permitida", str(error))
            return
        except Exception as error:  # pragma: no cover - red de seguridad
            messagebox.showerror(
                "Error inesperado",
                f"{type(error).__name__}: {error}"
            )
            return

        self.refresh_tasks()
        self.status_text.set(result)

    def delete_selected(self):
        try:
            user = self.current_user.get()
            index = self.get_index()
            result = delete_task(index, user)
        except TaskError as error:
            messagebox.showwarning("Operación no permitida", str(error))
            return
        except Exception as error:  # pragma: no cover - red de seguridad
            messagebox.showerror(
                "Error inesperado",
                f"{type(error).__name__}: {error}"
            )
            return

        self.refresh_tasks()
        self.status_text.set(result)

    def on_task_selected(self, event=None):
        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(selected[0], "values")

        if values:
            self.task_index.set(values[0])

    def refresh_tasks(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        user = self.current_user.get()

        # CORRECCIÓN:
        # list_tasks(user) ahora filtra por propietario, por lo que la
        # tabla solo muestra las tareas del usuario activo.
        visible_tasks = list_tasks(user)

        for i, task in enumerate(visible_tasks):
            status = "Completada" if task["completed"] else "Pendiente"

            self.tree.insert(
                "",
                "end",
                values=(
                    i,
                    task["title"],
                    task["user"],
                    status
                )
            )

        self.status_text.set(
            f"Usuario actual: {user} | Tareas mostradas: {len(visible_tasks)}"
        )


def main():
    if not TK_AVAILABLE:
        raise RuntimeError(
            "Tkinter no está disponible en este entorno. "
            "Instale python3-tk para ejecutar la interfaz gráfica."
        )

    root = tk.Tk()
    TaskManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
