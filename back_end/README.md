如今我换到了一个新电脑Mac——需要重新安装python包：
回到根目录用homebrew装（
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
）
通过echo重定向把homebrew加入PATH（
echo >> ~/.zprofile
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
)
安装python包（
brew install python
）
配置虚拟环境并激活后（
First time to launch: Set a venv——py -m venv venv
Activate it : venv\Scripts\activate.bat
Kill it: deactivate
Install package: pip install -r requirements.txt
）

运行（uvicorn app:app --reload --host 0.0.0.0 --port 8000）
