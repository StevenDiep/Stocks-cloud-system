import redis
from hotqueue import HotQueue
import uuid
import os


q = HotQueue("queue", host='127.0.0.1', port=6379, db=1)
rd = redis.StrictRedis(host='127.0.0.1',  port=6379, db=0, decode_responses=True)
rdi = redis.StrictRedis(host='127.0.0.1', port=6379, db=2)

def test():
    return rd.get(3)

def _generate_jid():
    return str(uuid.uuid4())

def _generate_job_key(jid):
    return 'job.{}'.format(jid)

def _save_job(job_key, job_dict):
    """Save a job object in the Redis database."""
    rd.hmset(job_key, job_dict)

def _queue_job(jid):
    """Add a job to the redis queue."""
    q.put(jid)

def _instantiate_job(jid, status, ticker):
    if type(jid) == str:
        return {'id': jid,
                'status': status,
                'ticker': ticker 
        }
    return {'id': jid.decode('utf-8'),
            'status': status.decode('utf-8'),
            'ticker': ticker.decode('utf-8'),
            }

def add_job(ticker, status="submitted"):
    """Add a job to the redis queue."""
    jid = _generate_jid()
    job_dict = _instantiate_job(jid, status, ticker)
    _save_job(_generate_job_key(jid), job_dict)
    _queue_job(jid)
    return job_dict

def return_job(jid):
    jid = _generate_job_key(jid)
    return(rd.hgetall(jid))

def return_image(jid):
    jid = _generate_job_key(jid)
    return(rdi.get(jid))

def update_job_status(jid, new_status):
    """Update the status of job with job id `jid` to status `status`."""
    jid, status, ticker= rd.hmget(_generate_job_key(jid), 'id', 'status', 'ticker')
    job = _instantiate_job(jid, status, ticker)
    if job:
        job['status'] = new_status
        _save_job(_generate_job_key(jid), job)
    else:
        raise Exception()