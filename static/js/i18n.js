/**
 * Zeta Project — i18n Localization Module
 * Supports EN / RU toggle. Stores preference in localStorage.
 */
(function() {
    'use strict';

    const TRANSLATIONS = {
        // ===== INDEX =====
        'index.subtitle': {
            en: 'Welcome to the next-gen web RTS.<br>Prove your tactical command skills in challenging battles against AI.',
            ru: 'Добро пожаловать в веб-РТС нового поколения.<br>Докажите свои навыки полководца в тактических сражениях с ИИ.'
        },
        'index.play': { en: 'PLAY NOW', ru: 'ИГРАТЬ' },
        'index.signin': { en: 'Sign In', ru: 'Войти в систему' },
        'index.register': { en: 'Register', ru: 'Регистрация' },

        // ===== LOGIN =====
        'login.title': { en: 'Sign In', ru: 'Вход' },
        'login.subtitle': { en: 'Commander Identification', ru: 'Идентификация Командира' },
        'login.callsign': { en: 'Callsign', ru: 'Позывной' },
        'login.accesscode': { en: 'Access Code', ru: 'Код Доступа' },
        'login.submit': { en: 'Authorize', ru: 'Авторизация' },
        'login.no_clearance': { en: 'No clearance?', ru: 'Нет допуска?' },
        'login.create_profile': { en: 'Create Profile', ru: 'Сформировать профиль' },
        'login.back_to_base': { en: 'Back to Base', ru: 'На базу' },

        // ===== REGISTER =====
        'reg.title': { en: 'Registration', ru: 'Регистрация' },
        'reg.subtitle': { en: 'Create New Commander Profile', ru: 'Создание нового профиля' },
        'reg.callsign': { en: 'Desired Callsign', ru: 'Желаемый Позывной' },
        'reg.secret': { en: 'Secret Code', ru: 'Секретный Код' },
        'reg.confirm': { en: 'Confirm Code', ru: 'Повторите Код' },
        'reg.submit': { en: 'Enlist', ru: 'Вступить в ряды' },
        'reg.has_profile': { en: 'Already have a profile?', ru: 'Уже есть профиль?' },
        'reg.signin': { en: 'Sign In', ru: 'Войти' },

        // ===== LOBBY =====
        'lobby.title': { en: 'Operations Base (Lobby) | Zeta Project', ru: 'База Операций (Лобби) | Zeta Project' },
        'lobby.hall_of_fame': { en: 'Hall of Fame', ru: 'Зал Славы' },
        'lobby.profile': { en: 'Profile', ru: 'Профиль' },
        'lobby.logout': { en: 'Logout', ru: 'Выход' },
        'lobby.home': { en: 'Home', ru: 'На Главную' },
        'lobby.register': { en: 'Register', ru: 'Регистрация' },
        'lobby.game_modes': { en: 'Game Modes', ru: 'Режимы игры' },
        'lobby.choose_mode': { en: 'Choose a mode to start the battle.', ru: 'Выберите режим, чтобы начать сражение.' },
        'lobby.single_player': { en: 'SINGLE PLAYER (vs AI)', ru: 'ОДИНОЧНАЯ ИГРА (vs ИИ)' },
        'lobby.host_pvp': { en: 'HOST PvP MATCH (Create Room)', ru: 'ПРОВЕСТИ PvP МАТЧ (Создать Комнату)' },
        'lobby.available_rooms': { en: 'Available Rooms (PvP)', ru: 'Доступные комнаты (PvP)' },
        'lobby.waiting': { en: 'Waiting for opponent...', ru: 'Ожидает противника...' },
        'lobby.join': { en: 'JOIN', ru: 'ВОЙТИ' },
        'lobby.no_rooms': { en: 'No active rooms. Be the first!', ru: 'Нет активных комнат. Будьте первыми!' },
        'lobby.status_guest': { en: 'GUEST OPERATIVE', ru: 'ГОСТЬ' },
        'lobby.status_unreg': { en: 'UNREGISTERED', ru: 'БЕЗ РЕГИСТРАЦИИ' },
        'lobby.ops_base': { en: 'OPERATIONS BASE:', ru: 'БАЗА ОПЕРАЦИЙ:' },

        // ===== PROFILE =====
        'profile.title': { en: 'Commander Profile | Zeta Project', ru: 'Профиль Командира | Zeta Project' },
        'profile.back': { en: 'Back', ru: 'Назад' },
        'profile.battle': { en: 'Battle', ru: 'В бой' },
        'profile.logout': { en: 'Logout', ru: 'Выйти' },
        'profile.home': { en: 'Home', ru: 'На Главную' },
        'profile.register': { en: 'Register', ru: 'Регистрация' },

        // ===== LEADERBOARD =====
        'lb.title': { en: 'Hall of Fame', ru: 'Зал Славы' },
        'lb.rank': { en: 'Rank', ru: 'Место' },
        'lb.commander': { en: 'Commander', ru: 'Командир' },
        'lb.wins': { en: 'Wins', ru: 'Победы' },
        'lb.winrate': { en: 'Win Rate', ru: 'Винрейт' },
        'lb.empty': { en: 'Database is empty. Be the first to write your name in history!', ru: 'База данных пуста. Запишите свое имя в историю первым!' },
        'lb.back': { en: 'Back', ru: 'Назад' },

        // ===== SIMULATOR =====
        'sim.tactical_mode': { en: 'TACTICAL MODE', ru: 'ТАКТИЧЕСКИЙ РЕЖИМ' },
        'sim.your_turn': { en: 'Your Turn!', ru: 'Ваш ход!' },
        'sim.opponent_turn': { en: "Opponent's turn...", ru: 'Сейчас ходит соперник...' },
        'sim.turn_ended': { en: 'Turn ended.', ru: 'Вы завершили ход.' },
        'sim.battle_started': { en: 'Battle started!', ru: 'Битва началась!' },
        'sim.hire_title': { en: 'Unit Recruitment', ru: 'Найм Юнитов' },
        'sim.tech_title': { en: 'Engineering (Tech Tree)', ru: 'Инженерия (Древо Технологий)' },
        'sim.close': { en: 'Close', ru: 'Закрыть' },
        'sim.recruit': { en: 'Recruit', ru: 'Нанять' },
        'sim.no_recruit_enemy_turn': { en: "You cannot recruit during opponent's turn!", ru: 'Вы не можете нанимать войска во время чужого хода!' },
        'sim.no_tech_enemy_turn': { en: 'Engineering is only available on your turn!', ru: 'Инженерия доступна только в ваш ход!' },
        'sim.new_rank': { en: 'New rank:', ru: 'Новое звание:' },
        'sim.max': { en: 'MAX', ru: 'МАКС' },
        'sim.enemy_destroyed': { en: 'destroyed!', ru: 'уничтожен!' },
        'sim.unit_fallen': { en: 'has fallen!', ru: 'пал в бою!' },
        'sim.defeat_hq': { en: 'Defeat! Your HQ has fallen.', ru: 'Поражение! Ваш Штаб пал.' },
        'sim.victory_hq': { en: 'Victory! Enemy HQ destroyed.', ru: 'Победа! Вражеский Штаб уничтожен.' },
        'sim.defeat': { en: 'Defeat', ru: 'Поражение' },
        'sim.victory': { en: 'Victory!', ru: 'Победа!' },
        'sim.victory_overlay': { en: 'VICTORY', ru: 'ПОБЕДА' },
        'sim.defeat_overlay': { en: 'DEFEAT', ru: 'ПОРАЖЕНИЕ' },
        'sim.match_finished': { en: 'Match finished!', ru: 'Матч завершен!' },
        'sim.waiting_commander': { en: 'Waiting for second Commander...', ru: 'Ожидание подключения второго Командира...' },
        'sim.deploy_units': { en: 'Deploy Base Units', ru: 'Развернуть юнитов' },
        'sim.tech_lab': { en: 'Tech Laboratory', ru: 'Инженерия' },
        'sim.dmg': { en: 'DMG', ru: 'Урон' },
        'sim.all_units_ready': { en: 'Your turn! All units are ready.', ru: 'Ваш ход! Можете управлять всеми войсками.' },
        'sim.enemy_dealt': { en: 'dealt', ru: 'нанес вам' },
        'sim.damage': { en: 'damage!', ru: 'ед. урона!' },
        'sim.advanced_attacked': { en: 'advanced and attacked!', ru: 'подошел и атаковал!' },
        'sim.turn': { en: 'Turn', ru: 'Ход' },
        'sim.reset': { en: 'Reset', ru: 'Сброс' },
        'sim.lobby': { en: 'Lobby', ru: 'Лобби' },
        'sim.profile': { en: 'Profile', ru: 'Профиль' },

        // ===== RANKS =====
        'rank.0': { en: 'Private', ru: 'Рядовой' },
        'rank.1': { en: 'Corporal', ru: 'Ефрейтор' },
        'rank.2': { en: 'Jr. Sergeant', ru: 'Мл. Сержант' },
        'rank.3': { en: 'Sergeant', ru: 'Сержант' },
        'rank.4': { en: 'Sr. Sergeant', ru: 'Ст. Сержант' },
        'rank.5': { en: 'Master Sgt.', ru: 'Старшина' },
        'rank.6': { en: 'Warrant Off.', ru: 'Прапорщик' },
        'rank.7': { en: 'Sr. Warrant', ru: 'Ст. Прапорщик' },
        'rank.8': { en: 'Jr. Lieutenant', ru: 'Мл. Лейтенант' },
        'rank.9': { en: 'Lieutenant', ru: 'Лейтенант' },
        'rank.10': { en: 'Sr. Lieutenant', ru: 'Ст. Лейтенант' },
        'rank.11': { en: 'Captain', ru: 'Капитан' },
        'rank.12': { en: 'Major', ru: 'Майор' },
        'rank.13': { en: 'Lt. Colonel', ru: 'Подполковник' },
        'rank.14': { en: 'Colonel', ru: 'Полковник' },
        'rank.15': { en: 'Brig. General', ru: 'Генерал-Майор' },
        'rank.16': { en: 'Lt. General', ru: 'Генерал-Лейтенант' },
        'rank.17': { en: 'General', ru: 'Генерал-Полковник' },
        'rank.18': { en: 'Army General', ru: 'Генерал Армии' },
        'rank.19': { en: 'Generalissimus', ru: 'Генералиссимус' },

        // ===== UNITS =====
        'unit.hq': { en: 'HQ', ru: 'Штаб' },
        'unit.infantry': { en: 'Infantry', ru: 'Пехота' },
        'unit.tank': { en: 'Tank', ru: 'Танк' },
        'unit.artillery': { en: 'Artillery', ru: 'Артиллерия' },
        'unit.air': { en: 'Air Force', ru: 'Авиация' },

        // ===== TECH TREE =====
        'tech.eco1': { en: 'Warehouses', ru: 'Склады' }, 'tech.eco1.d': { en: '+1 Resources/sec', ru: '+1 Ресурса/сек' },
        'tech.eco2': { en: 'Convoys', ru: 'Конвои' }, 'tech.eco2.d': { en: 'Starting Resources +50', ru: 'Старт. Ресурсы +50' },
        'tech.eco3': { en: 'Factories', ru: 'Заводы' }, 'tech.eco3.d': { en: '+2 Resources/sec', ru: '+2 Ресурса/сек' },
        'tech.eco4': { en: 'MIC', ru: 'ВПК' }, 'tech.eco4.d': { en: '+3 Resources/sec', ru: '+3 Ресурса/сек' },
        'tech.cap1': { en: 'Comm Hub', ru: 'Коммутатор' }, 'tech.cap1.d': { en: 'Upgrade 1: +1 Unit Cap', ru: 'Улучшение 1: +1 Лимит' },
        'tech.cap2': { en: 'Radio Tower', ru: 'Радиовышка' }, 'tech.cap2.d': { en: 'Upgrade 2: +2 Unit Cap', ru: 'Улучшение 2: +2 Лимит' },
        'tech.cap3': { en: 'Satellite', ru: 'Спутник' }, 'tech.cap3.d': { en: 'Upgrade 3: +3 Unit Cap', ru: 'Улучшение 3: +3 Лимит' },
        'tech.inf_hp1': { en: 'Armor', ru: 'Броня' }, 'tech.inf_hp1.d': { en: '+5 HP Infantry', ru: '+5 HP Пехоте' },
        'tech.inf_dmg1': { en: 'Gear', ru: 'Снаряжение' }, 'tech.inf_dmg1.d': { en: 'Infantry DMG +3', ru: 'Урон пехоты +3' },
        'tech.inf_hp2': { en: 'Exoskeleton', ru: 'Экзоскелет' }, 'tech.inf_hp2.d': { en: '+10 HP Infantry', ru: '+10 HP Пехоте' },
        'tech.inf_rng': { en: 'Optics', ru: 'Оптика' }, 'tech.inf_rng.d': { en: 'Infantry Range +1', ru: 'Дальность Пехоты +1' },
        'tech.tnk_dmg1': { en: 'Ammo', ru: 'Снаряды' }, 'tech.tnk_dmg1.d': { en: 'Tank DMG +3', ru: 'Урон Танков +3' },
        'tech.tnk_hp1': { en: 'Armor T-1', ru: 'Броня Т-1' }, 'tech.tnk_hp1.d': { en: 'Tank HP +15', ru: 'HP Танков +15' },
        'tech.tnk_dmg2': { en: 'Plasma', ru: 'Плазма' }, 'tech.tnk_dmg2.d': { en: 'Tank DMG +5', ru: 'Урон Танков +5' },
        'tech.tnk_hp2': { en: 'Tracks', ru: 'Траки' }, 'tech.tnk_hp2.d': { en: 'Tank HP +25', ru: 'HP Танков +25' },
        'tech.art_dmg1': { en: 'Guidance', ru: 'Наведение' }, 'tech.art_dmg1.d': { en: 'Artillery DMG +5', ru: 'Урон Арты +5' },
        'tech.art_rng1': { en: 'Barrels', ru: 'Стволы' }, 'tech.art_rng1.d': { en: 'Artillery Range +1', ru: 'Дальность Арты +1' },
        'tech.art_dmg2': { en: 'HE Rounds', ru: 'Фугас' }, 'tech.art_dmg2.d': { en: 'Artillery DMG +8', ru: 'Урон Арты +8' },
        'tech.art_mgr': { en: 'Chassis', ru: 'Шасси' }, 'tech.art_mgr.d': { en: 'Artillery Move +1', ru: 'Шаг Арты +1' },
        'tech.air_dmg1': { en: 'Guns', ru: 'Пулеметы' }, 'tech.air_dmg1.d': { en: 'Air DMG +4', ru: 'Урон Авиа +4' },
        'tech.air_hp1': { en: 'Flares', ru: 'Ловушки' }, 'tech.air_hp1.d': { en: 'Air HP +10', ru: 'HP Авиа +10' },
        'tech.air_dmg2': { en: 'A-G Missiles', ru: 'Ракеты В-З' }, 'tech.air_dmg2.d': { en: 'Air DMG +7', ru: 'Урон Авиа +7' },
        'tech.air_rng1': { en: 'Afterburner', ru: 'Форсаж' }, 'tech.air_rng1.d': { en: 'Air Move +1', ru: 'Шаг Авиа +1' },

        // ===== TECH TREE COLUMNS =====
        'tech.col.supply': { en: 'Supply', ru: 'Снабжение' },
        'tech.col.structure': { en: 'Structure', ru: 'Структура' },
        'tech.col.infantry': { en: 'Infantry', ru: 'Пехота' },
        'tech.col.tanks': { en: 'Tanks', ru: 'Танки' },
        'tech.col.artillery': { en: 'Artillery', ru: 'Артиллерия' },
        'tech.col.air': { en: 'Air Force', ru: 'Авиация' },

        // ===== BACKEND ERROR MESSAGES (used by data-i18n) =====
        'err.passwords_mismatch': { en: 'Passwords do not match', ru: 'Пароли не совпадают' },
        'err.password_short': { en: 'Access code must be at least 6 characters', ru: 'Код доступа должен быть не менее 6 символов' },
        'err.callsign_taken': { en: 'Callsign already taken', ru: 'Позывной уже занят' },
        'err.bad_login': { en: 'Invalid login or password', ru: 'Неверный логин или пароль' },
    };

    // Expose globally for the simulator JS to use
    window.ZETA_I18N = TRANSLATIONS;

    function getLang() {
        return localStorage.getItem('zeta_lang') || 'en';
    }

    function setLang(lang) {
        localStorage.setItem('zeta_lang', lang);
    }

    function t(key) {
        const entry = TRANSLATIONS[key];
        if (!entry) return key;
        return entry[getLang()] || entry['en'] || key;
    }

    // Expose t() globally
    window.t = t;
    window.zetaGetLang = getLang;
    window.zetaSetLang = setLang;

    function applyTranslations() {
        const lang = getLang();
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            const entry = TRANSLATIONS[key];
            if (entry) {
                if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                    el.placeholder = entry[lang] || entry['en'];
                } else {
                    el.innerHTML = entry[lang] || entry['en'];
                }
            }
        });
        // Update page title if present
        const titleEl = document.querySelector('[data-i18n-title]');
        if (titleEl) {
            const key = titleEl.getAttribute('data-i18n-title');
            const entry = TRANSLATIONS[key];
            if (entry) document.title = entry[lang] || entry['en'];
        }
        // Translate rank badges (data-i18n-rank="0" -> rank.0)
        document.querySelectorAll('[data-i18n-rank]').forEach(el => {
            const idx = el.getAttribute('data-i18n-rank');
            const key = 'rank.' + idx;
            const entry = TRANSLATIONS[key];
            if (entry) el.textContent = entry[lang] || entry['en'];
        });
    }

    function createToggleButton() {
        const btn = document.createElement('button');
        btn.id = 'lang-toggle';
        btn.style.cssText = `
            position: fixed;
            bottom: 15px;
            right: 15px;
            z-index: 99999;
            background: rgba(19, 20, 24, 0.85);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(0, 180, 216, 0.3);
            color: #00B4D8;
            font-family: 'Space Grotesk', monospace;
            font-weight: 700;
            font-size: 0.8rem;
            padding: 8px 14px;
            border-radius: 8px;
            cursor: pointer;
            letter-spacing: 1px;
            text-transform: uppercase;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
            display: flex;
            align-items: center;
            gap: 6px;
        `;

        function updateLabel() {
            const lang = getLang();
            btn.innerHTML = lang === 'en'
                ? '<i class="fa-solid fa-globe" style="font-size:0.9rem;"></i> EN → RU'
                : '<i class="fa-solid fa-globe" style="font-size:0.9rem;"></i> RU → EN';
        }

        btn.addEventListener('mouseenter', () => {
            btn.style.background = 'rgba(0, 180, 216, 0.15)';
            btn.style.borderColor = '#00B4D8';
            btn.style.boxShadow = '0 0 20px rgba(0, 180, 216, 0.3)';
        });
        btn.addEventListener('mouseleave', () => {
            btn.style.background = 'rgba(19, 20, 24, 0.85)';
            btn.style.borderColor = 'rgba(0, 180, 216, 0.3)';
            btn.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.4)';
        });

        btn.addEventListener('click', () => {
            const newLang = getLang() === 'en' ? 'ru' : 'en';
            setLang(newLang);
            updateLabel();
            applyTranslations();
            // Dispatch event for simulator to pick up
            window.dispatchEvent(new CustomEvent('zeta-lang-change', { detail: { lang: newLang } }));
        });

        updateLabel();
        document.body.appendChild(btn);
    }

    // Init on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => { applyTranslations(); createToggleButton(); });
    } else {
        applyTranslations();
        createToggleButton();
    }
})();
