"""Sample project structures for testing project detection."""

import json

# React + Vite project structure
REACT_VITE_PACKAGE_JSON = {
    "name": "react-vite-app",
    "version": "1.0.0",
    "type": "module",
    "scripts": {
        "dev": "vite",
        "build": "vite build",
        "preview": "vite preview"
    },
    "dependencies": {
        "react": "^18.2.0",
        "react-dom": "^18.2.0"
    },
    "devDependencies": {
        "@vitejs/plugin-react": "^4.0.0",
        "vite": "^4.3.9"
    }
}

# Next.js project structure
NEXTJS_PACKAGE_JSON = {
    "name": "nextjs-app",
    "version": "0.1.0",
    "scripts": {
        "dev": "next dev",
        "build": "next build",
        "start": "next start",
        "lint": "next lint"
    },
    "dependencies": {
        "next": "^14.0.0",
        "react": "^18.2.0",
        "react-dom": "^18.2.0"
    },
    "devDependencies": {
        "@types/node": "^20",
        "@types/react": "^18",
        "typescript": "^5"
    }
}

# Vue + Vite project structure
VUE_VITE_PACKAGE_JSON = {
    "name": "vue-vite-app",
    "version": "1.0.0",
    "scripts": {
        "dev": "vite",
        "build": "vite build"
    },
    "dependencies": {
        "vue": "^3.3.0"
    },
    "devDependencies": {
        "@vitejs/plugin-vue": "^4.0.0",
        "vite": "^4.3.9"
    }
}

# Angular project structure
ANGULAR_PACKAGE_JSON = {
    "name": "angular-app",
    "version": "0.0.0",
    "scripts": {
        "ng": "ng",
        "start": "ng serve",
        "build": "ng build"
    },
    "dependencies": {
        "@angular/common": "^17.0.0",
        "@angular/core": "^17.0.0",
        "@angular/platform-browser": "^17.0.0"
    },
    "devDependencies": {
        "@angular-devkit/build-angular": "^17.0.0",
        "@angular/cli": "^17.0.0",
        "@angular/compiler-cli": "^17.0.0"
    }
}

# Svelte project structure
SVELTE_PACKAGE_JSON = {
    "name": "svelte-app",
    "version": "1.0.0",
    "scripts": {
        "dev": "vite dev",
        "build": "vite build"
    },
    "dependencies": {
        "svelte": "^4.0.0"
    },
    "devDependencies": {
        "@sveltejs/vite-plugin-svelte": "^3.0.0",
        "vite": "^5.0.0"
    }
}

# Nuxt project structure
NUXT_PACKAGE_JSON = {
    "name": "nuxt-app",
    "version": "1.0.0",
    "scripts": {
        "dev": "nuxt dev",
        "build": "nuxt build",
        "generate": "nuxt generate"
    },
    "dependencies": {
        "nuxt": "^3.8.0",
        "vue": "^3.3.0"
    }
}

# Remix project structure
REMIX_PACKAGE_JSON = {
    "name": "remix-app",
    "version": "1.0.0",
    "scripts": {
        "dev": "remix dev",
        "build": "remix build"
    },
    "dependencies": {
        "@remix-run/node": "^2.0.0",
        "@remix-run/react": "^2.0.0",
        "react": "^18.2.0",
        "react-dom": "^18.2.0"
    },
    "devDependencies": {
        "@remix-run/dev": "^2.0.0"
    }
}

# FastAPI backend (Python)
FASTAPI_PYPROJECT_TOML = """[project]
name = "fastapi-backend"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.100.0",
    "uvicorn>=0.23.0",
    "pydantic>=2.0.0",
]
"""

# Flask backend (Python)
FLASK_REQUIREMENTS_TXT = """Flask==3.0.0
flask-cors==4.0.0
python-dotenv==1.0.0
"""

# Express backend (Node.js)
EXPRESS_PACKAGE_JSON = {
    "name": "express-backend",
    "version": "1.0.0",
    "scripts": {
        "start": "node server.js",
        "dev": "nodemon server.js"
    },
    "dependencies": {
        "express": "^4.18.0",
        "cors": "^2.8.5",
        "dotenv": "^16.0.0"
    },
    "devDependencies": {
        "nodemon": "^3.0.0"
    }
}

# NestJS backend
NESTJS_PACKAGE_JSON = {
    "name": "nestjs-backend",
    "version": "0.0.1",
    "scripts": {
        "start": "nest start",
        "start:dev": "nest start --watch",
        "build": "nest build"
    },
    "dependencies": {
        "@nestjs/common": "^10.0.0",
        "@nestjs/core": "^10.0.0",
        "@nestjs/platform-express": "^10.0.0"
    },
    "devDependencies": {
        "@nestjs/cli": "^10.0.0"
    }
}

# Fastify backend
FASTIFY_PACKAGE_JSON = {
    "name": "fastify-backend",
    "version": "1.0.0",
    "scripts": {
        "start": "node server.js",
        "dev": "nodemon server.js"
    },
    "dependencies": {
        "fastify": "^4.24.0",
        "@fastify/cors": "^8.4.0"
    }
}

