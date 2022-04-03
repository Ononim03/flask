from requests import put, get

print(put('http://localhost:5000/api/jobs/2', json={
    'team_leader': 1,
    'job': 'job',
    'work_size': 12,
    'collaborators': '1 2 4',
    'start_date': '12.03.2015',
    'end_date': '12.04.2016',
    'is_finished': True
}).json())  # корректный запрос
print(put('http://localhost:5000/api/jobs/555', json={
    'team_leader': 123,
    'work_size': 124,
    'collaborators': '1 2 4 5',
    'start_date': '12.03.2015',
    'is_finished': False
}).json())
print(get('http://localhost:5000/api/jobs').json())
