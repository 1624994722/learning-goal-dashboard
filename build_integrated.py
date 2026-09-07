# -*- coding: utf-8 -*-
"""整合构建脚本：landing/index.html + src/index.html -> integrated/index.html
阶段1 骨架重构 + 阶段2 暗色设计系统 + 阶段3 逻辑平移 + 阶段4 UI整合 + 阶段5 动效融合
"""
import io, re

WS = r"C:/Users/Zachary/WorkBuddy/2026-08-25-19-02-47"
app = io.open(WS + "/src/index.html", encoding="utf-8").read()
land = io.open(WS + "/landing/index.html", encoding="utf-8").read()

# ============ 1. 提取并暗色化 app CSS ============
css = re.search(r'<style[^>]*>(.*?)</style>', app, re.S).group(1)

# 1a. 类名防冲突：app .hero -> .app-hero（landing 也用 .hero）
css = css.replace('.hero-inner', '.app-hero-inner').replace('.hero-chips', '.app-hero-chips')
css = re.sub(r'\.hero(?=[\{ :,\.\[])', '.app-hero', css)

# 1b. :root 暗色 token（阶段2：三等阶 #050505/#101010/#1a1a1a + 语义色暗色变体）
root_map = [
    ('--bg:#f7f4ec;', '--bg:#0a0a0a;'),
    ('--card:#ffffff;', '--card:#141414;'),
    ('--ink:#1d1b18;', '--ink:#fafafa;'),
    ('--ink-2:#57544d;', '--ink-2:#a7a6a6;'),
    ('--ink-3:#7a766d;', '--ink-3:#8b8a8a;'),
    ('--line:#e9e5da;', '--line:rgba(255,255,255,.10);'),
    ('--brand:#1a1a1a;', '--brand:#fafafa;'),
    ('--brand-2:#3f3d38;', '--brand-2:#e5e5e5;'),
    ('--green:#047857;', '--green:#34d399;'),
    ('--red:#dc2626;', '--red:#f87171;'),
    ('--amber:#92400e;', '--amber:#fbbf24;'),
    ('--shadow:0 1px 2px rgba(29,27,24,.05),0 6px 24px -8px rgba(29,27,24,.10);',
     '--shadow:0 1px 2px rgba(0,0,0,.4),0 6px 24px -8px rgba(0,0,0,.5);'),
    ('--shadow-lg:0 8px 40px -8px rgba(26,26,26,.30);', '--shadow-lg:0 8px 40px -8px rgba(0,0,0,.6);'),
]
for old, new in root_map:
    assert old in css, "root var missing: " + old
    css = css.replace(old, new)

# 1c. 全局颜色映射（hex 用边界保护，rgba 精确替换）
HEX_MAP = {
    '#fbfaf6': '#181818',
    '#efece3': 'rgba(255,255,255,.08)',
    '#eae6db': 'rgba(255,255,255,.08)',
    '#d8d2c4': 'rgba(255,255,255,.25)',
    '#f3f0e7': 'rgba(255,255,255,.06)',
    '#e8f6f0': 'rgba(52,211,153,.16)',
    '#a7f3d0': '#6ee7b7',
    '#047857': '#34d399',
    '#dc2626': '#f87171',
    '#b45309': '#fbbf24',
    '#92400e': '#fbbf24',
    '#fee2e2': 'rgba(248,113,113,.14)',
    '#fecaca': 'rgba(248,113,113,.40)',
    '#fef2f2': 'rgba(248,113,113,.08)',
    '#fff5f5': 'rgba(248,113,113,.06)',
    '#fffbeb': 'rgba(251,191,36,.08)',
    '#fffdf5': 'rgba(251,191,36,.06)',
    '#fde68a': 'rgba(251,191,36,.45)',
    '#fef3c7': 'rgba(251,191,36,.12)',
    '#faecd7': 'rgba(251,191,36,.10)',
    '#ecfdf5': 'rgba(52,211,153,.10)',
    '#f0fdf4': 'rgba(52,211,153,.10)',
    '#f0fdf9': 'rgba(52,211,153,.10)',
    '#d1fae5': 'rgba(52,211,153,.22)',
    '#e0dcd0': 'rgba(255,255,255,.16)',
    '#e6e1d6': 'rgba(255,255,255,.10)',
    '#e8e4d9': 'rgba(255,255,255,.10)',
    '#f5f2ea': 'rgba(255,255,255,.04)',
    '#f8f6ef': 'rgba(255,255,255,.04)',
    '#ece7db': 'rgba(255,255,255,.06)',
    '#1a1a1a': '#fafafa',
    '#f7f4ec': '#050505',
    '#1d1b18': '#fafafa',
}
for old, new in sorted(HEX_MAP.items(), key=lambda x: -len(x[0])):
    css = re.sub(re.escape(old) + r'(?![0-9a-fA-F])', new, css)

