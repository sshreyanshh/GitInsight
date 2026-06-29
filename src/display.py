def display_user(data):
    print(f"Name:                   {data.get('name', 'N/A')}") #N/A is the default value, will be printed if no 'name' key exists or has a None value
    print(f"Username:               {data.get('login')}")
    print(f"Public Repositories:    {data.get('public_repos')}")
    print(f"Followers:              {data.get('followers')}")
    print(f"Following:              {data.get('following')}")
    print(f"Location:               {data.get('location', 'N/A')}")
    print(f"Account created at:     {data.get('created_at', 'N/A')}")