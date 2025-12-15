# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SOSLince is a multi-platform SOS emergency response application with three main components:

- **Backend (`back/`)**: Django REST API with PostgreSQL database
- **Frontend (`front/`)**: Vue 3 web application with Vuetify UI (staff dashboard)
- **Mobile (`movil/`)**: Capacitor-based mobile app for customers (Vue 3 + Vuetify)

The system manages Staff and Customer users, with customers sending SOS alerts that include location data from the mobile app, while staff monitor and respond via the web dashboard.

## Development Commands

### Backend (Django)
```bash
cd back/
python manage.py runserver                    # Start dev server (default: 8000)
python manage.py migrate                      # Apply database migrations
python manage.py makemigrations               # Create new migrations
python manage.py test                         # Run tests
```

### Frontend (Web)
```bash
cd front/
npm install                                   # Install dependencies
npm run dev                                   # Start dev server (port 3333)
npm run build                                 # Build for production (runs vue-tsc first)
npm run lint                                  # Lint and fix files
```

### Mobile (Capacitor)
```bash
cd movil/
npm install                                   # Install dependencies
npm run dev                                   # Start dev server (port 3000)
npm run build                                 # Build web assets
npx cap sync                                  # Sync web assets to native platforms
npx cap run android                           # Build and run on Android
npx cap run ios                               # Build and run on iOS
```

## Architecture

### Backend Structure (`back/`)
- **Two Django apps**: `core/` (main business logic) and `api/` (mobile-specific endpoints)
- **API versioning**: All endpoints prefixed with `/api/1.0/`
- **URL structure**:
  - `/api/1.0/core/` - Staff-facing endpoints (customer management, SOS monitoring)
  - `/api/1.0/auth/` - Authentication via djoser (JWT tokens)
  - `/api/1.0/` - Mobile app endpoints
- **ViewSets pattern**: `core/viewsets/` and `api/viewsets/` contain DRF ModelViewSets
- **Serializers**: Located in `core/serializers/` - handle nested Customer data within User model
- **DataTables integration**: `rest_framework_datatables` for server-side pagination/filtering

### Frontend Structure (`front/src/`)
- **Module-based routing**: Each feature in `modules/` has its own `router/`, `pages/`, `components/`, `composables/`, and `stores/`
  - `modules/auth/` - Login, password recovery
  - `modules/core/` - Dashboard, customer management, staff management
- **Custom `exp*` components** (`components/exp*/`): Reusable UI components wrapping Vuetify
  - `expDataTable` - Server-side paginated data table with DataTables protocol
  - `expModalForm` - Modal dialog for CRUD forms
  - `expDynamicForm` - Dynamic form generation
- **Key composables** (`composables/`):
  - `useCrud.ts` - Generic CRUD operations with loading states
  - `useDataTable.ts` - DataTables-compatible API requests
  - `useAuth.ts` (in auth module) - Authentication logic
- **State management**: Pinia stores with encrypted localStorage persistence (`stores/auth.ts`)
- **Path alias**: `@/` maps to `src/`

### Mobile Structure (`movil/src/`)
- Mirrors frontend structure but simplified for customer-facing mobile experience
- **Background geolocation**: `@transistorsoft/capacitor-background-geolocation` for continuous location tracking
- **App ID**: `com.lincesr.sos`

## API Conventions

### DataTables Protocol
The frontend `expDataTable` component sends requests compatible with jQuery DataTables:
```
GET /api/1.0/core/customer/?format=datatables&draw=0&length=10&start=0&search[value]=...
```

### CRUD Endpoints
Standard DRF ViewSet patterns:
- `GET /endpoint/` - List (with DataTables params)
- `GET /endpoint/{id}/` - Retrieve
- `POST /endpoint/` - Create
- `PATCH /endpoint/{id}/` - Update
- `DELETE /endpoint/{id}/` - Delete
- Custom actions use `@action` decorator (e.g., `/endpoint/list_sos/`, `/endpoint/close_sos/`)

## Environment Variables

Backend (`back/.env`):
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` - PostgreSQL config
- `REDIS_HOST`, `REDIS_PORT` - Redis for channel layers
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` - Email config

## Key Patterns

### Adding a New Feature
1. **Backend**: Create model in `core/models.py`, serializer in `core/serializers/`, viewset in `core/viewsets/`, register in `core/urls.py`
2. **Frontend**: Create page in `modules/core/pages/`, add route to `modules/core/router/`, use `useCrud` composable for API calls

### Customer Data Flow
- Customers are Django Users with `is_staff=False`
- Extended profile data stored in `Customer` model (one-to-one with User)
- `CustomerSerializer` handles nested creation/update of both User and Customer models