RGBA_MAP = {
    'rgba(29,27,24,.05)': 'rgba(255,255,255,.05)',
    'rgba(29,27,24,.07)': 'rgba(255,255,255,.07)',
    'rgba(29,27,24,.10)': 'rgba(255,255,255,.10)',
    'rgba(29,27,24,.14)': 'rgba(255,255,255,.14)',
    'rgba(29,27,24,.15)': 'rgba(255,255,255,.15)',
    'rgba(29,27,24,.30)': 'rgba(0,0,0,.50)',
    'rgba(29,27,24,.35)': 'rgba(255,255,255,.35)',
    'rgba(26,26,26,.22)': 'rgba(250,250,250,.25)',
    'rgba(26,26,26,.28)': 'rgba(255,255,255,.28)',
    'rgba(26,26,26,.30)': 'rgba(0,0,0,.50)',
    'rgba(26,26,26,.45)': 'rgba(250,250,250,.45)',
    'rgba(26,26,26,.72)': 'rgba(250,250,250,.72)',
    'rgba(26,26,26,0)': 'rgba(250,250,250,0)',
    'rgba(20,19,16,.35)': 'rgba(0,0,0,.50)',
    'rgba(20,19,16,.45)': 'rgba(0,0,0,.55)',
    'rgba(20,19,16,.5)': 'rgba(0,0,0,.55)',
    'rgba(20,19,16,.3)': 'rgba(0,0,0,.45)',
    'rgba(247,244,236,.92)': 'rgba(5,5,5,.85)',
    'rgba(247,244,236,.96)': 'rgba(5,5,5,.90)',
    'rgba(180,83,9,.18)': 'rgba(251,191,36,.18)',
}
for old, new in RGBA_MAP.items():
    css = css.replace(old, new)

# ============ 2. 提取 app 业务 markup（header/nav/main/modal/toast） ============
h_start = app.index('<header data-page-node-id="6EHATWQEwusOLKlMBvB10b" class="hero">')
h_end = app.index('</main>') + len('</main>')
appbody = app[h_start:h_end]

# nav 移出 header（吸顶 Tab 条需要挂在 workspace 流内）
nav_start = appbody.index('<nav ')
nav_end = appbody.index('</nav>') + len('</nav>')
nav_html = appbody[nav_start:nav_end]
appbody = appbody[:nav_start] + appbody[nav_end:]

# 类名同步改名
appbody = appbody.replace('class="hero"', 'class="app-hero"')
appbody = appbody.replace('class="hero-inner"', 'class="app-hero-inner"')
appbody = appbody.replace('class="hero-chips"', 'class="app-hero-chips"')

# modal + toast
m_start = app.index('<div data-page-node-id="o5ssLuQvjKYnyCUIs0hDBs"')
t_start = app.index('<div data-page-node-id="tdfKGguHRMIuuH90fkepnp"')
t_end = app.index('</div>', t_start) + len('</div>')
modal_toast = app[m_start:t_end]

# ============ 3. 提取 app 脚本并打暗色补丁 ============
scripts = re.findall(r'<script[^>]*>(.*?)</script>', app, re.S)
app_main = [s for s in scripts if 'DATABASE_ID' in s][0]
app_anim = [s for s in scripts if 'GSAP_URLS' in s][0]

# 3a. 目标配色板 -> 暗色变体
app_main = re.sub(
    r'var COLORS = \[[^\]]+\];',
    'var COLORS = ["#fafafa","#fbbf24","#34d399","#38bdf8","#a8a29e","#f87171","#fb923c","#2dd4bf"];',
    app_main, count=1)
# 3b. 旧数据颜色迁移表（亮色值 -> 暗色值）
app_main = re.sub(
    r'COLOR_MIG\s*=\s*\{[^}]+\}',
    'COLOR_MIG = {"#6366f1":"#fafafa","#8b5cf6":"#a8a29e","#1a1a1a":"#fafafa","#f59e0b":"#fbbf24","#10b981":"#34d399","#0ea5e9":"#38bdf8","#78716c":"#a8a29e","#ef4444":"#f87171","#f97316":"#fb923c","#14b8a6":"#2dd4bf","#047857":"#34d399","#dc2626":"#f87171","#92400e":"#fbbf24"}',
    app_main, count=1)
