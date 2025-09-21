from scrap_site import WikipediaScraper
import ollama
import time


URL = 'https://wikipedia.org'
MODEL = "llama3.2"
SYSTEM_PROMPT = "You are an expert summarizer. Summarize Wikipedia articles into clear, concise summaries while keeping main facts.Ignore reference markers like [1], [23], or “[citation needed]”. Focus only on the factual content but start with the content title. "

search = input("What do you want to research about?: ")
scraper = WikipediaScraper()
result =  scraper.parse_site(site_url=URL, search=search)
print(f"{result}\n\n")
time.sleep(5)
scraper.close()

USER_PROMPT = f"Summarize this Wikipedia article into bullet points, highlighting the most important facts and ideas. Do not include citation markers like [23]:\n\n{result}"


msg = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT}
        ]

response = ollama.chat(model=MODEL,
                       messages=msg) 
print(response['message']['content'])
