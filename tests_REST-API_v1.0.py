from requests import post, delete, get

print(post('http://localhost:5000/api/v2/users', json={
    'surname': 'surname',
    'name': 'name',
    'age': 15,
    'position': 'position',
    'speciality': 'speciality',
    'address': 'address',
    'email': 'email0',
    'password': 'password'
}).json())  # корректный запрос
print(post('http://localhost:5000/api/v2/users', json={
    'surname': 'surname',
    'name': 'name',
    'age': '15o',
    'position': 'position',
    'speciality': 'speciality',
    'address': 'address',
    'email': 'email1',
    'password': 'password'
}).json())
print(post('http://localhost:5000/api/v2/users', json={
    'surname': 'surname',
    'name': 'name',
    'age': 15,
    'position': 'position',
    'speciality': 'speciality',
    'address': 'address',
    'email': 'email0',
    'password': 'password'
}).json())

print(delete('http://localhost:5000/api/v2/users/1').json())
print(delete('http://localhost:5000/api/v2/users/-5').json())
print(delete('http://localhost:5000/api/v2/users/four').json())
print(get('http://localhost:5000/api/v2/users').json())
print(get('http://localhost:5000/api/v2/users/1').json())
print(get('http://localhost:5000/api/v2/users/999').json())
