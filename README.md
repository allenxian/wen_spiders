# wen_spiders
## Introduction
Here are some spiders.  
All the spiders will inherit from the `BaseSpider` in `utils.base`, which implements many useful functions, such as automaticly switch the header of request, parse the content by `xpath`.    
I use `mongodb` as the default database and `redis` to control the parallel. You can find the setting in `config` on each folder.  

## Spiders List
- [36kr news flashes](http://36kr.com/newsflashes)  
This spider crawl the[36kr news flashes](http://36kr.com/newsflashes), which includes the title, description and other many useful information. It can be the corpus for information extraction.
- [oxford words](http://www.oxfordlearnersdictionaries.com/us/wordlist/english/academic/)  
This spider crawl the words from [Oxford Learner's Dictionaries](http://www.oxfordlearnersdictionaries.com/us/wordlist/english/academic/) for my dear friend [Zhang Yu](https://github.com/neilsustc)'s [Plugin](https://github.com/neilsustc/vscode-dic-completion) for vscode, which can complete the word when you are typing.