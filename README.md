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