# 3c. JS 内旧亮色值全局替换（statCard 图标色、种子数据等）
JS_HEX = {
    '#1a1a1a': '#fafafa', '#f59e0b': '#fbbf24', '#10b981': '#34d399',
    '#0ea5e9': '#38bdf8', '#78716c': '#a8a29e', '#ef4444': '#f87171',
    '#f97316': '#fb923c', '#14b8a6': '#2dd4bf', '#efece3': 'rgba(255,255,255,.10)',
}
for old, new in JS_HEX.items():
    app_main = re.sub(re.escape(old) + r'(?![0-9a-fA-F])', new, app_main)

# 3d. 动效脚本里的 hero 选择器同步改名
app_anim = app_anim.replace('.hero-inner', '.app-hero-inner')

# ============ 4. landing 骨架重构（阶段1） ============
# 4a. CSS：解除整页滚动锁定
land = land.replace(
    'html,body{ height:100%; overflow:hidden; background:var(--bg); }',
    'html{ scroll-behavior:smooth; }\nhtml,body{ min-height:100%; background:var(--bg); }')
land = land.replace(
    '.stage{\n  position:fixed; inset:0; overflow:hidden;',
    '.stage{\n  position:relative; height:100vh; min-height:560px; overflow:hidden;')
land = land.replace(
    '.stage{ display:flex; flex-direction:column; }',
    '.stage{ display:flex; flex-direction:column; height:100vh; height:100dvh; min-height:560px; }')

# 4b. landing 主区 <main class="hero"> -> <section class="hero">（避免与 app main 冲突）
land = land.replace('<main class="hero">', '<section class="hero">', 1)
land = land.replace('</main>', '</section>', 1)

# 4c. logos 条从 stage 拆出 -> 页尾
lg_start = land.index('<div class="logos">')
tail = land[lg_start:]
close_pos = tail.index('\n  </div>\n\n</div>')
logos_block = tail[:close_pos + len('\n  </div>')]
land = land[:lg_start] + tail[close_pos + len('\n  </div>'):]

# 4d. CTA / 导航接线（阶段4）
land = land.replace('<a class="pill pill-nav" href="#">', '<a class="pill pill-nav" href="#workspace">')
land = land.replace('<a class="pill pill-cta" href="#">', '<a class="pill pill-cta" href="#workspace">')
land = land.replace('<a class="ghost" href="#">View Architecture</a>',
                    '<a class="ghost" href="#workspace" data-goto="board">View Architecture</a>')
land = land.replace('<a href="#">About</a>', '<a href="#workspace">About</a>')
land = land.replace('<a href="#">Features</a>', '<a href="#workspace" data-goto="board">Features</a>')
land = land.replace('<a href="#">FAQ</a>', '<a href="#workspace" data-goto="weekly">FAQ</a>')
land = land.replace('<a href="#">Contact</a>', '<a href="#workspace" data-goto="mine">Contact</a>')
land = land.replace('<a class="pill" href="#"><span>Get Started</span></a>',
                    '<a class="pill" href="#workspace"><span>Get Started</span></a>')

