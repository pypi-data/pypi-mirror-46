import os
import yaml

from celery.schedules import crontab

SPEC_FILENAME = 'pipeline-spec.yaml'


def find_specs(root_dir='.'):

    for dirpath, dirnames, filenames in os.walk(root_dir):
        if SPEC_FILENAME in filenames:
            abspath = os.path.abspath(dirpath)
            fullpath = os.path.join(abspath, SPEC_FILENAME)
            with open(fullpath) as spec_file:
                spec = yaml.load(spec_file)
                for pipeline_id, pipeline_details in spec.items():
                    pipeline_id = os.path.join(dirpath, pipeline_id)
                    yield abspath, pipeline_id, pipeline_details


def resolve_executor(executor, path):

    parts = []
    while executor.startswith('..'):
        parts.append('..')
        executor = executor[1:]

    if executor.startswith('.'):
        executor = executor[1:]

    executor = executor.split('.')
    executor[-1] += '.py'

    parts.extend(executor)

    local_parts = [path] + parts
    if os.path.exists('common'):
        common_parts = [os.path.abspath('common')] + parts
    else:
        common_parts = local_parts
    lib_parts = [os.path.dirname(__file__), '..', 'lib'] + parts

    resolve_order = [local_parts, common_parts, lib_parts]

    for option in resolve_order:
        option = os.path.join(*option)
        if os.path.exists(option):
            return option

    print(resolve_order)

    raise FileNotFoundError("Couldn't resolve {0} at {1}".format(executor, path))


def validate_required_keys(obj, keys, abspath):
    for required_key in keys:
        if required_key not in obj:
            raise KeyError('Missing parameter {0} in {1}'.format(required_key, abspath))


def validate_specs():

    all_pipeline_ids = set()

    for abspath, pipeline_id, pipeline_details in find_specs():

        if pipeline_id in all_pipeline_ids:
            raise KeyError('Duplicate key {0} in {1}'.format(pipeline_id, abspath))

        validate_required_keys(pipeline_details, ['pipeline', 'schedule'], abspath)

        pipeline = pipeline_details['pipeline']

        for step in pipeline:
            validate_required_keys(step, ['run'], abspath)

            executor = step['run']
            step['run'] = resolve_executor(executor, abspath)

        schedule = pipeline_details['schedule']
        if 'crontab' in schedule:
            crontab_spec = schedule['crontab'].split()
            schedule = crontab(*crontab_spec)
            pipeline_details['schedule'] = schedule
        else:
            raise NotImplementedError("Couldn't find valid schedule at {0}".format(abspath))

        yield pipeline_id, pipeline_details


def pipelines():
    return validate_specs()

