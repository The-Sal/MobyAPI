# MobyAPI Wrapper

A Python wrapper for interacting with the WW API to fetch and iterate through top picks data.

## Features

- Fetch top picks data from the WW API
- Automatic pagination handling
- Custom session management with configurable headers
- Built-in error handling for API responses


## Dependencies

- requests
- utils3

## Quick Start

```python
from mobyapi import MobyAPI

# Initialize the API client
api = MobyAPI()

# Get top picks iterator
top_picks = api.top_picks()

# Iterate through pages
for page in top_picks:
    for item in page.items:
        print(f"Title: {item.title}")
```

## Detailed Usage

### MobyAPI Class

The main class for interacting with the API.

```python
api = MobyAPI()
```

#### Methods

- `top_picks()`: Returns a TopPicksIterator for paginated access to top picks data

### TopPicksIterator

Handles pagination of top picks data.

```python
iterator = api.top_picks()
for page in iterator:
    # Process page data
    pass
```

### Custom Endpoints

You can update the API endpoints if needed (use with caution):

```python
from mobyapi import update_endpoints

new_endpoints = {
    'top-picks': 'https://new-api-url.com/endpoint'
}
update_endpoints(new_endpoints)
```

**Warning**: Only update endpoints if you know what you're doing.

## Error Handling

The wrapper includes custom exceptions:

- `MobyException`: Base exception class
- `NoMoreDataAvailable`: Raised when no more data is available or the API returns empty results

```python
try:
    for page in api.top_picks():
        # Process data
        pass
except NoMoreDataAvailable:
    print("No more data to fetch")
```

## Example

Here's a complete example that fetches top picks and counts unique companies:

```python
api = MobyAPI()
top_picks = api.top_picks()
pages = 0
total_companies = []

try:
    for page in top_picks:
        pages += 1
        print(f'Downloading Page: {pages}')
        
        for item in page.items:
            total_companies.append(item.title)
            total_companies = list(set(total_companies))
            print(f'Title: {item.title}')
            
        if pages == 3:
            break

    print(f'Total unique companies: {len(total_companies)}')
except NoMoreDataAvailable:
    print("Finished fetching data")
```

## Notes

- The API uses custom headers generated for each session
- Pagination is handled automatically by the TopPicksIterator
- Default endpoint targets the WW API's front/get_items endpoint

## Contributing

Feel free to submit issues and pull requests.

## License
Kill Yo Sef