# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python Discord webhook service that monitors Hoyoverse game updates and sends notifications. It tracks game packages, maintenance windows, and preload availability for multiple Hoyoverse titles (Genshin Impact, Honkai: Star Rail, Zenless Zone Zero, Honkai Impact 3rd) across different regions.

## Development Commands

### Running the Application
- **Main server**: `python run.py` (starts FastAPI server on port 8092 with integrated scheduler)
- **Test script**: `python test.py`

### Code Quality
- **Lint**: `ruff check` (comprehensive linting with custom rules)
- **Format**: `ruff format` (code formatting)
- **Type check**: `pyright` (type checking with standard mode)

### Package Management
- **Install dependencies**: `uv sync` (uses uv.lock for dependency resolution)
- **Update dependencies**: `uv update`

## Architecture Overview

### Core Components

**FastAPI Web Service (`hun/api.py`)**
- Web interface for webhook registration at `hun/index.html`
- REST endpoints: `/regions`, `/webhooks`, `/webhooks/test`
- Database initialization with Tortoise ORM (SQLite)
- aiohttp session management in lifespan
- APScheduler integration for automated game monitoring (runs every 10 minutes)

**Game Monitoring System (`hun/scheduler.py`)**
- Scheduled task that runs every 10 minutes via APScheduler
- Fetches game packages from Hoyoverse APIs (global & CN)
- Tracks version changes using semver comparison
- Monitors maintenance status via game-specific endpoints
- Sends Discord webhooks for updates/maintenance events
- Handles both regular packages and Sophon pre-downloads

**Database Models (`hun/models.py`)**
- `GamePackage`: Tracks game versions and preload status
- `GameMaint`: Maintenance notification state tracking
- `Webhook`: Discord webhook configurations per region

**Game Data Management (`hun/utils.py`)**
- API integration for fetching game packages and branches
- Maintenance status checking with custom headers
- Error handling and logging for external API calls

### Data Flow

1. **Game Package Monitoring**: APScheduler → `hun/scheduler.py` → Hoyoverse APIs → version comparison → Discord webhooks
2. **Maintenance Tracking**: Game-specific endpoints → maintenance status → notification state machine
3. **Webhook Management**: Web UI → FastAPI → database → Discord API

### Configuration Structure

**Game Regions (`hun/constants.py`)**
- Enum-based region definitions with unique game IDs
- Separate API endpoints for global vs CN regions
- Game-specific maintenance endpoints and business IDs
- Region names and icons mapping

**Settings & Dependencies**
- `pyproject.toml`: Python 3.11+, async dependencies (aiohttp, FastAPI, Tortoise ORM, APScheduler)
- `ruff.toml`: Comprehensive linting rules, Google docstring convention
- `pm2.json`: Process manager configuration for production deployment

## Key Patterns

### Async Architecture
- All database operations use Tortoise ORM async methods
- HTTP requests handled with aiohttp ClientSession
- Proper resource cleanup in FastAPI lifespan

### Error Handling
- Graceful fallbacks for API failures
- Webhook deletion on delivery failure
- Comprehensive logging with loguru

### Version Management
- Uses semver library for proper version comparison
- Prevents duplicate notifications via database state tracking
- Handles both main and preload package versions

## Testing Notes

- `test.py` file exists but is excluded from linting (`ruff.toml`)
- No formal test framework currently configured
- Manual testing via `/webhooks/test` endpoint