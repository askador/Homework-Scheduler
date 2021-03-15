import asyncio
from pyppeteer import launch
import pyppeteer
import os


async def generate_png(html_file="test.html"):
    _HTML = os.path.dirname(os.path.realpath(__file__)) + "/" + html_file
    _OUTFILE = "dz.png"
    sourcepath = 'file://' + _HTML
    browser = await launch({ "args": ['--no-sandbox'] })
    page = await browser.newPage()
    await page.goto(sourcepath)
    await page.screenshot({'path': _OUTFILE, 'fullPage': True})
    await browser.close()

    photo = open('dz.png', 'rb')
    return photo

