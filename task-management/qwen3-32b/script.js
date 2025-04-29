document.addEventListener("DOMContentLoaded", () => {
  let tasks = [];

  // Load tasks from localStorage
  const savedTasks = localStorage.getItem("tasks");
  if (savedTasks) {
    tasks = JSON.parse(savedTasks);
  }

  function saveTasks() {
    localStorage.setItem("tasks", JSON.stringify(tasks));
  }

  function getFilteredSortedTasks(filter, sortOption) {
    let filtered = [...tasks];

    // Apply filters
    switch (filter) {
      case "incomplete":
        filtered = tasks.filter((task) => task.status === "Incomplete");
        break;
      case "completed":
        filtered = tasks.filter((task) => task.status === "Completed");
        break;
      case "overdue":
        const today = new Date();
        filtered = tasks.filter((task) => {
          const dueDate = new Date(task.dueDate);
          return dueDate < today && task.status !== "Completed";
        });
        break;
    }

    // Apply sorting
    if (sortOption === "asc") {
      filtered.sort((a, b) => new Date(a.dueDate) - new Date(b.dueDate));
    } else if (sortOption === "desc") {
      filtered.sort((a, b) => new Date(b.dueDate) - new Date(a.dueDate));
    }

    return filtered;
  }

  function renderTaskList() {
    const filter = document.getElementById("task-filter").value;
    const sortOption = document.getElementById("task-sort").value;

    const filteredTasks = getFilteredSortedTasks(filter, sortOption);
    const taskListEl = document.getElementById("task-list");
    taskListEl.innerHTML = "";

    if (filteredTasks.length === 0) {
      const noTasksMsg = document.createElement("div");
      noTasksMsg.textContent = "No tasks found.";
      noTasksMsg.style.textAlign = "center";
      taskListEl.appendChild(noTasksMsg);
      return;
    }

    filteredTasks.forEach((task) => {
      const card = document.createElement("div");
      card.className = "task-card";

      const contentEl = document.createElement("div");
      contentEl.textContent = task.content;

      const dueDateEl = document.createElement("div");
      dueDateEl.textContent = `Due: ${task.dueDate}`;

      const statusLabel = document.createElement("span");
      statusLabel.className = "status-label";
      if (task.status === "Incomplete") {
        statusLabel.classList.add("incomplete");
        statusLabel.textContent = "Incomplete";
      } else {
        statusLabel.classList.add("completed");
        statusLabel.textContent = "Completed";
      }

      const buttonsDiv = document.createElement("div");
      buttonsDiv.className = "task-buttons";

      // Status toggle button
      const statusBtn = document.createElement("button");
      statusBtn.className = "status-btn";
      let buttonText;
      if (task.status === "Incomplete") {
        buttonText = "Mark Complete";
      } else {
        buttonText = "Restart Task";
      }
      statusBtn.textContent = buttonText;

      // Delete button
      const deleteBtn = document.createElement("button");
      deleteBtn.className = "delete-btn";
      deleteBtn.textContent = "Delete";

      card.appendChild(contentEl);
      card.appendChild(dueDateEl);
      card.appendChild(statusLabel);

      buttonsDiv.appendChild(statusBtn);
      buttonsDiv.appendChild(deleteBtn);
      card.appendChild(buttonsDiv);

      // Event handlers
      statusBtn.addEventListener("click", () => {
        task.status = task.status === "Incomplete" ? "Completed" : "Incomplete";
        saveTasks();
        renderTaskList();
      });

      deleteBtn.addEventListener("click", () => {
        tasks = tasks.filter((t) => t.id !== task.id);
        saveTasks();
        renderTaskList();
      });

      taskListEl.appendChild(card);
    });
  }

  // Form submission
  document.getElementById("task-form").addEventListener("submit", (e) => {
    e.preventDefault();

    const contentInput = document.getElementById("task-content");
    const dueDateInput = document.getElementById("due-date");

    const content = contentInput.value.trim();
    const dueDate = dueDateInput.value;

    if (!content || !dueDate) return;

    tasks.push({
      id: Date.now(),
      content,
      dueDate,
      status: "Incomplete",
    });

    saveTasks();
    renderTaskList();

    // Reset form
    contentInput.value = "";
    dueDateInput.value = "";
  });

  // Filter and sort handlers
  document
    .getElementById("task-filter")
    .addEventListener("change", renderTaskList);
  document
    .getElementById("task-sort")
    .addEventListener("change", renderTaskList);

  // Initial render
  renderTaskList();
});
