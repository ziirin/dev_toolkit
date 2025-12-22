from jinja2 import Environment, FileSystemLoader

def send_week_report(data_file: str) -> bool:
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('week_report.html')