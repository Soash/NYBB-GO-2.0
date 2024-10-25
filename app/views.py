from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from .models import Team


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def quiz1(request):
    if request.method == 'POST':
        submitted_code = request.POST.get('UnlockKey')
        if submitted_code == '2504':
            if hasattr(request.user, 'team'):
                team = request.user.team
                if team.quiz_1_status == False:
                    team.score += 100 
                team.quiz_1_status = True
                team.log += f"Quiz 1 Solved at UTC {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}<br>"
                team.save()
                return redirect(quiz2)
        else:
            return render(request, 'quiz1.html', {'error_message': 'Incorrect code entered!'})
    return render(request, 'quiz1.html')


@login_required
def quiz2(request):
    if request.user.team.quiz_1_status == True:
        if request.method == 'POST':
            submitted_code = request.POST.get('UnlockKey')
            if submitted_code == '12q23.2':
                if hasattr(request.user, 'team'):
                    team = request.user.team
                    if team.quiz_2_status == False:
                        team.score += 100 
                    team.quiz_2_status = True
                    team.log += f"Quiz 2 Solved at UTC {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}<br>"
                    team.save()
                    return redirect(quiz3) 
            else:
                return render(request, 'quiz2.html', {'error_message': 'Incorrect code entered!'})
            
        return render(request, 'quiz2.html')
  
    return redirect('quiz1')


@login_required
def quiz3(request):
    if request.user.team.quiz_2_status == True:
        if request.method == 'POST':
            submitted_code = request.POST.get('UnlockKey')
            if submitted_code == '373':
                if hasattr(request.user, 'team'):
                    team = request.user.team
                    if team.quiz_3_status == False:
                        team.score += 100
                    team.quiz_3_status = True
                    team.log += f"Quiz 3 Solved at UTC {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}<br>"
                    team.save()
                    return redirect(quiz4)
            else:
                return render(request, 'quiz3.html', {'error_message': 'Incorrect code entered!'})

        return render(request, 'quiz3.html')
    
    return redirect('quiz2')


@login_required
def quiz4(request):
    if request.user.team.quiz_3_status == True:
        if request.method == 'POST':
            submitted_code = request.POST.get('UnlockKey')
            if submitted_code == '1953':
                if hasattr(request.user, 'team'):
                    team = request.user.team
                    if team.quiz_4_status == False:
                        team.score += 105
                    team.quiz_4_status = True
                    team.log += f"Quiz 4 Solved at UTC {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}<br>"
                    team.save()
                    return redirect(quiz5)
                
        team = request.user.team
        team.score -= 5
        team.save()
        return render(request, 'quiz4.html')
    
    return redirect('quiz3')


@login_required
def quiz5(request):
    if request.user.team.quiz_4_status == True:
        if request.method == 'POST':
            submitted_code = request.POST.get('UnlockKey').lower()
            if submitted_code == 'crispr':
                if hasattr(request.user, 'team'):
                    team = request.user.team
                    if team.quiz_5_status == False:
                        team.score += 100
                    team.quiz_5_status = True
                    team.log += f"Quiz 5 Solved at UTC {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}<br>"
                    team.save()
                    return redirect('quiz6')
            return render(request, 'quiz5.html', {'error_message': 'Incorrect code entered!'})
        return render(request, 'quiz5.html')
    return redirect('quiz4')


@login_required
def quiz6(request):
    if request.user.team.quiz_5_status == True:
        if request.method == 'POST':
            submitted_code = request.POST.get('UnlockKey')
            if submitted_code == '2':
                if hasattr(request.user, 'team'):
                    team = request.user.team
                    if team.quiz_6_status == False:
                        team.score += 100
                    team.quiz_6_status = True
                    team.log += f"Quiz 6 Solved at UTC {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}<br>"
                    team.time = timezone.now()
                    team.save()
                    return redirect('congrats')
            else:
                if hasattr(request.user, 'team'):
                    team = request.user.team
                    team.score -= 50
                    team.save()
                    return render(request, 'quiz6.html', {'error_message': 'Incorrect code entered!'})
        return render(request, 'quiz6.html')
    return redirect('quiz5')


@login_required
def congrats(request):
    if request.user.team.quiz_6_status == True:
        return render(request, 'congrats.html')
    return redirect('quiz6')


@login_required
def b_ecoli(request):
    return render(request, 'b_ecoli.html')


# @login_required
# def b_lplant(request):
#     return render(request, 'b_lplant.html')
 

@login_required
def update_score(request):
    if request.method == 'POST':
        team = request.user.team
        team.score -= 10
        team.save()
        return JsonResponse({'status': 'success'})
    return redirect('index')



def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password!")
            return render(request, 'signin.html')

    return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':
        # print("ok")
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            messages.success(request, "Registration successful. Check your email for login details.")
            return redirect('signin')
        else:
            messages.error(request, "There was an error with your registration.")
    else:
        signup_form = SignUpForm()
    
    return render(request, 'signup.html', {'form': signup_form})

@login_required
def signout(request):
    logout(request)
    return redirect('signin')

def result(request):
    teams = Team.objects.all()
    return render(request, 'result.html', {'teams': teams})

def custom_404_page(request, exception):
    return render(request, '404.html', status=404)


