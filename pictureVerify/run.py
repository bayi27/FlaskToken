#!/usr/bin/env python 
#coding=utf-8
import os
import random
from flask import Flask,send_from_directory
from PIL import Image,ImageFont,ImageDraw,ImageFilter

app=Flask(__name__)
app.debug=True

class picture:
    def __init__(self):
        self.size = (240,60)
        self.mode="RGB"
        self.color="white"
        self.font = ImageFont.truetype("C:\Windows\Fonts\Arial.ttf", 36) #设置字体大小

    def randChar(self):
        basic='23456789abcdefghijklmnpqrstwxyzABCDEFGHIJKLMNPQRSTWXYZ'
        return basic[random.randint(0,len(basic)-1)] #随机字符

    def randBdColor(self):
        return (random.randint(64,255),random.randint(64,255),random.randint(64,255)) #背景

    def randTextColor(self):
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127)) #随机颜色

    def proPicture(self):
        new_image=Image.new(self.mode,self.size,self.color) #创建新图像有三个默认参数:尺寸,颜色,模式
        drawObject=ImageDraw.Draw(new_image) #创建一个可以对image操作的对象
        line_num = random.randint(4,6) # 干扰线条数
        for i in range(line_num):
            #size=(240,60)
            begin = (random.randint(0, self.size[0]), random.randint(0, self.size[1]))
            end = (random.randint(0, self.size[0]), random.randint(0, self.size[1]))
            drawObject.line([begin, end], self.randTextColor())

        for x in range(240):
            for y in range(60):
                tmp = random.randint(0,50)
                if tmp>30: #调整干扰点数量
                    drawObject.point((x,y),self.randBdColor())

        randchar=''  
        for i in range(5):
            rand=self.randChar()
            randchar+=rand
            drawObject.text([50*i+10,10],rand,self.randTextColor(),font=self.font) #写入字符

        new_image = new_image.filter(ImageFilter.SHARPEN) # 滤镜    

        return new_image,randchar
@app.route('/<filename>')
def get_file(filename):
    return send_from_directory(os.getcwd(),filename)

@app.route('/')
def index():
    test=picture()
    image,code=test.proPicture()
    image.save('new.jpg')
    url="http://127.0.0.1:5000/new.jpg"
    return '<img src='+url+' /><br/>'+"图中的code为："+code 
    #这里有缓存,需要CTRL+F5才会有效果

if __name__=="__main__":
    app.run()    