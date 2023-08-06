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
===================

>>> mtrx.sendgmail(username='your Gmail', password='your password', to='to gmail', text='your text')
'Sending Gmail'

>>> mtrx.qrcode(text='mtrx.ir', Format='svg')
'Creating QRcode'

>>> print(mtrx.dns(url='mtrx.ir'))
'Website DNS'

>>> print(mtrx.myip())
Your IP


>>> print(mtrx.timeNow())
>>> print(mtrx.dateNow())
'Get Time And Date'



get Information from mtrx

>>> mtrx.__author__
'Mostafa Vahedi Nejad'

>>> mtrx.__version__
'0.0.5'


