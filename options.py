import typer
from rich.prompt import Prompt

thisdict = {
  "sort": "Ford",
  "model": "Mustang",
  "year": 1964
}
#thisdict["year"] = 2018
def main():
    sort = Prompt.ask("Sort by(1=relevance, 2=popular, 3=recent)")
    tag = Prompt.ask("Sort by(1=light, 2=simple, 3=dark)")
    print(type(sort))
    if sort == "1":
        thisdict["sort"] = "relevance"
    if sort == "2":
        thisdict["sort"] = "popular"
    if sort == "3":
        thisdict["sort"] = "recent"

    
    #print(f"sort = {sort}")
    print(thisdict)
if __name__ == "__main__":
    typer.run(main)
