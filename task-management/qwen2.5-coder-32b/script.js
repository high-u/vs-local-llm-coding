document.addEventListener("DOMContentLoaded", () => {
  const taskInput = document.getElementById("taskInput");
  const addTaskButton = document.getElementById("addTaskButton");
  const filterSelect = document.getElementById("filterSelect");
  const sortSelect = document.getElementById("sortSelect");
  const taskList = document.getElementById("taskList");

  let tasks = loadTasks();

  // Event listeners
  addTaskButton.addEventListener("click", addTask);
  taskInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") addTask();
  });
  filterSelect.addEventListener("change", displayFilteredTasks);
  sortSelect.addEventListener("change", displaySortedTasks);

  // Initial load tasks
  displayTasks();

  function Task(content, scheduledDate, status = "incomplete") {
    this.content = content;
    this.scheduledDate = new Date(scheduledDate).toISOString().split("T")[0];
    this.status = status;
  }

  function saveTasks(tasks) {
    localStorage.setItem("tasks", JSON.stringify(tasks));
  }

  function loadTasks() {
    return JSON.parse(localStorage.getItem("tasks")) || [];
  }

  function addTask() {
    const content = taskInput.value.trim();
    if (!content) return;

    const scheduledDate = prompt(
      "Enter the scheduled completion date (YYYY-MM-DD):",
    ).trim();
    if (!scheduledDate) return;

    tasks.push(new Task(content, scheduledDate));
    saveTasks(tasks);
    displayTasks();
    taskInput.value = "";
  }

  function deleteTask(index) {
    tasks.splice(index, 1);
    saveTasks(tasks);
    displayTasks();
  }

  function updateStatus(index) {
    const currentStatus = tasks[index].status;
    tasks[index].status =
      currentStatus === "completed" ? "incomplete" : "completed";
    saveTasks(tasks);
    displayTasks();
  }

  function displayTasks() {
    taskList.innerHTML = "";

    let filteredTasks = [...tasks];

    if (filterSelect.value !== "all") {
      const filterValue = filterSelect.value;
      filteredTasks = tasks.filter(
        (task) =>
          task.status === filterValue ||
          (filterValue === "overdue" &&
            new Date(task.scheduledDate) <
              new Date().toISOString().split("T")[0]),
      );
    }

    if (sortSelect.value === "desc") {
      filteredTasks.sort(
        (a, b) => new Date(b.scheduledDate) - new Date(a.scheduledDate),
      );
    } else {
      filteredTasks.sort(
        (a, b) => new Date(a.scheduledDate) - new Date(b.scheduledDate),
      );
    }

    filteredTasks.forEach((task, index) => {
      const taskItem = document.createElement("div");
      taskItem.className = `task-item ${task.status} ${new Date(task.scheduledDate) < new Date().toISOString().split("T")[0] && task.status === "incomplete" ? "overdue" : ""}`;

      const taskContent = document.createElement("span");
      taskContent.textContent = `${task.content} - Due: ${task.scheduledDate}`;

      const buttonsContainer = document.createElement("div");

      const deleteButton = document.createElement("button");
      deleteButton.textContent = "Delete";
      deleteButton.addEventListener("click", () => deleteTask(index));

      const updateStatusButton = document.createElement("button");
      updateStatusButton.textContent =
        task.status === "completed" ? "Restart" : "Complete";
      updateStatusButton.addEventListener("click", () => updateStatus(index));

      buttonsContainer.appendChild(deleteButton);
      buttonsContainer.appendChild(updateStatusButton);

      taskItem.appendChild(taskContent);
      taskItem.appendChild(buttonsContainer);
      taskList.appendChild(taskItem);
    });
  }

  function displayFilteredTasks() {
    displayTasks();
  }

  function displaySortedTasks() {
    displayTasks();
  }
});
