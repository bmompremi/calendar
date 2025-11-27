# CLAUDE.md - AI Assistant Development Guide

## Project Overview

**Project Name:** Calendar Application
**Repository:** calendar
**License:** GNU General Public License v3.0
**Current Status:** Early Development / Skeleton Repository

This is a calendar application project currently in its initial setup phase. The repository contains minimal scaffolding and is ready for development.

## Repository Structure

```
calendar/
├── .github/
│   └── workflows/
│       └── deploy.yml        # GitHub Actions CI/CD pipeline
├── .gitignore                # PHP/Composer ignore patterns
├── LICENSE                   # GPL-3.0 License
├── README.md                 # Project README (minimal)
└── CLAUDE.md                 # This file - AI assistant guide
```

### Current State

The repository is in an **early-stage setup** with:
- Basic licensing and documentation files
- GitHub Actions deployment workflow configured
- No source code files yet
- No package manager configuration files yet

## Technology Stack

### Planned Stack (based on deploy.yml)

- **Primary Language:** Not yet determined (workflow suggests Node.js, but .gitignore suggests PHP)
- **Build System:** Node.js (as configured in deploy.yml)
- **Node Version:** 18.x
- **Package Manager:** npm
- **Deployment:** GitHub Pages (./dist directory)
- **CI/CD:** GitHub Actions

### Technology Conflicts to Resolve

⚠️ **Important:** There's a discrepancy between:
- `.gitignore` → Configured for PHP/Composer projects
- `deploy.yml` → Configured for Node.js/npm projects

**Action Required:** Clarify the primary technology stack with the project owner before proceeding with development.

## Development Workflows

### GitHub Actions CI/CD Pipeline

**File:** `.github/workflows/deploy.yml`

The deployment workflow runs on:
- Push to `main` branch
- Manual trigger via workflow_dispatch

**Pipeline Steps:**
1. Checkout repository
2. Setup Node.js 18.x environment
3. Install dependencies (if package.json exists)
4. Build application (if build script exists)
5. Run tests (if test script exists)
6. Deploy to GitHub Pages (from ./dist directory)

### Git Branching Strategy

**Development Branch Pattern:** `claude/claude-md-migx7grrr7brvose-*`

When working on this repository:
- Create feature branches with the `claude/` prefix
- Include the session ID suffix for tracking
- Push changes to feature branches, NOT directly to main
- Use `git push -u origin <branch-name>` for initial pushes

### Commit Message Conventions

When committing changes:
1. Review changes with `git status` and `git diff`
2. Check recent commits with `git log` to match the project's style
3. Write concise, descriptive commit messages (1-2 sentences)
4. Focus on "why" rather than "what"
5. Use conventional commit format when applicable

## Key Conventions for AI Assistants

### Before Making Changes

1. **Always read files before modifying them**
   - Never propose changes to code you haven't read
   - Understand the existing structure before suggesting modifications

2. **Check for existing patterns**
   - Look for similar implementations in the codebase
   - Follow established naming conventions
   - Maintain consistency with existing code style

3. **Verify the technology stack**
   - Confirm whether this is a PHP or Node.js project
   - Check for package.json, composer.json, or other config files
   - Don't assume the stack from incomplete information

### Code Quality Standards

1. **Security First**
   - Avoid OWASP top 10 vulnerabilities (XSS, SQL injection, command injection, etc.)
   - Validate user input at system boundaries
   - Don't store secrets in code or version control
   - If you write insecure code, fix it immediately

2. **Simplicity Over Cleverness**
   - Avoid over-engineering solutions
   - Only make changes that are directly requested or clearly necessary
   - Don't add extra features, refactoring, or "improvements" beyond the scope
   - Three similar lines are better than a premature abstraction

3. **Minimal Changes**
   - Don't add error handling for scenarios that can't happen
   - Don't add comments to code you didn't change
   - Don't create helpers/utilities for one-time operations
   - Trust internal code and framework guarantees

4. **No Backwards Compatibility Hacks**
   - Delete unused code completely (no `_var` renaming, `// removed` comments)
   - If something is unused, remove it entirely
   - Don't design for hypothetical future requirements

### File Operations

**Preferred Tools:**
- **Reading:** Use `Read` tool, not `cat`/`head`/`tail`
- **Writing:** Use `Write` tool, not `echo` redirects
- **Editing:** Use `Edit` tool, not `sed`/`awk`
- **Searching:** Use `Glob` for files, `Grep` for content
- **Terminal:** Use `Bash` only for actual system commands

### Testing and Validation

