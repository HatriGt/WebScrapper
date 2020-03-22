import os
import random
from datetime import datetime, timedelta
import subprocess

def create_commit(date):
    # Format date for Git
    formatted_date = date.strftime('%Y-%m-%d %H:%M:%S')
    
    # Create random changes to a file
    with open('agilify.txt', 'a') as f:
        f.write(f'Update {formatted_date}\n')
    
    # Set environment variables for backdating
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = formatted_date
    env['GIT_COMMITTER_DATE'] = formatted_date
    
    # Stage and commit
    subprocess.run(['git', 'add', '.'], check=True)
    subprocess.run(['git', 'commit', '-m', f"Update agilify app {formatted_date}"], env=env, check=True)

def generate_commits(start_date, end_date, commits_per_day=5):
    current_date = start_date
    
    while current_date <= end_date:
        # Get all days in current month
        month_start = current_date.replace(day=1)
        if month_start.month == 12:
            next_month = month_start.replace(year=month_start.year + 1, month=1)
        else:
            next_month = month_start.replace(month=month_start.month + 1)
        
        # Get 13 random days for this month
        month_days = []
        while len(month_days) < 13:
            day = random.randint(1, (next_month - timedelta(days=1)).day)
            if day not in month_days:
                month_days.append(day)
        
        # Check if current day is one of the random 13 days
        if current_date.day in month_days:
            # Do more than 5 commits
            num_commits = random.randint(6, 10)
            
            for _ in range(num_commits):
                # Random time between 9 AM and 6 PM
                hour = random.randint(9, 18)
                minute = random.randint(0, 59)
                commit_date = current_date.replace(hour=hour, minute=minute)
                
                try:
                    create_commit(commit_date)
                    print(f"Created commit for {commit_date}")
                except Exception as e:
                    print(f"Error creating commit: {e}")
        
        current_date += timedelta(days=1)

def main():
    # Set date range (example: last 30 days)
    end_date = datetime(2021, 12, 31)
    start_date = datetime(2020, 3, 22)
    
    # Initialize git if needed
    if not os.path.exists('.git'):
        subprocess.run(['git', 'init'], check=True)
        
    # Create initial file if it doesn't exist
    if not os.path.exists('agilify.txt'):
        open('agilify.txt', 'w').close()
    
    # Generate commits
    generate_commits(start_date, end_date)
    
    print("Completed generating commits!")
    print("Run 'git push origin main' to push changes")

if __name__ == "__main__":
    main()
