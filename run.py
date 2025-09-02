from applications.list_page_scraper.run import run as run_list_page_scraper
from applications.detail_page_scraper.manager import DetailPageScraperManager
from applications.data_extractor.run import run as run_data_extractor
from ui.main import run as run_ui
from interfaces.scraper_db.websites.service import get_all_tags, get_all_names
import questionary



def get_program_to_run():
    return questionary.select(
        "Select the script to run",
        choices=[
            "list_page_scraper", 
            "detail_page_scraper", 
            "data_extractor",
            "ui"
        ]
    ).ask()


def get_run_type():
    return questionary.select(
        "Select the run type",
        choices=[
            "all", "tag", "name"
        ]
    ).ask()


def get_tag():
    return questionary.select(
        "Select the tag",
        choices=get_all_tags()
    ).ask()


def get_name():
    return questionary.select(
        "Select the name",
        choices=get_all_names()
    ).ask()


def get_continuous():
    return questionary.confirm("Run continuously?").ask()




def main():
    program = get_program_to_run()
    if program == "list_page_scraper":
        run_type = get_run_type()
        if run_type == "tag":
            tag = get_tag()
            run_list_page_scraper(run_type=run_type, tag=tag, continuous=get_continuous())
        elif run_type == "name":
            name = get_name()
            run_list_page_scraper(run_type=run_type, name=name, continuous=get_continuous())
        else:
            run_list_page_scraper(run_type=run_type, continuous=get_continuous())


    elif program == "detail_page_scraper":
        manager = DetailPageScraperManager()
        manager.run()


    elif program == "data_extractor":
        run_type = get_run_type()
        if run_type == "tag":
            tag = get_tag()
            run_data_extractor(run_type=run_type, tag=tag, continuous=get_continuous())
        elif run_type == "name":
            name = get_name()
            run_data_extractor(run_type=run_type, name=name, continuous=get_continuous())
        else:
            run_data_extractor(run_type=run_type, continuous=get_continuous())

    elif program == "ui":
        run_ui()    


if __name__ == "__main__":
    main()