Before committing:
1. Ensure code compiles/runs without errors
2. Run existing tests if available
3. Verify no new security vulnerabilities introduced
4. Check that changes work as intended

## Common Tasks

### Creating New Features

1. **Determine the technology stack**
   ```bash
   # Check for existing package managers
   ls package.json composer.json requirements.txt
   ```

2. **Set up project structure** (if starting from scratch)
   - Create appropriate source directories (src/, lib/, app/, etc.)
   - Set up build/test configuration
   - Add necessary dependencies

3. **Implement features incrementally**
   - Break down into small, testable units
   - Commit working code frequently
   - Keep changes focused and atomic

### Setting Up the Project

Since the repository is in early stages, you may need to:

1. **Clarify the technology stack**
   ```bash
   # For Node.js project:
   npm init -y

   # For PHP project:
   composer init
   ```

2. **Create source directory structure**
   ```bash
   mkdir -p src tests docs
   ```

3. **Configure build tools**
   - Update package.json scripts
   - Set up bundler/compiler configuration
   - Ensure deploy.yml expects the correct output

4. **Update .gitignore**
   - Match the chosen technology stack
   - Include node_modules/, dist/, build/, etc.

### Making Changes

1. **Read before writing**
   ```bash
   # Always read files first
   cat path/to/file.js
   ```

2. **Make targeted edits**
   ```bash
   # Use Edit tool for specific changes
   # Don't rewrite entire files unnecessarily
   ```

3. **Test your changes**
   ```bash
   # Run tests
   npm test

   # Run build
   npm run build
   ```

4. **Commit with context**
   ```bash
   git add <files>
   git commit -m "Brief description of why this change was made"
   ```

### Pushing Changes

```bash
# Always push to feature branch with proper naming
git push -u origin claude/claude-md-migx7grrr7brvose-<session-id>

# Never force push to main/master without explicit permission
# Never skip hooks (--no-verify) without explicit permission
```

## Project-Specific Guidelines

### Deployment

- **Target Environment:** GitHub Pages
- **Build Output:** Must be in `./dist` directory
- **Build Trigger:** Push to main branch
- **Hosting:** Static site deployment

### Dependencies

**Not Yet Configured** - When adding dependencies:
- Use `npm install <package>` for Node.js
- Use `composer require <package>` for PHP
- Document major dependencies in README.md
- Keep dependencies minimal and purposeful

### Code Style

**Not Yet Established** - Recommendations:
- Choose a style guide early (Airbnb, Standard, PSR-12, etc.)
- Use automated formatters (Prettier, PHP-CS-Fixer)
- Configure linting in CI/CD pipeline
- Be consistent once a style is chosen

## Common Pitfalls to Avoid

1. **Don't assume the technology stack**
   - The .gitignore suggests PHP, deploy.yml suggests Node.js
   - Always verify before adding stack-specific code

2. **Don't create unnecessary files**
   - Only create files needed for the specific task
   - Prefer editing existing files over creating new ones

3. **Don't over-complicate early development**
   - Start simple and iterate
   - Add complexity only when needed
   - YAGNI (You Aren't Gonna Need It) principle

4. **Don't push directly to main**
   - Use feature branches
   - Follow the branch naming convention
   - Create PRs for review

5. **Don't ignore the deployment pipeline**
   - Ensure changes are compatible with deploy.yml
   - Test that builds succeed before pushing
   - Verify deployment requirements are met

## Questions to Clarify With Owner

Before proceeding with major development:

1. **Technology Stack:** Is this a Node.js or PHP project?
2. **Framework Choice:** Any specific framework (React, Vue, Laravel, Symfony)?
3. **Calendar Features:** What calendar functionality is needed?
4. **User Requirements:** Single-user or multi-user? Public or private?
5. **Data Storage:** Client-side only or database backend?
6. **Authentication:** Required? What type?

## Resources and Documentation

### External Resources

- **License:** [GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)
- **GitHub Actions:** [Actions Documentation](https://docs.github.com/en/actions)
- **GitHub Pages:** [Pages Documentation](https://docs.github.com/en/pages)

### Project Resources

- **README:** See README.md for user-facing documentation
- **Workflows:** See .github/workflows/ for CI/CD configuration
- **Issues:** Check repository issues for planned work

## Changelog

### 2025-11-27
- Initial CLAUDE.md created
- Documented current repository state
- Established conventions and guidelines
- Identified technology stack ambiguity requiring resolution

---

**Note for AI Assistants:** This document should be updated as the project evolves. When significant architectural decisions are made, update this guide to reflect the current state and conventions.
