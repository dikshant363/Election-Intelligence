# DEVELOPMENT_WORKFLOW.md

## Project Setup

### 1. Initial Setup
- Fork this repository
- Clone the repository: `git clone <repo-url>`
- Navigate to project directory
- Install dependencies (see `SETUP.md` for details)

### 2. Development Workflow

#### Branch Management
```
git checkout develop           # Start with develop branch
<work on develop branch>      # Add your feature
feature/<your-feature-name>   # Create feature branch
git checkout feature/<your-feature-name>
# Do your work
# Stage, commit, and push when ready
git add .
# git commit -m "brief description + Co-authored-by: Claude <noreply@anthropic.com>"
git push origin feature/<your-feature-name>
```

#### Making Changes
1. Work directly in the `feature/<your-feature-name>` branch
2. Use `git commit --amend -m <new-message>` for multiple commits
3. Push the changes to remote branch
4. Wait for CI/CD to run tests automatically
5. Submit a pull request to `develop` branch

#### Creating a Pull Request
1. Go to your repository on GitHub
2. Click on the "Pull requests" tab
3. Click the "New pull request" button
4. Select `develop` as the base branch
5. Select your feature branch as the compare branch
6. Add a clear description of changes
7. Add relevant screenshots or examples if helpful
8. Use the standard PR template:
   ```
   ### Summary
   <brief summary>
   
   ### What changed
   <list of changes>
   
   ### How to test
   <steps to verify>
   
   ### Breaking changes
   <N/A> or describe changes that break existing functionality
   ```
9. Submit the PR and wait for review

### 3. Review Process

#### Peer Review
- All code must be reviewed by at least one team member
- Review comments must be addressed before merging
- Maintain the coding standards and best practices

#### Team Coordination
- Use GitHub discussions or pull request comments
- Communicate about implementation changes and design decisions
- Share and review design documentation as you progress

### 4. Integration Testing

#### Testing Checklist
- [ ] Unit tests for modified code
- [ ] Integration tests for new features
- [ ] End-to-end tests if applicable
- [ ] Performance tests if needed
- [ ] Security tests for sensitive features
- [ ] Documentation updates

### 5. Integration

#### Merge Process
- Preferred method: Squash merge (all commits into one)
- Rebase feature branch onto `develop` before merging
- Ensure all tests are passing
- Verify changes with `git diff develop..HEAD`
- Merge after successful review

#### Post-Merge
- Update `CHANGELOG.md`
- Document major decisions
- Update task statuses in `TASKS.md`
- Close associated tasks

### 6. Documentation

#### Documentation Standards
- All new code must have docstrings
- Document public APIs and interfaces
- Keep documentation up to date with code changes
- Update `ARCHITECTURE.md` for major changes

### 7. Code Reviews and Quality Assurance

#### Code Review Checklist
- [ ] Follows coding standards
- [ ] Has unit tests
- [ ] Has documentation
- [ ] Is peer-reviewed
- [ ] Has clear commit messages
- [ ] No duplicate or commented-out code
- [ ] Has been tested locally

#### Automated Checks
- Run `ruff check app/` for Python code quality
- Run `black --check app/` for formatting
- Run `mypy app/` for type checking
- Run `pytest` for tests
- Run `dart format --set-exit-if-changed` for Flutter

### 8. Branch Cleanup

#### Delete Feature Branches
- After merging, delete the feature branch
- Use `git checkout develop` and `git branch -d feature/<your-feature-name>`
- Ensure remote branch is deleted

### 9. Best Practices

#### Commit Messages
```<type>(<scope>): <description>

<body>

<footer>

Types:
- feat: new feature
- fix: bug fix
- docs: documentation changes
- style: formatting, no code change
- refactor: refactoring
- perf: performance improvement
- test: testing
- build: build system changes
- ci: CI/CD changes
- chore: other non-code changes

Scopes:
- api: FastAPI-related changes
- flutter: Flutter-related changes
- database: Database-related changes
- auth: Authentication-related changes
- ui: UI/UX changes
- docs: Documentation changes
- config: Configuration changes
```

#### Pull Request Labels
- **Help wanted** - needs help from community
- **Good first issue** - suitable for beginners
- **Bug** - for bug reports or fixes
- **Enhancement** - for feature requests
- **Documentation** - for documentation updates
- **Design** - for design updates/changes