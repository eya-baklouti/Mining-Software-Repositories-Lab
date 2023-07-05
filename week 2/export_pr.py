import datetime
import requests
import pandas as pd
import globals
import api_handler
import unidiff
from datetime import datetime


def export_repo_pr(repo, output_name):

    # Following this documentation https://docs.github.com/en/rest/pulls/comments?apiVersion=2022-11-28
    # Function to get the pull requests from a repo, just provide the repository name
    # Should give back a json of the response

    page = 1
    pull_requests_list = []
    print("get_repo_pr() is called with params: "+repo)
    # While loop to get all the PRs in all the pages in one JSON to be parsed.

    while True:
        print('started while')
        # Make the API request
        response = api_handler.get_api('repos/'+repo+'/pulls', page)

        # If the response status code is not 200, break the loop
        if response.status_code != 200:
            break

        # Parse the response JSON and append the pull requests to the list
        pull_requests_list += response.json()

        # If the number of pull requests returned is less than 100, we've reached the end
        print('response len(response.json())'+str(len(response.json())))

        if len(response.json()) < 100:
            break

        # Increment the page number
        page += 1
        print('page'+str(page))

    df = pd.DataFrame(columns=["PR_Number", "title", "state",
                      "description", "comment_body", "review_body", "classifications"])
    rows = []

    counter = 0
    print(len(pull_requests_list))
    # Checking if there are still more pages
    for pull_request in pull_requests_list:
        counter += 1

        pr_number = pull_request['number']
        title = pull_request['title']
        state = pull_request['state']

        review_body = ''
        review_state = ''
        comment_body = ''
        # Call API to get list of reviews and comments
        reviews = api_handler.get_pr_reviews_list(
            repo, str(pull_request['number']))

        comments = api_handler.get_pr_comments_list(
            repo, str(pull_request['number']))

        # concatinate both values together to be added as one line
        for review in reviews:
            review_body = review_body + '\n' + review['body']
            review_state = review_state + '\n' + review['state']

        for comment in comments:
            comment_body = comment_body+'\n' + comment['body']

        if not (review_body == '' and review_state == '' and comment_body == ''):
            rows.append({
                "PR_Number": pr_number,
                "title": title,
                "state": state,
                "review_body": review_body,
                "review_state": review_state,
                "comment_body": comment_body,
            })

    print(counter)
    df = pd.DataFrame(rows)
    df.to_excel(output_name+'.xlsx', index=False)


def export_features(repo, output_name):

    # Following this documentation https://docs.github.com/en/rest/pulls/comments?apiVersion=2022-11-28
    # Function to get the pull requests from a repo, just provide the repository name
    # Should give back a json of the response

    page = 1
    pull_requests_list = []
    print("export_features() is called with params: "+repo)
    # While loop to get all the PRs in all the pages in one JSON to be parsed.

    while True:
        print('started while')
        # Make the API request
        response = api_handler.get_api('repos/'+repo+'/pulls', page)

        # If the response status code is not 200, break the loop
        if response.status_code != 200:
            break

        # Parse the response JSON and append the pull requests to the list
        pull_requests_list += response.json()

        # If the number of pull requests returned is less than 100, we've reached the end
        print('response len(response.json())'+str(len(response.json())))

        if len(response.json()) < 100:
            break

        # Increment the page number
        page += 1
        print('page '+str(page))

    current_repo = api_handler.get_repo(repo, page)
    repo_created_at = current_repo["created_at"]

    df = pd.DataFrame(columns=[
        "PR_Number", "num_commits", "merged_date",
        "added_lines", "deleted_lines", "changed_lines", "num_files",
        "reviews_num", "comments_num", "commits_word_count", "is_merged"])
    rows = []

    counter = 0
    print(len(pull_requests_list))
    # Checking if there are still more pages
    for pull_request in pull_requests_list:
        counter += 1
        pr_number = pull_request['number']
        current_pr = api_handler.get_pr(repo, str(pr_number))

        # Define features needed
        num_commits = 0
        added_lines = 0
        deleted_lines = 0
        changed_lines = 0
        num_files = 0
        reviews_num = 0
        comments_num = 0
        is_merged = False
        commits_word_count = 0

        is_merged = current_pr['merged']

        # Num of commits
        num_commits = current_pr["commits"]

        # Num of lineschanged
        # Num of fies changed
        # is_merged
        # Age
        # num of comments

        diff_url = current_pr["diff_url"]
        diff_response = requests.get(diff_url)
        # Process the diff in the source code
        if diff_response.status_code == 200:
            diff = unidiff.PatchSet(diff_response.text)
            num_files = len(diff)
            for file in diff:
                for hunk in file:
                    for line in hunk:
                        if line.is_added:
                            added_lines += 1
                        elif line.is_removed:
                            deleted_lines += 1
                        elif line.is_context:
                            changed_lines += 1

            # Print the for each PR!

        # Call API to get list of reviews
        reviews = api_handler.get_pr_reviews_list(
            repo, str(pull_request['number']))
        reviews_num = len(reviews)

        comments = api_handler.get_pr_comments_list(
            repo, str(pull_request['number']))
        comments_num = len(comments)

        commits = api_handler.get_pr_commits_list(
            repo, str(pull_request['number']))
        for commit in commits:
            commits_word_count += len(commit['commit']['message'].split())
        print(str(commits_word_count) + ' is words count in commits_word_count')
        pull_request_created_at = current_pr["created_at"]

        pull_request_created_at_date = datetime.strptime(
            pull_request_created_at, "%Y-%m-%dT%H:%M:%SZ")
        repo_created_at_date = datetime.strptime(
            repo_created_at, "%Y-%m-%dT%H:%M:%SZ")

        age = (
            pull_request_created_at_date - repo_created_at_date).days
        print(
            f"The pull request has been open for {age} days since the repository creation.")

        rows.append({"PR_Number": pr_number,
                    "num_commits": num_commits,
                     "age": age,
                     "added_lines": added_lines,
                     "deleted_lines": deleted_lines,
                     "changed_lines": changed_lines,
                     "num_files": num_files,
                     "reviews_num": reviews_num,
                     "comments_num": comments_num,
                     "commits_word_count": commits_word_count,
                     "is_merged": is_merged
                     })

    print(counter)
    df = pd.DataFrame(rows)
    df.to_excel(output_name+'.xlsx', index=False)
