Implement a web application based on the following requirements.

```markdown
# Task management web application

## Overview

Implement a web application for managing daily work tasks by individuals.

## Functional requirements

### Task information

- Task content
- Scheduled completion date
- Status
    - Incomplete
    - Completed

### Data management

- Data persistence
- Data loading
    - When the application is loaded
    - When data is saved
- Data saving
    - When a task is registered
    - When a task is deleted
    - When the task status is updated

### Task operations

- Registration
- Deletion
- Status update
    - Mark a task as completed.
    - Restart a task (mark it as incomplete).

### Displaying tasks

- Task list
    - Filter
        - All
        - Incomplete
        - Completed
        - Overdue
    - Sort
        - Scheduled completion date (ascending, descending)

## User interface requirements

### Color scheme

- Monotone base
- Matte texture

### Style

- Contemporary style
- Flat design

### Layout

- Liquid and responsive design
- Grid layout
- Grid-based spacing

### Displaying task status

- Visually distinguish different states.

### Constraints

- Do not change the status by turning a checkbox on or off.
- Do not show the completed state with a strikethrough.
- Do not use heading tags such as `<h1>`, `<h2>`, `<h3>`, etc., as various titles are not necessary in this application.

## Architectural requirements

### Programming language

- HTML
- JavaScript
- CSS

### Coding policy

- Emphasize maintainability.

### Data persistence

- localStorage
- JSON

### File structure

- index.html
- script.js
- styles.css

### Constraints

- Do not use external libraries.
```

Implement a production-ready application that meets the requirements, not a sample application.
When resolving questions or making decisions, use the user experience as a guide for implementation.
