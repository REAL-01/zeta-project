import json
import random
import time
from .models import MultiplayerRoom, Player

GRID_SIZE = 9

UNIT_TYPES = {
    'hq': {'cost': 0, 'hp': 100, 'dmg': [0,0], 'move': 0, 'range': 0},
    'infantry': {'cost': 15, 'hp': 15, 'dmg': [4, 6], 'move': 1, 'range': 1},
    'tank': {'cost': 40, 'hp': 40, 'dmg': [8, 12], 'move': 1, 'range': 1},
    'artillery': {'cost': 30, 'hp': 10, 'dmg': [5, 8], 'move': 1, 'range': 2},
    'air': {'cost': 50, 'hp': 20, 'dmg': [5, 8], 'move': 2, 'range': 1}
}

def has_tech(techs_str, tech_name):
    if not techs_str:
        return False
    return tech_name in techs_str.split(',')

def get_unit_stats(uclass, techs_str):
    hp = UNIT_TYPES[uclass]['hp']
    dmg = list(UNIT_TYPES[uclass]['dmg'])
    move = UNIT_TYPES[uclass]['move']
    rng = UNIT_TYPES[uclass]['range']
    
    if uclass == 'infantry':
        if has_tech(techs_str, 'inf_hp1'): hp += 5
        if has_tech(techs_str, 'inf_hp2'): hp += 10
        if has_tech(techs_str, 'inf_dmg1'): dmg[0]+=3; dmg[1]+=3
        if has_tech(techs_str, 'inf_rng'): rng += 1
    elif uclass == 'tank':
        if has_tech(techs_str, 'tnk_dmg1'): dmg[0]+=3; dmg[1]+=3
        if has_tech(techs_str, 'tnk_hp1'): hp += 15
        if has_tech(techs_str, 'tnk_dmg2'): dmg[0]+=5; dmg[1]+=5
        if has_tech(techs_str, 'tnk_hp2'): hp += 25
    elif uclass == 'artillery':
        if has_tech(techs_str, 'art_dmg1'): dmg[0]+=5; dmg[1]+=5
        if has_tech(techs_str, 'art_rng1'): rng += 1
        if has_tech(techs_str, 'art_dmg2'): dmg[0]+=8; dmg[1]+=8
        if has_tech(techs_str, 'art_mgr'): move += 1
    elif uclass == 'air':
        if has_tech(techs_str, 'air_dmg1'): dmg[0]+=4; dmg[1]+=4
        if has_tech(techs_str, 'air_hp1'): hp += 10
        if has_tech(techs_str, 'air_dmg2'): dmg[0]+=7; dmg[1]+=7
        if has_tech(techs_str, 'air_rng1'): move += 1
        
    return {'hp': hp, 'maxHp': hp, 'dmg': dmg, 'moveRange': move, 'attackRange': rng}

def get_max_units(techs_str):
    max_u = 3
    if has_tech(techs_str, 'cap1'): max_u += 1
    if has_tech(techs_str, 'cap2'): max_u += 2
    if has_tech(techs_str, 'cap3'): max_u += 3
    return max_u

def get_income_per_sec(techs_str, rank_idx=0):
    base = 3
    if has_tech(techs_str, 'eco1'): base += 1
    if has_tech(techs_str, 'eco3'): base += 2
    if has_tech(techs_str, 'eco4'): base += 3
    if rank_idx >= 10: base += 1
    return base

def init_room_state(room: MultiplayerRoom):
    # Initializes empty JSON state
    host_techs = room.host.researchedTechs if room.host else ""
    guest_techs = room.guest.researchedTechs if room.guest else ""
    
    host_hq = get_unit_stats('hq', host_techs)
    guest_hq = get_unit_stats('hq', guest_techs)
    
    # We store units in definitive server coordinates:
    # 0,0 is top-left. Host is at bottom (x=4, y=8). Guest is at top (x=4, y=0).
    uid_counter = 1
    units = [
        {
            "uid": uid_counter, "owner": "host", "uClass": "hq", "x": 4, "y": 8,
            "hp": host_hq['hp'], "maxHp": host_hq['maxHp'], "damage": host_hq['dmg'],
            "moveRange": host_hq['moveRange'], "attackRange": host_hq['attackRange'],
            "hasMoved": True, "hasAttacked": True
        },
        {
            "uid": uid_counter+1, "owner": "guest", "uClass": "hq", "x": 4, "y": 0,
            "hp": guest_hq['hp'], "maxHp": guest_hq['maxHp'], "damage": guest_hq['dmg'],
            "moveRange": guest_hq['moveRange'], "attackRange": guest_hq['attackRange'],
            "hasMoved": True, "hasAttacked": True
        }
    ]
    
    state = {
        "units": units,
        "next_uid": uid_counter + 2,
        "last_income_tick": time.time(),
        "pending_messages": []
    }
    room.game_data = json.dumps(state)
    room.save(update_fields=['game_data'])

