from random import choice

with open('applications/list_page_scraper/utils/user_agents.txt', 'r') as f:
    user_agents = f.readlines()

def get_user_agent():
    #return choice(user_agents).strip()
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    

