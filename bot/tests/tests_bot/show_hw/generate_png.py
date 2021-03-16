import asyncio
from pyppeteer import launch
import os


async def generate_png(html_file, output):
    _HTML = os.path.dirname(os.path.realpath(__file__)) + "/" + html_file
    _OUTFILE = output
    sourcepath = 'file://' + _HTML
    browser = await launch({ "args": ['--no-sandbox'] })
    page = await browser.newPage()
    await page.goto(sourcepath)
    await page.screenshot({'path': _OUTFILE, 'fullPage': True})
    await browser.close()

    photo = open(output, 'rb')
    return photo


# asyncio.get_event_loop().run_until_complete(generate_png())