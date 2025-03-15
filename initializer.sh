# # Initialize a new Git repository
# git init

# # Add your existing files
# git add README.md

# # Create a proper .gitignore file
# echo "__pycache__/" > .gitignore
echo "*.pyc" >> .gitignore
echo "venv/" >> .gitignore
echo ".env" >> .gitignore
echo ".idea/" >> .gitignore
echo ".vscode/" >> .gitignore

# Add the updated .gitignore
git add .gitignore

# Make your first commit
git commit -m "Initial commit: Setup Meeting Summarizer & Action Item Extractor"