from datetime import date

from django.test import TestCase

from analysis.tests.factories import CrawlFactory
from botify.bql.exceptions import QueryParsingException
from botify.bql.tests.backends.bigquery import QueryCheckerMixinCollections
from botify.search_console.bql.crawl import SearchConsoleSchemas
from projects.tests.factories import ProjectFactory


class SearchConsoleSchemaTestCase(TestCase, QueryCheckerMixinCollections):
    def setUp(self):
        self.maxDiff = None
        self.date_start = date(2018, 4, 10)
        self.date_end = date(2018, 5, 10)
        self.revision = {
            "internal": {"gcp_project": "botify-test"},
            "segments": {"names": ["pagetype"]},
        }

    def get_schemas(self):
        project_id = 1
        return SearchConsoleSchemas(
            project_id,
            self.date_start,
            self.date_end,
            self.revision,
            with_urls_and_segments=True,
        )

    def get_schemas_with_crawl(self):
        crawl = CrawlFactory()
        self.project_id = crawl.project.id
        return SearchConsoleSchemas(
            self.project_id,
            self.date_start,
            self.date_end,
            self.revision,
            with_urls_and_segments=True,
        )

    def test_no_dimension(self):
        self.date_start = date(2018, 4, 10)
        self.date_end = date(2018, 4, 20)

        schemas = self.get_schemas_with_crawl()
        bq = {
            "metrics": [
                "search_console.count_rankings",
                "search_console.count_keywords",
                "search_console.count_impressions",
                "search_console.count_links_keyword_in_anchor",
            ],
            "dimensions": [],
        }
        expected = """
SELECT sq_1.search_console__count_rankings_m f_0,
       sq_1.search_console__count_keywords_m f_1,
       IFNULL(sq_1.search_console__count_impressions_m, 0) f_2,
       sq_1.search_console__count_links_keyword_in_anchor_m f_3
FROM
  (SELECT APPROX_COUNT_DISTINCT(a.keyword_hash) search_console__count_keywords_m,
          APPROX_COUNT_DISTINCT(a.url_keyword_hash) search_console__count_rankings_m,
          SUM(a.count_links_keyword_in_anchor) search_console__count_links_keyword_in_anchor_m,
          SUM(a.impressions) search_console__count_impressions_m
   FROM
     (SELECT ANY_VALUE(keyword_hash) keyword_hash,
             ANY_VALUE(url_hash) url_hash,
             SUM(count_links_keyword_in_anchor) count_links_keyword_in_anchor,
             SUM(impressions) impressions,
             url_keyword_hash
      FROM
        (SELECT *
         FROM `botify-test.test_{project_id}.search_console_2*`
         WHERE _table_suffix BETWEEN "0180410" AND "0180420")
      GROUP BY url_keyword_hash) a) sq_1""".format(
            project_id=self.project_id
        )  # NOQA  sqlformat
        self.check_query(expected, bq, schemas)

    def test_counts(self):
        self.date_start = date(2018, 4, 10)
        self.date_end = date(2018, 4, 20)

        bq = {
            "metrics": ["search_console.count_rankings", "search_console.count_urls"],
            "dimensions": ["host"],
        }
        expected = """SELECT HOST f_0,
            sq_1.search_console__count_rankings_m f_1,
            sq_1.search_console__count_urls_m f_2
FROM
  (SELECT a.host HOST,
                 APPROX_COUNT_DISTINCT(a.url_hash) search_console__count_urls_m,
                 APPROX_COUNT_DISTINCT(a.url_keyword_hash) search_console__count_rankings_m
   FROM
     (SELECT ANY_VALUE(HOST) HOST,
                             ANY_VALUE(url_hash) url_hash,
                             url_keyword_hash
      FROM
        (SELECT *
         FROM `botify-test.test_1.search_console_2*`
         WHERE _table_suffix BETWEEN "0180410" AND "0180420")
      JOIN
        (SELECT *
         EXCEPT (url_hash,
                 keyword_hash,
                 url,
                 keyword)
         FROM `botify-test.test_1.search_console_unique_url_kw_20180401`
         WHERE min_date <= DATE("2018-04-20")
           AND max_date >= DATE("2018-04-10")) USING (url_keyword_hash)
      GROUP BY url_keyword_hash) a
   GROUP BY HOST) sq_1"""  # NOQA  sqlformat
        self.check_query(expected, bq)

    def test_one_month(self):
        self.date_start = date(2018, 4, 10)
        self.date_end = date(2018, 4, 20)

        bq = {"metrics": ["search_console.count_rankings"], "dimensions": ["host"]}
        expected = """SELECT host f_0,
sq_1.search_console__count_rankings_m f_1
FROM (SELECT a.host host,
APPROX_COUNT_DISTINCT(a.url_keyword_hash) search_console__count_rankings_m
FROM (SELECT ANY_VALUE(host) host,
ANY_VALUE(url_hash) url_hash,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180420")
JOIN
(SELECT * EXCEPT (url_hash, keyword_hash, url, keyword)
FROM `botify-test.test_1.search_console_unique_url_kw_20180401`
WHERE min_date <= DATE("2018-04-20") AND max_date >= DATE("2018-04-10"))
USING (url_keyword_hash)
GROUP BY url_keyword_hash) a
GROUP BY host) sq_1"""  # NOQA
        self.check_query(expected, bq)

    def test_one_period_multiple_months(self):
        bq = {"metrics": ["search_console.count_rankings"], "dimensions": ["host"]}
        expected = """SELECT host f_0,
sq_1.search_console__count_rankings_m f_1
FROM (SELECT a.host host,
APPROX_COUNT_DISTINCT(a.url_keyword_hash) search_console__count_rankings_m
FROM (SELECT ANY_VALUE(host) host,
ANY_VALUE(url_hash) url_hash,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
JOIN
(SELECT * EXCEPT (url_hash, keyword_hash, url, keyword)
FROM (SELECT *,
ROW_NUMBER() OVER (PARTITION BY url_keyword_hash) AS rn
FROM `botify-test.test_1.search_console_unique_url_kw_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180501")
WHERE rn = 1)
USING (url_keyword_hash)
GROUP BY url_keyword_hash) a
GROUP BY host) sq_1"""  # NOQA
        self.check_query(expected, bq)

    def test_fields(self):
        bq = {
            "dimensions": ["keyword", {"field": "url"}],
            "metrics": [
                "search_console.count_impressions",
                "search_console.count_clicks",
                "search_console.avg_position",
                {"field": "search_console.count_missed_clicks"},
                {
                    "function": "mul",
                    "args": [{"field": "search_console.count_impressions"}, 100],
                },
            ],
        }
        expected = """SELECT keyword f_0,
url f_1,
IFNULL(sq_1.search_console__count_impressions_m, 0) f_2,
IFNULL(sq_1.search_console__count_clicks_m, 0) f_3,
sq_1.search_console__avg_position_m f_4,
sq_1.search_console__count_missed_clicks_m f_5,
(IFNULL(sq_1.search_console__count_impressions_m, 0) * 100) f_6
FROM (SELECT (SUM((a.impressions * a.avg_position)) / SUM(a.impressions)) search_console__avg_position_m,
(SUM(a.impressions) - SUM(a.clicks)) search_console__count_missed_clicks_m,
a.keyword_hash,
a.url_hash,
ANY_VALUE(a.keyword) keyword,
ANY_VALUE(a.url) url,
SUM(a.clicks) search_console__count_clicks_m,
SUM(a.impressions) search_console__count_impressions_m
FROM (SELECT (SUM((impressions * avg_position)) / SUM(impressions)) avg_position,
ANY_VALUE(keyword) keyword,
ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
SUM(clicks) clicks,
SUM(impressions) impressions,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
GROUP BY url_keyword_hash) a
GROUP BY a.keyword_hash, a.url_hash) sq_1"""  # NOQA
        self.check_query(expected, bq)

    def test_avg_position_metric(self):
        bql = {"dimensions": ["keyword"], "metrics": ["search_console.avg_position"]}
        expected = """
SELECT keyword f_0,
sq_1.search_console__avg_position_m f_1
FROM (SELECT (SUM((a.impressions * a.avg_position)) / SUM(a.impressions)) search_console__avg_position_m,
a.keyword_hash,
ANY_VALUE(a.keyword) keyword
FROM (SELECT (SUM((impressions * avg_position)) / SUM(impressions)) avg_position,
ANY_VALUE(keyword) keyword,
ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(url_hash) url_hash,
SUM(impressions) impressions,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
GROUP BY url_keyword_hash) a
GROUP BY a.keyword_hash) sq_1
"""  # noqa
        self.check_query(expected, bql)

    def test_ctr(self):
        bq = {"dimensions": ["keyword", "url"], "metrics": ["search_console.ctr"]}
        expected = """
SELECT keyword f_0,
url f_1,
sq_1.search_console__ctr_m f_2
FROM (SELECT ((SUM(a.clicks) / SUM(a.impressions)) * 100) search_console__ctr_m,
a.keyword_hash,
a.url_hash,
ANY_VALUE(a.keyword) keyword,
ANY_VALUE(a.url) url
FROM (SELECT ANY_VALUE(keyword) keyword,
ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
SUM(clicks) clicks,
SUM(impressions) impressions,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
GROUP BY url_keyword_hash) a
GROUP BY a.keyword_hash, a.url_hash) sq_1"""  # NOQA
        self.check_query(expected, bq)

    def test_multiple_months(self):
        self.date_start = date(2018, 4, 1)
        self.date_end = date(2018, 5, 20)
        bq = {
            "dimensions": ["keyword", "host"],
            "metrics": ["search_console.count_impressions"],
        }
        expected = """SELECT keyword f_0,
host f_1,
IFNULL(sq_1.search_console__count_impressions_m, 0) f_2
FROM (SELECT a.host host,
a.keyword_hash,
ANY_VALUE(a.keyword) keyword,
SUM(a.impressions) search_console__count_impressions_m
FROM (SELECT ANY_VALUE(host) host,
ANY_VALUE(keyword) keyword,
ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(url_hash) url_hash,
SUM(impressions) impressions,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
JOIN
(SELECT * EXCEPT (url_hash, keyword_hash, url, keyword)
FROM (SELECT *,
ROW_NUMBER() OVER (PARTITION BY url_keyword_hash) AS rn
FROM `botify-test.test_1.search_console_unique_url_kw_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180501")
WHERE rn = 1)
USING (url_keyword_hash)
GROUP BY url_keyword_hash) a
GROUP BY a.keyword_hash, host) sq_1"""  # NOQA
        self.check_query(expected, bq)

    def test_new_rankings(self):
        self.date_start = date(2018, 4, 1)
        self.date_end = date(2018, 5, 20)
        bq = {"dimensions": ["date"], "metrics": ["search_console.count_new_rankings"]}
        expected = """SELECT date f_0,
sq_2.search_console__count_new_rankings_m f_1
FROM (SELECT a.date date,
COUNTIF(a.is_new) search_console__count_new_rankings_m
FROM (SELECT ANY_VALUE(url_hash) url_hash,
COUNT(1) = COUNTIF(date = first_seen) is_new,
date,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
GROUP BY date, url_keyword_hash) a
GROUP BY date) sq_2
WHERE date IS NOT NULL"""  # NOQA
        self.check_query(expected, bq)

    def test_new_rankings_with_functions(self):
        self.date_start = date(2018, 4, 1)
        self.date_end = date(2018, 5, 20)
        bq = {
            "dimensions": [{"function": "first_day_of_month", "args": ["date"]}],
            "metrics": ["search_console.count_new_rankings"],
        }
        expected = """SELECT func_1 f_0,
sq_2.search_console__count_new_rankings_m f_1
FROM (SELECT COUNTIF(a.is_new) search_console__count_new_rankings_m,
DATE(TIMESTAMP_TRUNC(CAST(a.date AS TIMESTAMP), MONTH)) func_1
FROM (SELECT ANY_VALUE(url_hash) url_hash,
COUNT(1) = COUNTIF(date = first_seen) is_new,
date,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
GROUP BY date, url_keyword_hash) a
GROUP BY func_1) sq_2
WHERE func_1 IS NOT NULL"""  # NOQA
        self.check_query(expected, bq)

    def test_global_fields(self):
        self.date_start = date(2018, 4, 1)
        self.date_end = date(2018, 5, 20)
        bq = {
            "dimensions": [
                "keyword",
                "url",
                "segments.pagetype.value",
                "segments.pagetype.depth_4",
                "segments.is_warning",
            ],
            "metrics": ["search_console.count_impressions"],
        }
        expected = """SELECT keyword f_0,
url f_1,
segments__pagetype__value f_2,
segments__pagetype__depth_4 f_3,
segments__is_warning f_4,
IFNULL(sq_1.search_console__count_impressions_m, 0) f_5
FROM (SELECT a.keyword_hash,
a.segments__pagetype__depth_4 segments__pagetype__depth_4,
a.segments__pagetype__value segments__pagetype__value,
a.segments__warning segments__is_warning,
a.url_hash,
ANY_VALUE(a.keyword) keyword,
ANY_VALUE(a.url) url,
SUM(a.impressions) search_console__count_impressions_m
FROM (SELECT ANY_VALUE(keyword) keyword,
ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(segments__pagetype__depth_4) segments__pagetype__depth_4,
ANY_VALUE(segments__pagetype__value) segments__pagetype__value,
ANY_VALUE(segments__warning) segments__warning,
ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
SUM(impressions) impressions,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
JOIN
(SELECT * EXCEPT (url_hash, keyword_hash, url, keyword),
segments__pagetype__depths[SAFE_OFFSET(3)] segments__pagetype__depth_4
FROM (SELECT *,
ROW_NUMBER() OVER (PARTITION BY url_keyword_hash) AS rn
FROM `botify-test.test_1.search_console_unique_url_kw_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180501")
WHERE rn = 1)
USING (url_keyword_hash)
GROUP BY url_keyword_hash) a
GROUP BY a.keyword_hash, a.url_hash, segments__is_warning, segments__pagetype__depth_4, segments__pagetype__value) sq_1"""  # NOQA
        self.check_query(expected, bq)

    def test_field_as_dimension(self):
        self.date_start = date(2018, 5, 1)
        self.date_end = date(2018, 5, 20)
        bq = {
            "dimensions": [{"field": "segments.pagetype.value"}],
            "metrics": ["search_console.count_impressions"],
        }
        expected = """SELECT segments__pagetype__value f_0,
IFNULL(sq_1.search_console__count_impressions_m, 0) f_1
FROM (SELECT a.segments__pagetype__value segments__pagetype__value,
SUM(a.impressions) search_console__count_impressions_m
FROM (SELECT ANY_VALUE(segments__pagetype__value) segments__pagetype__value,
ANY_VALUE(url_hash) url_hash,
SUM(impressions) impressions,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180501" AND "0180520")
JOIN
(SELECT * EXCEPT (url_hash, keyword_hash, url, keyword)
FROM `botify-test.test_1.search_console_unique_url_kw_20180501`
WHERE min_date <= DATE("2018-05-20") AND max_date >= DATE("2018-05-01"))
USING (url_keyword_hash)
GROUP BY url_keyword_hash) a
GROUP BY segments__pagetype__value) sq_1"""  # NOQA
        self.check_query(expected, bq)

    def test_avg_position_range(self):
        self.date_start = date(2018, 4, 1)
        self.date_end = date(2018, 5, 20)
        bq = {
            "dimensions": [
                {
                    "field": "search_console.avg_position",
                    "ranges": [
                        {"from": 1, "to": 2},
                        {"from": 2, "to": 3},
                        {"from": 3, "to": 4},
                    ],
                }
            ],
            "metrics": ["search_console.count_impressions"],
        }
        expected = """SELECT _r_0 f_0,
IFNULL(sq_1.search_console__count_impressions_m, 0) f_1
FROM (SELECT CASE WHEN a.search_console__avg_position >= 1 AND a.search_console__avg_position < 2 THEN '0000_from_1_to_2'
WHEN a.search_console__avg_position >= 2 AND a.search_console__avg_position < 3 THEN '0001_from_2_to_3'
WHEN a.search_console__avg_position >= 3 AND a.search_console__avg_position < 4 THEN '0002_from_3_to_4'
END _r_0,
SUM(a.impressions) search_console__count_impressions_m
FROM (SELECT (SUM((impressions * avg_position)) / SUM(impressions)) search_console__avg_position,
ANY_VALUE(url_hash) url_hash,
SUM(impressions) impressions,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
GROUP BY url_keyword_hash) a
GROUP BY _r_0) sq_1
"""  # NOQA
        self.check_query(expected, bq)

    def test_ctr_range(self):
        self.date_start = date(2018, 4, 1)
        self.date_end = date(2018, 5, 20)
        bq = {
            "dimensions": [
                {
                    "field": "search_console.ctr",
                    "ranges": [{"from": 0, "to": 1}, {"from": 1, "to": 5}, {"from": 5}],
                }
            ],
            "metrics": ["search_console.count_impressions"],
        }
        expected = """SELECT _r_0 f_0,
IFNULL(sq_1.search_console__count_impressions_m, 0) f_1
FROM (SELECT CASE WHEN a.search_console__ctr >= 0 AND a.search_console__ctr < 1 THEN '0000_from_0_to_1'
WHEN a.search_console__ctr >= 1 AND a.search_console__ctr < 5 THEN '0001_from_1_to_5'
WHEN a.search_console__ctr >= 5 THEN '0002_from_5_to_'
END _r_0,
SUM(a.impressions) search_console__count_impressions_m
FROM (SELECT ((SUM(clicks) / SUM(impressions)) * 100) search_console__ctr,
ANY_VALUE(url_hash) url_hash,
SUM(impressions) impressions,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
GROUP BY url_keyword_hash) a
GROUP BY _r_0) sq_1
"""  # NOQA
        self.check_query(expected, bq)

    def test_avg_position_range_function(self):
        self.date_start = date(2018, 4, 1)
        self.date_end = date(2018, 5, 20)
        bq = {
            "dimensions": [
                "segments.pagetype.depth_1",
                {
                    "function": "ranges",
                    "args": [
                        {"function": "mul", "args": ["search_console.avg_position", 2]},
                        [
                            {"from": 1, "to": 2},
                            {"from": 2, "to": 3},
                            {"from": 3, "to": 4},
                        ],
                    ],
                },
            ],
            "metrics": ["search_console.count_impressions"],
        }
        expected = """SELECT segments__pagetype__depth_1 f_0,
_r_1 f_1,
IFNULL(sq_1.search_console__count_impressions_m, 0) f_2
FROM (SELECT a.segments__pagetype__depth_1 segments__pagetype__depth_1,
CASE WHEN (a.search_console__avg_position * 2) >= 1 AND (a.search_console__avg_position * 2) < 2 THEN '0000_from_1_to_2'
WHEN (a.search_console__avg_position * 2) >= 2 AND (a.search_console__avg_position * 2) < 3 THEN '0001_from_2_to_3'
WHEN (a.search_console__avg_position * 2) >= 3 AND (a.search_console__avg_position * 2) < 4 THEN '0002_from_3_to_4'
END _r_1,
SUM(a.impressions) search_console__count_impressions_m
FROM (SELECT (SUM((impressions * avg_position)) / SUM(impressions)) search_console__avg_position,
ANY_VALUE(segments__pagetype__depth_1) segments__pagetype__depth_1,
ANY_VALUE(url_hash) url_hash,
SUM(impressions) impressions,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
JOIN
(SELECT * EXCEPT (url_hash, keyword_hash, url, keyword),
segments__pagetype__depths[SAFE_OFFSET(0)] segments__pagetype__depth_1
FROM (SELECT *,
ROW_NUMBER() OVER (PARTITION BY url_keyword_hash) AS rn
FROM `botify-test.test_1.search_console_unique_url_kw_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180501")
WHERE rn = 1)
USING (url_keyword_hash)
GROUP BY url_keyword_hash) a
GROUP BY _r_1, segments__pagetype__depth_1) sq_1
"""  # NOQA
        self.check_query(expected, bq)

    def test_dimension_function_date(self):
        bq = {
            "dimensions": [{"function": "first_day_of_month", "args": ["date"]}],
            "metrics": ["search_console.count_impressions"],
        }
        expected = """SELECT func_1 f_0,
IFNULL(sq_1.search_console__count_impressions_m, 0) f_1
FROM (SELECT DATE(TIMESTAMP_TRUNC(CAST(a.date AS TIMESTAMP), MONTH)) func_1,
SUM(a.impressions) search_console__count_impressions_m
FROM (SELECT ANY_VALUE(url_hash) url_hash,
SUM(impressions) impressions,
date,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
GROUP BY date, url_keyword_hash) a
GROUP BY func_1) sq_1

WHERE func_1 IS NOT NULL"""  # NOQA
        self.check_query(expected, bq)

    def test_dimension_url(self):
        bq = {"dimensions": ["url"], "metrics": ["search_console.count_impressions"]}
        expected = """SELECT url f_0,
IFNULL(sq_1.search_console__count_impressions_m, 0) f_1
FROM (SELECT a.url_hash,
ANY_VALUE(a.url) url,
SUM(a.impressions) search_console__count_impressions_m
FROM (SELECT ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
SUM(impressions) impressions,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
GROUP BY url_keyword_hash) a
GROUP BY a.url_hash) sq_1"""  # NOQA
        self.check_query(expected, bq)

    def test_is_new_metric(self):
        bq = {"dimensions": ["url"], "metrics": ["search_console.is_new"]}
        expected = """SELECT url f_0,
sq_2.search_console__is_new_m f_1
FROM (SELECT a.url_hash,
ANY_VALUE(a.url) url,
COUNTIF(a.is_new) > 0 search_console__is_new_m
FROM (SELECT ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
COUNT(1) = COUNTIF(date = first_seen) is_new,
date,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
GROUP BY date, url_keyword_hash) a
GROUP BY a.url_hash) sq_2"""  # NOQA
        self.check_query(expected, bq)

    def test_branded_count_rankings(self):
        self.date_start = date(2018, 4, 10)
        self.date_end = date(2018, 4, 20)

        bq = {
            "metrics": ["search_console.count_rankings"],
            "dimensions": ["keyword_meta.branded"],
        }
        expected = """SELECT keyword_meta__branded f_0,
sq_1.search_console__count_rankings_m f_1
FROM (SELECT a.branded keyword_meta__branded,
APPROX_COUNT_DISTINCT(a.url_keyword_hash) search_console__count_rankings_m
FROM (SELECT ANY_VALUE(branded) branded,
ANY_VALUE(url_hash) url_hash,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180420")
JOIN
(SELECT * EXCEPT (url_hash, keyword_hash, url, keyword)
FROM `botify-test.test_1.search_console_unique_url_kw_20180401`
WHERE min_date <= DATE("2018-04-20") AND max_date >= DATE("2018-04-10"))
USING (url_keyword_hash)
GROUP BY url_keyword_hash) a
GROUP BY keyword_meta__branded) sq_1
WHERE keyword_meta__branded IS NOT NULL"""  # NOQA
        self.check_query(expected, bq)

        bq = {
            "metrics": ["search_console.count_rankings"],
            "dimensions": ["segments.pagetype.value", "keyword_meta.branded"],
        }
        expected = """SELECT segments__pagetype__value f_0,
keyword_meta__branded f_1,
sq_1.search_console__count_rankings_m f_2
FROM (SELECT a.branded keyword_meta__branded,
a.segments__pagetype__value segments__pagetype__value,
APPROX_COUNT_DISTINCT(a.url_keyword_hash) search_console__count_rankings_m
FROM (SELECT ANY_VALUE(branded) branded,
ANY_VALUE(segments__pagetype__value) segments__pagetype__value,
ANY_VALUE(url_hash) url_hash,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180420")
JOIN
(SELECT * EXCEPT (url_hash, keyword_hash, url, keyword)
FROM `botify-test.test_1.search_console_unique_url_kw_20180401`
WHERE min_date <= DATE("2018-04-20") AND max_date >= DATE("2018-04-10"))
USING (url_keyword_hash)
GROUP BY url_keyword_hash) a
GROUP BY keyword_meta__branded, segments__pagetype__value) sq_1
WHERE keyword_meta__branded IS NOT NULL"""  # NOQA
        self.check_query(expected, bq)

    def test_branded_count_keywords(self):
        bq = {
            "metrics": ["search_console.count_keywords"],
            "dimensions": ["segments.pagetype.value", "keyword_meta.branded"],
        }
        expected = """SELECT segments__pagetype__value f_0,
keyword_meta__branded f_1,
sq_1.search_console__count_keywords_m f_2
FROM (SELECT a.branded keyword_meta__branded,
a.segments__pagetype__value segments__pagetype__value,
APPROX_COUNT_DISTINCT(a.keyword_hash) search_console__count_keywords_m
FROM (SELECT ANY_VALUE(branded) branded,
ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(segments__pagetype__value) segments__pagetype__value,
ANY_VALUE(url_hash) url_hash,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
JOIN
(SELECT * EXCEPT (url_hash, keyword_hash, url, keyword)
FROM (SELECT *,
ROW_NUMBER() OVER (PARTITION BY url_keyword_hash) AS rn
FROM `botify-test.test_1.search_console_unique_url_kw_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180501")
WHERE rn = 1)
USING (url_keyword_hash)
GROUP BY url_keyword_hash) a
GROUP BY keyword_meta__branded, segments__pagetype__value) sq_1
WHERE keyword_meta__branded IS NOT NULL"""  # NOQA
        self.check_query(expected, bq)

    def test_count_keywords_and_functions(self):
        bq = {
            "metrics": ["search_console.count_keywords"],
            "dimensions": [{"function": "first_day_of_month", "args": ["date"]}],
        }
        expected = """SELECT func_1 f_0,
sq_1.search_console__count_keywords_m f_1
FROM (SELECT APPROX_COUNT_DISTINCT(a.keyword_hash) search_console__count_keywords_m,
DATE(TIMESTAMP_TRUNC(CAST(a.date AS TIMESTAMP), MONTH)) func_1
FROM (SELECT ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(url_hash) url_hash,
date,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
GROUP BY date, url_keyword_hash) a
GROUP BY func_1) sq_1
WHERE func_1 IS NOT NULL"""  # NOQA
        self.check_query(expected, bq)

    def test_range_global_dimension(self):
        schemas = self.get_schemas()
        for sc_schema in schemas.schemas:
            sc_schema.update_prefix("sc")

        bql = {
            "metrics": [
                "sc.search_console.count_clicks",
                "sc.search_console.count_new_rankings",
            ],
            "dimensions": [
                {
                    "field": "keyword_meta.nb_words",
                    "ranges": [{"to": 2}, {"from": 2, "to": 3}, {"from": 3}],
                }
            ],
        }
        expected = """
SELECT _r_0 f_0,
IFNULL(sq_1.sc__search_console__count_clicks_m, 0) f_1,
sq_2.sc__search_console__count_new_rankings_m f_2
FROM (SELECT CASE WHEN a.nb_words < 2 THEN '0000_from__to_2'
WHEN a.nb_words >= 2 AND a.nb_words < 3 THEN '0001_from_2_to_3'
WHEN a.nb_words >= 3 THEN '0002_from_3_to_'
END _r_0,
SUM(a.clicks) sc__search_console__count_clicks_m
FROM (SELECT ANY_VALUE(nb_words) nb_words,
ANY_VALUE(url_hash) url_hash,
SUM(clicks) clicks,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
JOIN
(SELECT * EXCEPT (url_hash, keyword_hash, url, keyword)
FROM (SELECT *,
ROW_NUMBER() OVER (PARTITION BY url_keyword_hash) AS rn
FROM `botify-test.test_1.search_console_unique_url_kw_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180501")
WHERE rn = 1)
USING (url_keyword_hash)
GROUP BY url_keyword_hash) a
GROUP BY _r_0) sq_1

FULL OUTER JOIN

(SELECT CASE WHEN a.nb_words < 2 THEN '0000_from__to_2'
WHEN a.nb_words >= 2 AND a.nb_words < 3 THEN '0001_from_2_to_3'
WHEN a.nb_words >= 3 THEN '0002_from_3_to_'
END _r_0,
COUNTIF(a.is_new) sc__search_console__count_new_rankings_m
FROM (SELECT ANY_VALUE(nb_words) nb_words,
ANY_VALUE(url_hash) url_hash,
COUNT(1) = COUNTIF(date = first_seen) is_new,
date,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
JOIN
(SELECT * EXCEPT (url_hash, keyword_hash, url, keyword)
FROM (SELECT *,
ROW_NUMBER() OVER (PARTITION BY url_keyword_hash) AS rn
FROM `botify-test.test_1.search_console_unique_url_kw_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180501")
WHERE rn = 1)
USING (url_keyword_hash)
GROUP BY date, url_keyword_hash) a
GROUP BY _r_0) sq_2

USING (_r_0)

WHERE _r_0 IS NOT NULL
"""  # NOQA
        self.check_query(expected, bql, schemas)

    def test_range_global_dimension_function(self):
        schemas = self.get_schemas()
        for sc_schema in schemas.schemas:
            sc_schema.update_prefix("sc")

        bql = {
            "metrics": [
                "sc.search_console.count_clicks",
                "sc.search_console.count_new_rankings",
            ],
            "dimensions": [
                {
                    "function": "ranges",
                    "args": [
                        {"field": "keyword_meta.nb_words"},
                        [{"to": 2}, {"from": 2, "to": 3}, {"from": 3}],
                    ],
                }
            ],
        }
        expected = """
SELECT _r_0 f_0,
IFNULL(sq_1.sc__search_console__count_clicks_m, 0) f_1,
sq_2.sc__search_console__count_new_rankings_m f_2
FROM (SELECT CASE WHEN a.nb_words < 2 THEN '0000_from__to_2'
WHEN a.nb_words >= 2 AND a.nb_words < 3 THEN '0001_from_2_to_3'
WHEN a.nb_words >= 3 THEN '0002_from_3_to_'
END _r_0,
SUM(a.clicks) sc__search_console__count_clicks_m
FROM (SELECT ANY_VALUE(nb_words) nb_words,
ANY_VALUE(url_hash) url_hash,
SUM(clicks) clicks,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
JOIN
(SELECT * EXCEPT (url_hash, keyword_hash, url, keyword)
FROM (SELECT *,
ROW_NUMBER() OVER (PARTITION BY url_keyword_hash) AS rn
FROM `botify-test.test_1.search_console_unique_url_kw_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180501")
WHERE rn = 1)
USING (url_keyword_hash)
GROUP BY url_keyword_hash) a
GROUP BY _r_0) sq_1

FULL OUTER JOIN

(SELECT CASE WHEN a.nb_words < 2 THEN '0000_from__to_2'
WHEN a.nb_words >= 2 AND a.nb_words < 3 THEN '0001_from_2_to_3'
WHEN a.nb_words >= 3 THEN '0002_from_3_to_'
END _r_0,
COUNTIF(a.is_new) sc__search_console__count_new_rankings_m
FROM (SELECT ANY_VALUE(nb_words) nb_words,
ANY_VALUE(url_hash) url_hash,
COUNT(1) = COUNTIF(date = first_seen) is_new,
date,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
JOIN
(SELECT * EXCEPT (url_hash, keyword_hash, url, keyword)
FROM (SELECT *,
ROW_NUMBER() OVER (PARTITION BY url_keyword_hash) AS rn
FROM `botify-test.test_1.search_console_unique_url_kw_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180501")
WHERE rn = 1)
USING (url_keyword_hash)
GROUP BY date, url_keyword_hash) a
GROUP BY _r_0) sq_2

USING (_r_0)

WHERE _r_0 IS NOT NULL
"""  # NOQA
        self.check_query(expected, bql, schemas)

    def test_range_global_function_dimension(self):
        schemas = self.get_schemas()
        for sc_schema in schemas.schemas:
            sc_schema.update_prefix("sc")

        bql = {
            "metrics": [
                "sc.search_console.count_clicks",
                "sc.search_console.count_new_rankings",
            ],
            "dimensions": [
                {
                    "function": "ranges",
                    "args": [
                        {
                            "function": "add",
                            "args": [
                                {
                                    "function": "sub",
                                    "args": [5, {"field": "keyword_meta.nb_words"}],
                                },
                                100,
                            ],
                        },
                        [{"to": 200}, {"from": 200, "to": 300}, {"from": 300}],
                    ],
                }
            ],
        }
        expected = """
SELECT _r_0 f_0,
IFNULL(sq_1.sc__search_console__count_clicks_m, 0) f_1,
sq_2.sc__search_console__count_new_rankings_m f_2
FROM (SELECT CASE WHEN ((5 - a.nb_words) + 100) < 200 THEN '0000_from__to_200'
WHEN ((5 - a.nb_words) + 100) >= 200 AND ((5 - a.nb_words) + 100) < 300 THEN '0001_from_200_to_300'
WHEN ((5 - a.nb_words) + 100) >= 300 THEN '0002_from_300_to_'
END _r_0,
SUM(a.clicks) sc__search_console__count_clicks_m
FROM (SELECT ANY_VALUE(nb_words) nb_words,
ANY_VALUE(url_hash) url_hash,
SUM(clicks) clicks,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
JOIN
(SELECT * EXCEPT (url_hash, keyword_hash, url, keyword)
FROM (SELECT *,
ROW_NUMBER() OVER (PARTITION BY url_keyword_hash) AS rn
FROM `botify-test.test_1.search_console_unique_url_kw_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180501")
WHERE rn = 1)
USING (url_keyword_hash)
GROUP BY url_keyword_hash) a
GROUP BY _r_0) sq_1

FULL OUTER JOIN

(SELECT CASE WHEN ((5 - a.nb_words) + 100) < 200 THEN '0000_from__to_200'
WHEN ((5 - a.nb_words) + 100) >= 200 AND ((5 - a.nb_words) + 100) < 300 THEN '0001_from_200_to_300'
WHEN ((5 - a.nb_words) + 100) >= 300 THEN '0002_from_300_to_'
END _r_0,
COUNTIF(a.is_new) sc__search_console__count_new_rankings_m
FROM (SELECT ANY_VALUE(nb_words) nb_words,
ANY_VALUE(url_hash) url_hash,
COUNT(1) = COUNTIF(date = first_seen) is_new,
date,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
JOIN
(SELECT * EXCEPT (url_hash, keyword_hash, url, keyword)
FROM (SELECT *,
ROW_NUMBER() OVER (PARTITION BY url_keyword_hash) AS rn
FROM `botify-test.test_1.search_console_unique_url_kw_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180501")
WHERE rn = 1)
USING (url_keyword_hash)
GROUP BY date, url_keyword_hash) a
GROUP BY _r_0) sq_2

USING (_r_0)

WHERE _r_0 IS NOT NULL
"""  # NOQA
        self.check_query(expected, bql, schemas)

    def test_two_schemas_no_dimension(self):
        schemas = self.get_schemas()
        for sc_schema in schemas.schemas:
            sc_schema.update_prefix("sc")

        bql = {
            "metrics": [
                "sc.search_console.count_clicks",
                "sc.search_console.count_new_rankings",
            ],
            "dimensions": [],
        }
        expected = """
SELECT IFNULL(sq_1.sc__search_console__count_clicks_m, 0) f_0,
sq_2.sc__search_console__count_new_rankings_m f_1

FROM (SELECT SUM(a.clicks) sc__search_console__count_clicks_m
FROM (SELECT ANY_VALUE(url_hash) url_hash,
SUM(clicks) clicks,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
GROUP BY url_keyword_hash) a) sq_1,

(SELECT COUNTIF(a.is_new) sc__search_console__count_new_rankings_m
FROM (SELECT ANY_VALUE(url_hash) url_hash,
COUNT(1) = COUNTIF(date = first_seen) is_new,
date,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
GROUP BY date, url_keyword_hash) a) sq_2
"""  # NOQA
        self.check_query(expected, bql, schemas)

    def test_functions_metrics_multiple_schemas(self):
        bql = {
            "metrics": [
                {
                    "function": "add",
                    "args": [
                        "search_console.count_clicks",
                        {
                            "function": "sub",
                            "args": [
                                "search_console.count_new_rankings",
                                "search_console.count_impressions",
                            ],
                        },
                        50,
                    ],
                },
                {
                    "function": "mul",
                    "args": [
                        "search_console.count_impressions",
                        "search_console.count_new_rankings",
                    ],
                },
                "search_console.count_clicks",
                123.456,
            ],
            "dimensions": ["keyword"],
        }
        expected = """
SELECT keyword f_0,
(IFNULL(sq_1.search_console__count_clicks_m, 0) + (sq_2.search_console__count_new_rankings_m - IFNULL(sq_1.search_console__count_impressions_m, 0)) + 50) f_1,
(IFNULL(sq_1.search_console__count_impressions_m, 0) * sq_2.search_console__count_new_rankings_m) f_2,
IFNULL(sq_1.search_console__count_clicks_m, 0) f_3,
123.456 f_4

FROM (SELECT a.keyword_hash,
ANY_VALUE(a.keyword) keyword,
SUM(a.clicks) search_console__count_clicks_m,
SUM(a.impressions) search_console__count_impressions_m
FROM (SELECT ANY_VALUE(keyword) keyword,
ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(url_hash) url_hash,
SUM(clicks) clicks,
SUM(impressions) impressions,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
GROUP BY url_keyword_hash) a
GROUP BY a.keyword_hash) sq_1

FULL OUTER JOIN

(SELECT a.keyword_hash,
ANY_VALUE(a.keyword) keyword,
COUNTIF(a.is_new) search_console__count_new_rankings_m
FROM (SELECT ANY_VALUE(keyword) keyword,
ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(url_hash) url_hash,
COUNT(1) = COUNTIF(date = first_seen) is_new,
date,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
GROUP BY date, url_keyword_hash) a
GROUP BY a.keyword_hash) sq_2

USING (keyword)
"""  # NOQA
        self.check_query(expected, bql)

    def test_no_metric(self):
        bql = {"metrics": [], "dimensions": ["url", "keyword"]}
        expected = """
SELECT url f_0,
keyword f_1
FROM (SELECT a.keyword_hash,
a.url_hash,
ANY_VALUE(a.keyword) keyword,
ANY_VALUE(a.url) url

FROM (SELECT ANY_VALUE(keyword) keyword,
ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
GROUP BY url_keyword_hash) a
GROUP BY a.keyword_hash, a.url_hash) sq_1

FULL OUTER JOIN

(SELECT a.keyword_hash,
a.url_hash,
ANY_VALUE(a.keyword) keyword,
ANY_VALUE(a.url) url
FROM (SELECT ANY_VALUE(keyword) keyword,
ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
COUNT(1) = COUNTIF(date = first_seen) is_new,
date,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
GROUP BY date, url_keyword_hash) a
GROUP BY a.keyword_hash, a.url_hash) sq_2

USING (keyword, url)
"""  # NOQA
        self.check_query(expected, bql)

    def test_clicks_virtual_fields(self):
        bql = {
            "metrics": [
                "search_console.count_clicks",
                "search_console.devices.desktop.count_clicks",
                "search_console.devices.mobile.count_clicks",
                "search_console.devices.tablet.count_clicks",
                "search_console.branded.count_clicks",
                "search_console.not_branded.count_clicks",
            ],
            "dimensions": [],
        }
        expected = """
SELECT IFNULL(sq_1.search_console__count_clicks_m, 0) f_0,
IFNULL(sq_1.search_console__devices__desktop__count_clicks_m, 0) f_1,
IFNULL(sq_1.search_console__devices__mobile__count_clicks_m, 0) f_2,
IFNULL(sq_1.search_console__devices__tablet__count_clicks_m, 0) f_3,
IFNULL(sq_1.search_console__branded__count_clicks_m, 0) f_4,
IFNULL(sq_1.search_console__not_branded__count_clicks_m, 0) f_5
FROM (SELECT SUM(a.clicks) search_console__count_clicks_m,
SUM(IF(a.branded, a.clicks, NULL)) search_console__branded__count_clicks_m,
SUM(IF(a.device = 'desktop', a.clicks, NULL)) search_console__devices__desktop__count_clicks_m,
SUM(IF(a.device = 'mobile', a.clicks, NULL)) search_console__devices__mobile__count_clicks_m,
SUM(IF(a.device = 'tablet', a.clicks, NULL)) search_console__devices__tablet__count_clicks_m,
SUM(IF(NOT a.branded, a.clicks, NULL)) search_console__not_branded__count_clicks_m
FROM (SELECT ANY_VALUE(branded) branded,
ANY_VALUE(url_hash) url_hash,
SUM(clicks) clicks,
device,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
JOIN
(SELECT * EXCEPT (url_hash, keyword_hash, url, keyword)
FROM (SELECT *,
ROW_NUMBER() OVER (PARTITION BY url_keyword_hash) AS rn
FROM `botify-test.test_1.search_console_unique_url_kw_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180501")
WHERE rn = 1)
USING (url_keyword_hash)
GROUP BY device, url_keyword_hash) a) sq_1
"""  # NOQA
        self.check_query(expected, bql)

    def test_virtual_fields(self):
        bql = {
            "metrics": [
                "search_console.devices.mobile.count_impressions",
                "search_console.devices.desktop.avg_position",
                "search_console.devices.tablet.ctr",
            ],
            "dimensions": ["date"],
            "filters": {
                "and": [
                    {
                        "field": "search_console.devices.mobile.avg_position",
                        "predicate": "gt",
                        "value": 5,
                    },
                    {
                        "field": "url",
                        "predicate": "query",
                        "value": {
                            "filters": {
                                "field": "search_console.branded.ctr",
                                "predicate": "lt",
                                "value": 3,
                            }
                        },
                    },
                ]
            },
        }
        expected = """
SELECT date f_0,
IFNULL(sq_1.search_console__devices__mobile__count_impressions_m, 0) f_1,
sq_1.search_console__devices__desktop__avg_position_m f_2,
sq_1.search_console__devices__tablet__ctr_m f_3
FROM (SELECT ((SUM(IF(a.device = 'tablet', a.clicks, NULL)) / SUM(IF(a.device = 'tablet', a.impressions, NULL))) * 100) search_console__devices__tablet__ctr_m,
(SUM(IF(a.device = 'desktop', (a.impressions * a.avg_position), NULL)) / SUM(IF(a.device = 'desktop', a.impressions, NULL))) search_console__devices__desktop__avg_position_m,
(SUM(IF(a.device = 'mobile', (a.impressions * a.avg_position), NULL)) / SUM(IF(a.device = 'mobile', a.impressions, NULL))) search_console__devices__mobile__avg_position_m,
a.date date,
SUM(IF(a.device = 'mobile', a.impressions, NULL)) search_console__devices__mobile__count_impressions_m
FROM (SELECT ((SUM(IF(branded, clicks, NULL)) / SUM(IF(branded, impressions, NULL))) * 100) search_console__branded__ctr,
(SUM((impressions * avg_position)) / SUM(impressions)) avg_position,
ANY_VALUE(url_hash) url_hash,
SUM(clicks) clicks,
SUM(impressions) impressions,
date,
device,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
JOIN
(SELECT * EXCEPT (url_hash, keyword_hash, url, keyword)
FROM (SELECT *,
ROW_NUMBER() OVER (PARTITION BY url_keyword_hash) AS rn
FROM `botify-test.test_1.search_console_unique_url_kw_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180501")
WHERE rn = 1)
USING (url_keyword_hash)
GROUP BY date, device, url_keyword_hash) a
WHERE a.search_console__branded__ctr < 3
GROUP BY date) sq_1
WHERE date IS NOT NULL AND sq_1.search_console__devices__mobile__avg_position_m > 5
"""  # NOQA
        self.check_query(expected, bql)

    def test_kw_in_h1_dimension(self):
        schemas = self.get_schemas_with_crawl()
        bql = {
            "metrics": ["search_console.count_keywords"],
            "dimensions": [
                "search_console.keyword_in_h1",
                "search_console.keyword_in_title",
            ],
        }
        expected = """
SELECT keyword_in_h1 f_0,
keyword_in_title f_1,
sq_1.search_console__count_keywords_m f_2
FROM (SELECT a.keyword_in_h1 keyword_in_h1,
a.keyword_in_title keyword_in_title,
APPROX_COUNT_DISTINCT(a.keyword_hash) search_console__count_keywords_m
FROM (SELECT ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(keyword_in_h1) keyword_in_h1,
ANY_VALUE(keyword_in_title) keyword_in_title,
ANY_VALUE(url_hash) url_hash,
url_keyword_hash
FROM (SELECT * EXCEPT (keyword_in_h1, keyword_in_title),
LAST_VALUE(keyword_in_h1) OVER (PARTITION BY url_keyword_hash ORDER BY date) keyword_in_h1,
LAST_VALUE(keyword_in_title) OVER (PARTITION BY url_keyword_hash ORDER BY date) keyword_in_title
FROM `botify-test.test_{project_id}.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
GROUP BY url_keyword_hash) a
GROUP BY keyword_in_h1, keyword_in_title) sq_1
""".format(
            project_id=self.project_id
        )  # NOQA
        self.check_query(expected, bql, schemas)

    def test_kw_in_with_date(self):
        schemas = self.get_schemas_with_crawl()
        bql = {
            "metrics": ["search_console.count_keywords"],
            "dimensions": [
                "date",
                "search_console.keyword_in_h1",
                "search_console.keyword_in_title",
            ],
        }
        expected = """
SELECT date f_0,
keyword_in_h1 f_1,
keyword_in_title f_2,
sq_1.search_console__count_keywords_m f_3
FROM (SELECT a.date date,
a.keyword_in_h1 keyword_in_h1,
a.keyword_in_title keyword_in_title,
APPROX_COUNT_DISTINCT(a.keyword_hash) search_console__count_keywords_m
FROM (SELECT ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(keyword_in_h1) keyword_in_h1,
ANY_VALUE(keyword_in_title) keyword_in_title,
ANY_VALUE(url_hash) url_hash,
date,
url_keyword_hash
FROM (SELECT * EXCEPT (keyword_in_h1, keyword_in_title),
LAST_VALUE(keyword_in_h1) OVER (PARTITION BY url_keyword_hash ORDER BY date) keyword_in_h1,
LAST_VALUE(keyword_in_title) OVER (PARTITION BY url_keyword_hash ORDER BY date) keyword_in_title
FROM `botify-test.test_{project_id}.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
GROUP BY date, url_keyword_hash) a
GROUP BY date, keyword_in_h1, keyword_in_title) sq_1
WHERE date IS NOT NULL
""".format(
            project_id=self.project_id
        )  # NOQA
        self.check_query(expected, bql, schemas)

    def test_explorer_with_description(self):
        schemas = self.get_schemas_with_crawl()
        bql = {
            "metrics": [],
            "dimensions": ["url", "keyword", "search_console.keyword_in_description"],
        }
        expected = """
SELECT url f_0,
keyword f_1,
keyword_in_description f_2
FROM (SELECT a.keyword_hash,
a.keyword_in_description keyword_in_description,
a.url_hash,
ANY_VALUE(a.keyword) keyword,
ANY_VALUE(a.url) url
FROM (SELECT ANY_VALUE(keyword) keyword,
ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(keyword_in_description) keyword_in_description,
ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
url_keyword_hash
FROM (SELECT * EXCEPT (keyword_in_description),
LAST_VALUE(keyword_in_description) OVER (PARTITION BY url_keyword_hash ORDER BY date) keyword_in_description
FROM `botify-test.test_{project_id}.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
GROUP BY url_keyword_hash) a
GROUP BY a.keyword_hash, a.url_hash, keyword_in_description) sq_1

FULL OUTER JOIN

(SELECT a.keyword_hash,
a.keyword_in_description keyword_in_description,
a.url_hash,
ANY_VALUE(a.keyword) keyword,
ANY_VALUE(a.url) url
FROM (SELECT ANY_VALUE(keyword) keyword,
ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(keyword_in_description) keyword_in_description,
ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
COUNT(1) = COUNTIF(date = first_seen) is_new,
date,
url_keyword_hash
FROM (SELECT * EXCEPT (keyword_in_description),
LAST_VALUE(keyword_in_description) OVER (PARTITION BY url_keyword_hash ORDER BY date) keyword_in_description
FROM `botify-test.test_{project_id}.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
GROUP BY date, url_keyword_hash) a
GROUP BY a.keyword_hash, a.url_hash, keyword_in_description) sq_2

USING (keyword, keyword_in_description, url)
""".format(
            project_id=self.project_id
        )  # NOQA
        self.check_query(expected, bql, schemas)

    def test_filter_kw_in_title(self):
        schemas = self.get_schemas_with_crawl()
        bql = {
            "metrics": ["search_console.count_keywords"],
            "dimensions": [],
            "filters": {"field": "search_console.keyword_in_title", "value": True},
        }
        expected = """
SELECT sq_1.search_console__count_keywords_m f_0
FROM (SELECT APPROX_COUNT_DISTINCT(a.keyword_hash) search_console__count_keywords_m
FROM (SELECT ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(keyword_in_title) keyword_in_title,
ANY_VALUE(url_hash) url_hash,
url_keyword_hash
FROM (SELECT * EXCEPT (keyword_in_title),
LAST_VALUE(keyword_in_title) OVER (PARTITION BY url_keyword_hash ORDER BY date) keyword_in_title
FROM `botify-test.test_{project_id}.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
GROUP BY url_keyword_hash) a
WHERE a.keyword_in_title) sq_1
""".format(
            project_id=self.project_id
        )  # NOQA
        self.check_query(expected, bql, schemas)

    def test_estimated_revenue(self):
        test_project = ProjectFactory()
        test_project.conversion_rate_desktop = 0.5
        test_project.revenue_per_conversion_desktop = 5
        test_project.conversion_rate_mobile = 0.4
        test_project.revenue_per_conversion_mobile = 4
        test_project.conversion_rate_tablet = 0.3
        test_project.revenue_per_conversion_tablet = 3
        test_project.currency = "EUR"
        test_project.save()
        schemas = SearchConsoleSchemas(
            test_project.id,
            self.date_start,
            self.date_end,
            self.revision,
            with_urls_and_segments=True,
        )

        bql = {"metrics": ["search_console.revenue"], "dimensions": ["url", "keyword"]}
        expected = """
SELECT url f_0,
       keyword f_1,
       sq_1.search_console__revenue_m f_2
FROM
  (SELECT a.keyword_hash,
          a.url_hash,
          ANY_VALUE(a.keyword) keyword,
          ANY_VALUE(a.url) url,
          sum(CASE
                  WHEN a.device = 'tablet' THEN (a.clicks * 0.0009)
                  WHEN a.device = 'mobile' THEN (a.clicks * 0.0016)
                  WHEN a.device = 'desktop' THEN (a.clicks * 0.0025)
              END) search_console__revenue_m
   FROM
     (SELECT ANY_VALUE(keyword) keyword,
             ANY_VALUE(keyword_hash) keyword_hash,
             ANY_VALUE(url) url,
             ANY_VALUE(url_hash) url_hash,
             SUM(clicks) clicks,
             device,
             url_keyword_hash
      FROM
        (SELECT *
         FROM `botify-test.test_{}.search_console_2*`
         WHERE _table_suffix BETWEEN "0180410" AND "0180510")
      GROUP BY device,
               url_keyword_hash) a
   GROUP BY a.keyword_hash,
            a.url_hash) sq_1""".format(
            test_project.id
        )  # NOQA sqlformat
        self.check_query(expected, bql, schemas=schemas)

    def test_no_keyword_in_fields(self):
        schemas = SearchConsoleSchemas(
            None,
            self.date_start,
            self.date_end,
            self.revision,
            with_urls_and_segments=True,
        )

        bql = {
            "metrics": ["search_console.count_keywords"],
            "dimensions": [
                "search_console.keyword_in_h1",
                "search_console.keyword_in_title",
            ],
        }

        with self.assertRaises(QueryParsingException):
            self.transform_query(bql, schemas=schemas)

    def test_keyword_position_for_url(self):
        bq = {
            "metrics": ["search_console.keyword_position_for_url"],
            "dimensions": ["url", "keyword"],
        }
        expected = """
SELECT url f_0,
       keyword f_1,
       sq_1.search_console__keyword_position_for_url_m f_2
FROM
  (SELECT a.keyword_hash,
          a.url_hash,
          ANY_VALUE(a.keyword) keyword,
          ANY_VALUE(a.url) url,
          ROW_NUMBER() OVER (PARTITION BY any_value(a.url_hash)
                             ORDER BY SUM(a.clicks) DESC) search_console__keyword_position_for_url_m
   FROM
     (SELECT ANY_VALUE(keyword) keyword,
             ANY_VALUE(keyword_hash) keyword_hash,
             ANY_VALUE(url) url,
             ANY_VALUE(url_hash) url_hash,
             SUM(clicks) clicks,
             url_keyword_hash
      FROM
        (SELECT *
         FROM `botify-test.test_1.search_console_2*`
         WHERE _table_suffix BETWEEN "0180410" AND "0180510")
      GROUP BY url_keyword_hash) a
   GROUP BY a.keyword_hash,
            a.url_hash) sq_1"""  # NOQA sqlformat
        self.check_query(expected, bq)

    def test_keyword_position_for_url_with_dimensions(self):
        bq = {
            "metrics": ["search_console.keyword_position_for_url"],
            "dimensions": ["url", "keyword", "device", "country"],
        }
        expected = """
SELECT url f_0,
keyword f_1,
device f_2,
country f_3,
sq_1.search_console__keyword_position_for_url_m f_4
FROM (SELECT a.country country,
a.device device,
a.keyword_hash,
a.url_hash,
ANY_VALUE(a.keyword) keyword,
ANY_VALUE(a.url) url,
ROW_NUMBER() OVER (PARTITION BY ANY_VALUE(a.url_hash) ORDER BY SUM(a.clicks) DESC) search_console__keyword_position_for_url_m
FROM (SELECT ANY_VALUE(keyword) keyword,
ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
SUM(clicks) clicks,
country,
device,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180410" AND "0180510")
GROUP BY country, device, url_keyword_hash) a
GROUP BY a.keyword_hash, a.url_hash, country, device) sq_1
WHERE device IS NOT NULL AND country IS NOT NULL
"""  # NOQA
        self.check_query(expected, bq)
