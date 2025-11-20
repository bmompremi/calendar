# CLAUDE.md - AI Assistant Guide for Calendar Repository

**Last Updated:** 2025-11-20
**Repository:** bmompremi/calendar
**License:** GNU General Public License v3.0

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Current Repository State](#current-repository-state)
3. [Technology Stack](#technology-stack)
4. [Repository Structure](#repository-structure)
5. [Development Workflow](#development-workflow)
6. [CI/CD Pipeline](#cicd-pipeline)
7. [Conventions & Standards](#conventions--standards)
8. [Key Files](#key-files)
9. [Roadmap & Missing Components](#roadmap--missing-components)
10. [AI Assistant Guidelines](#ai-assistant-guidelines)

---

## Project Overview

### Purpose
Calendar application repository - specific functionality to be determined.

### Project Status
**⚠️ EARLY STAGE / SKELETON REPOSITORY**

This repository is in its initial setup phase with:
- Basic repository infrastructure (LICENSE, README, .gitignore)
- CI/CD workflow configured
- **No source code implementation yet**

### License
GNU General Public License v3.0 (GPL-3.0) - Open source project with copyleft requirements.

---

## Current Repository State

### What Exists
- ✅ Git repository initialized
- ✅ GPL-3.0 License file (complete)
- ✅ Basic README.md (minimal content)
- ✅ GitHub Actions workflow for deployment
- ✅ .gitignore configuration

### What's Missing
- ❌ Source code
- ❌ Dependency management files (package.json or composer.json)
- ❌ Testing framework
- ❌ Documentation beyond basic README
- ❌ Source code directory structure
- ❌ Configuration files

---

## Technology Stack

### ⚠️ TECHNOLOGY STACK CONFLICT DETECTED

**Conflicting Indicators:**

1. **PHP/Composer Signs:**
   - `.gitignore` is configured for PHP projects
   - Ignores: `composer.phar`, `/vendor/`, potential `composer.lock`

2. **Node.js/npm Signs:**
   - CI/CD workflow uses Node.js 18
   - Workflow expects `package.json`, `npm install`, `npm run build`, `npm test`
   - Deploys to GitHub Pages from `./dist` directory

**Recommendation for AI Assistants:**
Before implementing features, **clarify with the user** which technology stack to use:
- Pure PHP/Composer
- Pure Node.js/npm
- Hybrid (both PHP backend + Node.js frontend)

Then update configuration files accordingly.

---

## Repository Structure

```
/home/user/calendar/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions CI/CD pipeline
├── .git/                        # Git version control
├── .gitignore                   # Git ignore rules (PHP-focused)
├── LICENSE                      # GPL-3.0 License (674 lines)
└── README.md                    # Project README (minimal)
```

### Expected Future Structure

When implementation begins, expect directories like:
```
├── src/                         # Source code
├── public/                      # Public assets (if web app)
├── tests/                       # Test files
├── dist/                        # Build output (for deployment)
├── docs/                        # Additional documentation
├── config/                      # Configuration files
└── [package.json/composer.json] # Dependency management
```

---

## Development Workflow

### Branch Strategy

**Current Branch:** `claude/claude-md-mi6u20013369mwv6-01X9xsbRGti128QRjDopYTh5`

**Branch Naming Convention:**
- Feature branches: `claude/claude-md-[session-id]`
- All development should occur on designated feature branches
- **CRITICAL:** Branch names must start with `claude/` and end with matching session ID for successful push operations

### Git Operations

**Pushing Changes:**
```bash
git push -u origin <branch-name>
```

**Important Rules:**
1. Always push to the designated Claude branch
2. Branch must start with `claude/` and end with session ID
3. If push fails with 403, verify branch name matches pattern
4. Retry network failures up to 4 times with exponential backoff (2s, 4s, 8s, 16s)

**Fetching/Pulling:**
```bash
git fetch origin <branch-name>
git pull origin <branch-name>
```

### Commit Conventions

**Current Commits:**
- `640b30c` - "Create deploy.yml"
- `d576577` - "Initial commit"

**Recommended Convention:**
- Use clear, descriptive commit messages
- Format: `<type>: <description>`
- Types: feat, fix, docs, style, refactor, test, chore
- Example: `feat: add event creation functionality`

---

## CI/CD Pipeline

### GitHub Actions Workflow

**File:** `.github/workflows/deploy.yml`

**Workflow Name:** "Deploy Calendar App"

**Triggers:**
- Push to `main` branch
- Manual workflow dispatch (`workflow_dispatch`)

**Pipeline Steps:**

1. **Checkout Code**
   - Action: `actions/checkout@v4`

2. **Setup Node.js Environment**
   - Action: `actions/setup-node@v4`
   - Node Version: 18
   - Cache: npm dependencies

3. **Install Dependencies** (conditional)
   - Command: `npm install`
   - Only runs if `package.json` exists

4. **Build Application** (conditional)
   - Command: `npm run build --if-present`
   - Expects build script in package.json

5. **Run Tests** (conditional)
   - Command: `npm test --if-present`
   - Expects test script in package.json

6. **Deploy to GitHub Pages**
   - Action: `peaceiris/actions-gh-pages@v3`
   - Source: `./dist` directory
   - Only on `main` branch
   - Uses `GITHUB_TOKEN` for authentication

7. **Deployment Status Notification**
   - Outputs deployment status

**Current Issues:**
- ❌ No `package.json` exists - npm steps will be skipped
- ❌ No build output directory (`dist/`) - deployment will fail
- ❌ Workflow assumes Node.js but .gitignore suggests PHP

---

## Conventions & Standards

### Currently Established

1. **Open Source Licensing**
   - GPL-3.0 license
   - All contributions must comply with copyleft requirements

2. **Version Control**
   - Git-based workflow
   - Feature branches for development
   - Main branch for production deployments

3. **Deployment Target**
   - GitHub Pages (static site hosting)
   - Build artifacts in `dist/` directory

### Missing (To Be Established)

- ❌ Code style guide (.editorconfig, .prettierrc, .phpcs.xml)
- ❌ Linting rules (ESLint, PHP_CodeSniffer)
- ❌ Testing conventions
- ❌ Documentation standards
- ❌ Code review process
- ❌ Naming conventions
- ❌ Directory structure conventions
- ❌ Git hooks (pre-commit, pre-push)

---

## Key Files

### `.gitignore`
**Location:** `/home/user/calendar/.gitignore`
**Purpose:** Ignore PHP/Composer artifacts
**Contents:**
```
composer.phar
/vendor/

# Commit your application's lock file (optional)
# composer.lock
```

**Note:** Will need updating based on final technology choice.

### `LICENSE`
**Location:** `/home/user/calendar/LICENSE`
**Type:** GNU General Public License v3.0
**Size:** 674 lines (complete license text)
**Implications:** All code must be GPL-compatible, derivative works must be open-sourced.

### `README.md`
**Location:** `/home/user/calendar/README.md`
**Status:** Minimal (2 lines)
**Contents:**
```markdown
# calendar
United
```

**Needs:** Comprehensive documentation including:
- Project description
- Installation instructions
- Usage examples
- Contributing guidelines
- Development setup

### `.github/workflows/deploy.yml`
**Location:** `/home/user/calendar/.github/workflows/deploy.yml`
**Purpose:** CI/CD automation for deployment
**Size:** 72 lines
**Status:** Configured but non-functional (missing dependencies)

---

## Roadmap & Missing Components

### Phase 1: Foundation (Current Priority)

1. **Resolve Technology Stack**
   - Decide: PHP vs Node.js vs Hybrid
   - Update .gitignore accordingly
   - Add dependency management file(s)

2. **Create Source Structure**
   - Add `src/` directory
   - Add `public/` directory (if web app)
   - Add `tests/` directory
   - Add configuration directory

3. **Initialize Dependencies**
   - Create `package.json` (if Node.js)
   - Create `composer.json` (if PHP)
   - Add initial dependencies

### Phase 2: Development Infrastructure

4. **Add Testing Framework**
   - Choose: Jest/Mocha (JS) or PHPUnit (PHP)
   - Create test configuration
   - Add sample tests

5. **Code Quality Tools**
   - Add linter configuration
   - Add code formatter
   - Add pre-commit hooks

6. **Documentation**
   - Expand README.md
   - Add CONTRIBUTING.md
   - Add API documentation (if applicable)
   - Add code comments

### Phase 3: Implementation

7. **Core Functionality**
   - Implement calendar features
   - Add event management
   - Add user interface

8. **Build & Deploy**
   - Configure build process
   - Test deployment pipeline
   - Set up GitHub Pages

---

## AI Assistant Guidelines

### Before Starting Any Work

1. **Check Technology Stack**
   - Ask user to clarify: PHP, Node.js, or both?
   - Update configuration files based on decision

2. **Review Current Branch**
   - Verify you're on the correct Claude branch
   - Confirm branch name matches session ID pattern

3. **Understand the Task**
   - Clarify feature requirements
   - Identify dependencies
   - Plan implementation approach

### When Writing Code

1. **GPL-3.0 Compliance**
   - Ensure all code is GPL-compatible
   - Include license headers in new files
   - Document third-party dependencies

2. **No Source Code Exists Yet**
   - You're building from scratch
   - Establish patterns and conventions early
   - Ask for user preferences on:
     - Framework/library choices
     - Architecture patterns
     - File naming conventions

3. **Create Necessary Infrastructure**
   - Add package.json/composer.json when implementing
   - Set up testing framework
   - Configure build tools
   - Update .gitignore as needed

4. **Follow Security Best Practices**
   - Avoid command injection vulnerabilities
   - Sanitize inputs
   - Follow OWASP guidelines
   - Validate/escape output

### When Making Changes

1. **Plan with TodoWrite**
   - Break complex tasks into steps
   - Track progress
   - Mark tasks complete as you go

2. **Update Documentation**
   - Keep README.md current
   - Update this CLAUDE.md as project evolves
   - Document new conventions

3. **Test Before Committing**
   - Write tests for new features
   - Ensure existing tests pass
   - Test build process

### Git Operations

1. **Commits**
   - Clear, descriptive messages
   - Follow conventional commit format
   - Don't commit secrets or sensitive data

2. **Pushing**
   - Always: `git push -u origin <branch-name>`
   - Branch must start with `claude/`
   - Retry on network failures (4 attempts, exponential backoff)

3. **Pull Requests**
   - Use `gh pr create` (if available)
   - Include comprehensive description
   - Reference related issues

### CI/CD Awareness

**Current Pipeline Expectations:**
- Node.js 18 environment
- npm install (needs package.json)
- npm run build (needs build script)
- npm test (needs test script)
- Deployment from ./dist directory

**When Implementing:**
- Ensure package.json has required scripts
- Build output must go to ./dist/
- All tests must pass before deployment
- Consider GitHub Pages static site requirements

### Common Pitfalls to Avoid

1. ❌ **Don't assume technology stack** - always ask first
2. ❌ **Don't create files unnecessarily** - prefer editing existing
3. ❌ **Don't skip testing** - add tests for new features
4. ❌ **Don't ignore CI/CD** - ensure workflow remains functional
5. ❌ **Don't commit to wrong branch** - verify branch name
6. ❌ **Don't add GPL-incompatible code** - check license compatibility
7. ❌ **Don't use placeholders** - complete implementations only

### Asking for Clarification

**Always ask user about:**
- Technology stack choice (if implementing first feature)
- Framework/library preferences
- Architecture decisions
- UI/UX requirements
- API design choices
- Deployment preferences

**Don't ask about:**
- Standard conventions (use best practices)
- Code style (use language standards)
- Common patterns (use established patterns)

---

## Quick Reference

### Repository Info
- **Path:** `/home/user/calendar`
- **Branch:** `claude/claude-md-mi6u20013369mwv6-01X9xsbRGti128QRjDopYTh5`
- **Remote:** `http://local_proxy@127.0.0.1:36600/git/bmompremi/calendar`

### Essential Commands
```bash
# View status
git status

# Push changes
git push -u origin claude/claude-md-mi6u20013369mwv6-01X9xsbRGti128QRjDopYTh5

# View files
ls -la

# Run tests (when implemented)
npm test  # or php vendor/bin/phpunit

# Build (when implemented)
npm run build
```

### Key Contacts
- Repository Owner: bmompremi

---

## Conclusion

This is an **early-stage repository** awaiting implementation. AI assistants should:

1. **Clarify technology stack** before implementing features
2. **Establish conventions** as you build
3. **Document decisions** and update this file
4. **Follow GPL-3.0 requirements** for all code
5. **Maintain CI/CD functionality** as you add features

When this repository matures, update this CLAUDE.md with:
- Actual technology stack and dependencies
- Established conventions and patterns
- API documentation
- Testing strategies
- Deployment procedures
- Known issues and workarounds

---

**For Questions or Updates:**
Contact the repository owner or create an issue in the GitHub repository.
