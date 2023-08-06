
sense-html目前包含的功能主要有：


1）对文本的中不必要的文字进行过滤


## 安装方式

    pip install sense-html


## 使用指南

使用

    from sense_html import handle_text


示例代码：
    
    from sense_html import handle_text
    
    # html 可以为普通文本，也可以为dom树形式文本
    def handle_process_work(html):
        text = handle_text(html)
        return text
      

