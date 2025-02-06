"""Test the xParrot MySQL implementation."""
import os
import pytest
from datetime import datetime, timedelta
from xparrot_package.xparrot.database import init_db, Task, Project, Subproject, get_db
from xparrot_package.xparrot.xparrot_api import xParrotAPI, xPF

# Setup test database
os.environ['MYSQL_DATABASE'] = 'xparrot_test'

@pytest.fixture(scope="session")
def api():
    """Create test database and return API instance."""
    # Initialize database
    init_db()
    return xParrotAPI()

def test_create_task(api):
    """Test task creation."""
    task = api.create_task(
        name="Test Task",
        notes="This is a test task",
        status="",
        link="https://example.com"
    )
    assert task.name == "Test Task"
    assert task.notes == "This is a test task"
    assert task.status == ""
    assert task.link == "https://example.com"

def test_fetch_unstarted_tasks(api):
    """Test fetching unstarted tasks."""
    # Create an unstarted task
    api.create_task(name="Unstarted Task", status="")
    
    # Fetch unstarted tasks
    tasks = api.fetch(xPF.unstarted())
    assert len(tasks) > 0
    assert any(task.name == "Unstarted Task" for task in tasks)

def test_update_task(api):
    """Test task update."""
    # Create a task
    task = api.create_task(name="Update Test Task")
    
    # Update the task
    updated_task = api.update_task(
        task.id,
        status="Started",
        notes="Updated notes"
    )
    
    assert updated_task.status == "Started"
    assert updated_task.notes == "Updated notes"

def test_endangered_tasks(api):
    """Test endangered tasks detection."""
    # Create a task with old creation date
    task = api.create_task(name="Old Task")
    task.created_time = datetime.utcnow() - timedelta(days=6)
    api.db.commit()
    
    # Fetch endangered tasks
    tasks = api.fetch(xPF.endangered())
    assert len(tasks) > 0
    assert any(t.name == "Old Task" for t in tasks)

def test_delete_task(api):
    """Test task deletion."""
    # Create a task
    task = api.create_task(name="Task to Delete")
    
    # Delete the task
    result = api.delete_task(task.id)
    assert result is True
    
    # Verify task is deleted
    deleted_task = api.task(id=task.id)
    assert deleted_task is None
