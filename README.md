# Whatsyourfavorite
为无法科学上网的同人女提供最新最美味的中文版Fanfics（我调用了Google翻译，这让文章变得通俗易懂）
我产品（这回真的是我产品）：简洁————当点进网页、您只需要搜索想看的配对、搜索结果会以“最新”和“最热”呈现；美妙————即便拥有镜像网站也很难找到靠谱翻译？这里调用Google翻译的API，您可以看到最贴近作品灵魂的翻译；
写着写着感觉看到了五年前躲着高中重重课业仍坚持用彩云翻译看同人小说的自己，请燥候！

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
