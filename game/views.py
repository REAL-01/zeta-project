import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Player

def index_view(request):
    return render(request, 'game/index.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if username and password:
            if password != password_confirm:
                return render(request, 'game/register.html', {'error': 'Пароли не совпадают'})
            if len(password) < 6:
                return render(request, 'game/register.html', {'error': 'Код доступа должен быть не менее 6 символов'})
            if Player.objects.filter(username=username).exists():
                return render(request, 'game/register.html', {'error': 'Позывной уже занят'})
            
            user = Player.objects.create_user(username=username, password=password, role='user')
            login(request, user)
            return redirect('lobby')
    return render(request, 'game/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('lobby')
        else:
            return render(request, 'game/login.html', {'error': 'Неверный логин или пароль'})
    return render(request, 'game/login.html')

from django.views.decorators.http import require_POST

@require_POST
def logout_view(request):
    logout(request)
    return redirect('index')

def play_view(request):
    mode = request.GET.get('mode', 'single')
    room_id = request.GET.get('room')
    
    if request.user.is_authenticated:
        role = 'single'
        if mode == 'multiplayer':
            if not room_id:
                return redirect('lobby')
            from .models import MultiplayerRoom
            try:
                room = MultiplayerRoom.objects.get(id=room_id)
                if request.user != room.host and request.user != room.guest:
                    return redirect('lobby')
                role = 'host' if request.user == room.host else 'guest'
            except MultiplayerRoom.DoesNotExist:
                return redirect('lobby')

        context = {
            'is_guest': False,
            'player_xp': request.user.playerXp,
            'current_rank_idx': request.user.currentRankIdx,
            'lightbulbs': request.user.lightbulbs,
            'gold': request.user.playerGold,
            'techs': request.user.researchedTechs,
            'username': request.user.username,
            'mode': mode,
            'room_id': room_id,
            'role': role,
        }
        return render(request, 'game/simulator.html', context)
    else:
        games_played = request.session.get('guest_games_played', 0)
        if games_played >= 1:
            return redirect('register')
        
        context = {
            'is_guest': True,
            'player_xp': 0,
            'current_rank_idx': 0,
            'lightbulbs': 0,
            'gold': 50,
            'techs': '',
            'username': 'Гость',
            'mode': 'single',
            'room_id': None,
            'role': 'single',
        }
        return render(request, 'game/simulator.html', context)

@login_required
def profile_view(request):
    ranks = [
        ("Рядовой", "1_private.png"), ("Ефрейтор", "2_efreytor.png"), ("Мл. Сержант", "3_jsergeant.png"), 
        ("Сержант", "4_sergeant.png"), ("Ст. Сержант", "5_ssergeant.png"), ("Старшина", "6_starshina.png"), 
        ("Прапорщик", "7_praporshik.png"), ("Ст. Прапорщик", "8_spraporshik.png"), ("Мл. Лейтенант", "9_jleytenant.png"), 
        ("Лейтенант", "10_leytenant.png"), ("Ст. Лейтенант", "11_sleytenant.png"), ("Капитан", "12_captain.png"), 
        ("Майор", "13_major.png"), ("Подполковник", "14_jcolonel.png"), ("Полковник", "15_colonel.png"), 
        ("Генерал-Майор", "16_genmaj.png"), ("Генерал-Лейтенант", "17_genliet.png"), ("Генерал-Полковник", "18_gencol.png"), 
        ("Генерал Армии", "19_genarmy.png"), ("Генералиссимус", "20_generalisimus.png")
    ]
    
    idx = request.user.currentRankIdx
    if idx < 0: idx = 0
    if idx >= len(ranks): idx = len(ranks) - 1
        
    rank_name, rank_icon = ranks[idx]
    win_rate = 0
    if request.user.games_played > 0:
        win_rate = int((request.user.wins / request.user.games_played) * 100)
        
    from .models import MultiplayerRoom
    MultiplayerRoom.objects.filter(host=request.user, status='waiting').delete()

    context = {
        'user': request.user,
        'rank_name': rank_name,
        'rank_icon': rank_icon,
        'win_rate': win_rate
    }
    return render(request, 'game/profile.html', context)

@login_required
def custom_admin_view(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('index')
    
    players = Player.objects.all().order_by('-games_played')
    context = {
        'players': players
    }
    return render(request, 'game/custom_admin.html', context)

def api_save_game(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if request.user.is_authenticated:
                # XP и Bulbs клиент инкрементит корректно от базы, поэтому используем дельту
                xp_diff = data.get('xp', request.user.playerXp) - request.user.playerXp
                bulbs_diff = data.get('bulbs', request.user.lightbulbs) - request.user.lightbulbs
                rank_id = data.get('rankIdx', request.user.currentRankIdx)

                if xp_diff > 2000 or bulbs_diff > 500 or rank_id > request.user.currentRankIdx + 2:
                    return JsonResponse({'status': 'error', 'message': 'Anti-cheat trigger'}, status=400)

                request.user.playerXp += max(0, xp_diff)
                request.user.lightbulbs += max(0, bulbs_diff)
                request.user.currentRankIdx = rank_id
                request.user.researchedTechs = data.get('techs', request.user.researchedTechs)
                
                killed = data.get('enemies_killed', 0)
                if 0 <= killed <= 50:
                    request.user.enemies_destroyed += killed
                    request.user.playerGold += killed * 20 # 20 meta-gold per kill
                
                ended = data.get('ended', False)
                won = data.get('won', False)
                
                if ended:
                    request.user.games_played += 1
                    if won:
                        request.user.wins += 1
                        request.user.playerGold += 150 # Победный бонус
                    else:
                        request.user.losses += 1
                        request.user.playerGold += 35  # Утешительный бонус
                
                request.user.save()
            else:
                ended = data.get('ended', False)
                if ended:
                    request.session['guest_games_played'] = request.session.get('guest_games_played', 0) + 1

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'invalid method'}, status=405)

@login_required
def lobby_view(request):
    from .models import MultiplayerRoom
    from django.utils import timezone
    import datetime
    
    MultiplayerRoom.objects.filter(host=request.user, status='waiting').delete()
    
    time_threshold = timezone.now() - datetime.timedelta(seconds=10)
    rooms = MultiplayerRoom.objects.filter(status='waiting', updated_at__gte=time_threshold).exclude(host=request.user)
    
    ranks = [("Рядовой", "1_private.png"), ("Ефрейтор", "2_efreytor.png"), ("Мл. Сержант", "3_jsergeant.png"), 
             ("Сержант", "4_sergeant.png"), ("Ст. Сержант", "5_ssergeant.png"), ("Старшина", "6_starshina.png"), 
             ("Прапорщик", "7_praporshik.png"), ("Ст. Прапорщик", "8_spraporshik.png"), ("Мл. Лейтенант", "9_jleytenant.png"), 
             ("Лейтенант", "10_leytenant.png"), ("Ст. Лейтенант", "11_sleytenant.png"), ("Капитан", "12_captain.png"), 
             ("Майор", "13_major.png"), ("Подполковник", "14_jcolonel.png"), ("Полковник", "15_colonel.png"), 
             ("Генерал-Майор", "16_genmaj.png"), ("Генерал-Лейтенант", "17_genliet.png"), ("Генерал-Полковник", "18_gencol.png"), 
             ("Генерал Армии", "19_genarmy.png"), ("Генералиссимус", "20_generalisimus.png")]
    idx = request.user.currentRankIdx
    if idx < 0: idx = 0
    if idx >= len(ranks): idx = len(ranks) - 1
    rank_name, _ = ranks[idx]

    return render(request, 'game/lobby.html', {'rooms': rooms, 'rank_name': rank_name})

@login_required
def api_mp_create(request):
    from .models import MultiplayerRoom
    if request.method == 'POST':
        MultiplayerRoom.objects.filter(host=request.user, status='waiting').delete()
        room = MultiplayerRoom.objects.create(host=request.user, status='waiting')
        return redirect(f'/play/?mode=multiplayer&room={room.id}')
    return redirect('lobby')

from django.db import transaction

@login_required
@transaction.atomic
def api_mp_join(request, room_id):
    from .models import MultiplayerRoom
    if request.method == 'POST':
        try:
            room = MultiplayerRoom.objects.select_for_update().get(id=room_id, status='waiting')
            room.guest = request.user
            room.status = 'playing'
            room.save()
            request.session['role'] = 'guest'
            return redirect(f'/play/?mode=multiplayer&room={room.id}')
        except MultiplayerRoom.DoesNotExist:
            return redirect('lobby')
    return redirect('lobby')

@login_required
def api_mp_sync(request, room_id):
    from .models import MultiplayerRoom
    try:
        room = MultiplayerRoom.objects.get(id=room_id)
        is_host = request.user == room.host
        is_guest = request.user == room.guest
        
        if not (is_host or is_guest):
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
            
        role = 'host' if is_host else 'guest'

        if request.method == 'GET':
            room.save(update_fields=['last_activity'])

            return JsonResponse({
                'status': 'success',
                'room_status': room.status,
                'current_turn': room.current_turn,
                'game_data': room.game_data,
                'guest_joined': room.guest is not None
            })
            
        elif request.method == 'POST':
            if room.current_turn != role:
                return JsonResponse({'status': 'error', 'message': 'Not your turn'}, status=400)
                
            data = json.loads(request.body)
            room.game_data = data.get('game_data', '{}')
            room.current_turn = 'guest' if role == 'host' else 'host'
            
            if data.get('finished'):
                room.status = 'finished'
                
            room.save()
            return JsonResponse({'status': 'success'})
            
    except MultiplayerRoom.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Room not found'}, status=404)