def process_action(room: MultiplayerRoom, role: str, action: dict):
    """
    Process an action for a specific room and role ('host' or 'guest').
    Returns (success: bool, error_message: str|None)
    """
    if room.status != 'playing':
        return False, "Not playing"
        
    if room.current_turn != role and action.get("action") not in ["sync"]:
        return False, "Not your turn"

    state = json.loads(room.game_data)
    units = state.get("units", [])
    
    # passive income logic
    now_ts = time.time()
    elapsed = int(now_ts - state.get("last_income_tick", now_ts))
    
    # Both players generate income based on time elapsed
    if elapsed > 0:
        host_ps = get_income_per_sec(room.host.researchedTechs, room.host.currentRankIdx)
        guest_ps = get_income_per_sec(room.guest.researchedTechs, room.guest.currentRankIdx) if room.guest else 0
        
        room.host_gold_server += host_ps * elapsed
        room.guest_gold_server += guest_ps * elapsed
        state["last_income_tick"] = now_ts

    cmd = action.get("action")
    
    if cmd == "end_turn":
        # Reset move/attack stats for next player
        next_role = 'guest' if role == 'host' else 'host'
        room.current_turn = next_role
        for u in units:
            if u['owner'] == next_role:
                u['hasMoved'] = False
                u['hasAttacked'] = False
        state["pending_messages"].append(f"Turn passed to {next_role}")
    
    elif cmd == "hire":
        uclass = action.get("uClass")
        if uclass not in UNIT_TYPES or uclass == 'hq':
            return False, "Invalid unit type"
            
        cost = UNIT_TYPES[uclass]['cost']
        player_gold = room.host_gold_server if role == 'host' else room.guest_gold_server
        
        if player_gold < cost:
            return False, "Not enough gold"
            
        # Check Unit Cap
        current_cap = sum(1 for u in units if u['owner'] == role and u['uClass'] != 'hq')
        techs = room.host.researchedTechs if role == 'host' else room.guest.researchedTechs
        max_cap = get_max_units(techs)
        
        if current_cap >= max_cap:
            return False, "Unit capacity reached"
            
        # Find spawn coordinates
        sy_start = 8 if role == 'host' else 0
        sy_end = 7 if role == 'host' else 1
        step = -1 if role == 'host' else 1
        
        spawn_y = sy_start
        spawn_coords = None
        # X-range should be same for host (left to right 0->8) 
        # For guest, server x=8 is guest x=0 (left). So guest should iterate 8->0.
        x_range = range(GRID_SIZE) if role == 'host' else range(GRID_SIZE - 1, -1, -1)
        
        while True:
            for x in x_range:
                if not any(u['x'] == x and u['y'] == spawn_y for u in units):
                    spawn_coords = (x, spawn_y)
                    break
            if spawn_coords or spawn_y == sy_end:
                break
            spawn_y += step
            
        if not spawn_coords:
            return False, "No space to spawn"
            
        stats = get_unit_stats(uclass, techs)
        
        new_unit = {
            "uid": state["next_uid"],
            "owner": role,
            "uClass": uclass,
            "x": spawn_coords[0],
            "y": spawn_coords[1],
            "hp": stats['hp'],
            "maxHp": stats['maxHp'],
            "damage": stats['dmg'],
            "moveRange": stats['moveRange'],
            "attackRange": stats['attackRange'],
            "hasMoved": True,
            "hasAttacked": True
        }
        state["next_uid"] += 1
        units.append(new_unit)
        
        if role == 'host':
            room.host_gold_server -= cost
        else:
            room.guest_gold_server -= cost
    
    elif cmd == "move":
        uid = action.get("uid")
        target_x = action.get("target_x")
        target_y = action.get("target_y")
        
        unit = next((u for u in units if u['uid'] == uid and u['owner'] == role), None)
        if not unit: return False, "Unit not found"
        if unit['hasMoved']: return False, "Already moved"
        
        dist = max(abs(target_x - unit['x']), abs(target_y - unit['y']))
        if dist > unit['moveRange']: return False, "Out of move range"
        
        if any(u['x'] == target_x and u['y'] == target_y for u in units):
            return False, "Cell occupied"
            
        unit['x'] = target_x
        unit['y'] = target_y
        unit['hasMoved'] = True
        
    elif cmd == "attack":
        uid = action.get("uid")
        target_x = action.get("target_x")
        target_y = action.get("target_y")
        
        unit = next((u for u in units if u['uid'] == uid and u['owner'] == role), None)
        if not unit: return False, "Unit not found"
        if unit['hasAttacked']: return False, "Already attacked"
        
        target = next((u for u in units if u['x'] == target_x and u['y'] == target_y and u['owner'] != role), None)
        if not target: return False, "Valid target not found"
        
        dist = max(abs(target_x - unit['x']), abs(target_y - unit['y']))
        if dist > unit['attackRange']: return False, "Out of attack range"
        
        dmg_min, dmg_max = unit['damage']
        dmg = random.randint(dmg_min, dmg_max)
        target['hp'] -= dmg
        
        unit['hasAttacked'] = True
        
        if target['hp'] <= 0:
            units.remove(target)
            if target['uClass'] == 'hq':
                room.status = 'finished'
                state["pending_messages"].append(f"{role} DESTROYED HQ AND WON!")
    
    # Save back state
    state["units"] = units
    room.game_data = json.dumps(state)
    room.game_version += 1
    room.save()
    return True, None