# ============ 5. 整合覆盖 CSS（阶段2/4/5） ============
OVERRIDES = """
/* ============ 整合覆盖：工作台暗色 + 布局中和 ============ */
body{font-family:'Manrope',system-ui,-apple-system,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;background:#050505;color:var(--ink)}
@media(min-width:1024px){body{display:block !important}}
.workspace{position:relative;z-index:1;background:#050505}
.app-hero{background:linear-gradient(135deg,#101010 0%,#1a1712 58%,#26211a 100%)}
.nav{position:sticky !important;top:0;bottom:auto !important;left:auto !important;right:auto !important;z-index:30;max-width:760px;margin:0 auto;padding:10px 14px;background:rgba(5,5,5,.78) !important;backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border-top:none !important;border-bottom:1px solid rgba(255,255,255,.08)}
.nav-inner{background:rgba(255,255,255,.07) !important;flex-direction:row !important}
.nav button{color:#b6b5b5 !important}
.nav button.active{background:#fafafa !important;color:#050505 !important}
@media(min-width:1024px){
  .app-hero{position:static !important;height:auto !important;overflow:hidden}
  .app-hero-inner{min-height:0 !important;padding:36px 24px 30px !important}
  .nav button{flex:1;justify-content:center !important}
  main{grid-column:auto !important;max-width:1180px;margin-left:auto !important;margin-right:auto !important}
  .footer{grid-column:auto !important;max-width:1180px;margin-left:auto !important;margin-right:auto !important}
}
.pomo-glass{background:linear-gradient(165deg,rgba(255,255,255,.12) 0%,rgba(255,255,255,.04) 100%) !important;border-color:rgba(255,255,255,.16) !important}
.modal-mask{background:rgba(0,0,0,.66) !important}
.toast{z-index:60 !important}
.modal-mask{z-index:50 !important}
.site-footer{padding:64px 24px 48px;background:#050505;border-top:1px solid rgba(255,255,255,.06)}
.site-footer .logos{position:static;transform:none;width:auto;height:auto;display:flex;justify-content:center;align-items:center;gap:44px;flex-wrap:wrap;color:var(--strip);pointer-events:auto}
.site-footer .lg{position:static;display:flex;align-items:center;gap:8px;animation:none}
.site-footer .lg svg{width:22px;height:auto}
.site-footer .lg .word{position:static;font-size:14px}
.site-note{text-align:center;color:#5a5959;font-size:12px;margin-top:26px;font-family:'Manrope',sans-serif}
@media(max-width:640px){.site-footer .logos{gap:22px}}
"""
land = land.replace('</style>', OVERRIDES + '</style>')

# app CSS 注入（landing CSS 之后、覆盖块之前已在上一行插入 overrides；app css 放 landing css 后）
# 注意顺序：landing css -> app css -> overrides 已在 </style> 前，现把 app css 插到 OVERRIDES 前
land = land.replace(OVERRIDES + '</style>',
                    '\n/* ============ 工作台样式（暗色化） ============ */\n' + css + '\n' + OVERRIDES + '</style>')

# ============ 6. 组装 body ============
workspace = ('\n<section class="workspace" id="workspace">\n'
             + appbody + '\n' + nav_html + '\n</section>\n')
footer = ('\n<footer class="site-footer">\n' + logos_block
          + '\n<p class="site-note">学习目标管理台 · The Next Layer of Intelligence</p>\n</footer>\n')

# 插到 stage 关闭 </div> 之后、landing <script> 之前
script_pos = land.index('<script>')
land = land[:script_pos] + workspace + footer + modal_toast + '\n' + land[script_pos:]

# ============ 7. 组装脚本 ============
INTEG_JS = """
<script>
/* ============ 整合接线：锚点 + Tab 激活 ============ */
(function(){
  document.querySelectorAll('[data-goto]').forEach(function(a){
    a.addEventListener('click', function(){
      var tab = a.getAttribute('data-goto');
      setTimeout(function(){
        if(typeof window.switchTab === 'function') window.switchTab(tab);
      }, 80);
    });
  });
})();
</script>
"""
land = land.replace('</body>',
                    '<script>' + app_main + '</script>\n'
                    '<script>' + app_anim + '</script>\n'
                    + INTEG_JS + '</body>')

# app 云端同步绑定属性挂到 body
land = land.replace('<body>',
                    '<body data-sp-bindable="database" data-sp-database-id="00Gdjo9cPxyffcHKABtKPG">', 1)

# app 的 workbuddy 运行时注入（相对路径，非 workbuddy 环境 404 无害）
land = land.replace('<link rel="preconnect" href="https://fonts.googleapis.com">',
                    '<script src="/page/page_comm/inject.js"></script>\n<link rel="preconnect" href="https://fonts.googleapis.com">', 1)

out = WS + "/integrated/index.html"
import os
os.makedirs(WS + "/integrated", exist_ok=True)
io.open(out, "w", encoding="utf-8").write(land)
print("written:", out, len(land), "bytes")

# 自检
checks = {
    'workspace section': 'id="workspace"' in land,
    'app main script': 'DATABASE_ID' in land,
    'anim script': 'GSAP_URLS' in land,
    'burger js': "getElementById('burger')" in land,
    'integration js': 'data-goto' in land,
    'footer logos': 'site-footer' in land,
    'no fixed stage': 'position:fixed; inset:0; overflow:hidden' not in land,
    'hero renamed': 'class="app-hero"' in land,
    'single main tag': land.count('<main') == 1 and land.count('</main>') == 1,
    'sp binding': 'data-sp-database-id' in land,
}
for k, v in checks.items():
    print(('OK ' if v else 'FAIL ') + k)
