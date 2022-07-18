import pandas as pd
from serpapi import GoogleSearch
import json


params = {
  "api_key": "78838e36170ce2ee34918abe31f6e4f8d017bd99a637428ffbfea149e65e2733",
  "engine": "google_scholar",
  "hl": "en"
}


def find_articles_by_queries(queries, max_articles=1, verbose=1, **search_kwargs):
    result = pd.DataFrame(data=[], columns=['Title', 'Year', 'Journal', 'Citations', 'Url'])
    for q in queries:
        if verbose:
            print('Searching articles for ', q)

        parsed = []

        params['q'] = q
        search = GoogleSearch(params)
        results = search.get_dict()

        for res in results['organic_results']:
            title = res.get('title')
            url = res.get('link')
            if not title or not url:
                continue

            journal = '-'
            year = '-'
            summary = res.get('publication_info', {}).get('summary')
            if summary:
                try:
                    summary_parts = summary.split(' - ')
                    journal = summary_parts[-1]
                    year = summary_parts[-2].split(' ')[-1]
                except:
                    pass
            parsed.append({
                'Title': title,
                'Year': year,
                'Journal': journal,
                'Summary': summary,
                'Url': url,
            })

        if parsed:
            parsed = pd.DataFrame(parsed)
            parsed.index = [q] * len(parsed)

            result = pd.concat([result, parsed], axis=0)

    return result
