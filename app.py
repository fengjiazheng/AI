# -*- coding: utf-8 -*-

"""
"""
from flask import Flask, redirect, request, session
from flask.templating import render_template
from flask.helpers import url_for
import json
import os
from Model.feqa.interface_feqa_in import feqa_interface
from Model.factCC.interface_factcc_in import factcc_interface

app = Flask(__name__)


# 默认登录页面 根路径 设置访问的URL
@app.route('/', methods=['GET'])
def login():
    return render_template('Index.html')


@app.route('/Index', methods=['GET'])
def index():
    return render_template('Index.html')


@app.route('/Model_introduce_one')
def Model_introduce_one():
    return render_template('Introduce_Model_one.html')


@app.route('/Model_introduce_two')
def Model_introduce_two():
    return render_template('Introduce_Model_two.html')


@app.route('/Model_show_one')
def Model_show_one():
    return render_template('Show_Model_one.html')


@app.route('/Model_show_two')
def Model_show_two():
    return render_template('Show_Model_two.html')



@app.route('/ShowModelonetest', methods=["POST"])
def ShowModelonetest():
    upload_file = request.form['MRI_Name']
    text_content = request.form['text_content']
    text_summary = request.form['text_summary']

    print('upload_file: {}; text_content: {};text_summary :{}'.format(upload_file, text_content, text_summary))

    # 如果上传了文件
    if upload_file != '':
        file_upload = './static/resource/upload/' + upload_file
        f = open(file_upload, encoding='utf-8', errors='ignore')
        ls_article_in = f.readlines()
        str_article_in = ''.join(ls_article_in)
        print(str_article_in)  # 文件内的文章主体
        if text_content == '上传文件':
            # 如果填写框内数据为空，则仅读取txt中的 文件
            # 获取内容，并获得相似度，
            similar_res = factcc_interface(str_article_in, text_summary)

        else:
            # 如果填写框内数据不为空，则读取txt中的文件以及填写框内的文字
            str_article_in = str_article_in + text_content
            similar_res = factcc_interface(str_article_in, text_summary)

        print('return_msg is :{}'.format(similar_res))
        return redirect(url_for('ShowModelone_msg', msg=similar_res))

    else:  # 如果没有上传文件

        str_article_in = text_content
        print(' 没有上传文件')
        similar_res = factcc_interface(str_article_in, text_summary)

        print('return_msg is :{}'.format(similar_res))
        return redirect(url_for('ShowModelone_msg', msg=similar_res))


@app.route('/ShowModelone_msg/?<string:msg>')
def ShowModelone_msg(msg):
    return render_template('Show_Model_one.html', msg=msg)


@app.route('/ShowModeltwotest', methods=["POST"])
def ShowModeltwotest():
    upload_file = request.form['MRI_Name']
    text_content = request.form['text_content']
    text_summary = request.form['text_summary']

    print('upload_file: {}; text_content: {};text_summary :{}'.format(upload_file, text_content, text_summary))

    # 如果上传了文件
    if upload_file != '':
        print(' 上传了 文件--')
        file_upload = './static/resource/upload/' + upload_file
        f = open(file_upload, encoding='utf-8', errors='ignore')
        ls_article_in = f.readlines()
        str_article_in = ''.join(ls_article_in)
        print(str_article_in)  # 文件内的文章主体
        if text_content == '上传文件':
            # 如果填写框内数据为空，则仅读取txt中的 文件
            # 获取内容，并获得相似度，
            similar_res = feqa_interface(str_article_in, text_summary)

        else:
            # 如果填写框内数据不为空，则读取txt中的文件以及填写框内的文字
            str_article_in = str_article_in + text_content
            similar_res = feqa_interface(str_article_in, text_summary)

        print('return_msg is :{}'.format(similar_res))
        return redirect(url_for('ShowModeltwo_msg', msg=similar_res))

    else:  # 如果没有上传文件

        str_article_in = text_content
        print(' --没有上传文件')
        similar_res = feqa_interface(str_article_in, text_summary)

        print('return_msg is :{}'.format(similar_res))
        return redirect(url_for('ShowModeltwo_msg', msg=similar_res))


@app.route('/ShowModeltwo_msg/?<string:msg>')
def ShowModeltwo_msg(msg):
    return render_template('Show_Model_two.html', msg=msg)


@app.route('/Show_Model_two')
def Show_Model_two():
    return render_template('Show_Model_two.html')


# 写入txt文件
def storageimage(filename, content):
    with open(filename, "wb+") as f:
        f.write(content)


@app.route('/Upload', methods=["POST"])
def Upload():
    img = request.files.to_dict().get('file_data')
    filename = img.filename
    print(filename)
    content = img.read()
    print(content)
    if request.method == 'POST':
        try:
            dir = 'static/resource'
            if os.path.exists(dir):
                storageimage(dir + '/upload/' + filename, content)
                data = {'filename': filename}
                data = json.dumps(data)
                return data
            else:
                os.mkdir(dir)
                os.mkdir(dir + '/upload')
                storageimage(dir + '/upload/' + filename, content)
                data = {'filename': filename}
                data = json.dumps(data)
                return data
        except Exception as e:
            raise e
    return "false"


if __name__ == '__main__':
    app.run(debug=True)
