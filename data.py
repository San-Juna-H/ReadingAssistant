import streamlit as st
import openai
from openai import OpenAI
import pandas as pd
import random
from dotenv import load_dotenv
import os

def rewrite(example, personalized_info):

    return example