# lajobsparser

Parser for Los Angeles city jobs bulletins

* Source code - [Github][10]

[10]: https://github.com/gavinln/lajobsparser/

The city of Los Angeles (LA) is running a [Kaggle competion][20] that uses the
job bulletins for the city of LA jobs.

[20]: https://www.kaggle.com/c/data-science-for-good-city-of-los-angeles

The content, tone, and format of job bulletins can influence the quality of the
applicant pool. Overly-specific job requirements may discourage diversity. The
Los Angeles Mayor’s Office wants to reimagine the city’s job bulletins by using
text analysis to identify needed improvements.

The goal is to convert a folder full of plain-text job postings into a single
structured CSV file and then to use this data to:

1. identify language that can negatively bias the pool of applicants
2. improve the diversity and quality of the applicant pool
3. make it easier to determine which promotions are available to employees in
   each job class

This project helps parse the job bulletins and associated files.

## Miscellaneous

1. To install from github using pipenv

```
pipenv install -e git+https://github.com/gavinln/lajobsparser.git#egg=lajobsparser
```

