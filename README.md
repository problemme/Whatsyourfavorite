# Whatsyourfavorite
This project is built for fandom girls who don’t have reliable access to the global internet, yet still want to read the latest and most satisfying Chinese fanfictions.

To make this possible, I integrated Google Translate into the platform. The goal is not just “translation,” but readability — turning raw machine output into something smooth, approachable, and emotionally faithful to the original text.

This time, it really is my product.

The design philosophy is simple and intentional:

Simple — When you open the website, you only need to search for the pairing you care about. Results are displayed clearly by latest and most popular, no unnecessary steps.

Delightful — Even with mirror sites, it’s hard to find translations you can truly trust. By calling Google Translate’s API, this project aims to provide translations that stay as close as possible to the soul of the original work.

While writing this README, I kept seeing a version of myself from five years ago — hiding between overwhelming high school assignments, stubbornly relying on Caiyun Translate just to keep reading fanfiction. That experience never really left me, and this project is, in many ways, a response to it.

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
配置虚拟环境并激活
