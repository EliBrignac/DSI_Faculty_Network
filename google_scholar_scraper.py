from scholarly import scholarly
import pandas as pd
import time
from tqdm import tqdm
from datetime import datetime
import concurrent.futures
import threading
import os
import psutil
import math

def initialize_csv_files(base_filename):
    """Initialize CSV files with headers"""
    # Define headers for basic info
    basic_headers = ['Name', 'Scholar ID', 'Affiliation', 'Total Citations', 
                    'H-index', 'I10-index', 'Research Interests', 'Scholar URL']
    
    # Define headers for publications
    pub_headers = ['Author Name', 'Title', 'Year', 'Citations', 'Authors', 
                  'Journal', 'Conference', 'Publisher', 'Volume', 'Issue', 
                  'Pages', 'Abstract', 'Citation URL', 'Google Scholar URL', 
                  'Publication URL', 'DOI', 'ISSN', 'ISBN', 'Publication Type', 
                  'Language']
    
    # Create empty DataFrames with headers and save them
    pd.DataFrame(columns=basic_headers).to_csv(f'{base_filename}_basic_info.csv', index=False)
    pd.DataFrame(columns=pub_headers).to_csv(f'{base_filename}_publications.csv', index=False)

def append_to_csv(data, filename, mode='a', header=False):
    """Append data to CSV file"""
    df = pd.DataFrame([data] if isinstance(data, dict) else data)
    df.to_csv(filename, mode=mode, header=header, index=False)

def get_optimal_worker_count():
    """
    Calculate the optimal number of workers based on system resources.
    Returns a number of workers that won't overwhelm the system or Google Scholar.
    """
    # Get CPU count
    cpu_count = os.cpu_count()
    
    # Get available memory (in GB)
    available_memory = psutil.virtual_memory().available / (1024 * 1024 * 1024)
    
    # Calculate workers based on CPU and memory
    cpu_based_workers = cpu_count * 2  # Traditional rule of thumb for I/O bound tasks
    memory_based_workers = math.floor(available_memory / 0.5)  # Assuming each worker needs ~500MB
    
    # Get the limiting factor
    max_workers = min(cpu_based_workers, memory_based_workers)
    
    # Cap the maximum workers to avoid overwhelming Google Scholar
    SCHOLAR_MAX_WORKERS = 16  # Maximum recommended for Google Scholar
    optimal_workers = min(max_workers, SCHOLAR_MAX_WORKERS)
    
    return max(1, optimal_workers)  # Ensure at least 1 worker

class AdaptiveThreadPool:
    """
    Thread pool that adapts to system load and rate limiting.
    """
    def __init__(self, initial_workers=None):
        self.current_workers = initial_workers or get_optimal_worker_count()
        self.lock = threading.Lock()
        self.consecutive_errors = 0
        self.error_threshold = 3
        
    def get_worker_count(self):
        """Get current worker count with rate limiting awareness"""
        with self.lock:
            return self.current_workers
    
    def handle_success(self):
        """Handle successful request"""
        with self.lock:
            self.consecutive_errors = 0
    
    def handle_error(self):
        """Handle request error and adjust workers if needed"""
        with self.lock:
            self.consecutive_errors += 1
            if self.consecutive_errors >= self.error_threshold:
                self.current_workers = max(1, self.current_workers - 1)
                self.consecutive_errors = 0
                print(f"Reducing workers to {self.current_workers} due to errors")

# Previous ThreadSafeCounter class remains the same
class ThreadSafeCounter:
    def __init__(self):
        self._lock = threading.Lock()
        self._value = 0
    
    def increment(self):
        with self._lock:
            self._value += 1
            return self._value
            
    @property
    def value(self):
        return self._value

