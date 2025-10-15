from scraper import scrape_jobs

if __name__ == "__main__":
    print("🚀 Starting scraper...")
    jobs = scrape_jobs(max_pages=5, location_encoded="Minneapolis%2C+MN")
    print(f"\n✅ Done! Found {len(jobs)} new jobs.")
    for j in jobs:
        print("\n---")
        print(j)
