// script.js
document.addEventListener("DOMContentLoaded", () => {
  const taskForm = document.getElementById("task-form");
  const taskList = document.getElementById("task-list");
  const filterSelect = document.getElementById("filter-select");
  const sortSelect = document.getElementById("sort-select");

  let tasks = [];

  // Load tasks from localStorage
  function loadTasks() {
    const storedTasks = localStorage.getItem("tasks");
    if (storedTasks) {
      tasks = JSON.parse(storedTasks);
    }
  }

  // Save tasks to localStorage
  function saveTasks() {
    localStorage.setItem("tasks", JSON.stringify(tasks));
  }

  // Render tasks based on filter and sort
  function renderTasks() {
    taskList.innerHTML = "";
    const filter = filterSelect.value;
    const sort = sortSelect.value;

    let filteredTasks = [...tasks];

    // Apply filters
    if (filter === "incomplete") {
      filteredTasks = tasks.filter((task) => task.status === "Incomplete");
    } else if (filter === "completed") {
      filteredTasks = tasks.filter((task) => task.status === "Completed");
    } else if (filter === "overdue") {
      const today = new Date().toISOString().split("T")[0];
      filteredTasks = tasks.filter(
        (task) => task.dueDate < today && task.status !== "Completed",
      );
    }

    // Apply sorting
    filteredTasks.sort((a, b) => {
      if (sort === "asc") {
        return new Date(a.dueDate) - new Date(b.dueDate);
      } else {
        return new Date(b.dueDate) - new Date(a.dueDate);
      }
    });

    // Create task elements
    filteredTasks.forEach((task) => {
      const taskDiv = document.createElement("div");
      taskDiv.className = "task";
      if (task.status === "Completed") {
        taskDiv.classList.add("completed");
      }

      const content = document.createElement("span");
      content.textContent = task.content;
      taskDiv.appendChild(content);

      const buttons = document.createElement("div");
      buttons.className = "status-buttons";

      // Status toggle buttons
      if (task.status === "Incomplete") {
        const completeBtn = document.createElement("button");
        completeBtn.textContent = "Mark as Completed";
        completeBtn.className = "status-button completed-btn";
        completeBtn.onclick = () => updateTaskStatus(task.id, "Completed");
        buttons.appendChild(completeBtn);
      } else {
        const restartBtn = document.createElement("button");
        restartBtn.textContent = "Restart Task";
        restartBtn.className = "status-button restart-btn";
        restartBtn.onclick = () => updateTaskStatus(task.id, "Incomplete");
        buttons.appendChild(restartBtn);
      }

      // Delete button
      const deleteBtn = document.createElement("button");
      deleteBtn.textContent = "Delete";
      deleteBtn.className = "status-button delete-btn";
      deleteBtn.onclick = () => deleteTask(task.id);
      buttons.appendChild(deleteBtn);

      taskDiv.appendChild(buttons);
      taskList.appendChild(taskDiv);
    });
  }

  // Add new task
  taskForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const content = document.getElementById("task-content").value.trim();
    const dueDate = document.getElementById("task-date").value;

    if (content && dueDate) {
      const newTask = {
        id: Date.now(),
        content,
        dueDate,
        status: "Incomplete",
      };
      tasks.push(newTask);
      saveTasks();
      renderTasks();
      taskForm.reset();
    }
  });

  // Delete a task
  function deleteTask(id) {
    tasks = tasks.filter((task) => task.id !== id);
    saveTasks();
    renderTasks();
  }

  // Update task status
  function updateTaskStatus(id, newStatus) {
    tasks = tasks.map((task) =>
      task.id === id ? { ...task, status: newStatus } : task,
    );
    saveTasks();
    renderTasks();
  }

  // Event listeners for filter and sort changes
  filterSelect.addEventListener("change", renderTasks);
  sortSelect.addEventListener("change", renderTasks);

  // Initial load
  loadTasks();
  renderTasks();
});
