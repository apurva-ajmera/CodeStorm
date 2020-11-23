# CodeStorm-Competitve Programming Website
competitive programming website like geeksforgeeks and hackerrank etc.

This project developed on django framework.Where you can find articles on basic data structure like Stack,Queue,Tree and algorithms like Sorting,Greedy and Dynamic programming.Each
article contain related question which was asked in product based companies.And to solve these problems there is also online ide where you can write your code in c or c++.

<h2>Installation of django ace editor<h2>
<pre>
    pip install django-ace
</pre>

<h4>For apply text highlights and mode</h4>
For apply text highlighting like whenever you write code text is shows in different color and if you type wrong syntax cross sign is highlighted

To do this you have to copy django_ace folder which is present in given path:

<pre>
  CodeStorm/practice/static/django_ace
</pre>

and paste it into your static folder of your project directory

<h2>
 Showing mode, marker and other feature in your django-ace editor
</h2>

If you want to show mode(select language to code), error marker, language tools etc then you need to copy below folder and paste it into that directory where you want to show your ace editor.

Here ace editor used in practice folder therefore this folder(named as scripts) pasted into practice folder

<pre>
  CodeStorm/practice/scripts
</pre>

For saving code of user you have to make one database which store user's code, who write the code and date. Here this database named as Snippet.

<h2>
  Rendering django-ace editor as a form
</h2>

Taking a user's code as input declare a form with required fields and also render your ace editor.For rendering a ace editor show below code and paste it into your forms.py file.

<pre>
  from .models import Snippet
  from django import forms
  from django_ace import AceWidget


  class SnippetForm(forms.ModelForm):
      class Meta:
          model = Snippet
          widgets = {
              "text": AceWidget(mode='c_cpp', theme='twilight',wordwrap=False, width='100%', height='400px',fontsize="20px", toolbar=True, showprintmargin=True),
          }
          exclude = ()
</pre>  

Whenever users submit their code you have to copy that code into one file with required extension so here in practice folder you find one folder named as files where you can find file named as program.cpp.

When user submit the code it just take the code from your database and paste it into this file.

<h2>
 compile and run program from django-ace editor
</h2>

Performing compilation and run operation you need one module which is subprocess. Through suprocess module you can write cmd(command prompt) commands in your python files. See Below code:

<pre>
  p1 = subprocess.run('g++ practice/files/program.cpp -o practice/files/program.exe',capture_output=True,text=True,shell = False)
        if(p1.stderr):
            result_compiler = str(p1.stderr,"UTF-8")
            return render(request,"practice/practice_online.html",{"form":form,"result":result_compiler})
        else:
            p2 = subprocess.run('practice/files/program.exe',input=input_data,capture_output=True,shell=False)
            return render(request, "practice/practice_online.html", {
                "form": form,
                "snippets": Snippet.objects.first(),"result":p2.stdout.decode("UTF-8")
            })
</pre>   

For running a program you have to insert inputs in input parameter. This parameter takes the input means if you write program for addition of two numbers so this will take two numbers as an input.

<h2>Deployment to AWS,GCP OR Azure etc.</h2>

If you want to deploy this project then you need a compiler. In this project we use only c and c++ language so you can download GCC compiler for this project and then add your 
TDM-GCC-64 folder(this folder exists in C: drive) and paste it into that directory where you want to prform compilation and run a program. Here we compile and run a program into practice folder. Now you have to edit subprocess.run() line in your views.py file. 

<pre>
  p1 = subprocess.run('/TDM-GCC-64/bin/g++.exe filename.cpp -o filename.exe', capture_output=True, text=True, shell=false)
</pre>

Above line find the g++.exe file from TDM-GCC-64 folder and then it will execute and take the filename.cpp file to compile and make filename.exe file
