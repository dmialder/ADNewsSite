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

def get_summarization_text(news_text):
    
    conf = read_config("/Users/dmitryderyugin/startups/ADNews/ADNewsSite/src/adnews/analysis/config/config.yaml")
    text = conf["Prompts"]["summarize"] + news_text

    return text