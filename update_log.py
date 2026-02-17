import os
import subprocess
import datetime

def get_latest_commit_info():
    try:
        # Get the latest commit hash and message
        commit_hash = subprocess.check_output(['git', 'log', '-1', '--format=%h']).decode('utf-8').strip()
        commit_msg = subprocess.check_output(['git', 'log', '-1', '--format=%s']).decode('utf-8').strip()
        commit_author = subprocess.check_output(['git', 'log', '-1', '--format=%an']).decode('utf-8').strip()
        return commit_hash, commit_msg, commit_author
    except Exception as e:
        return "Unknown", f"Error getting git info: {e}", "Unknown"

def update_html(commit_hash, commit_msg, commit_author):
    html_file = 'index.html'
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_entry = f"""
            <div class="log-entry new">
                <div class="log-header">
                    <div class="log-meta">
                        <span class="commit-hash">{commit_hash}</span>
                        <span class="log-author">{commit_author}</span>
                    </div>
                    <span class="log-timestamp">{timestamp}</span>
                </div>
                <div class="log-message">{commit_msg}</div>
            </div>
    """
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Insert the new entry at the top of the logs container
        marker = '<!-- Logs will be injected here by the pipeline -->'
        if marker in content:
            updated_content = content.replace(marker, marker + '\n' + new_entry)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Successfully added log for commit {commit_hash}")
        else:
            print("Error: Could not find the log injection marker in index.html")
            
    except FileNotFoundError:
        print(f"Error: {html_file} not found.")

if __name__ == "__main__":
    h, m, a = get_latest_commit_info()
    update_html(h, m, a)
