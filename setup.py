import os

print("pipenv와 라이브러리 설치중...")
os.system("python -m pip install --upgrade pip")
if os.system("pip list | grep pipenv"):
    os.system("pip install pipenv")
os.system("pipenv install")
os.system("pipenv install --dev")

print("git 설정중...")
if not os.path.exists(".git"):
    os.system("git init")
os.system("git config --local commit.template ./commit_template")
os.system("cp .git/hooks/commit-msg.sample .git/hooks/commit-msg")
with open(".git/hooks/commit-msg", "a") as f:
    f.write("python check_commit_template.py $1")

print("pre-commit 설정중...")
os.system("pipenv run pre-commit install")
