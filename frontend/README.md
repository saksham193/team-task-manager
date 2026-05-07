# Team Task Manager Frontend

A React frontend for the Team Task Manager application with JWT authentication and modern UI.

## Features

- **User Authentication**: Login and registration with JWT tokens
- **Dashboard**: Statistics overview with team and task counts
- **Team Management**: Create teams and manage team members
- **Task Management**: Kanban-style task board with drag-and-drop functionality
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean, minimal design with Tailwind CSS

## Tech Stack

- **React 18**: Modern React with hooks
- **React Router**: Client-side routing
- **Axios**: HTTP client for API calls
- **Tailwind CSS**: Utility-first CSS framework
- **Context API**: State management for authentication

## Getting Started

### Prerequisites

- Node.js 16+
- npm or yarn
- Backend server running (see backend README)

### Installation

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

4. **Open your browser:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000 (make sure it's running)

## Project Structure

```
frontend/
├── public/
│   └── index.html          # HTML template
├── src/
│   ├── components/
│   │   └── Navbar.jsx      # Navigation component
│   ├── context/
│   │   └── AuthContext.js  # Authentication context
│   ├── pages/
│   │   ├── Login.jsx       # Login page
│   │   ├── Register.jsx    # Registration page
│   │   ├── Dashboard.jsx   # Dashboard with stats
│   │   ├── Teams.jsx       # Team management
│   │   └── Tasks.jsx       # Task management (Kanban)
│   ├── services/
│   │   └── api.js          # API service configuration
│   ├── App.js              # Main app component
│   ├── App.css             # Global styles
│   └── index.js            # App entry point
├── package.json            # Dependencies and scripts
├── tailwind.config.js      # Tailwind configuration
└── postcss.config.js       # PostCSS configuration
```

## API Integration

The frontend connects to the backend API at `http://127.0.0.1:8000`. The API service automatically:

- Adds JWT tokens to authenticated requests
- Handles authentication errors
- Provides consistent error handling

### Key API Endpoints Used

- `POST /register` - User registration
- `POST /login` - User authentication
- `GET /dashboard/stats` - Dashboard statistics
- `GET /teams/` - List user's teams
- `POST /teams/` - Create new team
- `GET /tasks` - List user's tasks
- `POST /tasks` - Create new task
- `PATCH /tasks/{id}` - Update task status

## Authentication Flow

1. **Registration**: Users create accounts via the Register page
2. **Login**: Users authenticate and receive JWT tokens
3. **Token Storage**: Tokens are stored in localStorage
4. **Auto-login**: Users stay logged in across browser sessions
5. **Logout**: Tokens are cleared from storage

## Features Overview

### Dashboard
- Displays total teams, tasks, completed tasks, and pending tasks
- Quick action buttons to navigate to Teams and Tasks pages
- Real-time statistics from the backend

### Team Management
- List all teams the user belongs to
- Create new teams with custom names
- View team member counts
- Add team members (UI ready, backend integration complete)

### Task Management
- Kanban board with three columns: Todo, In Progress, Completed
- Create new tasks with title, description, priority, and team assignment
- Move tasks between status columns
- Priority indicators (High, Medium, Low)
- Team-based task filtering

### Navigation
- Responsive navbar with logout functionality
- Protected routes that redirect to login when not authenticated
- Clean navigation between all major sections

## Styling

The application uses Tailwind CSS for styling with:
- Clean, minimal design
- Consistent color scheme
- Responsive grid layouts
- Hover states and transitions
- Form styling with focus states

## Development

### Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm eject` - Eject from Create React App

### Code Style

- Functional components with hooks
- Context API for state management
- Axios for API calls
- Tailwind CSS for styling
- Clean, readable component structure

## Production Deployment

### Vercel/Netlify Deployment

1. **Build the app:**
   ```bash
   npm run build
   ```

2. **Deploy to Vercel/Netlify:**
   - Connect your GitHub repository
   - Set build command: `npm run build`
   - Set publish directory: `build`

3. **Environment Variables:**
   - Update API base URL to production backend URL
   - Example: `REACT_APP_API_URL=https://your-backend-url.com`

### Backend URL Configuration

Update the API base URL in `src/services/api.js` for production:

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';
```

## Testing

### Manual Testing Checklist

- [ ] User registration works
- [ ] User login persists across browser refresh
- [ ] Dashboard shows correct statistics
- [ ] Team creation works
- [ ] Task creation works
- [ ] Task status updates work
- [ ] Kanban board displays correctly
- [ ] Responsive design works on mobile
- [ ] Logout clears authentication

### API Testing

Test all endpoints with the backend:
- Authentication endpoints
- Dashboard statistics
- Team CRUD operations
- Task CRUD operations

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Follow the existing code style
2. Use functional components and hooks
3. Add proper error handling
4. Test manually before committing
5. Update documentation as needed

## License

This project is licensed under the MIT License.