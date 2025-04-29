// script.js
document.addEventListener("DOMContentLoaded", () => {
  let tasks = [];
  let currentFilter = "all";
  let currentSort = "date_asc";

  const loadTasks = () => {
    const saved = localStorage.getItem("tasks");
    return saved ? JSON.parse(saved) : [];
  };

  const saveTasks = () => {
    localStorage.setItem("tasks", JSON.stringify(tasks));
  };

  const setupEventListeners = () => {
    document
      .getElementById("task-form")
      .addEventListener("submit", handleAddTask);
    document.querySelectorAll(".filter-controls button").forEach((button) => {
      button.addEventListener("click", () => {
        currentFilter = button.dataset.filter;
        renderTasks();
      });
    });

    document.querySelectorAll(".sort-controls button").forEach((button) => {
      button.addEventListener("click", () => {
        currentSort = button.dataset.sort;
        renderTasks();
      });
    });
  };

  const handleAddTask = (e) => {
    e.preventDefault();
    const contentInput = document.getElementById("task-content");
    const dueDateInput = document.getElementById("due-date");
    const content = contentInput.value.trim();
    const dueDateStr = dueDateInput.value;

    if (!content || !dueDateStr) return;

    const newTask = {
      id: Date.now(),
      content,
      dueDate: dueDateStr,
      status: "incomplete",
    };

    tasks.push(newTask);
    saveTasks();
    renderTasks();

    contentInput.value = "";
    dueDateInput.value = "";
  };

  const renderTasks = () => {
    const container = document.getElementById("task-list");
    container.innerHTML = "";

    let filtered = [...tasks];

    if (currentFilter === "incomplete") {
      filtered = tasks.filter((task) => task.status === "incomplete");
    } else if (currentFilter === "completed") {
      filtered = tasks.filter((task) => task.status === "completed");
    } else if (currentFilter === "overdue") {
      const today = new Date();
      filtered = tasks.filter((task) => {
        const dueDate = new Date(task.dueDate);
        return task.status === "incomplete" && dueDate < today;
      });
    }

    // Apply sorting
    if (currentSort === "date_asc") {
      filtered.sort((a, b) => new Date(a.dueDate) - new Date(b.dueDate));
    } else if (currentSort === "date_desc") {
      filtered.sort((a, b) => new Date(b.dueDate) - new Date(a.dueDate));
    }

    // Render each task
    filtered.forEach((task) => {
      const taskEl = document.createElement("div");
      taskEl.className = "task-card";
      if (task.status === "completed") {
        taskEl.classList.add("completed");
      }

      const contentEl = document.createElement("div");
      contentEl.textContent = task.content;
      contentEl.classList.add("task-content");

      const dueDateEl = document.createElement("div");
      dueDateEl.textContent = `Due: ${task.dueDate}`;
      dueDateEl.classList.add("due-date");

      const statusButtons = document.createElement("div");
      statusButtons.className = "status-buttons";

      if (task.status === "incomplete") {
        const completeBtn = document.createElement("button");
        completeBtn.textContent = "Complete";
        completeBtn.addEventListener("click", () => {
          task.status = "completed";
          saveTasks();
          renderTasks();
        });
        statusButtons.appendChild(completeBtn);
      } else {
        const restartBtn = document.createElement("button");
        restartBtn.textContent = "Restart";
        restartBtn.addEventListener("click", () => {
          task.status = "incomplete";
          saveTasks();
          renderTasks();
        });
        statusButtons.appendChild(restartBtn);
      }

      const deleteBtn = document.createElement("button");
      deleteBtn.textContent = "Delete";
      deleteBtn.className = "delete-btn";
      deleteBtn.addEventListener("click", () => {
        tasks = tasks.filter((t) => t.id !== task.id);
        saveTasks();
        renderTasks();
      });

      taskEl.appendChild(contentEl);
      taskEl.appendChild(dueDateEl);
      taskEl.appendChild(statusButtons);
      taskEl.appendChild(deleteBtn);

      container.appendChild(taskEl);
    });
  };

  tasks = loadTasks();
  setupEventListeners();
  renderTasks();
});
