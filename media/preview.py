from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent
TIMES=[0,2.8,5.7,7.7,9.4,11.7,15.6,18.5,23.3,26.0,29.6,31.9]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
    for theme in ['dark','light']:
        svg=(ROOT/f'experiment-{theme}.svg').read_text()
        page=browser.new_page(viewport={'width':910,'height':352},device_scale_factor=1)
        page.set_content('<html><body style="margin:0;background:#888;overflow:hidden">'+svg+'</body></html>')
        page.evaluate('document.querySelector("svg").pauseAnimations()')
        images=[]
        for i,t in enumerate(TIMES):
            page.evaluate(f'document.querySelector("svg").setCurrentTime({t})')
            page.screenshot(path=str(ROOT/f'frame-{theme}-{i:02d}.png'),clip={'x':0,'y':0,'width':900,'height':340})
            im=Image.open(ROOT/f'frame-{theme}-{i:02d}.png').convert('RGB')
            # scale contact sheet down to 450px wide per frame
            im.thumbnail((450,170),Image.Resampling.LANCZOS)
            images.append(im)
        sheet=Image.new('RGB',(900,6*196), (230,230,230))
        d=ImageDraw.Draw(sheet)
        for idx,(im,t) in enumerate(zip(images,TIMES)):
            x=(idx%2)*450;y=(idx//2)*196
            sheet.paste(im,(x,y+21))
            d.text((x+8,y+3),f'{t:04.1f}s',fill=(30,30,30))
        sheet.save(ROOT/f'contact-{theme}.png')
        print(theme,'done',ROOT/f'contact-{theme}.png')
        page.close()
    browser.close()
