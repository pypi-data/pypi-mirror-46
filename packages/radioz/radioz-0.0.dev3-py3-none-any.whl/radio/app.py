from radio.core.log import logger

from radio.tui import App

application = App()


def main():
    logger.info("init app")
    application.run()
