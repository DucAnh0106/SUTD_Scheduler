from bs4 import BeautifulSoup
import unicodedata

def is_week_empty(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
    except Exception as e:
        print(f"Error parsing: {e}")
        return False

    rows = soup.find_all('tr')[1:] 
    for row in rows:
        cells = row.find_all('td')
        if len(cells) == 8:
            day_cells = cells[1:]
        elif len(cells) == 7:
            day_cells = cells
        else:
            continue

        for cell in day_cells:
            text = cell.get_text()
            normalized_text = unicodedata.normalize("NFKD", text)
            clean_text = normalized_text.strip()
            if clean_text:
                return False 
    return True
