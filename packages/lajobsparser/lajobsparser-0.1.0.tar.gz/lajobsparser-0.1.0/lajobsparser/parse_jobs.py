import logging
import pathlib
from typing import List

import re
import pandas as pd

import pyparsing as pyp

from collections import namedtuple

'''
# when using ipython
%load_ext autoreload
%autoreload 2
import parse_jobs as pj
'''

log = logging.getLogger(__name__)

SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()


def is_common_header(text: str) -> bool:
    ' common headers in job bulletins '
    headers = [
        'AN EQUAL EMPLOYMENT OPPORTUNITY EMPLOYER',
        'ANNUAL SALARY',
        'APPLICATION DEADLINE',
        'DUTIES',
        'INTERDEPARTMENTAL PROMOTIONAL AND AN OPEN COMPETITIVE BASIS',
        'NOTE:',
        'NOTES:',
        'NOTICE:',
        'ON AN INTERDEPARTMENTAL PROMOTIONAL BASIS',
        'PROCESS NOTES',
        'REQUIREMENT/MINIMUM QUALIFICATION',
        'REQUIREMENTS',
        'REQUIREMENTS/MINIMUM QUALIFICATIONS',
        'SELECTION PROCESS',
        'THIS EXAMINATION IS TO BE GIVEN BOTH ON AN',
        'THIS EXAMINATION IS TO BE GIVEN ONLY',
        'WHERE TO APPLY'
    ]
    for header in headers:
        if text == header:
            return True
    headers_start = ['Class Code', 'Open Date', 'REVISED']
    for header in headers_start:
        if text.startswith(header):
            return True
    return False


def get_headers(path) -> List[List]:
    ' return headers for job bulletin text file'
    headers: List[List] = []

    def is_valid_first_header() -> bool:
        # first non-blank line is header (job title)
        return len(headers) == 0

    # The header only has upper case letters and symbols
    header_re = re.compile(r"^[A-Z0-9\t\/\(\):_'\- ]+$")

    def is_header(text: str) -> bool:
        return not header_re.match(text) is None

    with path.open(encoding="ISO-8859-1") as f:
        for idx, file_line in enumerate(f.readlines()):
            line = file_line.strip()
            # if not empty line
            if len(line) > 0:
                if is_valid_first_header():
                    headers.append([line, ''])
                elif is_common_header(line):
                    # add code to header
                    headers.append([line, ''])
                else:
                    # add text to header
                    if len(headers) > 0:
                        last_header = headers[-1]
                        last_header[1] += '\n' + line
    return headers


JobInfo = namedtuple(
    'JobInfo', [
        'file_name', 'job_class_title', 'job_class_no', 'open_date',
        'annual_salary', 'job_duties'
    ]
)


def get_salary_range_list_parser():
    ''' Use pyparsing to process salary ranges

    converts from old-format to new-format

    "$90,118 (flat-rated)" to "90118"
    "$125,175 to $155,514" to "125175-155514"
    "$49,903 to $72,996 and $55,019 to $80,472" to "49903-72996|55019-80472"

    Extended Backus-Naur form grammar

    currency ::= '$'
    number ::= [0-9,]+
    salary ::= currency + number
    to ::= 'to'
    salary_range ::= salary + to + salary
    range_sep ::= (';' | 'and')
    range_list ::= salary_range + (range_sep + salary_range)*
    '''
    currency = pyp.Suppress(pyp.Word('$'))
    number = pyp.Word(pyp.nums + ',').setParseAction(
        lambda x: x[0].replace(',', ''))
    salary = currency + number
    to = pyp.Literal('to').setParseAction(lambda x: '-')
    salary_range = salary + pyp.Optional(to + salary)
    range_sep = (pyp.Literal(';') | pyp.Literal('and'))
    range_sep.setParseAction(lambda x: '|')

    range_list = salary_range + pyp.Optional(range_sep + salary_range)
    return range_list


def parse_salary(salary_parser, salary_str: str) -> List:
    if salary_str:
        try:
            salary_parts = salary_parser.parseString(salary_str)
            return salary_parts
        except pyp.ParseException:
            pass
    return []


def process_salary_text(salary_parser, salary_text: str) -> str:
    ' returns the first non-blank line '
    lines = salary_text.split('\n')
    for line in lines:
        if len(line.strip()) > 0:
            salary_parts = parse_salary(salary_parser, line)
            if salary_parts:
                return ''.join(salary_parts)
            return ''
    return ''


