document.addEventListener("DOMContentLoaded", () => {
  const taskForm = document.getElementById("task-form");
  const taskList = document.getElementById("task-list");
  const filterButtons = document.querySelectorAll(".filter-btn");

  let tasks = JSON.parse(localStorage.getItem("tasks")) || [];

  function saveTasks() {
    localStorage.setItem("tasks", JSON.stringify(tasks));
  }

  function loadTasks() {
    taskList.innerHTML = "";
    tasks.forEach((task) => {
      addTaskToDOM(task);
    });
  }

  function addTaskToDOM(task) {
    const li = document.createElement("li");
    li.dataset.id = task.id;

    const contentSpan = document.createElement("span");
    contentSpan.textContent = task.content;
    li.appendChild(contentSpan);

    const dateSpan = document.createElement("span");
    dateSpan.textContent = new Date(task.date).toLocaleDateString();
    li.appendChild(dateSpan);

    const statusSpan = document.createElement("span");
    statusSpan.classList.add("task-status", task.status);
    statusSpan.textContent =
      task.status.charAt(0).toUpperCase() + task.status.slice(1);
    li.appendChild(statusSpan);

    const deleteButton = document.createElement("button");
    deleteButton.classList.add("delete");
    deleteButton.textContent = "Delete";
    deleteButton.addEventListener("click", () => {
      tasks = tasks.filter((t) => t.id !== task.id);
      saveTasks();
      loadTasks();
    });
    li.appendChild(deleteButton);

    const updateStatusButton = document.createElement("button");
    updateStatusButton.classList.add("update-status");
    updateStatusButton.textContent =
      task.status === "completed" ? "Restart" : "Complete";
    updateStatusButton.addEventListener("click", () => {
      task.status = task.status === "completed" ? "incomplete" : "completed";
      saveTasks();
      loadTasks();
    });
    li.appendChild(updateStatusButton);

    taskList.appendChild(li);
  }

  function filterTasks(filter) {
    const filteredTasks = tasks.filter((task) => {
      if (filter === "all") return true;
      if (filter === "incomplete" || filter === "completed")
        return task.status === filter;
      if (filter === "overdue") return new Date(task.date) < new Date();
    });
    taskList.innerHTML = "";
    filteredTasks.forEach((task) => {
      addTaskToDOM(task);
    });
  }

  taskForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const content = document.getElementById("task-content").value;
    const date = document.getElementById("task-date").value;

    if (!content || !date) return;

    const task = {
      id: Date.now().toString(),
      content,
      date,
      status: "incomplete",
    };

    tasks.push(task);
    saveTasks();
    loadTasks();

    taskForm.reset();
  });

  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      document.querySelector(".filter-btn.active").classList.remove("active");
      button.classList.add("active");
      filterTasks(button.dataset.filter);
    });
  });

  loadTasks();
});
