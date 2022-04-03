from requests import post, delete, get

print(post('http://localhost:5000/api/v2/jobs', json={
    'team_leader': 1,
    'job': 'job',
    'work_size': 12,
    'collaborators': '1 2 4',
    'start_date': '12.03.2015',
    'is_finished': False
}).json())  # корректный запрос
print(post('http://localhost:5000/api/v2/jobs', json={
    'team_leader': 123,
    'work_size': 124,
    'collaborators': '1 2 4 5',
    'start_date': '12.03.2015',
    'is_finished': False
}).json())

print(delete('http://localhost:5000/api/v2/jobs/1').json())
print(delete('http://localhost:5000/api/v2/jobs/-5').json())
print(delete('http://localhost:5000/api/v2/jobs/four').json())
print(get('http://localhost:5000/api/v2/jobs').json())
print(get('http://localhost:5000/api/v2/jobs/1').json())
print(get('http://localhost:5000/api/v2/jobs/999').json())
