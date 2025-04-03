import os
import sys
import subprocess
import time

def run_command(command, description=None):
    """Run a shell command and print its output"""
    if description:
        print(f"\n{description}")
    
    print(f"$ {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout.strip())
    
    if result.stderr and result.returncode != 0:
        print(f"Error: {result.stderr.strip()}")
        return False
    
    return result.returncode == 0

def init_git_repo():
    """Initialize a Git repository and commit the Chess Project"""
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    print(f"Initializing Git repository in: {project_root}")
    
    # Check if git is installed
    if not run_command("git --version", "Checking Git installation"):
        print("Error: Git is not installed or not in PATH. Please install Git first.")
        return False
    
    # Check if .git directory already exists
    if os.path.exists(os.path.join(project_root, ".git")):
        print("Git repository already exists.")
        choice = input("Do you want to continue and add/commit changes? (y/n): ")
        if choice.lower() != 'y':
            return False
    else:
        # Initialize new git repository
        if not run_command("git init", "Initializing new Git repository"):
            return False
    
    # Add all files (except those in .gitignore)
    if not run_command("git add .", "Adding files to Git"):
        return False
    
    # Show status
    run_command("git status", "Current Git status")
    
    # Commit files
    commit_msg = input("\nEnter commit message (default: 'Initial commit of Chess Project'): ")
    if not commit_msg:
        commit_msg = "Initial commit of Chess Project"
    
    if not run_command(f'git commit -m "{commit_msg}"', "Committing changes"):
        return False
    
    # Show log
    run_command("git log --oneline -n 3", "Recent commits")
    
    return True

def setup_git_config():
    """Setup basic Git configuration if not already done"""
    username = subprocess.run("git config --global user.name", shell=True, capture_output=True, text=True).stdout.strip()
    email = subprocess.run("git config --global user.email", shell=True, capture_output=True, text=True).stdout.strip()
    
    if not username:
        print("\nGit username not set. Let's set it up:")
        username = input("Enter your name: ")
        if username:
            run_command(f'git config --global user.name "{username}"')
    
    if not email:
        print("\nGit email not set. Let's set it up:")
        email = input("Enter your email: ")
        if email:
            run_command(f'git config --global user.email "{email}"')
    
    if username and email:
        print(f"\nGit is configured with:")
        print(f"Username: {username}")
        print(f"Email: {email}")
    
    return username and email

def check_remote():
    """Check if a remote repository is configured and offer to add one"""
    remotes = subprocess.run("git remote -v", shell=True, capture_output=True, text=True).stdout.strip()
    
    if not remotes:
        print("\nNo remote repository is configured.")
        add_remote = input("Would you like to add a GitHub remote repository? (y/n): ")
        
        if add_remote.lower() == 'y':
            print("\nTo add a GitHub remote, first create a new repository on GitHub.")
            print("Then run the following command:")
            print('  git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git')
            print('  git branch -M main')
            print('  git push -u origin main')

def main():
    print("Chess Project Git Initialization")
    print("================================")
    
    # Make sure git configuration is set
    if not setup_git_config():
        print("\nGit configuration incomplete. Please set your user.name and user.email")
        return
    
    # Initialize and commit
    if init_git_repo():
        print("\nGit repository successfully initialized!")
        
        # Check for remote repository
        time.sleep(1)  # Slight pause for better readability
        check_remote()
        
        print("\nYour Chess Project is now under version control!")
        print("\nHelpful Git commands:")
        print("  git status              # Check current status")
        print("  git add .               # Add all changes")
        print("  git commit -m 'Message' # Commit changes")
        print("  git log                 # View commit history")
        print("  git push                # Push to remote (if configured)")
    else:
        print("\nFailed to initialize Git repository.")

if __name__ == "__main__":
    main()
