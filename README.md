  A simple python skript for updating repos.
  It compares against an <sources.txt> files for existing/target repos.
  The whole process looks like this:
1. Check if existing repository
        - if not, break operation
2. Git pull from remote branch
3. Add the updated files via <git add>
4. Generate an automatic commit message
5. Fetch current branch name and push to remote origin