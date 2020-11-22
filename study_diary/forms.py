from django import forms
from .models import User, Diary, Monthly
 # 장고에서 기본적으로 지원하는 forms import
 # Blog 모델 가져오기 (models.py)
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class CreateUser(forms.ModelForm):
    repassword = forms.CharField(
        label = 'Password Check',
        widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'style': 'width: 50%', 'placeholder': '비밀번호 확인'}
        )
    )
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'repassword']
        widgets = {
                    'id': forms.TextInput(
                        attrs={'label':'ID', 'class': 'form-control', 'style': 'width: 50%', 'placeholder' : '아이디'}
                    ),
                    'name': forms.TextInput(
                        attrs={'label':'Name', 'class': 'form-control', 'style': 'width: 50%', 'placeholder' : '이름'}
                    ),
                    'email':forms.EmailInput(
                        attrs={'class': 'form-control', 'style': 'width: 50%', 'placeholder': '이메일'}
                    ),
                    'password':forms.PasswordInput(
                         attrs={'class': 'form-control', 'style': 'width: 50%', 'placeholder': '비밀번호'}
                    ),
                }


class CreateDiary(forms.ModelForm):
    class Meta:
        model = Diary
 
        fields = ['date', 'title', 'is_public', 'content'] 
        # fields = '__all__' : 모든 필드를 가져오겠다

# 블로그 생성
# 장고에서는 Meta 클래스는 내부 클래스로 활용, 기본 필드의 값을 재정의할 때 사용
# Blog 클래스로부터 모델을 가져오고 그 중 'title', 'author', 'body' 가져오는 것

        CHOICES=((2,'공개'),
                 (1, '친구만'),
                 (0,'나만'))

        widgets = {
                    'date': forms.DateInput(
                        attrs={'type':'date'}
                    ),
                    'title': forms.TextInput(
                        attrs={'class': 'form-control', 'style': 'width: 55%; height:30px', 'placeholder': '제목을 입력하세요.'}
                    ),
                    'is_public': forms.RadioSelect(
                        attrs={'label':'private', 'style':'list-style-type: none'}, choices=CHOICES
                    ),
                    # 'author': forms.Select(
                    #     attrs={'class': 'custom-select'},
                    # ),
                    'content': forms.CharField(widget=CKEditorUploadingWidget()),
                }

# widgets 을 지정하면, 장고에서 자체적으로 제공하는 폼의 형태 빌려올 수 있음
# attrs : 폼에 적용되는 css의 class

class CreateMonthly(forms.ModelForm):
    class Meta:
        model = Monthly
        fields = ['date', 'content']
        widgets = {
                    'date': forms.DateInput(
                        attrs={'type':'date'}
                    ),                    
                    'content': forms.TextInput(
                        attrs={'label':'일정 내용', 'class': 'form-control', 'style': 'width: 50%'}
                    )
        }
