from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.jobs import Jobs

parser = reqparse.RequestParser()
parser.add_argument('team_leader', required=True, type=int)
parser.add_argument('job', required=True, type=str)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('collaborators', required=True, type=str)
parser.add_argument('start_date', required=True, type=str)
parser.add_argument('end_date', type=str)
parser.add_argument('is_finished', required=True, type=bool)


class JobsResource(Resource):
    def get(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        return jsonify({'jobs': jobs.to_dict(rules=('-user', '-user.jobs'))})

    def delete(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(jobs_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': item.to_dict(rules=('-user', '-user.jobs')) for item in jobs})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        if 'id' in args and session.query(Jobs).get(args['id']):
            return jsonify({'error': 'Id already exists.'})
        new_job = Jobs()
        if 'id' in args:
            new_job.id = args['id']
        if 'team_leader' in args:
            new_job.team_leader = args['team_leader']
        if 'job' in args:
            new_job.job = args['job']
        if 'work_size' in args:
            new_job.work_size = args['work_size']
        if 'collaborators' in args:
            new_job.collaborators = args['collaborators']
        if 'start_date' in args:
            new_job.start_date = args['start_date']
        if 'end_date' in args:
            new_job.end_date = args['end_date']
        if 'is_finished' in args:
            new_job.is_finished = args['is_finished']
        session.add(new_job)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_jobs_not_found(jobs_id):
    if not isinstance(jobs_id, int):
        abort(404, message=f"Jobs {jobs_id} not found")
    session = db_session.create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        abort(404, message=f"Jobs {jobs_id} not found")