def process_publication(args):
    """Process a single publication with rate limiting"""
    pub, author_name, counter, total, thread_pool = args
    try:
        time.sleep(0.05)  # Base rate limiting
        pub_filled = scholarly.fill(pub)
        
        pub_data = {
            'Author Name': author_name,
            'Title': pub_filled['bib'].get('title', 'N/A'),
            'Year': pub_filled['bib'].get('pub_year', 'N/A'),
            'Citations': pub_filled.get('num_citations', 0),
            'Authors': pub_filled['bib'].get('author', 'N/A'),
            'Journal': pub_filled['bib'].get('journal', 'N/A'),
            'Conference': pub_filled['bib'].get('conference', 'N/A'),
            'Publisher': pub_filled['bib'].get('publisher', 'N/A'),
            'Volume': pub_filled['bib'].get('volume', 'N/A'),
            'Issue': pub_filled['bib'].get('issue', 'N/A'),
            'Pages': pub_filled['bib'].get('pages', 'N/A'),
            'Abstract': pub_filled.get('abstract', 'N/A'),
            'Citation URL': pub_filled.get('citation_url', 'N/A'),
            'Google Scholar URL': pub_filled.get('url_scholarbib', 'N/A'),
            'Publication URL': pub_filled['bib'].get('url', 'N/A'),
            'DOI': pub_filled['bib'].get('doi', 'N/A'),
            'ISSN': pub_filled['bib'].get('issn', 'N/A'),
            'ISBN': pub_filled['bib'].get('isbn', 'N/A'),
            'Publication Type': pub_filled['bib'].get('type', 'N/A'),
            'Language': pub_filled['bib'].get('language', 'N/A')
        }
        
        thread_pool.handle_success()
        current = counter.increment()
        if current % 10 == 0:
            print(f'Processed {current}/{total} publications using {thread_pool.get_worker_count()} workers')
            
        return pub_data
    except Exception as e:
        thread_pool.handle_error()
        print(f"Error processing publication: {str(e)}")
        return None

from scholarly import scholarly
import pandas as pd
import time
from tqdm import tqdm
from datetime import datetime
import concurrent.futures
import threading
import os
import psutil
import math
import aiohttp
import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial

async def async_process_publication(pub, author_name, counter, total, thread_pool, semaphore):
    """Process a single publication with async HTTP requests"""
    async with semaphore:  # Control concurrent requests
        try:
            await asyncio.sleep(0.05)  # Non-blocking rate limiting
            
            # Create a thread for scholarly operations since it's not async-compatible
            with ThreadPoolExecutor(max_workers=1) as executor:
                loop = asyncio.get_event_loop()
                pub_filled = await loop.run_in_executor(
                    executor,
                    partial(scholarly.fill, pub)
                )
            
            pub_data = {
                'Author Name': author_name,
                'Title': pub_filled['bib'].get('title', 'N/A'),
                'Year': pub_filled['bib'].get('pub_year', 'N/A'),
                'Citations': pub_filled.get('num_citations', 0),
                'Authors': pub_filled['bib'].get('author', 'N/A'),
                'Journal': pub_filled['bib'].get('journal', 'N/A'),
                'Conference': pub_filled['bib'].get('conference', 'N/A'),
                'Publisher': pub_filled['bib'].get('publisher', 'N/A'),
                'Volume': pub_filled['bib'].get('volume', 'N/A'),
                'Issue': pub_filled['bib'].get('issue', 'N/A'),
                'Pages': pub_filled['bib'].get('pages', 'N/A'),
                'Abstract': pub_filled.get('abstract', 'N/A'),
                'Citation URL': pub_filled.get('citation_url', 'N/A'),
                'Google Scholar URL': pub_filled.get('url_scholarbib', 'N/A'),
                'Publication URL': pub_filled['bib'].get('url', 'N/A'),
                'DOI': pub_filled['bib'].get('doi', 'N/A'),
                'ISSN': pub_filled['bib'].get('issn', 'N/A'),
                'ISBN': pub_filled['bib'].get('isbn', 'N/A'),
                'Publication Type': pub_filled['bib'].get('type', 'N/A'),
                'Language': pub_filled['bib'].get('language', 'N/A')
            }
            
            thread_pool.handle_success()
            current = counter.increment()
            if current % 10 == 0:
                print(f'Processed {current}/{total} publications')
                
            return pub_data
        except Exception as e:
            thread_pool.handle_error()
            print(f"Error processing publication: {str(e)}")
            return None

async def process_publications_batch(pubs_batch, author_name, counter, total, thread_pool):
    """Process a batch of publications concurrently"""
    # Control concurrent requests with a semaphore
    semaphore = asyncio.Semaphore(thread_pool.get_worker_count() * 2)
    
    # Create tasks for all publications in the batch
    tasks = [
        async_process_publication(pub, author_name, counter, total, thread_pool, semaphore)
        for pub in pubs_batch
    ]
    
    # Run tasks concurrently and gather results
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Filter out errors and None results
    return [r for r in results if r is not None and not isinstance(r, Exception)]

