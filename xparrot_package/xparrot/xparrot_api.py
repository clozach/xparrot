# -*- coding: utf-8 -*-
"""
xParrotAPI Class Instance
***********************

>>> api = xParrotAPI()
>>> api.fetch(started())
[{'id': 1, 'name': 'Mess with Flutter', 'notes': 'How much effort is needed...', 'status': 'Started'}]

Task management system using MySQL as the backend database.
"""
from datetime import datetime, timedelta
from sqlalchemy import or_
from sqlalchemy.orm import Session
from .database import get_db, Task, Project, Subproject

# Configuration constants
days_til_endangered = 5
days_til_stale = 7
hours_til_expiry = 18

class xParrotAPI:
    def __init__(self):
        self.db = next(get_db())
    
    def _apply_filter(self, query, filter_string):
        """Convert filter string to SQLAlchemy filter"""
        if not filter_string:
            return query
            
        if "Status=''" in filter_string:
            return query.filter(Task.status == '')
        elif "Status='Started'" in filter_string:
            return query.filter(Task.status == 'Started')
        elif "Status='Endangered'" in filter_string:
            return query.filter(Task.status == 'Endangered')
        
        return query

    def fetch(self, filter_string, remote=None):
        """Fetch tasks based on filter"""
        query = self.db.query(Task)
        filtered_query = self._apply_filter(query, filter_string)
        return filtered_query.all()

    def fetch_projects(self, filter_string=''):
        """Fetch projects"""
        return self.db.query(Project).all()

    def fetch_subprojects(self, filter_string=''):
        """Fetch subprojects"""
        return self.db.query(Subproject).all()

    def task(self, id=None, name=None):
        """Get task by ID or name"""
        if id is None and name is None:
            print('No task identifier given.')
            return None
            
        query = self.db.query(Task)
        if id is not None:
            return query.filter(Task.id == id).first()
        return query.filter(Task.name == name).first()

    def create_task(self, name, notes=None, status='', link=None):
        """Create a new task"""
        task = Task(
            name=name,
            notes=notes,
            status=status,
            link=link
        )
        self.db.add(task)
        self.db.commit()
        return task

    def update_task(self, task_id, **fields):
        """Update task fields"""
        task = self.task(id=task_id)
        if task:
            for key, value in fields.items():
                setattr(task, key, value)
            self.db.commit()
        return task

    def delete_task(self, task_id):
        """Delete a task"""
        task = self.task(id=task_id)
        if task:
            self.db.delete(task)
            self.db.commit()
        return True

class xPF:
    """xParrot Filters"""
    
    @staticmethod
    def unstarted():
        return "Status=''"

    @classmethod
    def endangered(cls, dte=days_til_endangered):
        """Tasks that will be auto-archived if no action is taken soon"""
        return f"AND(Status='',{cls.older_than('created_time', dte)})"

    @staticmethod
    def by_name(name):
        return f"Name='{name}'"

    @staticmethod
    def started():
        return "Status='Started'"

    @staticmethod
    def older_than(field, days):
        """Tasks older than specified days"""
        return f"{field}<'{(datetime.utcnow() - timedelta(days=days)).isoformat()}'"

    @staticmethod
    def done():
        return "Status='Done'"

    @staticmethod
    def auto_archived():
        return "Status='Auto-archived'"

    @classmethod
    def stale(cls, dts=days_til_stale):
        """Tasks ready to have the `Auto-archived` tag and `Auto-archive Date` applied"""
        return f"AND(OR(Status='',Status='Endangered'),{cls.older_than('created_time', dts)})"

    @staticmethod
    def expired():
        """Tasks needing to be archived"""
        return "OR(Status='Done',Status='Auto-archived')"

class xPPropertyJSON:
    """Task property updates"""
    
    @staticmethod
    def status_endangered():
        return {'status': 'Endangered'}

    @staticmethod
    def status_auto_archived():
        return {'status': 'Auto-Archived'}