def get_job_info(headers: List[List], path: pathlib.Path) -> JobInfo:
    ''' convert job bulletin headers to a tuple with selected items

        Using the lower case column names from the data dictionary

        1	FILE_NAME
        2	JOB_CLASS_TITLE
        3	JOB_CLASS_NO
        4	REQUIREMENT_SET_ID
        5	REQUIREMENT_SUBSET_ID
        6	JOB_DUTIES
        7	EDUCATION_YEARS
        8	SCHOOL_TYPE
        9	EDUCATION_MAJOR
        10	EXPERIENCE_LENGTH
        11	FULL_TIME_PART_TIME
        12	EXP_JOB_CLASS_TITLE
        13	EXP_JOB_CLASS_ALT_RESP
        14	EXP_JOB_CLASS_FUNCTION
        15	COURSE_COUNT
        16	COURSE_LENGTH
        17	COURSE_SUBJECT
        18	MISC_COURSE_DETAILS
        19	DRIVERS_LICENSE_REQ
        20	DRIV_LIC_TYPE
        21	ADDTL_LIC
        22	EXAM_TYPE
        23	ENTRY_SALARY_GEN
        24	ENTRY_SALARY_DWP
        25	OPEN_DATE
    '''

    job_class_no_re = re.compile('Class Code: +([0-9]+)')
    open_date_re = re.compile('Open Date: +([0-9]{2}-[0-9]{2}-[0-9]{2})')

    salary_parser = get_salary_range_list_parser()

    def find_group_pattern(pat_re, text):
        pat_match = pat_re.search(text)
        if pat_match and len(pat_match.groups()) > 0:
            return pat_match.group(1)
        return None

    (job_class_title, job_class_no, open_date, annual_salary,
     job_duties) = [None] * 5

    for idx, (code, text) in enumerate(headers):
        if idx == 0:
            job_class_title = code.strip()
        else:
            pat_match = find_group_pattern(job_class_no_re, code)
            if pat_match:
                job_class_no = pat_match
                continue

            pat_match = find_group_pattern(open_date_re, code)
            if pat_match:
                open_date = pat_match
                continue

            if code.startswith('ANNUAL SALARY'):
                annual_salary = process_salary_text(
                    salary_parser, text.strip())
                continue

            if code.startswith('DUTIES'):
                job_duties = text.replace('\n', '').strip()
                continue

    job_info = JobInfo(
        path.name, job_class_title, job_class_no, open_date, annual_salary,
        job_duties)
    return job_info


def get_job_info_df(paths: List[pathlib.Path]):
    job_info_list = []
    # for path in paths:
    for path in paths:
        headers = get_headers(path)
        job_info = get_job_info(headers, path)
        job_info_list.append(job_info)

    return pd.DataFrame.from_records(
        data=job_info_list, columns=JobInfo._fields)


def get_header_counts(header_df, header):
    return header_df.groupby(header).size()


def check_job_bulletins(paths: List[pathlib.Path]) -> pd.DataFrame:
    bulletin_df = get_job_info_df(paths)

    invalid_job_class_title_df = bulletin_df[
        bulletin_df.job_class_title.str.find('Class Code') >= 0]
    log.info('invalid job titles: {}'.format(len(invalid_job_class_title_df)))
    log.debug(invalid_job_class_title_df)

    # check duplicate class codes
    class_code_num = bulletin_df.job_class_no.value_counts()
    duplicate_class_codes = class_code_num[class_code_num > 1]
    log.info('Duplicate class codes count {}'.format(
        len(duplicate_class_codes)))

    log.debug('Duplicate class codes')
    log.debug(duplicate_class_codes)

    problem_class_codes = bulletin_df[
        bulletin_df.job_class_no.isin(
            duplicate_class_codes.index
        )][['file_name', 'job_class_no']].sort_values(by='job_class_no')
    log.debug(problem_class_codes)
    return bulletin_df


def check_job_class_titles(title_df, bulletin_df):
    ' compare job titles from title file and job bulletin files '
    bulletin_job = set(bulletin_df.job_class_title)
    title_job = set(title_df.job_class_title)

    jobs_in_both = bulletin_job | title_job
    log.debug(jobs_in_both)

    all_jobs = bulletin_job & title_job
    log.debug(all_jobs)

    title_list_only = title_job - bulletin_job
    log.debug(title_list_only)

    bulletin_list_only = bulletin_job - title_job
    log.debug(bulletin_list_only)

    title_compare_df = pd.DataFrame({
        'jobs_in_both': len(jobs_in_both),
        'all_jobs': len(all_jobs),
        'jobs_in_title_list_only': len(title_list_only),
        'jobs_in_bulletin_list_only': len(bulletin_list_only)
    }, index=[0])
    log.info(title_compare_df)


def check_data_dictionary(data_dictionary_path: pathlib.Path) -> pd.DataFrame:
    ' retrieve the data dictionary as a data frame '
    data_dict_df = pd.read_csv(data_dictionary_path, header=0)
    columns = [name.replace(' ', '_') for name in data_dict_df.columns]
    data_dict_df.columns = columns
    return data_dict_df