def get_and_save_faculty_data(faculty_names, base_filename, fetch_detailed_pubs=False):
    """Process faculty data with async-enabled parallel publication fetching"""
    
    initialize_csv_files(base_filename)
    thread_pool = AdaptiveThreadPool()
    
    faculty_pbar = tqdm(faculty_names, desc="Processing faculty", position=0, leave=True)
    
    total_publications = 0
    processed_faculty = 0
    
    # Create event loop for async operations
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    for name in faculty_pbar:
        faculty_pbar.set_description(f"Processing faculty: {name}")
        
        try:
            search_query = scholarly.search_author(name)
            author = scholarly.fill(next(search_query))
            
            faculty_profile = {
                'Name': author['name'],
                'Scholar ID': author.get('scholar_id', 'N/A'),
                'Affiliation': author.get('affiliation', 'N/A'),
                'Total Citations': author.get('citedby', 0),
                'H-index': author.get('hindex', 0),
                'I10-index': author.get('i10index', 0),
                'Research Interests': ', '.join(author.get('interests', [])),
                'Scholar URL': f"https://scholar.google.com/citations?user={author.get('scholar_id', '')}"
            }
            
            append_to_csv(faculty_profile, f'{base_filename}_basic_info.csv')
            processed_faculty += 1
            #print(f"{name} {len(author.get('publications', []))}")
            '''
            if fetch_detailed_pubs:
                pubs_list = author.get('publications', [])
                counter = ThreadSafeCounter()
                
                # Process publications in batches using async
                batch_size = thread_pool.get_worker_count() * 4  # Larger batches for async
                for i in range(0, len(pubs_list), batch_size):
                    batch = pubs_list[i:i + batch_size]
                    results = loop.run_until_complete(
                        process_publications_batch(
                            batch, 
                            author['name'],
                            counter,
                            len(pubs_list),
                            thread_pool
                        )
                    )
                    
                    if results:
                        append_to_csv(results, f'{base_filename}_publications.csv')
                        total_publications += len(results)
            
            else:
                # Basic publication info processing remains the same
                for pub in author.get('publications', []):
                    pub_data = {
                        'Author Name': author['name'],
                        'Title': pub['bib'].get('title', 'N/A'),
                        'Year': pub['bib'].get('pub_year', 'N/A'),
                        'Citations': pub.get('num_citations', 0),
                        'Authors': pub['bib'].get('author', 'N/A'),
                        'Journal': pub['bib'].get('journal', 'N/A'),
                        'Publisher': pub['bib'].get('publisher', 'N/A')
                    }
                    append_to_csv(pub_data, f'{base_filename}_publications.csv')
                    total_publications += 1

            '''

        except StopIteration:
            faculty_pbar.write(f"No results found for: {name}")
            print(f"No results found for: {name}")
            continue
        except Exception as e:
            faculty_pbar.write(f"Error processing {name}: {str(e)}")
            print(f"Error processing {name}: {str(e)}")
            continue
    
    loop.close()
    
    final_summary = {
        'Total Faculty Processed': processed_faculty,
        'Total Publications': total_publications,
        'Final Worker Count': thread_pool.get_worker_count(),
        'Completion Time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    pd.DataFrame([final_summary]).to_csv(f'{base_filename}_summary.csv', index=False)
    
    return processed_faculty, total_publications
# Example usage
if __name__ == "__main__":


    faculty_names = pd.read_csv('ud_dsi_faculty.csv')['Name'].tolist()
    faculty_names = [name for name in faculty_names if name == name]  # Remove NaN values
    faculty_names = [name + ' University of Delaware' for name in faculty_names]
    
    base_filename = 'ud_faculty_scholar_attempt_2'
    
    print(f"Starting with {get_optimal_worker_count()} workers")
    processed_faculty, total_publications = get_and_save_faculty_data(
        faculty_names,
        base_filename,
        fetch_detailed_pubs=True
    )
    
    print(f"\nProcessing complete!")
    print(f"Total faculty processed: {processed_faculty}")
    print(f"Total publications processed: {total_publications}")