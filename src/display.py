def display_user(data):
    print(f"Name:                   {data.get('name', 'N/A')}") #N/A is the default value, will be printed if no 'name' key exists or has a None value
    print(f"Username:               {data.get('login')}")
    print(f"Public Repositories:    {data.get('public_repos')}")
    print(f"Followers:              {data.get('followers')}")
    print(f"Following:              {data.get('following')}")
    print(f"Location:               {data.get('location', 'N/A')}")
    print(f"Account created at:     {data.get('created_at', 'N/A')}")

def display_repos(repoList):
    if not repoList:
        print("User does not have any repository.")
        return
    
    sortedData = sorted(repoList, key = lambda x: x['stargazers_count'], reverse = True)
    
    print(f"\nTotal Repositories: {len(sortedData)} \n")
    print('-' * 65)
    print(
        "Repositories".ljust(30) + 
        "Language".ljust(15) + 
        "Stars".rjust(10) + 
        "Forks".rjust(10)
    )
    print('-' * 65)

    for repo in sortedData:
        name = repo.get('name')
        lang = repo.get('language') or "N/A" #when first arg is None (false), or evaluates second argument
        stars = str(repo.get('stargazers_count'))
        fork = str(repo.get('forks'))

        print(
            name.ljust(30) + 
            lang.ljust(15) + 
            stars.rjust(10) + 
            fork.rjust(10)
        )