import tkinter as tk
from tkinter import ttk, messagebox


tasks = []


def add_task(title, user):
    tasks.append({
        "title": title,
        "user": user,
        "completed": False
    })


def list_tasks(user):
    return tasks


def complete_task(index, user):
    # Usa la lista visible para el usuario actual.
    # Cuando list_tasks() sea corregida, esta operación también
    # quedará limitada a sus propias tareas.
    user_tasks = list_tasks(user)
    user_tasks[index]["completed"] = True
    return "Tarea completada"


def delete_task(index, user):
    # Usa la lista visible para el usuario actual.
    user_tasks = list_tasks(user)
    user_tasks.pop(index)
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
        title = self.task_title.get()
        user = self.current_user.get()

        add_task(title, user)

        self.task_title.set("")
        self.refresh_tasks()

        self.status_text.set(
            f"Tarea creada para el usuario: {user}"
        )

    def get_index(self):
        return int(self.task_index.get())

    def complete_selected(self):
        user = self.current_user.get()
        index = self.get_index()

        try:
            result = complete_task(index, user)
            self.refresh_tasks()
            self.status_text.set(result)
        except Exception as error:
            messagebox.showerror(
                "Error durante la operación",
                f"{type(error).__name__}: {error}"
            )

    def delete_selected(self):
        user = self.current_user.get()
        index = self.get_index()

        try:
            result = delete_task(index, user)
            self.refresh_tasks()
            self.status_text.set(result)
        except Exception as error:
            messagebox.showerror(
                "Error durante la operación",
                f"{type(error).__name__}: {error}"
            )

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

        # ========================================================
        # PROBLEMA INTENCIONAL DEL TALLER
        # ========================================================
        # La interfaz ya conoce el usuario actual, pero la función
        # list_tasks() todavía devuelve todas las tareas.
        # El estudiante debe corregir esta parte para que solo se
        # muestren las tareas del usuario seleccionado.
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
    root = tk.Tk()
    TaskManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
