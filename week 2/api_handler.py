import requests
import globals


def get_api(repo, page):
    # Function to communicate using GET requests with github

    print("get_api() is called with params: "+repo)

    # repo variable should be validated
    query_url = f"https://api.github.com/{repo}"

    params = {
        "Accept": "application/vnd.github+json",
        'state': 'all',
        "per_page": 500,  # Set the pagination limit , actually its 100 by default from GH,
        "page": page
    }
    # Please add the Token,
    headers = {'Authorization': f'token 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'}
    response = None
    if (int(globals.calls_left) > 0):
        response = requests.get(query_url, headers=headers, params=params)
        response_headers = response.headers
        remaining_calls = response_headers['X-RateLimit-Remaining']
        print(remaining_calls)
        globals.calls_left = remaining_calls

    return response


def get_pr_reviews_list(repo, pr_number):
    response = get_api('repos/'+repo+'/pulls/'+pr_number+'/reviews', 1)
    print(response.status_code)
    return response.json()


def get_pr_reviews_list(repo, pr_number):
    response = get_api('repos/'+repo+'/pulls/'+pr_number+'/reviews', 1)
    print(response.status_code)
    return response.json()


def get_pr(repo, pr_number):
    response = get_api('repos/'+repo+'/pulls/'+pr_number, 1)
    return response.json()


def get_pr_comments_list(repo, pr_number):
    response = get_api('repos/'+repo+'/pulls/'+pr_number+'/comments', 1)
    print(response.status_code)
    return response.json()

def get_pr_commits_list(repo, pr_number):
    response = get_api('repos/'+repo+'/pulls/'+pr_number+'/commits', 1)
    print(response.status_code)
    return response.json()


def get_repo(repo, pr_number):
    response = get_api('repos/'+repo, 1)
    print(response.status_code)
    return response.json()
