import asyncio
import logging
from pathlib import Path

from playwright.async_api import BrowserContext, async_playwright


async def convert_to_pdf(context: BrowserContext, url: str):
    try:
        logging.info(f"Converting {url} to PDF")
        page = await context.new_page()
        await page.goto(url)
        filename = url.split("https://playwright.dev/python/docs/")[1].replace("/", "_") + ".pdf"
        filepath = "pdfs/" / Path(filename)
        logging.info(f"Saving {url} to {filepath}")
        await page.pdf(path=filepath)
    except Exception as e:
        logging.error(f"An error occurred while converting {url} to PDF: {e}")


async def convert_many_to_pdf():
    async with async_playwright() as playwright:
        chromium = playwright.chromium
        browser = await chromium.launch()
        context = await browser.new_context()

        urls = []
        with open("urls.txt") as file:
            urls = [line.strip() for line in file]

        async with asyncio.TaskGroup() as task_group:
            for url in urls:
                task_group.create_task(convert_to_pdf(context, url))
        await browser.close()


logging.basicConfig(level=logging.INFO)
asyncio.run(convert_many_to_pdf())
