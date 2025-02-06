# A task management tool, inspired by Mark Forster's Autofocus (if I'm not misremembering)

# xParrot

Task management system with MySQL backend.

## Quick Start

1. Install dependencies:
```bash
# Install MySQL
brew install mysql
brew services start mysql

# Install Python packages
pip install -r requirements.txt
```

2. Configure environment:
```bash
# Copy example config
cp .env.example .env

# Edit .env with your MySQL credentials
# Default values should work for local development
```

3. Initialize database:
```bash
python -m xparrot_package.xparrot.migrate
```

That's it! You're ready to use xParrot.

## Basic Operations

```python
from xparrot_package.xparrot.xparrot_api import xParrotAPI, xPF

# Initialize API
api = xParrotAPI()

# Create a task
task = api.create_task(
    name="My first task",
    notes="This is a task description",
    status=""  # Empty status means unstarted
)

# List unstarted tasks
tasks = api.fetch(xPF.unstarted())

# Mark task as started
api.update_task(task.id, status="Started")

# Mark task as done
api.update_task(task.id, status="Done")

# Delete task
api.delete_task(task.id)