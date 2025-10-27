# Fixing npm Permissions Issues (EACCES Error)

## The Problem

You're seeing this error when trying to install npm packages globally:

```
npm error code: 'EACCES',
npm error syscall: 'rename',
npm error path: '/usr/local/lib/node_modules/@anthropic-ai/claude-code'
```

This happens because npm is trying to write to system directories (`/usr/local/lib/node_modules/`) that require elevated permissions.

## Solution 1: Use a Node Version Manager (Recommended)

The best long-term solution is to use a Node version manager like `nvm` (Node Version Manager), which installs Node.js and npm in your user directory, avoiding permissions issues entirely.

### For macOS/Linux:

1. **Install nvm:**
   ```bash
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
   ```

2. **Restart your terminal or run:**
   ```bash
   source ~/.bashrc  # or ~/.zshrc for zsh
   ```

3. **Install the latest Node.js:**
   ```bash
   nvm install node
   nvm use node
   ```

4. **Now install packages globally without sudo:**
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

### Benefits:
- No more permission issues
- Easy Node.js version switching
- Clean uninstallation
- No system-level modifications needed

## Solution 2: Change npm's Default Directory

If you prefer to keep your current Node.js installation, change where npm installs global packages.

1. **Create a directory for global installations:**
   ```bash
   mkdir ~/.npm-global
   ```

2. **Configure npm to use this directory:**
   ```bash
   npm config set prefix '~/.npm-global'
   ```

3. **Add the new directory to your PATH:**

   For **bash** (add to `~/.bashrc` or `~/.bash_profile`):
   ```bash
   echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
   source ~/.bashrc
   ```

   For **zsh** (add to `~/.zshrc`):
   ```bash
   echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.zshrc
   source ~/.zshrc
   ```

4. **Now install packages globally:**
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

## Solution 3: Fix Permissions on Node Modules Directory (Use with Caution)

This fixes permissions on your current npm directory. **Note:** This may cause issues with other system tools.

```bash
sudo chown -R $(whoami) /usr/local/lib/node_modules
sudo chown -R $(whoami) /usr/local/bin
sudo chown -R $(whoami) /usr/local/share
```

## What NOT to Do

### Don't use sudo with npm install
```bash
# DON'T DO THIS:
sudo npm install -g @anthropic-ai/claude-code
```

**Why?** This can create permission problems for future installations and may pose security risks.

## Verifying Your Fix

After applying one of the solutions above, verify it works:

```bash
# Check npm prefix
npm config get prefix

# Should show your user directory, not /usr/local
# For nvm: /Users/yourusername/.nvm/versions/node/vX.X.X
# For custom prefix: /Users/yourusername/.npm-global

# Try installing a package globally
npm install -g @anthropic-ai/claude-code

# Verify installation
claude-code --version
```

## Troubleshooting

### Command not found after installation

Add the npm global bin directory to your PATH:

```bash
# Find npm bin directory
npm bin -g

# Add to PATH (example for bash)
echo 'export PATH="$(npm bin -g):$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Still getting EACCES errors

1. Check npm cache permissions:
   ```bash
   sudo chown -R $(whoami) ~/.npm
   ```

2. Clear npm cache:
   ```bash
   npm cache clean --force
   ```

3. Verify Node.js installation ownership:
   ```bash
   ls -la $(which node)
   ls -la $(which npm)
   ```

## Quick Reference

| Method | Difficulty | Recommended |
|--------|------------|-------------|
| nvm | Easy | Yes - Best for most users |
| Change npm prefix | Medium | Yes - Good alternative |
| Fix permissions | Easy | Caution - May cause issues |
| Use sudo | Very Easy | No - Security risk |

## Additional Resources

- [npm documentation on permissions](https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally)
- [nvm GitHub repository](https://github.com/nvm-sh/nvm)
- [Node.js installation guides](https://nodejs.org/en/download/package-manager/)

## For This Specific Error

Based on your error, you're trying to install/update `@anthropic-ai/claude-code`. After fixing permissions using one of the methods above, run:

```bash
npm install -g @anthropic-ai/claude-code
```

If you already have a broken installation, you may need to remove it first:

```bash
# Using nvm or fixed permissions:
npm uninstall -g @anthropic-ai/claude-code

# Then reinstall:
npm install -g @anthropic-ai/claude-code
```
