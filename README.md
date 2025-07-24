# Awesome Babushka

Awesome Babushka is a next-generation, full-stack social platform engineered to foster authentic conversations and meaningful connections. Leveraging a modern technology stack—Bun, Vite, React, TailwindCSS on the frontend, and FastAPI with MongoDB on the backend—it delivers a seamless, adaptive, and secure user experience.

## Features

- 🧑‍💻 **Modern UI**: Responsive, accessible, and visually appealing interface built with React, TailwindCSS, and Neumorphism-inspired components.
- 🔒 **Robust Authentication**: Secure registration, login, JWT-based session management, and email verification.
- 🗨️ **Interactive Social Feed**: Create posts, like, comment, and engage with the community in real time.
- 🏠 **Personalized Home**: Dynamic layouts, animated UI elements, and user-focused content areas.
- ⚡ **High Performance**: Fast development and deployment powered by Bun, Vite, FastAPI, and MongoDB.
- 📧 **Integrated Email**: Configurable email verification and notifications for enhanced security and engagement.

## Getting Started

### Prerequisites

- [Bun](https://bun.sh/) (>=1.0.0)
- Node.js (>=18) *(if not using Bun for all tooling)*
- Python (>=3.10)
- MongoDB (local or remote)
- *Optional*: Docker for containerized development

### Installation

#### 1. Clone the repository

```bash
git clone https://github.com/your-org/awesome-babushka.git
cd awesome-babushka/ui-dev
```

#### 2. Install frontend dependencies

```bash
cd ui
bun install
```

#### 3. Install backend dependencies

```bash
cd ../services/auth-service
pip install -r requirements.txt
```

#### 4. Configure environment variables

Copy `.env.example` to `.env` in `services/auth-service` and update as needed.

#### 5. Start the backend

```bash
cd services/auth-service/src
uvicorn auth_service.main:api --reload
```

#### 6. Start the frontend

```bash
cd ui
bun run dev
```

Visit [http://localhost:5173](http://localhost:5173) to access the application.

## Usage

- Register a new account or sign in.
- Explore the social feed, create posts, and interact with the community.
- Experience a dynamic, animated, and user-friendly platform.

## Development

- **Linting:**  
  - Frontend: `bun run lint`
  - Backend: `pre-commit run --all-files`
- **Formatting:**  
  - Frontend: ESLint and Prettier
  - Backend: Black, isort, and flake8
- **Testing:**  
  - *(Add your test instructions here if available)*

## Contributing

We welcome contributions from the community! Please open issues or submit pull requests for new features, bug fixes, or suggestions.

1. Fork the repository and create your feature branch.
2. Make your changes and add tests where appropriate.
3. Run linting and formatting checks.
4. Submit a pull request for review.

## License

[MIT](LICENSE) © 2024 Awesome Babushka Contributors

## Authors & Acknowledgments

- [@himansu9805](https://github.com/himansu9805)
- [@algoberzerker](https://github.com/algoberzerker)
- Special thanks to all contributors and the open-source community.

## Project Status

🚧 **Pre-alpha**: This project is under active development. Features and APIs are subject to change. Feedback and contributions are highly encouraged!