# Fullstack project (React + FastAPI)
FULLSTACK_REACT_FASTAPI = {
    "frontend": REACT_VITE_PACKAGE_JSON,
    "backend": FASTAPI_PYPROJECT_TOML
}

# Monorepo structure (Turborepo)
TURBOREPO_PACKAGE_JSON = {
    "name": "monorepo",
    "version": "1.0.0",
    "private": True,
    "workspaces": [
        "apps/*",
        "packages/*"
    ],
    "scripts": {
        "dev": "turbo run dev",
        "build": "turbo run build"
    },
    "devDependencies": {
        "turbo": "^1.10.0"
    }
}

# Mixed frameworks (should trigger conflict)
MIXED_FRAMEWORKS_PACKAGE_JSON = {
    "name": "mixed-app",
    "version": "1.0.0",
    "dependencies": {
        "react": "^18.2.0",
        "vue": "^3.3.0",
        "angular": "^17.0.0",
        "next": "^14.0.0"
    }
}

# Empty project
EMPTY_PACKAGE_JSON = {
    "name": "empty-project",
    "version": "1.0.0"
}

# Corrupted package.json (invalid JSON)
CORRUPTED_PACKAGE_JSON = '{"name": "corrupted", invalid json'

# Package.json with no dependencies
NO_DEPS_PACKAGE_JSON = {
    "name": "no-deps",
    "version": "1.0.0",
    "scripts": {
        "start": "node index.js"
    }
}

# Very large project structure (for performance testing)
LARGE_PROJECT_PACKAGE_JSON = {
    "name": "large-project",
    "version": "1.0.0",
    "dependencies": {
        **{f"package-{i}": "^1.0.0" for i in range(100)}
    }
}

# Project with custom build scripts
CUSTOM_BUILD_PACKAGE_JSON = {
    "name": "custom-build",
    "version": "1.0.0",
    "scripts": {
        "build": "webpack --config custom.config.js",
        "dev": "webpack serve --mode development"
    },
    "dependencies": {
        "react": "^18.2.0"
    },
    "devDependencies": {
        "webpack": "^5.0.0",
        "webpack-cli": "^5.0.0"
    }
}

# SvelteKit project
SVELTEKIT_PACKAGE_JSON = {
    "name": "sveltekit-app",
    "version": "1.0.0",
    "scripts": {
        "dev": "vite dev",
        "build": "vite build"
    },
    "dependencies": {
        "svelte": "^4.0.0"
    },
    "devDependencies": {
        "@sveltejs/kit": "^2.0.0",
        "vite": "^5.0.0"
    }
}

# Solid.js project
SOLIDJS_PACKAGE_JSON = {
    "name": "solidjs-app",
    "version": "1.0.0",
    "scripts": {
        "dev": "vite",
        "build": "vite build"
    },
    "dependencies": {
        "solid-js": "^1.8.0"
    },
    "devDependencies": {
        "vite": "^5.0.0",
        "vite-plugin-solid": "^2.8.0"
    }
}

# Hono backend
HONO_PACKAGE_JSON = {
    "name": "hono-backend",
    "version": "1.0.0",
    "scripts": {
        "dev": "tsx watch src/index.ts",
        "build": "tsx src/index.ts"
    },
    "dependencies": {
        "hono": "^3.10.0"
    }
}

def get_sample_project_json(project_type: str) -> str:
    """Get sample package.json content for a project type."""
    samples = {
        "react-vite": REACT_VITE_PACKAGE_JSON,
        "nextjs": NEXTJS_PACKAGE_JSON,
        "vue-vite": VUE_VITE_PACKAGE_JSON,
        "angular": ANGULAR_PACKAGE_JSON,
        "svelte": SVELTE_PACKAGE_JSON,
        "nuxt": NUXT_PACKAGE_JSON,
        "remix": REMIX_PACKAGE_JSON,
        "express": EXPRESS_PACKAGE_JSON,
        "nestjs": NESTJS_PACKAGE_JSON,
        "fastify": FASTIFY_PACKAGE_JSON,
        "mixed": MIXED_FRAMEWORKS_PACKAGE_JSON,
        "empty": EMPTY_PACKAGE_JSON,
        "corrupted": CORRUPTED_PACKAGE_JSON,
        "no-deps": NO_DEPS_PACKAGE_JSON,
        "large": LARGE_PROJECT_PACKAGE_JSON,
        "custom-build": CUSTOM_BUILD_PACKAGE_JSON,
        "sveltekit": SVELTEKIT_PACKAGE_JSON,
        "solidjs": SOLIDJS_PACKAGE_JSON,
        "hono": HONO_PACKAGE_JSON,
        "turborepo": TURBOREPO_PACKAGE_JSON
    }

    if project_type in samples:
        content = samples[project_type]
        if isinstance(content, str):
            return content
        return json.dumps(content, indent=2)

    raise ValueError(f"Unknown project type: {project_type}")
