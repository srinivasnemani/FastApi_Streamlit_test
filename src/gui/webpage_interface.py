from abc import ABC, abstractmethod
import configparser
import requests
import streamlit as st

class IWebPage(ABC):
    """
        The IWebPage class is an abstract base class that defines a common interface for all web pages.
        Attributes:
        ----------
        config: A ConfigParser object that reads the configuration file for the web page.
        session_state: A dictionary-like object that stores session data for the web page.
        Methods:

        render_the_page(): An abstract method that need to be implemented by the sub classes.
    """

    def __init__(self, config_file, session_state):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.session_state = session_state

    @abstractmethod
    def render_the_page(self):
        pass
        