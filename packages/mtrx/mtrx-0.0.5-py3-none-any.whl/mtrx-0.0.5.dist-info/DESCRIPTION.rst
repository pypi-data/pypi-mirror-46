MTRX
=====

A Python ToolBox for Python Programmers

website :  https://mtrx.ir/

Features
=============
 * works with Python 2.4+ and Python 3.x
 * all dates as datetime objects
 * possibility to cache results


$ pip3 install mtrx
===================

>>> import mtrx

Sending Gmail
>>> mtrx.sendgmail(username='your Gmail', password='your password', to='to gmail', text='your text')

Creating QRcode
>>> mtrx.qrcode(text='mtrx.ir', Format='svg')

Website DNS
>>> print(mtrx.dns(url='mtrx.ir'))

Your IP
>>> print(mtrx.myip())

Get Time And Date
>>> print(mtrx.timeNow())
>>> print(mtrx.dateNow())




get Information from mtrx

>>> mtrx.__author__
'Mostafa Vahedi Nejad'

>>> mtrx.__version__
'0.0.5'


