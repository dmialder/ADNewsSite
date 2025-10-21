import yaml

def read_config(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            
            data = yaml.safe_load(file)
            return data
        
    except FileNotFoundError:
        print(f"File {file_path} not found")
        return None
    except yaml.YAMLError as exc:
        print(f"Error with reading yaml-file: {exc}")
        return None


#--------------------------------------------------------------

# returns prompt for summarizator to make news short
def get_summarization_prompt(news_text):
    
    conf = read_config("/Users/dmitryderyugin/startups/ADNews/ADNewsSite/src/adnews/analysis/config/config.yaml")
    prompt = conf["Prompts"]["summarize"] + news_text

    return prompt


# returns prompt of spheres, that news was related
def get_sphere_prompt(summ):
    
    conf = read_config("/Users/dmitryderyugin/startups/ADNews/ADNewsSite/src/adnews/analysis/config/config.yaml")
    prompt = conf["Prompts"]["spheres_1"] + summ + conf["Prompts"]["spheres_2"] + conf["Spheres"]

    return prompt


def get_advice_prompt(summ, list_s):

    conf = read_config("/Users/dmitryderyugin/startups/ADNews/ADNewsSite/src/adnews/analysis/config/config.yaml")
    prompt = conf["Prompts"]["advice_1"] + list_s + conf["Prompts"]["advice_2"] + summ

    return prompt