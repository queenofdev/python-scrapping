import requests

def fetch_html(url, output_file):
    response = requests.get(url)
    
    if response.status_code == 200:
        html_content = response.text

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(html_content)
    else:
        print(f"Failed to fetch page: HTTP Status Code {response.status_code}")

if __name__ == "__main__":
    url = "https://www.coindesk.com/policy/2023/11/22/digital-euro-isnt-pressing-but-work-should-continue-spanish-central-bank-governor/?_gl=1*1m3h7h4*_up*MQ..*_ga*Mzg5MDgyNDA3LjE3MDA2NTQ5NzQ.*_ga_VM3STRYVN8*MTcwMDY1NDk3My4xLjEuMTcwMDY1NjQxNi4wLjAuMA.."  # Replace with the URL you want to fetch
    output_file = "page_content.html"  # Name of the file to save HTML content
    fetch_html(url, output_file)
